# Count the lines of code in PypeIt

## Goals

- Count the lines of code in PypeIt
- Estimate the number that were written with GenAI
- Make a figure

## Context

This is the repository for PypeIt, a package for spectroscopic data reduction:
https://github.com/pypeit/PypeIt

## Prompts

1. Read the goals and context and ask me a set of questions to answer before
   proceeding.  Put them in the Q&A section below.  Log your work.

2. Read my answers in the Q&A section and proceed as best you can to 
   achieve the goals.  Log your work.


## Q&A

Questions from Claude (2026-10-21), each with a recommended answer. Facts
below come from the sibling clone at `/Users/xavier/Projects/PypeIt/PypeIt`.

**What I found before asking.** The clone has ~20.5k commits on `develop`,
spanning 2015-06-05 to 2026-10-16. Tracked Python under `pypeit/` totals
~195k physical lines (including tests); `doc/` adds ~4k lines of Python and
~600 `.rst` files. On `develop`, 230 commits carry a `Co-Authored-By: Claude`
trailer, the first on 2026-03-16 and the latest on 2026-10-14; a looser search
for "claude", "copilot", "chatgpt" or "generated with" in commit messages finds
243. The top three author names (`profxj`, `Kyle Westfall`, `joe`) include
duplicates of the same people under different names (`profxj` /
`J. Xavier Prochaska`; `rcooke` / `rcooke-ast` / `Ryan Cooke`). No line
counter (`cloc`, `tokei`, `scc`) is installed; `pygount` could be installed
into `pypeit14`, or I can write a small counter.

1. **Which files count as "code"?**
   Options: (a) Python under `pypeit/` only; (b) Python in `pypeit/` and
   `doc/`; (c) everything text, including `.rst` docs and notebooks.
   *Recommended:* (a) for the headline number, with `pypeit/tests/` reported
   separately, and `.rst` docs as a third optional line. Data files (`.fits`,
   `.dat`, `.gz`) are excluded.
   Answer: Both (a) and (b).  Docs are a big deal for this code base

2. **Physical lines or source lines?**
   A physical count includes blanks, comments and docstrings; a source-line
   count strips them. PypeIt is docstring-heavy, so the two differ a lot.
   *Recommended:* report both, plotting source lines as the main curve. If a
   tool is fine, `pip install pygount` into `pypeit14`; otherwise I write a
   counter using `tokenize`.
   Answer: Physical count

3. **Which branch, and as a snapshot or over time?**
   `develop` (20,536 commits) is ahead of `release` (19,141). The "make a
   figure" goal suggests a time series.
   *Recommended:* `develop`, sampled at every tagged release plus a fixed
   cadence (e.g. quarterly) back to 2015, computed by checking out each commit
   in a temporary worktree so the clone's working branch (`edge_2208`) is
   never touched.
   Answer: `develop`

4. **What signal identifies GenAI-written code?**
   The only machine-readable marker is the `Co-Authored-By: Claude` trailer
   (230 commits since 2026-03-16). Earlier AI assistance (Copilot
   autocomplete, ChatGPT snippets pasted in, Claude sessions committed without
   the trailer) would be invisible.
   *Recommended:* use the trailer as the primary signal. Please tell me
   whether (a) the trailers are complete for the period they cover, and (b)
   you want me to add any branches, PR numbers or date ranges by hand that
   you know were AI-assisted but untagged. If so, list them here.
   Answer: Use the trailer as the primary signal.  I believe all code written
   by Tim Pickering and Debora since 2026-04-16 was written with GenAI.

5. **"Written with GenAI" means which lines?**
   Two sensible definitions: (a) lines added in AI-coauthored commits,
   cumulative, regardless of later edits or deletions; (b) lines surviving at
   HEAD whose `git blame` points to an AI-coauthored commit.
   *Recommended:* (b) as the headline, since it answers "how much of PypeIt
   today was AI-written"; report (a) alongside as "AI-touched lines added".
   Both treat a line human-edited after AI generation as human.
   Answer: (b) 

6. **What should the figure show?**
   Options: (a) total lines vs. time with the AI-attributed portion as a
   stacked band; (b) a per-release bar chart; (c) a pie of the current
   composition.
   *Recommended:* (a), 2015 to present, with release tags marked on the axis
   and a one-line annotation at the first AI commit (2026-03-16). Output PNG
   and PDF via matplotlib. If you say what venue this is for (talk, proposal,
   paper), I will size and style it accordingly.
   Answer: (a)

7. **Where do the script and outputs live?**
   *Recommended:* a new top-level directory `lines_of_code/` in this repo
   holding the Python script(s), a CSV of the per-snapshot counts so the
   figure can be remade without re-running the git walk, and the figure
   files. Nothing is written into the PypeIt clone.
   Answer: Use your recommendation

8. **Is a per-author breakdown wanted?**
   It is cheap to add from the same blame pass, but requires a mapping of the
   duplicate author names (`profxj` = `J. Xavier Prochaska`, `joe` = ?, the
   three `rcooke` variants, etc.).
   *Recommended:* not for the first pass. If you want it, supply the name
   mapping here.
   Answer: No per-author

