# Getting started

## Goals

This repository will hold this and that related to PypeIt that does not belong
in the main code base: deprecated modules kept for reference, the JOSS paper,
presentations, proposals, and prompt docs for one-off analyses of the PypeIt
project (e.g. counting lines of code).  It is a miscellany, not a Python
package.

## Prompts

1. Read this file.  Execute the 1st task under "Claude/CLAUDE.md file"
2. Read this file.  Execute the 1st task under "Claude/Skills"
3. Read this file.  Execute the 1st task under "Claude/Settings"
4. Read this file.  Execute the 1st task under "Basic start up"

## Claude

### CLAUDE.md file

1. Please generate a basic CLAUDE.md file for this project.  Have it indicate:

    - I will perform git commands
    - If you do any calculation, generate it as a python script and write it to
      disk so that I can add it to the Repository
    - If you need to run Python, use the `pypeit14` conda environment
    - The main PypeIt repository is a sibling clone at
      `/Users/xavier/Projects/PypeIt/PypeIt` and the development suite is at
      `/Users/xavier/Projects/PypeIt/PypeIt-development-suite`.  Analyses in
      this repo will often read from those; they should never write to them.
    - Prompt docs live in `prompts/` (not `claude_prompts/`).  Read the
      relevant one before acting and do only the numbered task you were
      pointed at.
    - Describe the layout: `deprecated/` (old PypeIt code, reference only, do
      not modernize), `paper/` (JOSS paper), `presentations/`, `proposals/`,
      `prompts/`.

### Skills

1. Copy over the skills/ files from the IOPtics repository
   (`/Users/xavier/Oceanography/python/IOPtics/.claude/skills`) into
   `.claude/skills/`.  Expect `critical-partner` and `grill-me`.

### Settings

1. Copy over the settings.json file from the IOPtics repository
   (`/Users/xavier/Oceanography/python/IOPtics/.claude/settings.json`) into
   `.claude/settings.json`.  Copy the policy, not the accumulated
   path-specific allow entries.  Replace `ocean14` with `pypeit14`.  Keep the
   deny list for `git push` / `git commit` / `git reset` / `git rebase`.

## Basic start up

1. Generate the basic files that one needs for a GitHub repository of this
   kind, e.g. a `.gitignore` and a fuller `README.md` that describes each
   top-level directory.  This is not a Python package, so do not add
   `setup.py` or `requirements.txt` unless a script in `prompts/` ends up
   needing dependencies; if so, put them in `requirements.txt`.  Examine the
   other Repositories in `Projects/PypeIt` to see how I tend to organize
   things.  Also, make a suggestion of which of their settings.json files to
   copy into this one.

### Report

Recommendation: use **first-hires-exoplanet**'s `.claude/settings.json` as the
reference (keck-etcs is a near-identical superset of it).  Of the siblings,
only the-holy-grail, keck-etcs, first-hires-exoplanet and shane-telescope have
a `settings.json`; PypeIt-development-suite and MUSERePipe have only
`skills/`.  shane-telescope's is a two-line stub (`python *`, `pypeit14b`) and
the-holy-grail's still says `ocean14` and allows all of WebFetch/WebSearch.
first-hires-exoplanet and keck-etcs share the same IOPtics-derived policy
this repo already has (same deny list for `git push`/`commit`/`reset`/`rebase`,
`ask` on `rm`, `conda run -n pypeit14`), but with astronomy WebFetch domains
instead of ocean-optics publishers.  keck-etcs adds Keck web sites and
`pypeit_sensfunc`/`pypeit_flux_calib`, which this repo does not need.

This repo's current `settings.json` (from IOPtics, `ocean14` -> `pypeit14`)
differs from first-hires-exoplanet's only in small ways, so there is no need
to copy the file wholesale.  Suggested merge:

- Replace the three ocean-optics WebFetch domains (`opg.optica.org`,
  `aslopubs.onlinelibrary.wiley.com`, `www.tandfonline.com`; keep `doi.org`)
  with `ui.adsabs.harvard.edu`, `arxiv.org`, `iopscience.iop.org` and
  `pypeit.readthedocs.io`.  Consider `github.com`/`api.github.com` too, for
  the line-count analysis, and `joss.theoj.org` for the paper.
- Add `Bash(diff:*)`, which both PypeIt siblings allow.
- Skip `pypeit_setup`/`run_pypeit` and `koa.ipac.caltech.edu`; this repo does
  not reduce data.

Not applied; `settings.json` was left unchanged.

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-10-21 (Generated basic CLAUDE.md)

Executed task 1 under "Claude/CLAUDE.md file": created `CLAUDE.md` at the repo
root.  It states that the user performs all git commands, that any
calculation should be written to disk as a Python script so it can be added to
the repo, that Python runs in the `pypeit14` conda environment, that the main
PypeIt repo (`/Users/xavier/Projects/PypeIt/PypeIt`) and the development suite
(`/Users/xavier/Projects/PypeIt/PypeIt-development-suite`) are read-only
sibling clones, that prompt docs live in `prompts/` and only the pointed-at
numbered task should be done, and it describes the layout.  Surveying the repo:
`deprecated/` holds ~70 old PypeIt modules plus a `bin/` of old `pypeit_*`
scripts; `paper/` has the JOSS `paper.md`/`paper.bib` and sky-subtraction
figures; `presentations/` has `DRWG/`, `SSC/` (mostly .odp) and `py/users.py`;
`proposals/` has `ADAP/`, `NSF/`, `UCO/`, `WMKO/`; `prompts/` has
`start_up.md` and `count_the_lines.md`.  README.md is a two-line stub and
LICENSE is BSD 3-Clause.  Style followed the-holy-grail's CLAUDE.md.  No git
commands were run; nothing was staged or committed.

