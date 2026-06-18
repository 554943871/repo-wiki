# Repo Wiki Skill Suite

This context describes a skill suite for helping teams maintain human-readable, repository-local system knowledge.

For the operational design, see [Wiki Skill Suite Design](./wiki-suite-design.md).

## Language

**Repo Wiki Skill Suite**:
A set of agent skills that help create, inspect, diagnose, and update a repository-local wiki for a target repository.
_Avoid_: raw archive workflow

**Local Skill Suite**:
A group of ordinary local agent skills maintained together without packaging them as a plugin bundle.
_Avoid_: plugin bundle

**Skill Suite Source Repository**:
The repository that contains the skill suite's own source, instructions, templates, and supporting assets.
_Avoid_: target repo, repo-local wiki

**Target Repository**:
The product or application repository that the Repo Wiki Skill Suite is applied to.
_Avoid_: skill suite repository

**Repo-Local Wiki**:
Human-readable system knowledge stored in a top-level `wiki/` directory inside a target repository alongside its code.
_Avoid_: raw conversation archive, nested wiki directory

**Numbered Wiki Structure**:
A repo-local wiki layout where top-level content pages and folders use numeric prefixes for reading order, while README files stay unnumbered and child content pages stay unnumbered.
_Avoid_: numbered README files, numbered child pages

**Guidance**:
Human-readable writing and reading guidance for wiki sections, intended for people and LLM semantic judgment rather than mechanical checking.
_Avoid_: schema, validator, lint, compliance, PASS

**Wiki Guidance System**:
The complete guidance set used by the Repo Wiki Skill Suite, including Wiki Guidance Principles, Wiki Structure, Writing Guidance, Writing Blocks, and Drift Page Rules.
_Avoid_: schema system, validator suite, template framework

**Wiki Guidance Principles**:
The shared principles that every wiki skill follows when writing, rewriting, or judging repo-local wiki content.
_Avoid_: validator rules, compliance gate

**Reader-Facing Chinese Headings**:
The convention that final `wiki/**/*.md` page titles, catalog entries, and section headings use Chinese by default for Chinese-native readers, while preserving stable English aliases when they help LLMs and cross-page anchors stay aligned.
_Avoid_: English-only reader headings, forced translation of code symbols

**No Mechanical Correctness Theater**:
The principle that schema, validator, lint, PASS/FAIL, compliance framing, or complete-looking fields must not be treated as proof of semantic wiki quality.
_Avoid_: fake certainty, mechanical correctness proof

**Information Preservation**:
The principle that readability, structure, movement, deletion, merging, and diagramming must not lose unique information, evidence anchors, naming, boundaries, decision meaning, or uncertainty.
_Avoid_: cleanup by deletion, lossy rewrite

**Canonical Index**:
The repo-local wiki's stable naming and navigation source for a knowledge family, such as roles, external systems, flows, pages, modules, models, or decisions.
_Avoid_: standalone glossary, schema registry

**Canonical Roles**:
The repo-wide role names used consistently in activity maps, model relations, sequences, page navigation, and system context. In `wiki/01-system.md`, this index belongs inside C1 (System Context) because roles are external behavior subjects around the repository boundary; runtime units do not belong here.
_Avoid_: role enum, ad hoc actor names, runtime unit as role

**Canonical External Systems**:
The repo-wide external-system names used consistently when explaining system context, dependencies, flows, modules, and evidence. In `wiki/01-system.md`, this index belongs inside C1 (System Context) because it names highly relevant external context nodes around the repository boundary.
_Avoid_: adapter names as external systems, local synonyms

**Public Surface**:
A stable externally visible entry point, capability, API, tool, route, page entry, or event surface that helps readers understand a system or module boundary.
_Avoid_: helper list, private implementation method

**wiki-doctor**:
The explicit refresh skill that checks whether an existing Repo-Local Wiki follows the current Wiki Guidance System, then rewrites formatting, structure, and expression when the original information can be preserved.
_Avoid_: validator, readability drift, wiki-drift-radar, wiki-drift-govern

**Drift Page**:
The top-level numbered repo-local wiki file that records the current active semantic drift and coverage gaps while they are being governed; a new wiki-drift-radar check must not start while it still contains active items.
_Avoid_: drift directory, drift backlog archive, append-only drift history

**Evidence Note**:
A short citation in the Drift Page that names the relevant wiki text or missing coverage, the current system evidence, the suggested owner page, and any candidate wiki note without preserving the full radar analysis or treating candidates as stable facts.
_Avoid_: full reasoning transcript, raw conversation archive, stable wiki fact

