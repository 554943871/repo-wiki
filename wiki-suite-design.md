# Wiki Skill Suite Design

This document records the current operating design for the Repo Wiki Skill Suite. `CONTEXT.md` remains the glossary; this file holds the workflow and output structure.

## Scope

The suite is a Local Skill Suite, not a plugin bundle.

The suite writes a Repo-Local Wiki into a Target Repository. The Repo-Local Wiki is the top-level `wiki/` directory only.

## Skill Set

V1 has four skills:

```text
wiki-sink
wiki-doctor
wiki-drift-radar
wiki-drift-govern
```

## Source Repository Layout

The V1 target Skill Suite Source Repository uses ordinary local skill directories:

```text
skills/
  wiki-sink/
    SKILL.md
    agents/
      openai.yaml
  wiki-doctor/
    SKILL.md
    agents/
      openai.yaml
  wiki-drift-radar/
    SKILL.md
    agents/
      openai.yaml
  wiki-drift-govern/
    SKILL.md
    agents/
      openai.yaml
  references/
    wiki-guidance-principles.md
    wiki-structure.md
    drift-page-rules.md
    writing-guidance/
      system-overview.md
      flow-page.md
      page-page.md
      module-page.md
      model-page.md
      decision-map.md
      drift-page.md
    writing-blocks/
      activity-map.md
      canonical-index.md
      decision-tradeoff.md
      dependency-map.md
      model-relation.md
      page-navigation.md
      public-surface.md
      sequence.md
      state-transition.md
```

This is the suite's source layout. It is separate from the `wiki/` output that `wiki-sink` creates inside a Target Repository.

Shared references stay thin and only hold stable cross-skill rules. Individual skill instructions should not duplicate the fixed wiki structure or Drift Page rules.

The suite deliberately avoids schema-oriented language. Do not introduce Doc Schema, Fragment Schema, page schema, validators, linters, compliance checks, or PASS/FAIL language. Wiki quality is judged through human-readable guidance and LLM semantic checking, not mechanical structure checks.

`wiki-structure.md` includes the fixed layout and minimal initial page text with human-readable guidance. It must not define rigid field templates for child pages.

`wiki-guidance-principles.md` is the shared principle layer for all wiki skills. It records cross-cutting rules such as Information Preservation, reader-first structure, evidence-aware writing, canonical naming, no guessing stable knowledge, and no mechanical correctness theater.

`writing-guidance/` holds central quality guidance for each wiki page family. `writing-blocks/` holds reusable writing patterns for common explanatory blocks. These files are semantic standards for LLM writing and review, not schemas or mechanically checked templates.

Guidance and block files must be self-contained. They may be authored from prior documentation experience, but they must not advertise inheritance from another documentation system or create compatibility expectations.

Guidance and block files use Chinese prose by default, while keeping English file names and stable terms such as `wiki-doctor`, `wiki-drift-radar`, `Wiki Drift`, and `Coverage Gap`.

The suite should absorb useful fine-grained writing lessons from mem-style Doc Schema and Fragment Schema work, but only as natural-language guidance. It must not import schema names, schema gates, validators, PASS/FAIL states, or mechanical compliance claims.

`caliber-map` is intentionally out of scope for V1. If a target repo has a few important field meanings, they belong in model pages as key fields. If it needs full field-caliber governance, that is a later design question, not part of the first wiki readability improvement.

### wiki-sink

`wiki-sink` is used when `wiki/07-drift.md` has no active items.

It initializes the fixed Repo-Local Wiki skeleton and records confirmed or evidence-grounded reusable knowledge into stable wiki pages.

It must not write guessed stable knowledge. It must not persist raw conversation archives. It does not own radar result persistence.

When initializing an existing `wiki/`, `wiki-sink` must not overwrite existing files. It may create missing skeleton files only when the user explicitly asked to initialize or complete the skeleton; otherwise it reports the missing paths and asks first.

### wiki-doctor

