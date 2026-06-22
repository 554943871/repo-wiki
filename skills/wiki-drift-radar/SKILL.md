---
name: wiki-drift-radar
description: Compare a target repository's current working-tree system with its top-level repo-local wiki, classify Wiki Drift, Code Drift, Coverage Gap, or Wiki Too Thin, ask the user to resolve ambiguity, and refresh only wiki/07-drift.md. Use when the user asks to scan, radar, inspect drift, find coverage gaps, or compare wiki docs against the current code/system.
---

# wiki-drift-radar

## Required References

Read these before acting:

- `../references/wiki-guidance-principles.md`
- `../references/drift-page-rules.md`
- `../references/wiki-structure.md`
- `../references/writing-blocks/canonical-index.md`
- Relevant `../references/writing-guidance/*.md` files for the requested scope
- Relevant `../references/writing-blocks/*.md` files when judging evidence anchors, module boundary, page layout, page navigation, sequence, dependency, state, or decision content

## Boundary

Use the current working tree as the current system. Do not require git to be clean.

Only write `wiki/07-drift.md`. Do not write any other file.

Read canonical indexes to judge expected coverage, existing owner pages, and suggested owner pages. Do not update canonical indexes or stable wiki pages. If an index is missing, conflicted, or unclear, record that as a finding, candidate wiki note, or clarification need in `wiki/07-drift.md`.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Judge by semantic reading, code evidence, and user clarification.

Outdated guidance shape alone is not semantic drift. For example, an existing `wiki/01-system.md` that has not yet been reorganized into the current C1 / C2 / Runtime Topology shape is a `wiki-doctor` guidance-refresh candidate, not a Drift Page item, unless it also contains wrong facts, missing important coverage, or boundary/name mismatches compared with the current system.

## Workflow

1. Locate the target repository's top-level `wiki/` directory.
2. Inspect `wiki/07-drift.md`.
   - If it has active items, stop and tell the user to run `wiki-drift-govern` first.
   - If it is missing because the wiki has not been initialized, report `Wiki Too Thin` and suggest `wiki-sink`.
3. Read the relevant wiki pages for the whole project by default, or the user-specified scope. When comparing `wiki/01-system.md`, read `../references/writing-guidance/system-overview.md` to understand canonical indexes, C1/C2/Runtime Topology boundaries, and coverage expectations; do not classify guidance-shape lag alone as drift.
4. Read the relevant canonical indexes:
   - Roles, External Systems, and Main Runtime Units in `wiki/01-system.md`.
   - Flows in `wiki/02-flows/README.md`.
   - Pages in `wiki/03-pages/README.md`.
   - Modules in `wiki/04-modules/README.md`.
   - Models in `wiki/05-models/README.md`.
   - Decisions in `wiki/06-decisions.md`.
5. Use canonical indexes to decide whether a concept is already covered, which page should own it, and what `Suggested owner page` should be. Treat unclear names, owner conflicts, and missing boundaries as risks to report, not as permission to rewrite indexes.
6. Read current system evidence from code, tests, routes, config, docs, and git diff as useful for the scope.
7. Classify each finding before writing:
   - `Wiki Drift`: wiki is outdated or wrong, so wiki should change.
   - `Code Drift`: code diverges from wiki-described behavior that the user confirms should still hold, so code should change.
   - `Coverage Gap`: important current system knowledge is missing from wiki.
   - `Wiki Too Thin`: wiki lacks enough relevant content for meaningful comparison.
8. If classification is ambiguous, ask the user a focused question and wait. Do not write ambiguous items.
9. Refresh `wiki/07-drift.md` with current findings, concise evidence notes, suggested owner pages, and candidate wiki notes when useful.

## Output

After writing `wiki/07-drift.md`, summarize:

- Counts by finding type.
- Any user clarifications that changed classification.
- Any canonical index gaps or owner conflicts found.
- The next recommended action, usually `wiki-drift-govern`.

If there are no active findings, leave `wiki/07-drift.md` in empty state.