**Decision Map**:
The repo-local wiki page that summarizes current active decisions and tradeoffs for human understanding.
_Avoid_: history archive, decision inbox

**System Overview**:
The top-level repo-local wiki page for human-readable system context, major runtime-unit overview, and lightweight deployment/runtime topology, roughly covering C4 C1 (System Context), C2 (Container), and small Deployment / Runtime Topology views without going into component or code-level detail.
_Avoid_: component map, class documentation

**System Overview Default Structure**:
The named default section order and heading set for `wiki/01-system.md`, detailed in the System Overview Guidance.
_Avoid_: free-form system overview, empty template section

**System Overview Default Blocks**:
The named set of default content blocks for `wiki/01-system.md`, including C1 context, canonical indexes, C2 runtime units, Deployment topology, and continue-reading navigation.
_Avoid_: title-only skeleton, mandatory filler diagram, prose-only topology

**System Overview Canonical Tables**:
The canonical role, external-system, and runtime-unit tables in `wiki/01-system.md`. Their detailed columns and evidence rules live in System Overview Guidance, not in the glossary.
_Avoid_: ad hoc table columns, bilingual column clutter, owner-page boilerplate, schema fields

**System Context Node**:
A node in the C1 (System Context) view, such as the repository's system, an external role, or a highly relevant external system or platform around the repository boundary. Roles are external behavior subjects; runtime units are C2 concepts. Use this term instead of treating C1 itself as an entity.
_Avoid_: C1 as entity, runtime unit, module

**Canonical Main Runtime Units**:
The repo-wide runtime-unit names used consistently when explaining C2 (Container), deployment topology, flows, modules, pages, and models. In `wiki/01-system.md`, this index belongs inside C2 because it is the canonical source for major runtime units.
_Avoid_: package list, helper list, infrastructure inventory

**Deployment Topology**:
A lightweight system-overview view that shows how stable entry points, major runtime units, external systems, and persistence points are operationally connected for the runtime scope being explained. It defaults to a Mermaid `flowchart`, and diagram nodes should reuse names from Canonical Roles, Canonical External Systems, and Canonical Main Runtime Units whenever applicable. A single topology may include multiple stable entry points when that is still readable.
_Avoid_: request sequence, component map, prose-only topology, infrastructure inventory, hard-coded entry exclusion

**Major Runtime Unit**:
The reader-facing phrase for C4 C2 Container-level applications, services, tools, data stores, or other independently meaningful runtime units. Use this phrase after expanding C2 (Container) once, because the Chinese word 容器 can be confused with Docker or Kubernetes containers.
_Avoid_: Docker container, package, helper, component

**Flow Catalog**:
The repo-local wiki section that explains key user, business, and system flows before readers inspect page behavior or module boundaries.
_Avoid_: ordinary call chain, implementation trace log, test scenario dump, troubleshooting SOP

**Activity Map**:
A graph-first writing block for flow pages that explains who performs which business activity under which condition, including branches, joins, abnormal exits, and cross-role handoffs. Complex flows should use Mermaid `flowchart` as the main expression. Activity nodes use SVO labels with confirmed Subjects, different Subjects use distinct visual classes or colors, and evidence stays nearby.
_Avoid_: activity table as the default, technical call graph, Controller-Service-SQL diagram

**Activity Table**:
A compact table for very short linear flows or for evidence and node explanation beside a Mermaid Activity Map. It is not the primary representation for flows with branches, joins, abnormal exits, or handoffs.
_Avoid_: replacement for complex Activity Map, fixed-field table, implementation trace table

**Sequence Diagram**:
A Mermaid-first writing block for explaining key participant collaboration, call order, branches, retries, callbacks, async handoffs, and abnormal exits inside a specific scenario. Participant names should stay at one abstraction level.
_Avoid_: main business flow replacement, mixed-level call graph, steps table as default

**Page Navigation Map**:
A Mermaid-first writing block for user-visible page-to-page navigation, entries, exits, returns, and reader route choices. It explains where a reader or user goes next, not backend calls or component internals.
_Avoid_: backend call chain, component interaction map, SVG as default

**Page Layout Map**:
A page-detail writing block for stable user-visible regions, major components, overlays, drawers, tabs, placeholders, page variants, and visible state projection. It explains page structure and page-level interaction surfaces without becoming a DOM tree, CSS spec, screenshot archive, or component inventory.
_Avoid_: pixel-perfect mockup, React tree, component-library dump, backend call chain

