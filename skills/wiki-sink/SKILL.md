---
name: wiki-sink
description: Initialize the fixed top-level repo-local wiki structure and write confirmed or evidence-grounded reusable knowledge into stable wiki pages. Use when the user asks to create the wiki, seed wiki pages, sink knowledge, or update system, flow, page, module, model, or decision documentation outside an active drift-governance queue.
---

# wiki-sink

## Required References

Read these before acting:

- `../references/wiki-structure.md`
- `../references/drift-page-rules.md`
- Relevant `../references/writing-guidance/*.md` files for target pages
- Relevant `../references/writing-blocks/*.md` files for explanatory blocks

## Boundary

Use this skill only when `wiki/07-drift.md` is missing because the wiki has not been initialized, or when it has no active items.

Write only the top-level repo-local `wiki/` structure and stable wiki pages.

Do not persist raw conversation archives. Do not write guessed stable knowledge. Use confirmed user statements, current repo evidence, or clearly cited source material.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Use human-readable guidance and LLM semantic judgment.

## Workflow

1. Inspect whether top-level `wiki/` exists.
2. If `wiki/07-drift.md` exists and has active items, stop and tell the user to run `wiki-drift-govern` first.
3. For initialization:
   - If `wiki/` is absent, create the fixed structure from `../references/wiki-structure.md`, including all README files and empty `wiki/07-drift.md`.
   - If `wiki/` already exists, never overwrite existing files. Compare it with the fixed structure, list missing skeleton paths, and create only missing files when the user explicitly asked to initialize or complete the skeleton. Otherwise, report the missing paths and ask before creating them.
4. For stable knowledge writes, choose the owner page:
   - `01-system.md` for system context and major runtime units.
   - `02-flows/**` for key user, business, or system flows.
   - `03-pages/**` for user-visible pages, entry points, navigation, and page states.
   - `04-modules/**` for capability and responsibility boundaries.
   - `05-models/**` for system-understanding models.
   - `06-decisions.md` for current active decisions and tradeoffs.
5. Read the matching writing guidance before editing.
6. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions when evidence is not enough.
7. Keep edits human-readable and concise. Prefer stable wiki content over raw notes.

## Output

Report:

- Wiki pages created or updated.
- What evidence or confirmation supported the write.
- Any knowledge intentionally left out because it was unconfirmed or too implementation-local.
