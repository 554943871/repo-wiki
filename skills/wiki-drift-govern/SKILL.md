---
name: wiki-drift-govern
description: Resolve active items in wiki/07-drift.md by updating repo-local wiki pages for Wiki Drift or Coverage Gap, changing code for confirmed Code Drift, and clearing resolved drift items. Use when the Drift Page has active items and the user wants to govern, resolve, fix, or clear wiki drift findings.
---

# wiki-drift-govern

## Required References

Read these before acting:

- `../references/drift-page-rules.md`
- `../references/wiki-structure.md`
- Relevant `../references/writing-guidance/*.md` files for affected pages
- Relevant `../references/writing-blocks/*.md` files for affected explanatory blocks

## Boundary

Use this skill only when `wiki/07-drift.md` has active items.

Resolve only classified Drift Page items. Do not perform open-ended refactors, broad documentation rewrites, or new radar checks.

Do not silently resolve ambiguous findings. If a Drift Page item is ambiguous or lacks a clear type, ask the user to classify it as `Wiki Drift`, `Code Drift`, `Coverage Gap`, or remove it from the governance queue. Do not ask the user to rerun `wiki-drift-radar` while the Drift Page has active items.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Judge and write by semantic fit, evidence, and user clarification.

## Workflow

1. Read `wiki/07-drift.md` and identify active items.
2. For each selected item, read the suggested owner page and relevant guidance.
3. If an item is ambiguous or lacks a clear type, ask the user to classify or remove it before continuing.
4. Resolve by type:
   - `Wiki Drift`: update the relevant wiki page so it matches current system facts.
   - `Coverage Gap`: add missing wiki coverage.
   - `Code Drift`: change code so implementation matches the wiki-described behavior the user confirmed should still hold.
5. For coverage gaps, write code-proven facts directly when evidence is clear. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions.
6. For code changes, keep the edit scoped to the Drift Page item and run the narrowest meaningful compile/test check for the changed area.
7. Remove resolved items from `wiki/07-drift.md`.
8. If no active items remain, write the empty state:

```md
# Drift

No active drift or coverage gaps.
```

## Output

Report:

- Items resolved.
- Files changed.
- Any user questions needed for unresolved items.
- Verification commands run for code changes.
