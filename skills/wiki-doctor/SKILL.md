---
name: wiki-doctor
description: Refresh existing repo-local wiki pages, including module Whitebox Component Diagram source models and generated views, against the latest Wiki Guidance System without losing original information. Use when the user asks to audit, dry run, doctor, clean up, restructure, rewrite, split, merge, rename, or normalize existing wiki pages for reader quality.
---

# wiki-doctor

## Required References

Read these before acting:

- `../references/wiki-guidance-principles.md`
- `../references/wiki-structure.md`
- `../references/drift-page-rules.md`
- `../references/writing-blocks/canonical-index.md`
- Relevant `../references/writing-guidance/*.md` files for the scoped wiki pages
- Relevant `../references/writing-blocks/*.md` files for the rewrite shape
- For module-page refreshes, `../references/writing-guidance/module-page.md` and `../references/writing-blocks/whitebox-component.md`

For whole-wiki refresh, read all page-family guidance and the writing blocks needed by the existing pages. For narrow page or directory scope, read only the matching guidance plus any block guidance needed to preserve the page's information.

## Boundary

Use this skill only for an existing target repository's top-level `wiki/`.

If `wiki/` is missing, stop immediately and recommend `wiki-sink`. Do not initialize a missing wiki from scratch.

Require an empty Drift Page before any audit or rewrite. This gate applies to `audit-only` mode too.

Do not inspect source code, tests, routes, config, root `README.md`, `docs/**`, ADRs, AGENTS files, or skill source files to decide whether wiki facts are current. `wiki-doctor` reads existing wiki content and refreshes its reader-facing structure; it does not compare the wiki with the current system.

Do not classify drift, do not rewrite an existing `wiki/07-drift.md`, and do not capture new stable knowledge. If a finding needs code/wiki comparison, fact verification, or missing coverage classification, report `drift_or_coverage_suspect` and recommend `wiki-drift-radar`.

For module pages, `wiki-doctor` may create or refresh the co-located `.whitebox.yaml` source model and generated complete/derived Whitebox SVGs under a module-local `assets/` subdirectory only from facts already present in the existing wiki content being refreshed. It must not inspect target source code to discover new whitebox facts, must not treat generated SVGs as fact sources, and must not write Whitebox files outside the target repo's top-level `wiki/`.

Do not use schema, validator, lint, compliance, PASS, or FAIL language. This is semantic reader-quality work, not mechanical validation.

## Modes

`audit-only` mode means read and report only. Treat phrases like "dry run", "plan only", "only check", "do not edit files", or "audit-only" as `audit-only`.

Default mode is semantic audit plus direct writes for safe items. Write only items classified as `safe_guidance_rewrite`; report all risks without editing those areas.

## Drift Page Gate

1. Locate top-level `wiki/`.
2. If `wiki/` is missing, stop and recommend `wiki-sink`.
3. Inspect `wiki/07-drift.md` before auditing any stable page.
4. If `wiki/07-drift.md` exists and has active items, stop and tell the user to run `wiki-drift-govern` first.
5. If `wiki/07-drift.md` exists and is semantically empty but not in the standard empty-state format, continue but do not rewrite it; include a gate note.
6. If `wiki/07-drift.md` is missing in an existing wiki, search only inside `wiki/` for old drift-like queues or unresolved drift/radar/gap notes.
   - If any old drift-like queue exists, stop and ask the user to clarify whether it should be governed, migrated, or removed. Do not audit stable pages yet.
   - If no old drift-like queue exists, `complete_skeleton` may create the standard empty state in default mode. In `audit-only` mode, report the needed `complete_skeleton` action and stop before stable-page audit unless the user permits writing the skeleton.

The standard empty state is:

```md
# 漂移治理（Drift）

No active drift or coverage gaps.
```

## Skeleton Completion

For an existing wiki, `wiki-doctor` may perform `complete_skeleton` before page refresh when the Drift Page gate is clear or can be made clear by creating a missing empty `wiki/07-drift.md`.

Allowed `complete_skeleton` work:

- Create missing fixed skeleton files from `../references/wiki-structure.md`.
- Create missing catalog directories and README files.
- Create a missing `wiki/07-drift.md` only as the standard empty state.

Constraints:

- Never overwrite an existing file.
- Never rewrite an existing Drift Page.
- Never invent stable knowledge while completing the skeleton.
- If old drift-like queues or unresolved drift notes exist, stop and ask the user.
- In `audit-only` mode, report the structural changes that would be made instead of writing them.

## Scope Rules

