---
name: wiki-sink
description: Initialize the fixed top-level repo-local wiki structure and write confirmed or evidence-grounded reusable knowledge, including canonical module owner pages plus module Whitebox Component Diagram source models and generated views, into stable wiki pages. Use when the user asks to create the wiki, seed wiki pages, sink knowledge, or update system, flow, page, module, model, or decision documentation outside an active drift-governance queue.
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
- For canonical module owner pages, including C2 root module pages and confirmed lower-level module pages tied to a C2 root or upper owner page, `../references/writing-guidance/module-page.md` and `../references/writing-blocks/whitebox-component.md`
- `../references/writing-guidance/module-overview.md` only when maintaining or interpreting older skill-suite references; do not use it as a new page-family route.

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
   - Initialization creates skeleton files only. Do not infer or fill Canonical Roles, Canonical External Systems, Canonical Main Runtime Units, flows, pages, modules, models, decisions, or Runtime Topology just because the skeleton contains those sections.
   - If `wiki/` already exists, never overwrite existing files. Compare it with the fixed structure, list missing skeleton paths, and create only missing files when the user explicitly asked to initialize or complete the skeleton. Otherwise, report the missing paths and ask before creating them.
4. For stable knowledge writes, read the relevant current canonical index before choosing the owner page:
   - `01-system.md` for system context and major runtime units.
   - `02-flows/**` for key user, business, or system flows.
   - `03-pages/**` for user-visible pages, entry points, navigation, page layout, page variants, visible states, and page-level interactions.
   - `04-modules/**` for capability boundaries, public surfaces, internal capabilities, collaboration rules, module-to-module drill-down routes, and related flows/pages/models.
   - `05-models/**` for model families, member system-understanding models, model relationships, key fields, demo/examples, and source-of-truth facts.
   - `06-decisions.md` for current active decisions and tradeoffs.
5. Read the matching writing guidance before editing. When writing or updating `wiki/01-system.md`, read `../references/writing-guidance/system-overview.md`.
   - When writing or updating any canonical module owner page under `wiki/04-modules/**`, including former `module-map.md` pages whose enclosing C2 runtime unit is confirmed as a C2 root module or whose lower-level boundary is tied to a C2 root or upper owner page, read `../references/writing-guidance/module-page.md`.
   - When writing or updating any model family page under `wiki/05-models/**`, read `../references/writing-guidance/model-page.md`.
   - When choosing or creating a `wiki/05-models/**` owner page, group models by shared reader question, stable fact chain, lifecycle, source-of-truth relationship, or demo/example explainability. Do not group or split model pages by code directory, table name, DTO/package name, field similarity, or because each model seems individually important.
   - Do not create ownerless directory-level module overview pages. If a proposed `module-map.md` does not have a confirmed canonical module name, owner page, and boundary, ask for confirmation instead of writing it as a separate overview page family.
6. Read the relevant writing blocks for the content shape:
   - `canonical-index.md` for any new or updated stable name, owner route, boundary, or catalog README entry.
   - `evidence-anchor.md` for stable facts, uncertainty, candidate notes, code anchors, user confirmations, or other short evidence support.
   - `activity-map.md`, `sequence.md`, or `state-transition.md` for flow content.
   - `model-relation.md` or `state-transition.md` for model relationships, lifecycle, source-of-truth facts, or stable states.
   - `public-surface.md` for system, module, or page surfaces such as APIs, tools, routes, page entries, events, or capabilities.
   - `whitebox-component.md` for every canonical module owner page's required Whitebox Component Diagram / Module Boundary Map.
   - `module-boundary.md` for module responsibility boundaries, public surfaces, internal capabilities, collaboration direction, and module rules.
   - `page-navigation.md` for README/catalog routing and user-visible page navigation.
   - `page-layout.md` for page visible regions, stable components, overlays, drawers, tabs, page variants, visible state projection, and page-level layout.
   - `dependency-map.md` or `decision-tradeoff.md` for stable dependencies, active decisions, and current tradeoffs.
7. When writing or updating a canonical module owner page under `wiki/04-modules/**`, follow `../references/writing-guidance/module-page.md`. Route its required Whitebox Component Diagram / Module Boundary Map work to `../references/writing-blocks/whitebox-component.md`, and write only facts confirmed by repo evidence, existing wiki facts, or user confirmation.
8. When writing or updating a former module overview or module-map page under `wiki/04-modules/**`, first confirm the enclosing boundary as a canonical module in `wiki/04-modules/README.md`. Then treat the page as a canonical module owner page and follow `../references/writing-guidance/module-page.md`. If that confirmation is missing, ask the user instead of inventing a module or preserving an ownerless overview page family.
9. Update the owner page and its canonical index together when the name, owner page, and boundary are confirmed. If a name conflict, unclear boundary, or unconfirmed owner would cause meaning loss, ask the user or leave it out instead of canonicalizing it.
10. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions when evidence is not enough.
11. Keep edits human-readable and concise. Prefer stable wiki content over raw notes.

## Output

Report:

- Wiki pages created or updated.
- Module Whitebox Component Diagram source models, complete SVGs, and non-empty derived SVGs created, updated, rendered, validated, and linked, or why they were left incomplete.
- Module owner pages created or updated, including former module-map pages converted to confirmed owner pages.
- Canonical indexes maintained, or why an index update was skipped.
- What evidence or confirmation supported the write.
- Any knowledge intentionally left out because it was unconfirmed or too implementation-local.
