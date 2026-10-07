# Handoff

## Repository

- Project: **Programska oprema pri pouku**
- Current branch: `main`
- Remote status at last check: branch was up to date with `origin/main`
- Working directory: `c:\Users\pm87299\Documents\POP\programska-oprema-pri-pouku`

## Context

The user is preparing short, student-friendly mathematics study guides in Slovenian. The current topic is **zaporedja** (sequences). The user explicitly asked to keep the README separate from the study material and to leave the existing sequence guide unchanged when producing a LaTeX copy.

## Completed work

- `PREGLED-SNOVI/Zaporedja.md` — original Markdown guide, covering sequence notation, arithmetic and geometric sequences, sum formulas, worked examples, and a problem-solving procedure. The user asked to keep this file unchanged during the LaTeX conversion.
- `PREGLED-SNOVI/Zaporedja.tex` — LaTeX copy of the guide; uses UTF-8, Slovenian babel, AMS math, and A4 layout.
- Commit `af9218e` (“Add sequences study guide”) added the Markdown guide and was pushed to `origin/main`.

## State at handoff

Last checked, `README.md` had a staged change as well as additional unstaged changes. Its latest visible content was the project heading and the sentence “Gradivo in izdelki pri predmetu Programska oprema pri pouku.” Do not reset, overwrite, or include those README changes in another commit without the user's instruction.

The LaTeX source was untracked and there were untracked TeX build artifacts in `PREGLED-SNOVI/`: `.aux`, `.fdb_latexmk`, `.log`, and `.synctex(busy)`. The `.synctex(busy)` filename suggests a build may still be running; check before removing artifacts. The repository was otherwise reported up to date with the remote before these new local changes.

## Suggested next steps

1. Preserve the Markdown guide and README changes unless explicitly asked to edit them.
2. Check whether the LaTeX build has finished, then compile `Zaporedja.tex` and review any errors if requested.
3. Before staging or committing, inspect `git status` and include only files the user explicitly wants committed.