Default scope is the whole stable wiki: `wiki/**/*.md` except `wiki/07-drift.md`.

Supported scopes:

- A single wiki page.
- A wiki directory.
- A named topic already present in wiki content.
- Whole wiki.

Scope limits writes. Scope-external wiki pages may be read for context, but are not rewritten except for canonical-index updates directly required by a safe action. If the user explicitly restricts edits to one file, do not update other files; report any needed index or link updates as out-of-scope suggestions.

`wiki-doctor` only processes top-level `wiki/`. It does not edit target-repository files outside `wiki/`, and it does not edit this Skill Suite Source Repository's `CONTEXT.md`, `wiki-suite-design.md`, `skills/references/**`, or skill instructions. Changes to the Wiki Guidance System itself are skill-suite maintenance work, not `wiki-doctor` work.

Within any scope that includes module pages, safe Whitebox refresh may also write the module page's co-located `.whitebox.yaml` source model. Generated Whitebox SVG outputs, including the complete diagram and non-empty Derived Whitebox View SVGs, must be written under that module directory's `assets/` subdirectory. Other non-Markdown files remain out of scope.

## Classifications

Classify each candidate change before editing:

- `safe_guidance_rewrite`: Existing wiki information can be reformatted, moved, split, merged, renamed, indexed, tabled, or diagrammed without changing meaning or losing evidence.
- `meaning_loss_risk`: The change may alter meaning, naming, ownership, page/module/model boundary, business intent, decision meaning, evidence, uncertainty, or unique information.
- `drift_or_coverage_suspect`: The issue appears to require code/wiki comparison, fact verification, drift classification, or new coverage.

Only `safe_guidance_rewrite` can be written by default. `meaning_loss_risk` and `drift_or_coverage_suspect` are report-only unless the user gives new confirmation that turns the work into a safe existing-wiki rewrite.

For `wiki/01-system.md`, migrate older system-overview structures to the current C1 / C2 / Runtime Topology shape by default only when all existing information, names, boundaries, evidence, and uncertainty can be preserved. If migration would require deciding current system facts, changing meaning, or dropping unique information, report `meaning_loss_risk` or `drift_or_coverage_suspect` instead of rewriting that area.

For `wiki/04-modules/**`, refresh older module maps into Whitebox Component Diagrams only when the existing wiki already contains enough confirmed information to build a legal source model: enclosing module name, at least one boundary port, at least one external node, an `external` connector between them, and any internal parts or interface roles being migrated. A Mermaid diagram, PlantUML sketch, draw.io XML, Markdown table, prose block, generated SVG, or image can be migration input, but the resulting `.whitebox.yaml` becomes the fact source and every SVG is derived output. Preserve meaningful old-map arrow labels as connector labels when they say action, data, protocol, contract, ownership, buffering, or persistence; do not create visible connector labels that only restate endpoints like `A -> B`. If a dense source model generates non-empty Derived Whitebox Views, embed them directly after the complete diagram and visible source model link with clear `... Derived Whitebox View` headings and alt text. If the old map does not identify legal whitebox facts, connector direction, evidence, or uncertainty clearly enough, report `meaning_loss_risk`; if deciding the facts requires code/wiki comparison or missing coverage classification, report `drift_or_coverage_suspect`.

## Action Vocabulary

Use these action names in reports. They are vocabulary, not a machine schema:

- `rewrite_page`: Reshape dense prose, headings, lists, tables, or diagrams while preserving all information.
- `add_reader_entry`: Add or improve an intro, reader question, reading route, or next-step cue from existing wiki content.
- `add_table_or_diagram`: Convert existing dense relationships, activities, states, surfaces, navigation, or module-boundary maps into a clearer table, Mermaid diagram, or Whitebox Component Diagram.
- `update_canonical_index`: Rebuild or adjust an index from existing wiki pages without inventing names or deciding conflicts.
- `relocate_content`: Move content to the page that already owns the same canonical concept.
- `split_page`: Split a page only when each destination preserves the same confirmed concepts and all links/evidence remain recoverable.
- `deduplicate_content`: Remove duplicate presentation only after preserving every unique fact, condition, evidence anchor, and uncertainty.
- `safe_page_delete`: Delete only a redundant page whose unique information has been migrated and whose canonical concept is preserved elsewhere.
- `safe_file_rename`: Rename only when the same canonical concept is preserved, links are updated, and aliases or uncertainty are not lost.
- `safe_page_merge`: Merge pages only when they are the same canonical concept and all unique information/evidence survives.
- `complete_skeleton`: Add missing fixed skeleton files for an existing wiki under the gate rules.
- `risk_report_only`: Report a `meaning_loss_risk` without editing.
- `recommend_drift_radar`: Report a `drift_or_coverage_suspect` and recommend `wiki-drift-radar`.

