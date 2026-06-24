---
name: wiki-sink
description: Initialize the fixed top-level repo-local wiki structure and write confirmed or evidence-grounded reusable knowledge, including module Whitebox Component Diagram source models and generated views, into stable wiki pages. Use when the user asks to create the wiki, seed wiki pages, sink knowledge, or update system, flow, page, module, model, or decision documentation outside an active drift-governance queue.
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
- For module pages, `../references/writing-guidance/module-page.md` and `../references/writing-blocks/whitebox-component.md`

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
   - `whitebox-component.md` for every module page's required Whitebox Component Diagram / Module Boundary Map.
   - `module-boundary.md` for module responsibility boundaries, public surfaces, internal capabilities, collaboration direction, and module rules.
   - `page-navigation.md` for README/catalog routing and user-visible page navigation.
   - `page-layout.md` for page visible regions, stable components, overlays, drawers, tabs, page variants, visible state projection, and page-level layout.
   - `dependency-map.md` or `decision-tradeoff.md` for stable dependencies, active decisions, and current tradeoffs.
7. When writing or updating a module page under `wiki/04-modules/**`, maintain its Whitebox Component Diagram as the Module Boundary Map:
   - Create or update the co-located `.whitebox.yaml` source model from confirmed repo evidence, existing wiki facts, or user confirmation.
   - Store generated complete and derived SVGs in an `assets/` subdirectory beside the module page and source model. Do not place generated `.whitebox*.svg` files directly beside the Markdown page.
   - Keep `.whitebox.yaml` as the only diagram fact source. Mermaid, PlantUML, draw.io XML, Markdown prose, generated SVG, and other generated images are not the fact source.
   - Include at least one confirmed boundary port connected to an external node. Simple modules may omit internal `parts`, but they still need this external interaction.
   - Use connector labels only when they add relationship meaning such as action, data, protocol, contract, ownership, buffering, or persistence. Do not add visible labels that only restate endpoints like `A -> B`; omit the label if no meaningful phrase is confirmed.
   - Render the complete `.whitebox.svg` into the module-local `assets/` directory after source changes. When the suite renderer is available, use `python3 scripts/check_whitebox_fixtures.py render <source.whitebox.yaml> assets/<name>.whitebox.svg` or the equivalent installed command.
   - For dense diagrams, render non-empty Derived Whitebox Views from the same source model into the same module-local `assets/` directory with `python3 scripts/check_whitebox_fixtures.py render-derived <source.whitebox.yaml> assets/` or the equivalent installed command. Embed only generated non-empty derived SVGs.
   - Validate the source model after edits. When the suite checker is available, use `python3 scripts/check_whitebox_fixtures.py validate <source.whitebox.yaml>` or the equivalent installed command.
   - Treat obvious generated-view readability defects, including connector lines crossing port labels or arrowheads landing over port text, as renderer or fixture issues to fix before publishing.
   - Link the complete generated SVG first using `./assets/<name>.whitebox.svg`, keep the `.whitebox.yaml` source model link visible beside it, then embed non-empty Derived Whitebox Views from `./assets/` with clear `... Derived Whitebox View` headings and alt text.
   - Treat every generated SVG, including derived SVGs, as reader-facing output only. Never read facts back out of a derived SVG, and never create extra source models for derived views.
   - If the evidence does not confirm a boundary port, external node, connector direction, internal part, interface role, or ownership boundary, ask the user or leave the fact out instead of filling a placeholder.
8. Update the owner page and its canonical index together when the name, owner page, and boundary are confirmed. If a name conflict, unclear boundary, or unconfirmed owner would cause meaning loss, ask the user or leave it out instead of canonicalizing it.
9. Ask the user before writing business intent, design rationale, page names, module names, or boundary decisions when evidence is not enough.
10. Keep edits human-readable and concise. Prefer stable wiki content over raw notes.

## Output

Report:

- Wiki pages created or updated.
- Module Whitebox Component Diagram source models, complete SVGs, and non-empty derived SVGs created, updated, rendered, validated, and linked, or why they were left incomplete.
- Canonical indexes maintained, or why an index update was skipped.
- What evidence or confirmation supported the write.
- Any knowledge intentionally left out because it was unconfirmed or too implementation-local.