9. **Should the development suite be included?**
   `PypeIt-development-suite` holds test infrastructure and also has
   AI-coauthored commits.
   *Recommended:* no, keep the scope to the `PypeIt` package.
   Answer: No dev suite

## Logs

### 2026-10-21 (Read goals and context; posed questions in Q&A)

Read `count_the_lines.md` and surveyed the sibling PypeIt clone (read-only)
to avoid asking what the repository can answer itself: history span, commit
counts on `develop` vs `release`, tracked file types, Python line totals, and
the presence of `Co-Authored-By: Claude` trailers (230 commits on `develop`,
2026-03-16 to 2026-10-14). Learned that no line-counting tool is installed on
this machine, that author names in the history are duplicated under several
spellings, and that the clone's working branch is `edge_2208`, so any
historical walk must use a temporary worktree rather than checkouts. Wrote
nine questions into the Q&A section, each with a recommended answer, covering
file scope, counting method, branch and time sampling, the GenAI attribution
signal and definition, figure design, output location, per-author breakdown,
and whether the dev suite is in scope. No scripts were written and no
state-changing git commands were run in either repository.

### 2026-10-21 (Counted lines, attributed GenAI lines, made the figure)

Executed prompt #2 using the answers in Q&A. All work is in the new
`lines_of_code/` directory: `count_lines.py` (the git walk and blame pass),
`line_counts.csv` (one row per snapshot, so the figure can be remade without
re-running the walk), `plot_lines.py`, and `lines_of_code.png` / `.pdf`. Python
was run with `conda run -n pypeit14`; only the standard library, numpy and
matplotlib are used (no pandas in that environment). Nothing was written into
the PypeIt clone and no state-changing git commands were run in either repo.

**Method.** Snapshots on `origin/develop` (tip 437c9000, 2026-10-20) are every
tag on that branch's ancestry, the first commit of each quarter since 2015, the
first of each month in 2026, and the tip: 115 snapshots. Each snapshot is read
straight from the object store (`git ls-tree` + `git cat-file --batch`), so the
clone's working branch (`edge_2208`) was never touched. Physical lines (blanks
and comments included) are counted in five categories: `pypeit_src`,
`pypeit_tests`, `doc_py`, `doc_hand` (.rst), and `doc_gen` (the auto-generated
`doc/api`, `doc/include`, `doc/help` .rst). GenAI attribution follows the Q&A:
a commit is "AI" if its message carries a `Co-Authored-By: Claude` trailer
(230 commits since 2026-03-16) or if it was authored by Tim Pickering or
Debora Pelliccia on or after 2026-04-16 (270 commits; 189 of them also carry
the trailer), giving 311 AI commits touching 208 files. For each snapshot on or
after 2026-03-16, `git blame` at that snapshot is run on those files and a line
is AI if it is blamed on an AI commit (definition (b): surviving lines, so a
line later edited by a human counts as human).

**Results at the tip (2026-10-20).** Total 255,140 physical lines, of which
20,949 (8.2%) are attributed to GenAI. Code (pypeit + tests + doc scripts):
199,466 lines, 18,517 (9.3%) AI. Docs (.rst): 55,674 lines, 2,432 (4.4%) AI;
9,173 of the doc lines are auto-generated. The test suite is the most
AI-written slice: 20,154 lines, 4,238 (21.0%) AI. The AI share was essentially
zero until June 2026 and jumped in July 2026 (first large batch of trailer
commits) and again in October 2026.

**What I learned about the repo, and two scope decisions.** (1) The package was
`src/` from 2015 to mid-2016, `pypit/` until mid-2018, then `pypeit/`; all three
are counted, otherwise the curve starts at zero in 2018. (2) `pypeit/deprecated/`
(63 files, ~36k lines) was removed from the repo in early 2024 and now lives in
this repo's `deprecated/`; it is excluded at every snapshot, otherwise the
figure shows a 36k-line cliff at 1.15.0 that is housekeeping, not lost code.
The 2.0.1 tag (2026-03-23) shows zero AI lines because it was cut from the
release branch before the first AI commits were merged into it. Tags with a
leading `v` duplicate unprefixed tags and are deduplicated by commit.

**Figure.** Stacked area, 2015 to present: Code (human), Code (GenAI), Docs
(human), Docs (GenAI). Hue follows the entity (blue = code, orange = docs,
the two leading slots of the validated reference palette from the dataviz
skill); GenAI is the full-strength hatched band, human the light tint. x.y.0
release tags are marked along the top, thinned to at least 150 days apart so
labels never collide; the first Claude co-authored commit is a dashed line;
each band is direct-labeled with its current line count. Caveat: the skill's
palette validator needs `node`, which is not installed here, so the CVD check
on the exact tint pairs was not run; the pairs differ strongly in lightness and
the hatch is a second channel, and the legend plus direct labels make identity
never color-alone.

**Caveats on the estimate.** The trailer is only present from 2026-03-16;
earlier AI assistance (Copilot, pasted snippets, untagged sessions) is
invisible. The Tim/Debora rule counts everything they committed after
2026-04-16 as AI, including hand edits. `git blame` is run without `-w`, so
reformatting a line by hand re-attributes it to the human. `count_lines.log`
in `lines_of_code/` is the run log and is git-ignored by the `*.log` rule.
