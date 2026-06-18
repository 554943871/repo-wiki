---
name: wiki-radar
description: Compare a target repository's current working-tree system with its top-level repo-local wiki, classify Wiki Drift, Code Drift, Coverage Gap, or Wiki Too Thin, ask the user to resolve ambiguity, and refresh only wiki/07-drift.md. Use when the user asks to scan, radar, inspect drift, find coverage gaps, or compare wiki docs against the current code/system.
---

# wiki-radar

## Required References

Read these before acting:

- `../references/drift-page-rules.md`
- `../references/wiki-structure.md`
- Relevant `../references/writing-guidance/*.md` files for the requested scope
- Relevant `../references/writing-blocks/*.md` files when judging page navigation, sequence, dependency, state, or decision content

## Boundary

Use the current working tree as the current system. Do not require git to be clean.

Only write `wiki/07-drift.md`. Do not write any other file.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Judge by semantic reading, code evidence, and user clarification.

## Workflow

1. Locate the target repository's top-level `wiki/` directory.
2. Inspect `wiki/07-drift.md`.
   - If it has active items, stop and tell the user to run `wiki-govern` first.
   - If it is missing because the wiki has not been initialized, report `Wiki Too Thin` and suggest `wiki-sink`.
3. Read the relevant wiki pages for the whole project by default, or the user-specified scope.
4. Read current system evidence from code, tests, routes, config, docs, and git diff as useful for the scope.
5. Classify each finding before writing:
   - `Wiki Drift`: wiki is outdated or wrong, so wiki should change.
   - `Code Drift`: code diverges from wiki-described behavior that the user confirms should still hold, so code should change.
   - `Coverage Gap`: important current system knowledge is missing from wiki.
   - `Wiki Too Thin`: wiki lacks enough relevant content for meaningful comparison.
6. If classification is ambiguous, ask the user a focused question and wait. Do not write ambiguous items.
7. Refresh `wiki/07-drift.md` with current findings and concise evidence notes.

## Output

After writing `wiki/07-drift.md`, summarize:

- Counts by finding type.
- Any user clarifications that changed classification.
- The next recommended action, usually `wiki-govern`.

If there are no active findings, leave `wiki/07-drift.md` in empty state.
