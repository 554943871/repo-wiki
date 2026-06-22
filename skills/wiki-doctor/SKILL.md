---
name: wiki-doctor
description: Refresh existing repo-local wiki pages against the latest Wiki Guidance System without losing original information. Use when the user asks to audit, dry run, doctor, clean up, restructure, rewrite, split, merge, rename, or normalize existing wiki pages for reader quality.
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

For whole-wiki refresh, read all page-family guidance and the writing blocks needed by the existing pages. For narrow page or directory scope, read only the matching guidance plus any block guidance needed to preserve the page's information.

## Boundary

Use this skill only for an existing target repository's top-level `wiki/`.

If `wiki/` is missing, stop immediately and recommend `wiki-sink`. Do not initialize a missing wiki from scratch.

Require an empty Drift Page before any audit or rewrite. This gate applies to `audit-only` mode too.

Do not inspect source code, tests, routes, config, root `README.md`, `docs/**`, ADRs, AGENTS files, or skill source files to decide whether wiki facts are current. `wiki-doctor` reads existing wiki content and refreshes its reader-facing structure; it does not compare the wiki with the current system.

Do not classify drift, do not rewrite an existing `wiki/07-drift.md`, and do not capture new stable knowledge. If a finding needs code/wiki comparison, fact verification, or missing coverage classification, report `drift_or_coverage_suspect` and recommend `wiki-drift-radar`.

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

## Classifications

Classify each candidate change before editing:

- `safe_guidance_rewrite`: Existing wiki information can be reformatted, moved, split, merged, renamed, indexed, tabled, or diagrammed without changing meaning or losing evidence.
- `meaning_loss_risk`: The change may alter meaning, naming, ownership, page/module/model boundary, business intent, decision meaning, evidence, uncertainty, or unique information.
- `drift_or_coverage_suspect`: The issue appears to require code/wiki comparison, fact verification, drift classification, or new coverage.

Only `safe_guidance_rewrite` can be written by default. `meaning_loss_risk` and `drift_or_coverage_suspect` are report-only unless the user gives new confirmation that turns the work into a safe existing-wiki rewrite.

For `wiki/01-system.md`, migrate older system-overview structures to the current C1 / C2 / Runtime Topology shape by default only when all existing information, names, boundaries, evidence, and uncertainty can be preserved. If migration would require deciding current system facts, changing meaning, or dropping unique information, report `meaning_loss_risk` or `drift_or_coverage_suspect` instead of rewriting that area.

## Action Vocabulary

Use these action names in reports. They are vocabulary, not a machine schema:

- `rewrite_page`: Reshape dense prose, headings, lists, tables, or diagrams while preserving all information.
- `add_reader_entry`: Add or improve an intro, reader question, reading route, or next-step cue from existing wiki content.
- `add_table_or_diagram`: Convert existing dense relationships, activities, states, surfaces, or navigation into a clearer table or Mermaid diagram.
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
7. Classify candidate changes.
8. In `audit-only`, write nothing and report proposed actions.
9. In default mode, apply only `safe_guidance_rewrite` and allowed `complete_skeleton` changes.
10. Stop and ask a focused question only when a small number of `meaning_loss_risk` items block an otherwise safe rewrite. Otherwise report risks without editing them.

## Output

Always report:

- Gate notes, including whether `wiki/07-drift.md` was empty, missing, non-standard empty, or blocking.
- Structural changes made or proposed, especially `complete_skeleton`.
- Changed pages, with action names.
- Skipped risk items classified as `meaning_loss_risk`.
- Suspected drift or coverage items classified as `drift_or_coverage_suspect`, with a recommendation to run `wiki-drift-radar`.
- Out-of-scope suggestions caused by scope limits.
- Deleted, renamed, merged, or redirected pages, if any.
- Whether the run was `audit-only` or default safe rewrite.

If no pages changed, say so clearly and report the remaining risks or next recommended skill.