`wiki-doctor` checks an existing Repo-Local Wiki against the current Wiki Guidance System.

It rewrites formatting, structure, and expression when the original information can be preserved. It is for guidance refresh and reader-first normalization, not for drift classification, code comparison, or new stable knowledge capture.

It must not write guessed stable knowledge, classify code/wiki drift, refresh `wiki/07-drift.md`, or change confirmed meanings while making pages easier to read.

`wiki-doctor` has a hard Drift Page gate. It normally requires `wiki/07-drift.md` to be empty before doing any page audit or rewrite. If `wiki/07-drift.md` contains active items, it stops and asks the user to run `wiki-drift-govern`.

If `wiki/` exists but fixed skeleton files are missing, `wiki-doctor` may perform `complete_skeleton`. This includes creating missing fixed skeleton files, missing catalog README files, and a missing `wiki/07-drift.md` empty state. It must not initialize a missing `wiki/` from scratch; that remains `wiki-sink`.

If `wiki/07-drift.md` exists and is semantically empty but not in standard empty-state format, `wiki-doctor` may continue but does not rewrite the Drift Page. It reports the format issue only. If a missing `wiki/07-drift.md` is accompanied by old drift-like files or unresolved queues, `wiki-doctor` stops and asks for human clarification.

`wiki-doctor` supports explicit `audit-only` mode. User phrases such as "dry run", "plan only", "only check", or "do not edit files" are treated as `audit-only`. The default mode is audit plus direct rewrite of safe items.

The result classifications are:

- `safe_guidance_rewrite`: the existing wiki information can be reformatted, moved, split, merged, renamed, indexed, or diagrammed without changing meaning.
- `meaning_loss_risk`: the change may alter meaning, naming, ownership, page/module/model boundary, business intent, decision meaning, or unique evidence.
- `drift_or_coverage_suspect`: the issue appears to require code/wiki comparison, fact verification, or missing coverage classification, so `wiki-doctor` reports it and recommends `wiki-drift-radar`.

`wiki-doctor` may write only `safe_guidance_rewrite` items. It reports `meaning_loss_risk` and `drift_or_coverage_suspect` without changing those areas. It can ask focused follow-up questions for a small number of blocking `meaning_loss_risk` items, but it is not a broad interview skill.

Supported actions are report vocabulary, not a machine schema:

- `rewrite_page`
- `add_reader_entry`
- `add_table_or_diagram`
- `update_canonical_index`
- `relocate_content`
- `split_page`
- `deduplicate_content`
- `safe_page_delete`
- `safe_file_rename`
- `safe_page_merge`
- `complete_skeleton`
- `risk_report_only`
- `recommend_drift_radar`

`wiki-doctor` can create, rename, merge, or delete pages only when the action preserves the same canonical concept and all unique information, evidence anchors, links, and navigation remain recoverable. It may not use these actions to create a new concept boundary or decide which conflicting fact is correct.

`wiki-doctor` defaults to the whole stable wiki scope: `wiki/**/*.md` except `wiki/07-drift.md`. It supports page, directory, or wiki-topic scope. Scope limits writes. Scope-external pages may be read for context but are not rewritten, except for canonical index updates directly required by a safe action unless the user explicitly says to edit only one file.

`wiki-doctor` does not process files outside the target repository's top-level `wiki/`, such as root `README.md`, `docs/**`, ADRs, AGENTS files, source code, this Skill Suite Source Repository's `CONTEXT.md`, or skill source files.

`wiki-doctor` does not run mechanical checks. Its report is semantic: reader-quality audit, changed pages, skipped risk items, suspected drift or coverage, out-of-scope suggestions, deleted/renamed/merged pages, and Drift Page gate notes.

### wiki-drift-radar

`wiki-drift-radar` compares the Target Repository's current working-tree system with its Repo-Local Wiki. It defaults to whole-project review and may accept a user-specified scope.

It classifies findings as:

- `Wiki Drift`: the wiki is outdated or wrong, so the wiki should change.
- `Code Drift`: code diverges from wiki-described behavior that the user confirms should still hold, so code should change.
- `Coverage Gap`: important current system knowledge is missing from the wiki.

If classification is ambiguous, `wiki-drift-radar` must ask the user before writing. It must not hand ambiguous drift to `wiki-drift-govern`.

`wiki-drift-radar` may refresh only `wiki/07-drift.md`, and it may do so without confirmation after classification. It must not write stable wiki pages.

Before starting, `wiki-drift-radar` checks only `wiki/07-drift.md`. If it contains active items, `wiki-drift-radar` stops and asks the user to run governance first. It does not require a clean git working tree; the current working tree is the current system being compared.

If the wiki is too thin for meaningful comparison, `wiki-drift-radar` stops normal checking and refreshes `wiki/07-drift.md` with a `Wiki Too Thin` status and needed wiki seeds.

### wiki-drift-govern

`wiki-drift-govern` is used when `wiki/07-drift.md` has active items.

It resolves classified items:

- For `Wiki Drift`, update the relevant wiki page.
- For `Coverage Gap`, add missing wiki coverage.
- For `Code Drift`, change code so implementation matches the wiki-described behavior.

For coverage gaps, code-proven facts may be written directly. Business intent, design rationale, page or module naming, and boundary decisions require user confirmation.

After an item is resolved, `wiki-drift-govern` removes it from `wiki/07-drift.md`. When all active items are resolved, it writes the empty state.

`wiki-drift-govern` is not an open-ended refactor skill. If a Drift Page item is ambiguous or lacks a clear type, `wiki-drift-govern` asks the user to classify it as `Wiki Drift`, `Code Drift`, `Coverage Gap`, or remove it from the governance queue. It must not send the user back to `wiki-drift-radar` while active items remain.

## Canonical Index

The Repo-Local Wiki does not use a separate glossary page. Canonical naming and navigation are distributed to the owner pages that already explain each knowledge family:

| Knowledge kind | Canonical source |
| --- | --- |
| Roles | `wiki/01-system.md` |
| External Systems | `wiki/01-system.md` |
| Main Runtime Units | `wiki/01-system.md` |
| Flows | `wiki/02-flows/README.md` |
| Pages | `wiki/03-pages/README.md` |
| Modules | `wiki/04-modules/README.md` |
| Models | `wiki/05-models/README.md` |
| Decisions | `wiki/06-decisions.md` |

`wiki/01-system.md` should provide repo-wide Canonical Roles, Canonical External Systems, and Main Runtime Units. Other pages should reuse those names rather than inventing synonyms.

Catalog README files are canonical indexes for their own family. They are not passive directories; they route readers and agents to the right flow, page, module, or model page.

`wiki-sink` must maintain canonical indexes when writing new stable knowledge whose name, owner, and boundary are confirmed. `wiki-doctor` may rebuild or update canonical indexes from existing wiki pages. `wiki-drift-radar` reads canonical indexes to judge coverage and owner pages but does not write them. `wiki-drift-govern` must update canonical indexes when resolving Wiki Drift or Coverage Gap items that change stable wiki content.

If names conflict, boundaries are unclear, or owner pages are not confirmed, the skill must ask the user or report `meaning_loss_risk`; it must not invent a canonical name.

## Fine-Grained Writing Blocks

V1 should strengthen the Wiki Guidance System with fine-grained writing blocks inspired by mem-style fragment guidance, while keeping them as prose guidance.

New blocks:

- `activity-map`: flow主链路表达；说明谁在什么条件下做什么业务动作，表达分支、汇合、异常和跨角色交接。它 does not turn Controller/Service/SQL/runtime/adapter/payload into business activities.
- `model-relation`: model关系表达；推荐使用 `泛化`、`组成`、`引用`、`衍生`、`事实源` as semantic relationship labels. It must preserve the distinction between `引用` and `衍生`.
- `canonical-index`: repo-wide and catalog-wide naming/navigation rules.
- `public-surface`: stable public entry points, user-facing surfaces, tools, APIs, or module capabilities needed to understand a boundary.

