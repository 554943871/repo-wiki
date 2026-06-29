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
      wiki-root.md
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
      evidence-anchor.md
      model-relation.md
      module-boundary.md
      page-layout.md
      page-navigation.md
      public-surface.md
      sequence.md
      state-transition.md
      whitebox-component.md
```

This is the suite's source layout. It is separate from the `wiki/` output that `wiki-sink` creates inside a Target Repository.

Shared references stay thin and only hold stable cross-skill rules. Individual skill instructions should not duplicate the fixed wiki structure or Drift Page rules.

The suite deliberately avoids schema-oriented language. Do not introduce Doc Schema, Fragment Schema, page schema, validators, linters, compliance checks, or PASS/FAIL language. Wiki quality is judged through human-readable guidance and LLM semantic checking, not mechanical structure checks.

`wiki-structure.md` includes the fixed layout and minimal initial page text. Detailed page-family writing rules belong in `writing-guidance/*.md`, not in the structure skeleton. It must not define rigid field templates for child pages.

`wiki-guidance-principles.md` is the shared principle layer for all wiki skills. It records cross-cutting rules such as Information Preservation, reader-first structure, evidence-aware writing, canonical naming, no guessing stable knowledge, and no mechanical correctness theater.

Every skill's Required References must list `wiki-guidance-principles.md` before narrower page-family guidance, block-family guidance, or workflow-specific references. The principles are the shared reader-quality baseline; narrower references explain how to apply them to a page family, block family, or drift lifecycle.

`writing-guidance/` holds central quality guidance for each wiki page family. Every active page family has exactly one primary meta-knowledge document in this directory. Detailed rules for one page family must not be split across multiple page-family documents, copied into `wiki-structure.md`, or hidden inside skill instructions. `writing-blocks/` holds block-family guidance: reusable semantic expression families for common explanatory blocks that may appear inside multiple page families. These files are semantic standards for LLM writing and review, not schemas or mechanically checked templates.

Guidance and block files must be self-contained. They may be authored from prior documentation experience, but they must not advertise inheritance from another documentation system or create compatibility expectations.

Guidance and block files use Chinese prose by default, while keeping English file names and stable terms such as `wiki-doctor`, `wiki-drift-radar`, `Wiki Drift`, and `Coverage Gap`. Final reader-facing wiki headings should use Chinese by default and keep English aliases only as stable anchors, for example `系统总览（System）` or `模型关系（Relationships）`.

The suite should absorb useful fine-grained writing lessons from mem-style Doc Schema and Fragment Schema work, but only as natural-language guidance. It must not import schema names, schema gates, validators, PASS/FAIL states, or mechanical compliance claims.

## Page-Family Meta-Knowledge Ownership

Each active page family owns one dedicated and exclusive meta-knowledge document under `skills/references/writing-guidance/`. `wiki-structure.md` may initialize the fixed skeleton and minimal starter text, but it must defer detailed page-family rules to the owner document below.

| Page family | Target wiki pages | Primary meta-knowledge document |
| --- | --- | --- |
| Wiki Root | `wiki/README.md` | `skills/references/writing-guidance/wiki-root.md` |
| System Overview | `wiki/01-system.md` | `skills/references/writing-guidance/system-overview.md` |
| Flow Pages | `wiki/02-flows/README.md`, `wiki/02-flows/*.md` | `skills/references/writing-guidance/flow-page.md` |
| Page Pages | `wiki/03-pages/README.md`, `wiki/03-pages/*.md` | `skills/references/writing-guidance/page-page.md` |
| Module Pages | `wiki/04-modules/README.md`, `wiki/04-modules/*.md` | `skills/references/writing-guidance/module-page.md` |
| Model Family Pages | `wiki/05-models/README.md`, `wiki/05-models/*.md` | `skills/references/writing-guidance/model-page.md` |
| Decision Map | `wiki/06-decisions.md` | `skills/references/writing-guidance/decision-map.md` |
| Drift Page | `wiki/07-drift.md` | `skills/references/writing-guidance/drift-page.md` plus `skills/references/drift-page-rules.md` for workflow ownership and lifecycle |

`module-overview.md` is compatibility guidance for older terminology only. It is not an active page-family owner; confirmed C2-root module-map or overview content is routed to `module-page.md`, while stable-subsystem or code-module maps need an explicit C2-root or upper-owner relationship before they become lower-level module pages. Unclear ownerless overviews are reported as `meaning_loss_risk`.

`caliber-map` is intentionally out of scope for V1. If a target repo has a few important field meanings, they belong in model family pages as key fields. If it needs full field-caliber governance, that is a later design question, not part of the first wiki readability improvement.

### wiki-sink

`wiki-sink` is used when `wiki/07-drift.md` has no active items.

It initializes the fixed Repo-Local Wiki skeleton and records confirmed or evidence-grounded reusable knowledge into stable wiki pages.

Initialization creates skeleton files only. Stable content writes require user confirmation, current repo evidence, or existing wiki content; `wiki-sink` must not fill canonical indexes or topology sections by inference during skeleton creation.

It must not write guessed stable knowledge. It must not persist raw conversation archives. It does not own radar result persistence.

When initializing an existing `wiki/`, `wiki-sink` must not overwrite existing files. It may create missing skeleton files only when the user explicitly asked to initialize or complete the skeleton; otherwise it reports the missing paths and asks first.

### wiki-doctor

`wiki-doctor` checks an existing Repo-Local Wiki against the current Wiki Guidance System.

It rewrites formatting, structure, and expression when the original information can be preserved, and it may write direct evidence-grounded stable facts from current target-repository context. It is for guidance refresh, reader-first normalization, and scoped repo-evidence updates, not for queue-style drift classification or broad coverage inventory.

`wiki-doctor` may read target-repository source code, tests, routes, config, root `README.md`, `docs/**`, ADRs, AGENTS files, and other locally available files while refreshing wiki pages. These reads support safe rewriting and direct stable wiki updates: understanding names already present in the wiki, preserving links and evidence anchors, avoiding meaning loss, and writing current repo facts when the evidence is direct, local, readable, and cited.

Outside-wiki files are allowed stable fact sources for `wiki-doctor` writes. If outside-wiki context is conflicting, ambiguous, too broad to inspect in the requested scope, or insufficient to decide a name, boundary, relationship, field, module, flow, or ownership fact, `wiki-doctor` reports `drift_or_coverage_suspect` and recommends `wiki-drift-radar` or focused user confirmation instead of guessing.

It must not write guessed stable knowledge, refresh `wiki/07-drift.md`, run queue-style drift classification, or change confirmed meanings without evidence while making pages easier to read.

`wiki-doctor` has a hard Drift Page gate. It normally requires `wiki/07-drift.md` to be empty before doing any page audit or rewrite. If `wiki/07-drift.md` contains active items, it stops and asks the user to run `wiki-drift-govern`.

If `wiki/` exists but fixed skeleton files are missing, `wiki-doctor` may perform `complete_skeleton`. This includes creating missing fixed skeleton files, missing catalog README files, and a missing `wiki/07-drift.md` empty state. It must not initialize a missing `wiki/` from scratch; that remains `wiki-sink`.

If `wiki/07-drift.md` exists and is semantically empty but not in standard empty-state format, `wiki-doctor` may continue but does not rewrite the Drift Page. It reports the format issue only. If a missing `wiki/07-drift.md` is accompanied by old drift-like files or unresolved queues, `wiki-doctor` stops and asks for human clarification.

`wiki-doctor` supports explicit `audit-only` mode. User phrases such as "dry run", "plan only", "only check", or "do not edit files" are treated as `audit-only`. The default mode is audit plus direct rewrite of safe items.

The result classifications are:

- `safe_guidance_rewrite`: the existing wiki information can be reformatted, moved, split, merged, renamed, indexed, or diagrammed without changing meaning.
- `evidence_grounded_update`: current target-repository evidence directly supports a new or corrected stable wiki fact, with enough evidence to write and cite it without guessing.
- `meaning_loss_risk`: the change may alter meaning, naming, ownership, page/module/model boundary, business intent, decision meaning, or unique evidence.
- `drift_or_coverage_suspect`: the issue appears to require broad current-system comparison, unresolved conflict handling, missing coverage classification, or a fact decision not directly supported by inspected evidence, so `wiki-doctor` reports it and recommends `wiki-drift-radar` or focused confirmation.

`wiki-doctor` may write `safe_guidance_rewrite` and `evidence_grounded_update` items. It reports `meaning_loss_risk` and unresolved `drift_or_coverage_suspect` without changing those areas. It can ask focused follow-up questions for a small number of blocking risk items, but it is not a broad interview skill.

Supported actions are report vocabulary, not a machine schema:

- `rewrite_page`
- `add_reader_entry`
- `add_table_or_diagram`
- `write_evidence_grounded_fact`
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

`wiki-doctor` writes only inside the target repository's top-level `wiki/`, including allowed Whitebox artifacts. It may read files outside `wiki/` for context, but it does not edit target source code, root `README.md`, `docs/**`, ADRs, AGENTS files, config, or this Skill Suite Source Repository's `CONTEXT.md`, `wiki-suite-design.md`, `skills/references/**`, or skill source files.

`wiki-doctor` does not run mechanical checks. Its report is semantic: reader-quality audit, changed pages, skipped risk items, suspected drift or coverage, out-of-scope suggestions, deleted/renamed/merged pages, and Drift Page gate notes.

`wiki-doctor` is never used to update the Wiki Guidance System itself. Edits to `wiki-suite-design.md`, `CONTEXT.md`, `skills/references/**`, or skill instructions are skill-suite maintenance and must be made directly or through an explicit skill-refinement workflow.

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

Guidance-shape lag is not drift by itself. If a page is semantically current but not in the latest guidance shape, recommend `wiki-doctor`; create Drift Page items only for wrong facts, missing important coverage, or current-system boundary/name mismatches.

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

Catalog README files are canonical indexes for their own family. They are not passive directories; they route readers and agents to the right flow, page, module, or model family page.

`wiki-sink` must maintain canonical indexes when writing new stable knowledge whose name, owner, and boundary are confirmed. `wiki-doctor` may rebuild or update canonical indexes from existing wiki pages or direct target-repository evidence during a refresh. `wiki-drift-radar` reads canonical indexes to judge coverage and owner pages but does not write them. `wiki-drift-govern` must update canonical indexes when resolving Wiki Drift or Coverage Gap items that change stable wiki content.

If names conflict, boundaries are unclear, or owner pages are not confirmed, the skill must ask the user or report `meaning_loss_risk`; it must not invent a canonical name.

## Fine-Grained Writing Blocks

V1 should strengthen the Wiki Guidance System with fine-grained writing blocks inspired by mem-style fragment guidance, while keeping them as prose guidance.

A block family is a reusable semantic expression family under `skills/references/writing-blocks/`. It defines when to use that expression, what reader question it answers, preferred diagram/table/prose shape, evidence and uncertainty rules, and common anti-patterns. It is not a required section schema.

New blocks:

- `activity-map`: flow主链路表达；默认用 Mermaid `flowchart` 承载复杂业务主活动图，说明谁在什么条件下做什么业务动作，表达分支、汇合、异常和跨角色交接；活动节点使用 confirmed Subject + SVO 业务动作短句，不同 Subject 用不同 Mermaid class / classDef 或等价样式分色；活动表只用于短线性 flow 或作为 Mermaid 的证据补充。它 does not turn Controller/Service/SQL/runtime/adapter/payload into business activities.
- `evidence-anchor`: short traceable evidence support for stable wiki facts, uncertainty, and candidate notes. It borrows the useful verification discipline from mem-style evidence docs without adding a separate evidence family or verification matrix to repo-wiki V1.
- `model-relation`: model关系表达；默认用 Mermaid `flowchart` 或等价关系图表达多节点、多方向、事实源或拓扑关系，表格用于补充 evidence 和 uncertainty；Model-to-model edges use `泛化`、`组成`、`引用`、`衍生`, while Canonical Role / Canonical External System to Model edges use `事实源`. It must preserve the distinction between `引用` and `衍生`, and must not turn fields, DTOs, Services, modules, payloads, runtime records, or logs into relation-graph nodes.
- `module-drill-down`: module owner page 内的读者路线表达；先从 confirmed C2 runtime unit 生成 root module owner page，再在 root page 或上层 owner page 的 internal parts 中识别可下钻的 canonical child modules。用 `内部模块` 摘要表和 related-module links 引导下钻，不在 `README.md` 中制造强制模块树，也不创建 ownerless overview page。
- `module-boundary`: module边界表达；说明 stable responsibility boundary、public surfaces、internal capabilities、collaboration direction 和 current module rules。它 must not turn package trees, private helpers, deployment inventory, or unconfirmed ownership into module contracts.
- `whitebox-component`: canonical module owner page 的必备 Module Boundary Map；以 `.whitebox.yaml` 作为唯一 diagram fact source，生成 SVG 作为 reader-facing rendering，并用 confirmed boundary ports、externals、internal parts、interface roles 和 typed connectors 表达边界内部组装关系。Reader-facing Markdown 可在图旁补 `内部模块` 表和 per-port contract tables，但这些不进入 source model。
- `canonical-index`: repo-wide and catalog-wide naming/navigation rules.
- `public-surface`: stable public entry points, user-facing surfaces, tools, APIs, or module capabilities needed to understand a boundary.
- `page-layout`: page detail expression for stable visible regions, major components, overlays, drawers, tabs, placeholders, page variants, visible state projection, and page-level interaction surfaces. It must not become DOM/CSS/component-library documentation or a screenshot archive.

Do not add a separate `runtime-topology` block in V1. Runtime Topology rules currently belong in `writing-guidance/system-overview.md`; extract a reusable block only if multiple page families need the same topology rules.

Existing guidance / blocks to strengthen:

- `sequence`: complex participant collaboration defaults to Mermaid `sequenceDiagram`; participant names must stay at one abstraction level; actors are triggers or result receivers; implementation details are evidence, not participants.
- `state-transition`: stable states only; no temporary booleans or display states unless explicitly marked as display states.
- `page-navigation`: multi-page navigation defaults to Mermaid `flowchart` / `graph`; user-visible navigation only; route params, visibility conditions, and backend calls should not be forced into navigation edges.
- `page-page`: page guidance should preserve page target, entry points, navigation, visible regions/layout, page variants, state matrix, exit routes, page-level backend interactions, key interactions, related flows/modules/models, and evidence anchors, while avoiding fixed schema mechanics.
- `module-page`: module guidance should preserve owns / does-not-own boundary, public surfaces, internal capabilities, collaboration direction, module rules, related flows/pages/models, and code anchors, while avoiding package tree or helper-list documentation.
- `dependency-map`: distinguish runtime calls, data references, responsibility dependencies, ownership, and fact sources.
- `decision-tradeoff`: decision blocks must explain a real current tradeoff and what it rules out.

Cross-block guidance to add:

- Stable anchors: central diagrams should use stable names, aliases, or short node labels when downstream tables, drill-down sections, evidence, or related pages refer back to them.
- Traceability root: complex flow pages should treat the main activity map as the reader-facing mainline; sequence, state, navigation, dependency, evidence, and drill-down sections should supplement it rather than define a competing flow.
- Canonical subjects: activity subjects, fact sources, page nodes, sequence participants, owners, and public surfaces should come from confirmed roles, external systems, runtime units, pages, modules, models, or page-local declared subject lists, not payloads, DTOs, adapters, helpers, SQL, records, or file paths. Activity maps additionally require SVO labels and distinct subject colors/classes.
- Semantic review checklist: wiki quality review should ask reader question, main expression, stable anchors, canonical subjects, evidence/uncertainty, owner-page fit, information preservation, and diagram readability. This remains natural-language review, not a validator or PASS/FAIL gate.

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
# 漂移治理（Drift）

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

Explains how to read the wiki and what each top-level section contains. Detailed reader-entry rules live in `skills/references/writing-guidance/wiki-root.md`; `wiki-structure.md` only carries the initial skeleton text.

### 01-system.md

Provides a human-readable system overview. It defaults to the C1 / C2 / Runtime Topology shape decided by the System Overview Guidance, while `wiki-structure.md` only carries the minimal skeleton that `wiki-sink` can initialize. Detailed headings, canonical-table columns, Mermaid topology rules, evidence rules, and semantic checks are maintained in `skills/references/writing-guidance/system-overview.md`.

The `wiki-structure.md` skeleton may include `TBD` placeholders, including a minimal Mermaid topology placeholder. Stable written pages should replace placeholders with a real Runtime Topology graph; when relationships are incomplete, draw the confirmed C1/C2 nodes and edges and state the remaining gaps after the diagram.

### 02-flows/

Explains key user, business, and system flows before readers inspect pages and module boundaries. It excludes ordinary call chains, test steps, trace dumps, and troubleshooting SOPs.

### 03-pages/

Explains user-visible pages, entry points, navigation, visible regions, page variants, visible states, page-level interactions, and page relationships to flows, modules, and models. It excludes DOM trees, CSS details, component-library inventories, screenshot archives, and backend call chains.

### 04-modules/

Explains human-meaningful capability and responsibility boundaries, stable public surfaces, internal capabilities, collaboration rules, module-to-module drill-down routes, and related flows/pages/models. Module generation starts from confirmed C2 runtime units, which become C2 root module owner pages. Stable subsystems, code modules, or other lower-level modules may become child or collaborating module owner pages only when tied to a C2 root module or upper owner page. `README.md` owns the flat Canonical Module Index; former `module-map.md`-style pages must become C2 root module pages when they draw a confirmed C2 runtime unit as the enclosing component, or remain blocked as `meaning_loss_risk` until their root boundary is clarified.

### 05-models/

Explains model families: highly related groups of system-understanding models, their relationships, member definitions, key fields, demo/examples, state, and rules. Model family boundaries are driven by shared reader questions, stable fact chains, lifecycle, source-of-truth relationships, or demo explainability. These are not strict DDD models, not one-page-per-model inventories, and do not focus on persistence technology such as MySQL or Redis.

### 06-decisions.md

Summarizes current active decisions and tradeoffs for human understanding.

### 07-drift.md

Stores the current active radar findings while they are being governed. It is not a history archive.

## Drift Page Contract

`wiki/07-drift.md` represents the current governance queue.

Empty state:

```md
# 漂移治理（Drift）

No active drift or coverage gaps.
```

When non-empty, it may contain:

```md
# 漂移治理（Drift）

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
