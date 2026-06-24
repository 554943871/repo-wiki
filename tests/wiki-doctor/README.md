# Wiki Doctor Regression Fixtures

These fixtures give future `wiki-doctor` edits concrete examples for its most important boundaries.

Run from the repository root:

```sh
python3 scripts/check_wiki_doctor_fixtures.py
```

The script checks fixture coverage, expected action vocabulary, expected classification vocabulary, gate notes, and wording that would turn the fixture report into mechanical quality theater. It is not a judge of semantic quality, and it does not prove that any target wiki meaning is right.

Each fixture has:

- `case.json`: the behavior contract being covered.
- `input/wiki/`: the target wiki snippets that `wiki-doctor` would read.
- `expected/report.md`: the expected final report shape.
- Optional `expected/wiki/`: snippets that demonstrate required preservation, link updates, or no-write behavior.

Whitebox refresh fixtures may include co-located `.whitebox.yaml`, the complete `.whitebox.svg`, and non-empty Derived Whitebox View SVGs. The module page should show the complete diagram first, keep the source model link visible, and then embed generated derived views as reader aids from the same source model.

The cases intentionally stay small. They are not a replacement for LLM semantic review; they make boundary regressions visible when the skill text changes.

## Sample Refresh Demonstration

`sample-refresh/` contains hand-authored demonstration evidence from a generated
wiki sample. It shows how `wiki-doctor` guidance can improve reader-facing
structure while preserving original information. It is intentionally separate
from the regression fixtures and is not a universal quality benchmark.
