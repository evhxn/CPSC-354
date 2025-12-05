# CPSC-354 Report Repository

This repository contains my semester-long report for **Principles of Programming Languages (CPSC-354, 2025)**.

The report is written in **LaTeX** and compiled weekly to include homework assignments, lecture summaries, and other required submissions.

## Structure

- `.gitignore` → keeps LaTeX build files and editor junk out of version control.
- `report/`
  - `report.tex` → the LaTeX source for the report.
  - `report.pdf` → the compiled report, updated weekly with new homework.
- **Programming Assignments** (nested structure):
  - `PA1/` → Assignment 1: Calculator
    - `PA2/` → Assignment 2: Calculator Extensions
      - `PA3/` → Assignment 3: Functional Language Interpreter
        - Complete functional programming language with lambda calculus, recursion, and lists
        - See `PA1/PA2/PA3/README.md` for detailed documentation

## Workflow

- This report is **continuously updated** throughout the semester.
- Weekly homework is added to `report.tex` and recompiled into `report.pdf`.
- The final version will contain all assignments, lecture notes, and the concluding essay.

## Notes

- Only `report.tex` and `report.pdf` are kept in version control — all LaTeX auxiliary files are ignored via `.gitignore`.
- The history of the report can be seen in the commit log, reflecting incremental progress across the semester.