`safe_page_delete`, `safe_file_rename`, and `safe_page_merge` require extra care: preserve the same canonical concept, migrate unique information and evidence, update internal links, and report the migration. Do not keep migration history in wiki body; use the final report. Short redirect pages are allowed only when compatibility is needed.

## Workflow

1. Read the required references for the requested scope. When auditing or rewriting `wiki/01-system.md`, read `../references/writing-guidance/system-overview.md`.
2. Run the Drift Page gate and skeleton check.
3. If the gate blocks, stop before auditing stable pages.
4. Determine mode and scope from the user request.
5. Read scoped stable wiki pages and relevant canonical indexes.
6. Compare existing page structure against the Wiki Guidance System:
   - preserve information first;
   - improve reader entry, navigation, canonical names, tables, diagrams, and evidence placement when safe;
   - keep uncertainty visible;
   - avoid template-filling and mechanical completeness claims.
7. For scopes that include module pages, identify any existing Module Boundary Map, Module Boundary block, dependency-like boundary map, Mermaid/PlantUML/draw.io diagram, table, prose map, SVG, or image that appears to describe module boundaries. Treat conversion to a Whitebox Component Diagram as a candidate change only when every converted fact is already explicit in the wiki content and can be preserved without choosing new meaning.
8. Classify candidate changes.
9. In `audit-only`, write nothing and report proposed actions.
10. When a Whitebox refresh is classified as `safe_guidance_rewrite` in default mode:
   - Create or update the co-located `.whitebox.yaml` source model.
   - Create or reuse an `assets/` subdirectory beside the module page for generated Whitebox SVG files. Do not place generated `.whitebox*.svg` files directly beside the Markdown page.
   - Keep visible connector labels meaningful. Use action/data/protocol/contract phrases from confirmed wiki facts, and omit labels that would only repeat endpoint direction.
   - Render the complete `.whitebox.svg` from that source model into the module-local `assets/` directory. When the suite renderer is available, use `python3 scripts/check_whitebox_fixtures.py render <source.whitebox.yaml> assets/<name>.whitebox.svg` or the equivalent installed command.
   - For dense diagrams, render non-empty Derived Whitebox Views from the same source model into the same module-local `assets/` directory with `python3 scripts/check_whitebox_fixtures.py render-derived <source.whitebox.yaml> assets/` or the equivalent installed command. Do not embed empty derived views.
   - Validate the source model. When the suite checker is available, use `python3 scripts/check_whitebox_fixtures.py validate <source.whitebox.yaml>` or the equivalent installed command.
   - Treat obvious generated-view readability defects, including connector lines crossing port labels or arrowheads landing over port text, as renderer or fixture issues to fix before publishing.
   - Update the module page Markdown to embed the complete generated SVG first using `./assets/<name>.whitebox.svg`, keep the `.whitebox.yaml` source model link visible beside the diagrams, and then embed non-empty Derived Whitebox Views from `./assets/` with clear headings and alt text.
   - Keep generated complete and derived SVGs out of the fact-source chain. If a later refresh needs facts, read the `.whitebox.yaml` source model and existing wiki prose, not the generated SVGs.
   - Preserve old-map information that does not fit the diagram as prose, uncertainty, or risk notes instead of deleting it.
11. In default mode, apply only `safe_guidance_rewrite` and allowed `complete_skeleton` changes.
12. Stop and ask a focused question only when a small number of `meaning_loss_risk` items block an otherwise safe rewrite. Otherwise report risks without editing them.

## Output

Always report:

- Gate notes, including whether `wiki/07-drift.md` was empty, missing, non-standard empty, or blocking.
- Structural changes made or proposed, especially `complete_skeleton`.
- Changed pages, with action names.
- Whitebox Component Diagram source models, complete SVGs, and non-empty derived SVGs created, refreshed, rendered, validated, and linked, or why old module maps were left unchanged.
- Skipped risk items classified as `meaning_loss_risk`.
- Suspected drift or coverage items classified as `drift_or_coverage_suspect`, with a recommendation to run `wiki-drift-radar`.
- Out-of-scope suggestions caused by scope limits.
- Deleted, renamed, merged, or redirected pages, if any.
- Whether the run was `audit-only` or default safe rewrite.

If no pages changed, say so clearly and report the remaining risks or next recommended skill.
