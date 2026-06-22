---
name: wiki-drift-govern
description: Resolve active items in wiki/07-drift.md by updating repo-local wiki pages for Wiki Drift or Coverage Gap, changing code for confirmed Code Drift, and clearing resolved drift items. Use when the Drift Page has active items and the user wants to govern, resolve, fix, or clear wiki drift findings.
---

# wiki-drift-govern

## Required References

Read these before acting:

- `../references/wiki-guidance-principles.md`
- `../references/drift-page-rules.md`
- `../references/wiki-structure.md`
- `../references/writing-blocks/canonical-index.md`
- Relevant `../references/writing-guidance/*.md` files for affected pages
- Relevant `../references/writing-blocks/*.md` files for affected explanatory blocks

## Boundary

Use this skill only when `wiki/07-drift.md` has active items.

Resolve only classified Drift Page items. Do not perform open-ended refactors, broad documentation rewrites, or new radar checks.

Update stable wiki pages and canonical indexes only as part of resolving active Drift Page items. Do not capture unrelated new stable knowledge or refresh indexes outside the selected governance item.

Do not silently resolve ambiguous findings. If a Drift Page item is ambiguous or lacks a clear type, ask the user to classify it as `Wiki Drift`, `Code Drift`, `Coverage Gap`, or remove it from the governance queue. Do not ask the user to rerun `wiki-drift-radar` while the Drift Page has active items.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Judge and write by semantic fit, evidence, and user clarification.

## Workflow

1. Read `wiki/07-drift.md` and identify active items.
2. For each selected item, read the suggested owner page, the affected canonical index, and relevant guidance.
3. If an item is ambiguous or lacks a clear type, ask the user to classify or remove it before continuing.
4. Resolve by type:
   - `Wiki Drift`: update the relevant wiki page so it matches current system facts. If the resolution changes a confirmed stable name, owner page, boundary, or catalog route, update the canonical index in the same governance change.
   - `Coverage Gap`: add missing wiki coverage. If the new coverage introduces a confirmed stable name, owner page, boundary, or catalog route, update the canonical index in the same governance change.
   - `Code Drift`: change code so implementation matches the wiki-described behavior the user confirmed should still hold. Do not update canonical indexes unless the same active item also requires a stable wiki content change.
5. Read the affected page-family guidance and writing blocks before editing stable wiki content. When updating `wiki/01-system.md`, read `../references/writing-guidance/system-overview.md` and apply its C1 / C2 / Runtime Topology, canonical table, topology, and evidence guidance. Use `canonical-index.md` for index updates, `evidence-anchor.md` for evidence support, and the relevant block guidance for activity maps, model relations, module boundaries, public surfaces, page layout, page navigation, dependency maps, decisions, sequences, or state transitions.
6. For coverage gaps, write code-proven facts directly when evidence is clear. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions.
7. For code changes, keep the edit scoped to the Drift Page item and run the narrowest meaningful compile/test check for the changed area.
8. Remove resolved items from `wiki/07-drift.md`.
9. If no active items remain, write the empty state:

```md
# 漂移治理（Drift）

No active drift or coverage gaps.
```

## Output

Report:

- Items resolved.
- Files changed.
- Canonical indexes updated, or why no index update was needed.
- Any user questions needed for unresolved items.
- Verification commands run for code changes.
