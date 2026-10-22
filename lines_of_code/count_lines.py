#!/usr/bin/env python
"""
Count physical lines of code and documentation in the PypeIt repository
over time, and attribute lines to GenAI (Claude) where possible.

Nothing is checked out; every snapshot is read straight from the git object
store with ``git ls-tree`` / ``git cat-file``, so the clone's working branch
is never touched.

Categories (physical line counts, i.e. including blanks and comments):

    pypeit_src   -- pypeit/**/*.py excluding pypeit/tests/
    pypeit_tests -- pypeit/tests/**/*.py

Before mid-2018 the package lived in ``pypit/`` and, before mid-2016, in
``src/``; those directories are counted in the same categories.  ``pypeit/deprecated/`` (removed from the repo in early
2024 and now kept in PypeIt-misc/deprecated/) is excluded at every snapshot so
that housekeeping does not appear as a loss of code.
    doc_py       -- doc/**/*.py (Sphinx conf and doc build scripts)
    doc_hand     -- doc/**/*.rst excluding the auto-generated subdirectories
    doc_gen      -- doc/api/, doc/include/, doc/help/ *.rst (auto-generated)

GenAI attribution (the ``*_ai`` columns) uses ``git blame`` at each snapshot
on or after the first AI-coauthored commit.  A line is "AI" if the commit it
is blamed on is either

    (a) a commit whose message carries a ``Co-Authored-By: Claude`` trailer, or
    (b) a commit authored by T. E. Pickering or Debora Pelliccia on or after
        2026-04-16 (per the owner's statement in prompts/count_the_lines.md).

Usage:
    python count_lines.py [--repo PATH] [--branch REF] [--out CSV] [--jobs N]
"""
import argparse
import csv
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime

AI_TRAILER_RE = re.compile(r'co-authored-by:\s*claude', re.IGNORECASE)
AI_AUTHOR_EMAILS = {
    'te.pickering@gmail.com',
    'dpelliccia@ucolick.org',
    'dpelliccia@ucdavis.edu',
}
AI_AUTHOR_SINCE = date(2026, 4, 16)
FIRST_AI_DATE = date(2026, 3, 16)   # first Co-Authored-By: Claude commit
GEN_DOC_DIRS = ('doc/api/', 'doc/include/', 'doc/help/')
CATEGORIES = ['pypeit_src', 'pypeit_tests', 'doc_py', 'doc_hand', 'doc_gen']

BLAME_HDR_RE = re.compile(rb'^([0-9a-f]{40}) \d+ \d+(?: \d+)?$')


def git(repo, *args, binary=False):
    out = subprocess.run(['git', '-C', repo, *args], check=True,
                         capture_output=True)
    return out.stdout if binary else out.stdout.decode('utf-8', 'replace')


PKG_DIRS = ('pypeit/', 'pypit/', 'src/')


def categorize(path):
    if '/deprecated/' in path:
        return None
    if path.endswith('.py'):
        if path.startswith(('pypeit/tests/', 'pypit/tests/')):
            return 'pypeit_tests'
        if path.startswith(PKG_DIRS):
            return 'pypeit_src'
        if path.startswith('doc/'):
            return 'doc_py'
    elif path.endswith('.rst') and path.startswith('doc/'):
        if path.startswith(GEN_DOC_DIRS):
            return 'doc_gen'
        return 'doc_hand'
    return None


def snapshot_files(repo, commit):
    """Return {path: category} for all counted files at a commit."""
    names = git(repo, 'ls-tree', '-r', '--name-only', '-z', commit).split('\0')
    files = {}
    for p in names:
        c = categorize(p)
        if c is not None:
            files[p] = c
    return files


def count_physical(repo, commit, files):
    """Physical line count per category via one git cat-file --batch call."""
    spec = ''.join(f'{commit}:{p}\n' for p in files).encode()
    proc = subprocess.run(['git', '-C', repo, 'cat-file', '--batch'],
                          input=spec, check=True, capture_output=True)
    data = proc.stdout
    counts = {c: 0 for c in CATEGORIES}
    nfiles = {c: 0 for c in CATEGORIES}
    pos = 0
    paths = list(files)
    for p in paths:
        nl = data.index(b'\n', pos)
        header = data[pos:nl].decode()
        pos = nl + 1
        parts = header.split()
        if parts[-1] == 'missing':
            continue
        size = int(parts[2])
        blob = data[pos:pos + size]
        pos += size + 1  # trailing newline after the blob
        n = blob.count(b'\n')
        if blob and not blob.endswith(b'\n'):
            n += 1
        counts[files[p]] += n
        nfiles[files[p]] += 1
    return counts, nfiles