Existing blocks to strengthen:

- `sequence`: participant names must stay at one abstraction level; actors are triggers or result receivers; implementation details are evidence, not participants.
- `state-transition`: stable states only; no temporary booleans or display states unless explicitly marked as display states.
- `page-navigation`: user-visible navigation only; route params, visibility conditions, and backend calls should not be forced into navigation edges.
- `dependency-map`: distinguish runtime calls, data references, responsibility dependencies, ownership, and fact sources.
- `decision-tradeoff`: decision blocks must explain a real current tradeoff and what it rules out.

Do not add a separate `reader-map` block in V1. Reader-first entry guidance belongs in principles and page-family guidance, and should be used for README pages, catalog pages, system overview, and complex long pages.

Do not add `caliber-map` in V1.

## Drift Page Ownership

`wiki/07-drift.md` is a current-state governance queue with different permissions per skill:

| Skill | Drift Page permission |
| --- | --- |
| `wiki-drift-radar` | May refresh active findings or write the standard empty state when it owns the radar pass. |
| `wiki-drift-govern` | May resolve and remove active items; must write the standard empty state when the queue is cleared. |
| `wiki-sink` | May create the standard empty state during wiki initialization or skeleton completion; otherwise only reads the gate and reports non-standard empty formatting. |
| `wiki-doctor` | Only reads the gate, except it may create a missing `wiki/07-drift.md` empty state as part of `complete_skeleton` for an existing wiki. It does not rewrite an existing Drift Page. |

The standard empty state is:

```md
# Drift

No active drift or coverage gaps.
```

## Target Wiki Structure

`wiki-sink` initializes this fixed structure:

```text
wiki/
  README.md
  01-system.md
  02-flows/
    README.md
  03-pages/
    README.md
  04-modules/
    README.md
  05-models/
    README.md
  06-decisions.md
  07-drift.md
```

Top-level content pages and folders use numeric prefixes for reading order. `README.md` files are never numbered. Child content pages inside folders are not numbered.

### README.md

Explains how to read the wiki and what each top-level section contains.

### 01-system.md

Provides a human-readable system overview. It roughly covers C4 C1 and C2: system context and major runtime units. It does not enter component, class, or function-level detail.

### 02-flows/

Explains key user, business, and system flows before readers inspect pages and module boundaries. It excludes ordinary call chains, test steps, trace dumps, and troubleshooting SOPs.

### 03-pages/

Explains user-visible pages, entry points, navigation, visible states, and page relationships to flows, modules, and models. It excludes DOM trees, CSS details, component-library inventories, and backend call chains.

### 04-modules/

Explains human-meaningful capability and responsibility boundaries. A module may or may not match a code directory, page, service process, or package.

### 05-models/

Explains important system-understanding models: core objects, state, relationships, and rules. These are not strict DDD models and do not focus on persistence technology such as MySQL or Redis.

### 06-decisions.md

Summarizes current active decisions and tradeoffs for human understanding.

### 07-drift.md

Stores the current active radar findings while they are being governed. It is not a history archive.

## Drift Page Contract

`wiki/07-drift.md` represents the current governance queue.

Empty state:

```md
# Drift

No active drift or coverage gaps.
```

When non-empty, it may contain:

```md
# Drift

## Wiki Too Thin

## Active Drift

## Coverage Gaps
```

Each active item should include a short Evidence Note:

```md
### {Finding title}
- Type: Wiki Drift | Code Drift | Coverage Gap
- Wiki text or missing coverage: ...
- Current evidence: ...
- Evidence: path/to/file
- Suggested owner page: wiki/...
- Candidate wiki note: ...
```

`Candidate wiki note` is optional and is never a stable fact until `wiki-drift-govern` or `wiki-sink` writes it into a stable page.

`wiki/07-drift.md` is refreshed for current state, not appended as history. Governance history belongs in git commits or pull requests.