### 2026-10-21 (Copied critical-partner and grill-me skills)

Executed task 1 under "Claude/Skills": created `.claude/skills/` and copied
the two skill directories verbatim (`cp -R`) from
`/Users/xavier/Oceanography/python/IOPtics/.claude/skills`, giving
`.claude/skills/critical-partner/SKILL.md` (2629 bytes) and
`.claude/skills/grill-me/SKILL.md` (635 bytes).  `diff -r` against the source
is clean, and contents were not edited.  `critical-partner` makes Claude a
constructive-disagreement partner: it surfaces untested assumptions, argues the
strongest opposing case and reviews weaknesses first (triggered by "poke
holes", "devil's advocate", "be critical", etc.).  `grill-me` interviews the
user one question at a time about a plan or design, walking each branch of the
decision tree and offering a recommended answer per question.  Each skill is
a single `SKILL.md` with YAML front matter (`name`, `description`) and no
supporting files.  No state-changing git commands were run; nothing was staged
or committed.

### 2026-10-21 (Created .claude/settings.json from IOPtics policy)

Executed task 1 under "Claude/Settings": created `.claude/settings.json` from
`/Users/xavier/Oceanography/python/IOPtics/.claude/settings.json`, keeping the
policy and dropping the accumulated entries.  The source has 65 allow, 7 deny
and 1 ask entries; the result has 37 allow, 7 deny and 1 ask.  Kept: read-only
shell commands (`ls`, `cat`, `grep`, `rg`, `find`, `head`, `tail`, `wc`,
`sort`, etc.), file operations that do not delete (`mkdir`, `touch`, `cp`,
`mv`), read-only git (`status`, `diff`, `log`, `show`, `branch`),
conda/python/pip/pytest/jupyter, and the four WebFetch publisher domains
(optica, wiley/ASLO, doi.org, tandfonline).  The deny list (`sudo`,
`rm -rf /`, `rm -rf ~`, `git push`/`commit`/`reset`/`rebase`) and the ask
entry for `rm` were copied unchanged.  The single `ocean14` occurrence among
the kept entries (`conda run -n ocean14:*`) became `pypeit14`.  Pruned 28
one-off entries that had built up in IOPtics sessions: two Crossref `curl`
lookups and their `python3 -c` JSON parsers, absolute-path
`.../envs/ocean14/bin/python` pytest/sphinx/probe commands (some with
`timeout` and `env -u OS_COLOR`), commands that point at IOPtics test files
(`ioptics/tests/...`), IOPtics scratchpad scripts (`probe1.py`, `probe3.py`,
`sphinx_t4*`), a grep of an IOPtics report, and greps inside the ocean14
bokeh bundle.  None of them generalize.  The broad `python:*` and `python3:*`
rules already cover most of them anyway.  What I learned: the IOPtics file
mixes a deliberate policy (the first 37 allow entries plus deny/ask) with
entries that Claude Code appended automatically when a prompt was approved,
so the split was clean.  The WebFetch domains are ocean-optics publishers and
are of limited use for PypeIt; they were kept as the task asked and can be
swapped for astronomy publishers (e.g. iopscience, academic.oup.com, arxiv.org)
later.  `.claude/skills/` was not touched.  The JSON passed validation with
`python3 -m json.tool`.  No state-changing git commands were run; nothing was
staged or committed.

### 2026-10-21 (Basic start up: .gitignore, README, settings suggestion)

Executed task 1 under "Basic start up".  `.gitignore` already existed (the
stock GitHub Python template from the initial commit), and the siblings
(the-holy-grail, keck-etcs, shane-telescope, first-hires-exoplanet) all use
that same template with repo-specific lines appended at the bottom, so I kept
it and appended a PypeIt-misc section: LaTeX build products (`.aux`, `.bbl`,
`.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, beamer and
biblatex files, etc.), LibreOffice lock files, macOS `.DS_Store`/`._*`,
editor files (`.vscode/`, `.idea/`, `*.code-workspace`, swap and backup
files), and `.claude/settings.local.json` (as first-hires-exoplanet does).
`*.log` was already covered by the template.  No patterns for `.pdf`, `.odp`,
`.tex`, `.bib` or `.sty`; `git ls-files -ci --exclude-standard` reports no
tracked file being ignored.  Rewrote `README.md` in the style of keck-etcs
and first-hires-exoplanet (short intro, a "Layout" list, "Authors" with
Claude listed, plus a License line): it links to the main PypeIt repo, says
this is not a package, describes each top-level directory, flags
`deprecated/` as reference only, and lists the two prompt docs.  No
`setup.py` or `requirements.txt` was added.  Wrote the settings.json
recommendation under "Report" above (first-hires-exoplanet as the model;
swap the ocean-optics WebFetch domains for ADS/arXiv/IOP/PypeIt docs, add
`diff`); `settings.json` itself was not edited.  What I learned about the
siblings: the recent Claude-era repos (keck-etcs, first-hires-exoplanet,
the-holy-grail, shane-telescope) share a template (GitHub Python
`.gitignore` plus data-file ignores such as `*.fits` with `!` exceptions for
package data, a markdown README with Installation/Layout/Authors, `CLAUDE.md`,
`claude_prompts/`, and `.claude/skills/`), while the older
PypeIt-development-suite and MUSERePipe use short hand-written `.gitignore`
files and longer, install-focused READMEs (`README.rst` in the dev suite) and
have only `.claude/skills/`, no `settings.json`.  This repo uses
`prompts/` instead of `claude_prompts/`.  No state-changing git commands
were run; nothing was staged or committed.
