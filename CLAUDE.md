# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**PypeIt-misc** -- "this and that" related to
[PypeIt](https://github.com/pypeit/PypeIt) that does not belong in the main
code base: deprecated modules kept for reference, the JOSS paper,
presentations, proposals, and prompt docs for one-off analyses of the PypeIt
project (e.g. counting lines of code).  It is a miscellany, **not** a Python
package.

## Conventions

- **Git is handled by the user.**  Do not run `git add`, `git commit`,
  `git push`, or any other state-changing git commands; the user performs all
  git operations.  Read-only commands (`git status`, `git log`, `git diff`)
  are fine when they help.
- **Calculations go in scripts.**  If you do any calculation, write it as a
  Python script on disk (not an inline one-off) so the user can add it to the
  repository.
- **Python environment.**  If you need to run Python, use the `pypeit14`
  conda environment (e.g. `conda run -n pypeit14 python ...`).

## Related repositories (read-only)

- Main PypeIt repo: `/Users/xavier/Projects/PypeIt/PypeIt`
- Development suite: `/Users/xavier/Projects/PypeIt/PypeIt-development-suite`

Analyses in this repo will often read from those sibling clones.  **Never
write to them.**

## Prompts

- Prompt docs live in [prompts/](prompts/) (not `claude_prompts/`).
- Read the relevant prompt doc before acting, and do only the numbered task
  you were pointed at.
- Work performed by Claude is logged under the "Logs" section of the prompt
  doc (e.g. [prompts/start_up.md](prompts/start_up.md)), using the format in
  its "Logging" section.

## Layout

- `deprecated/` -- old PypeIt code (modules plus `bin/` scripts), kept for
  reference only.  Do not modernize, lint, or refactor it.
- `paper/` -- the JOSS paper (`paper.md`, `paper.bib`, figures).
- `presentations/` -- talks and slides (e.g. `DRWG/`, `SSC/`, `py/`).
- `proposals/` -- funding/telescope proposals (`ADAP/`, `NSF/`, `UCO/`,
  `WMKO/`).
- `prompts/` -- prompt docs driving Claude tasks and their logs.
- `lines_of_code/` -- line-count analysis of the PypeIt repo (scripts, CSV,
  figure); re-run `count_lines.py` then `plot_lines.py` with `pypeit14`.
- `README.md`, `LICENSE` (BSD 3-Clause).
