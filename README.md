# PypeIt-misc

This and that related to [PypeIt](https://github.com/pypeit/PypeIt) that
does not belong in the main code base.

This is a miscellany, not a Python package.  There is nothing to install.

## Layout

- `deprecated/` -- old PypeIt modules and `bin/` scripts that have been
  pulled from the main repo.  Kept for reference only; they are not
  maintained and will not run against a current PypeIt.
- `paper/` -- the JOSS paper (`paper.md`, `paper.bib`) and its
  sky-subtraction figures.
- `presentations/` -- talks and slides (mostly LibreOffice `.odp`), e.g. for
  the Keck DRWG and SSC, plus a small script in `py/`.
- `proposals/` -- funding and telescope proposals (`ADAP/`, `NSF/`, `UCO/`,
  `WMKO/`): LaTeX source, PDFs, slides, notebooks, and the Python used to make their
  figures.
- `prompts/` -- Claude Code prompt docs and a dated log of the work done
  from them:
  - `start_up.md` -- setting up this repo (CLAUDE.md, skills, settings,
    these basic files)
  - `count_the_lines.md` -- counting the lines of code in PypeIt
- `CLAUDE.md` -- conventions for working in this repository with Claude Code.

## Authors

- J. Xavier Prochaska
- Claude

## License

BSD 3-Clause; see [LICENSE](LICENSE).
