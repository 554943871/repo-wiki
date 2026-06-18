---
name: wiki-sink
description: Initialize the fixed top-level repo-local wiki structure and write confirmed or evidence-grounded reusable knowledge into stable wiki pages. Use when the user asks to create the wiki, seed wiki pages, sink knowledge, or update system, flow, page, module, model, or decision documentation outside an active drift-governance queue.
---

# wiki-sink

## Required References

Read these before acting:

- `../references/wiki-guidance-principles.md`
- `../references/wiki-structure.md`
- `../references/drift-page-rules.md`
- `../references/writing-blocks/canonical-index.md`
- Relevant `../references/writing-guidance/*.md` files for target pages
- Relevant `../references/writing-blocks/*.md` files for explanatory blocks

## Boundary

Use this skill only when `wiki/07-drift.md` is missing because the wiki has not been initialized, or when it has no active items.

Write only the top-level repo-local `wiki/` structure and stable wiki pages.

Create `wiki/07-drift.md` only as the standard empty state during wiki initialization or explicit skeleton completion. Otherwise, only read it as the gate and report non-standard empty formatting instead of rewriting it.

Maintain canonical indexes when writing new stable knowledge whose name, owner page, and boundary are confirmed by repo evidence, existing wiki content, or the user. Do not create a separate glossary page.

Do not persist raw conversation archives. Do not write guessed stable knowledge. Use confirmed user statements, current repo evidence, or clearly cited source material.

When the user explicitly asks to seed or update `wiki/01-system.md`, `wiki-sink` may read target-repository README files, source code, configuration, and existing wiki content to write evidence-grounded system overview facts. Facts directly supported by current repo evidence may be written with short Evidence Anchors. Business intent, canonical names, role boundaries, external-system boundaries, and runtime-unit boundaries that are not clear from evidence must be confirmed with the user instead of guessed.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. Use human-readable guidance and LLM semantic judgment.

## Workflow

1. Inspect whether top-level `wiki/` exists.
2. If `wiki/07-drift.md` exists and has active items, stop and tell the user to run `wiki-drift-govern` first.
3. For initialization:
   - If `wiki/` is absent, create the fixed structure from `../references/wiki-structure.md`, including all README files and empty `wiki/07-drift.md`.
   - Initialization creates skeleton files only. Do not infer or fill Canonical Roles, Canonical External Systems, Canonical Main Runtime Units, flows, pages, modules, models, decisions, or Deployment topology just because the skeleton contains those sections.
   - If `wiki/` already exists, never overwrite existing files. Compare it with the fixed structure, list missing skeleton paths, and create only missing files when the user explicitly asked to initialize or complete the skeleton. Otherwise, report the missing paths and ask before creating them.
4. For stable knowledge writes, read the relevant current canonical index before choosing the owner page:
   - `01-system.md` for system context and major runtime units.
   - `02-flows/**` for key user, business, or system flows.
   - `03-pages/**` for user-visible pages, entry points, navigation, page layout, page variants, visible states, and page-level interactions.
   - `04-modules/**` for capability boundaries, public surfaces, internal capabilities, collaboration rules, and related flows/pages/models.
   - `05-models/**` for system-understanding models.
   - `06-decisions.md` for current active decisions and tradeoffs.
5. Read the matching writing guidance before editing. When writing or updating `wiki/01-system.md`, read `../references/writing-guidance/system-overview.md`.
6. Read the relevant writing blocks for the content shape:
   - `canonical-index.md` for any new or updated stable name, owner route, boundary, or catalog README entry.
   - `evidence-anchor.md` for stable facts, uncertainty, candidate notes, code anchors, user confirmations, or other short evidence support.
   - `activity-map.md`, `sequence.md`, or `state-transition.md` for flow content.
   - `model-relation.md` or `state-transition.md` for model relationships, lifecycle, source-of-truth facts, or stable states.
   - `public-surface.md` for system, module, or page surfaces such as APIs, tools, routes, page entries, events, or capabilities.
   - `module-boundary.md` for module responsibility boundaries, public surfaces, internal capabilities, collaboration direction, and module rules.
   - `page-navigation.md` for README/catalog routing and user-visible page navigation.
   - `page-layout.md` for page visible regions, stable components, overlays, drawers, tabs, page variants, visible state projection, and page-level layout.
   - `dependency-map.md` or `decision-tradeoff.md` for stable dependencies, active decisions, and current tradeoffs.
7. Update the owner page and its canonical index together when the name, owner page, and boundary are confirmed. If a name conflict, unclear boundary, or unconfirmed owner would cause meaning loss, ask the user or leave it out instead of canonicalizing it.
8. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions when evidence is not enough.
9. Keep edits human-readable and concise. Prefer stable wiki content over raw notes.

## Output

Report:

- Wiki pages created or updated.
- Canonical indexes maintained, or why an index update was skipped.
- What evidence or confirmation supported the write.
- Any knowledge intentionally left out because it was unconfirmed or too implementation-local.