def ai_commit_set(repo, tip):
    """Hashes of commits considered GenAI-written, plus the files they touched."""
    raw = git(repo, 'log', tip, '--since=2026-03-01', '--date=short',
              '--name-only',
              '--format=%x1e%H%x00%ae%x00%ad%x00%B%x1f')
    ai = set()
    touched = set()
    for rec in raw.split('\x1e'):
        if not rec.strip():
            continue
        head, _, filelist = rec.partition('\x1f')
        h, email, ad, body = head.split('\x00', 3)
        adate = datetime.strptime(ad, '%Y-%m-%d').date()
        is_ai = bool(AI_TRAILER_RE.search(body)) or (
            email.lower() in AI_AUTHOR_EMAILS and adate >= AI_AUTHOR_SINCE)
        if is_ai:
            ai.add(h)
            for f in filelist.split('\n'):
                f = f.strip()
                if f:
                    touched.add(f)
    return ai, touched


def blame_ai_lines(repo, commit, path, ai):
    try:
        out = git(repo, 'blame', '--line-porcelain', commit, '--', path,
                  binary=True)
    except subprocess.CalledProcessError:
        return 0
    n = 0
    for line in out.split(b'\n'):
        m = BLAME_HDR_RE.match(line)
        if m and m.group(1).decode() in ai:
            n += 1
    return n


def count_ai(repo, commit, files, ai, touched, jobs):
    cand = [p for p in files if p in touched]
    counts = {c: 0 for c in CATEGORIES}
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for p, n in zip(cand, ex.map(
                lambda p: blame_ai_lines(repo, commit, p, ai), cand)):
            counts[files[p]] += n
    return counts


def build_snapshots(repo, branch):
    """(date, commit, label) sorted by date; quarterly + monthly-in-AI-era + tags."""
    snaps = {}

    def add(d, commit, label):
        if commit and commit not in snaps:
            snaps[commit] = (d, commit, label)

    # tags on the branch's ancestry; prefer names without a leading 'v'
    tags = git(repo, 'tag').split()
    for t in sorted(tags, key=lambda s: (s.startswith('v'), s)):
        try:
            subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor',
                            t, branch], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            continue
        commit = git(repo, 'rev-list', '-1', t).strip()
        d = git(repo, 'log', '-1', '--format=%ad', '--date=short', commit).strip()
        add(date.fromisoformat(d), commit, t)

    # calendar sampling
    first = date.fromisoformat(
        git(repo, 'log', branch, '--reverse', '--format=%ad', '--date=short'
            ).split('\n', 1)[0])
    today = date.today()
    dates = []
    y, m = first.year, ((first.month - 1) // 3 + 1) * 3 + 1
    if m > 12:
        y, m = y + 1, 1
    while date(y, m, 1) <= today:
        dates.append(date(y, m, 1))
        m += 3
        if m > 12:
            y, m = y + 1, m - 12
    y, m = 2026, 1
    while date(y, m, 1) <= today:
        dates.append(date(y, m, 1))
        m += 1
        if m > 12:
            y, m = y + 1, 1
    for d in dates:
        commit = git(repo, 'rev-list', '-1', f'--before={d.isoformat()}',
                     branch).strip()
        if commit:
            cd = git(repo, 'log', '-1', '--format=%ad', '--date=short',
                     commit).strip()
            add(date.fromisoformat(cd), commit, '')

    # branch tip
    tip = git(repo, 'rev-list', '-1', branch).strip()
    td = git(repo, 'log', '-1', '--format=%ad', '--date=short', tip).strip()
    add(date.fromisoformat(td), tip, 'tip')

    return sorted(snaps.values()), tip


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', default='/Users/xavier/Projects/PypeIt/PypeIt')
    ap.add_argument('--branch', default='origin/develop')
    ap.add_argument('--out', default='line_counts.csv')
    ap.add_argument('--jobs', type=int, default=8)
    args = ap.parse_args()

    snaps, tip = build_snapshots(args.repo, args.branch)
    print(f'{len(snaps)} snapshots on {args.branch}; tip {tip[:10]}',
          file=sys.stderr)

    ai, touched = ai_commit_set(args.repo, tip)
    print(f'{len(ai)} GenAI-attributed commits touching {len(touched)} files',
          file=sys.stderr)

    cols = (['date', 'commit', 'label']
            + CATEGORIES
            + [f'{c}_files' for c in CATEGORIES]
            + [f'{c}_ai' for c in CATEGORIES])
    with open(args.out, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for d, commit, label in snaps:
            files = snapshot_files(args.repo, commit)
            counts, nfiles = count_physical(args.repo, commit, files)
            if d >= FIRST_AI_DATE:
                aic = count_ai(args.repo, commit, files, ai, touched, args.jobs)
            else:
                aic = {c: 0 for c in CATEGORIES}
            row = ([d.isoformat(), commit, label]
                   + [counts[c] for c in CATEGORIES]
                   + [nfiles[c] for c in CATEGORIES]
                   + [aic[c] for c in CATEGORIES])
            w.writerow(row)
            fh.flush()
            tot = sum(counts.values())
            tot_ai = sum(aic.values())
            print(f'{d} {commit[:8]} {label:8s} total={tot:7d} ai={tot_ai:6d}',
                  file=sys.stderr)


if __name__ == '__main__':
    main()