**Evidence Anchor**:
A short, traceable support note for stable wiki facts, uncertainty, and candidate notes. It names what evidence supports and where readers can verify it, without turning stable wiki pages into raw logs, chat archives, or full code indexes.
_Avoid_: raw transcript, full log dump, local absolute path, unsupported conclusion

**Model Relation Map**:
A graph-first writing block for stable model relationships and fact sources. It uses relationship labels such as `泛化`, `组成`, `引用`, `衍生`, and `事实源`; tables should supplement evidence and uncertainty, not replace relation topology.
_Avoid_: database ER dump, runtime call graph, vague dependency table

**Module Boundary Map**:
A module-detail writing block for stable responsibility boundaries, public surfaces, internal capabilities, collaboration direction, and current module rules. It explains what neighboring flows, pages, modules, or systems can rely on without turning private helpers or package trees into contracts.
_Avoid_: package tree, helper list, deployment inventory, unconfirmed ownership

**Stable Anchor**:
A reader-facing stable name, short alias, or local node label used to keep diagrams, tables, drill-down notes, evidence, and related pages pointing to the same concept.
_Avoid_: machine ID requirement, invented numbering, throwaway label drift

**Traceability Root**:
The main diagram or owner page that downstream diagrams, tables, and drill-down sections return to when explaining a narrower scenario. For complex flows, the Activity Map usually acts as the traceability root.
_Avoid_: competing mainline, duplicate truth source, disconnected drill-down

**Canonical Subject**:
The confirmed role, external system, runtime unit, page, module, model, or page-local declared subject that can validly appear as the subject of an activity, fact source, navigation edge, participant, owner, or public surface.
_Avoid_: payload as actor, adapter as business role, route file as page name

**Page Catalog**:
The repo-local wiki section that explains user-visible pages, entry points, navigation, visible regions, page variants, visible states, page-level interactions, and how pages connect to flows, modules, and models.
_Avoid_: DOM tree, CSS detail, component inventory, backend call chain

**Module Catalog**:
The repo-local wiki section that explains human-meaningful capability and responsibility boundaries, stable public surfaces, internal capabilities, collaboration rules, and related flows/pages/models after key flows are understood, even when those boundaries do not match code directories.
_Avoid_: package tree, runtime unit inventory, page inventory

**Model Catalog**:
The repo-local wiki section that explains important system-understanding models, including their meaning, state, and relationships, without requiring strict DDD classification or focusing on persistence technology.
_Avoid_: strict DDD model, database table catalog, storage inventory

**wiki-drift-radar**:
The radar skill that compares the target repository's current working-tree system with its repo-local wiki across the whole project by default or a user-specified scope, classifies each finding as wiki drift, code drift, or coverage gap, asks the user to resolve ambiguity before writing, and may refresh the Drift Page without confirmation after classification when the Drift Page has no active items.
_Avoid_: wiki-radar, wiki-xray, validator, stable wiki page writer, ambiguous drift handoff, git clean gate

**wiki-drift-govern**:
The governance skill used when the Drift Page has active items; it resolves classified Drift Page items by updating wiki pages for wiki drift or coverage gaps, or by changing code when code drift means the implementation should return to the wiki-described behavior; after all active items are resolved, it clears the Drift Page to its empty state.
_Avoid_: wiki-govern, ambiguous drift resolver, open-ended refactor skill, guessing intent from code

**wiki-sink**:
The write skill used when the Drift Page has no active items; it initializes the fixed repo-local wiki skeleton and records confirmed or evidence-grounded reusable knowledge into it, including system, flow, page, module, model, and decision knowledge, while excluding radar findings persisted to the Drift Page.
_Avoid_: wiki-update, wiki-adr, raw archive, agent-doc sync, radar result persistence, guessed stable knowledge, drift governance

**Coverage Gap**:
Important current system knowledge that exists in the target repository but is missing from the repo-local wiki.
_Avoid_: every undocumented implementation detail

**Wiki Drift**:
A mismatch where wiki content is outdated or wrong compared with the current system, so the wiki should change.
_Avoid_: code drift

**Code Drift**:
A mismatch where the current implementation diverges from wiki-described behavior that the user confirms should still hold, so code should change.
_Avoid_: wiki drift, open-ended refactor

**Wiki Too Thin**:
A repo-local wiki with too little relevant content for meaningful radar comparison; wiki-drift-radar may stop and refresh the Drift Page with this status instead of producing drift or coverage-gap findings.
_Avoid_: pretending a meaningful comparison is possible
