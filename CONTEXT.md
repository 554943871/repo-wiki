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

**Canonical Name**:
A single stable reader-facing name for one confirmed concept in a Canonical Index. It must not combine competing names or concept candidates with slash, "or", or similar mixed-name syntax; if the stable name is unclear, keep aliases or candidate notes outside the canonical name and ask for confirmation. A canonical name has one owner index; other pages or indexes should reference it instead of duplicating the same canonical entry. Different concepts across knowledge-family indexes may share a natural domain root, but must not use the exact same canonical name.
_Avoid_: slash-joined name, or-joined name, candidate-name bundle, cross-index duplicate name, duplicated canonical entry

**Canonical Roles**:
The repo-wide role names used consistently in activity maps, model relations, sequences, page navigation, and system context. In `wiki/01-system.md`, this index belongs inside C1 (System Context) because roles are external behavior subjects around the repository boundary; runtime units do not belong here.
_Avoid_: role enum, ad hoc actor names, runtime unit as role, target system as role

**Canonical External Systems**:
The repo-wide external-system names used consistently when explaining system context, dependencies, flows, modules, and evidence. In `wiki/01-system.md`, this index belongs inside C1 (System Context) because it names highly relevant external systems, platforms, services, or organizational systems outside the target system boundary that interact with the target system at runtime or across a clear data/dependency boundary. External origin alone is not enough: libraries, SDKs, runtime frameworks, and protocols are not Canonical External Systems unless they are themselves exposed as an independent external service or platform.
_Avoid_: adapter names as external systems, local synonyms, dependency library, runtime framework, protocol

**Public Surface**:
A stable externally visible entry point, capability, API, tool, route, command, page entry, or event surface that helps readers understand a system, module, page, or runtime-unit boundary. A Public Surface is the interaction point exposed by a boundary; it is not automatically the Major Runtime Unit itself.
_Avoid_: helper list, private implementation method, runtime unit by default

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
The top-level repo-local wiki page for human-readable system context, major runtime-unit overview, and lightweight runtime topology, roughly covering C4 C1 (System Context), C2 (Container), and small Runtime Topology views without going into component or code-level detail.
_Avoid_: component map, class documentation

**System Overview Default Structure**:
The named default section order and heading set for `wiki/01-system.md`, detailed in the System Overview Guidance.
_Avoid_: free-form system overview, empty template section

**System Overview Default Blocks**:
The named set of default content blocks for `wiki/01-system.md`, including C1 context, canonical indexes, C2 runtime units, Runtime Topology, and continue-reading navigation.
_Avoid_: title-only skeleton, mandatory filler diagram, prose-only topology

**System Overview Canonical Tables**:
The canonical role, external-system, and runtime-unit tables in `wiki/01-system.md`. Their detailed columns and evidence rules live in System Overview Guidance, not in the glossary.
_Avoid_: ad hoc table columns, bilingual column clutter, owner-page boilerplate, schema fields

**System Context Node**:
A node in the C1 (System Context) view, such as the repository's system, an external role, or a highly relevant external system or platform outside the repository boundary. Roles are external behavior subjects; runtime units are C2 concepts; dependency libraries, SDKs, runtime frameworks, and protocols are not System Context Nodes by themselves. Use this term instead of treating C1 itself as an entity.
_Avoid_: C1 as entity, runtime unit, module, dependency library, protocol

**Canonical Main Runtime Units**:
The repo-wide Major Runtime Unit names used consistently when explaining C2 (Container), Runtime Topology, flows, modules, pages, and models. In `wiki/01-system.md`, this index belongs inside C2 because it is the canonical source for independently running process-boundary units. Each entry must have an independent runtime process boundary; data exchange with another C2 crosses that boundary and cannot rely on shared memory.
_Avoid_: package list, helper list, infrastructure inventory, interface layer, in-process capability

**Runtime Topology**:
A lightweight system-overview view that shows how Canonical Roles, Canonical External Systems, and Canonical Main Runtime Units are operationally connected for the runtime scope being explained. It defaults to a Mermaid `flowchart`; every entity node in the diagram must reuse a C1 or C2 canonical name from those three indexes only. Protocols, read/write modes, files, persistence media, modules, pages, flows, models, decisions, and other non-C1/C2 details belong in edge labels, short notes, or continue-reading routes, not as topology nodes. A single topology may include multiple stable entry points when that is still readable.
_Avoid_: request sequence, component map, prose-only topology, infrastructure inventory, hard-coded entry exclusion, topology-local entity node, module node, page node, flow node

**Major Runtime Unit**:
The reader-facing phrase for C4 C2 Container-level applications, services, tools, data stores, or other independently meaningful runtime units. A Major Runtime Unit must have an independent runtime process boundary; data exchange between two Major Runtime Units crosses that process boundary and cannot rely on shared memory. Use this phrase after expanding C2 (Container) once, because the Chinese word 容器 can be confused with Docker or Kubernetes containers.
_Avoid_: Docker container, package, helper, component, shared-memory internal component

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

**Whitebox Component Diagram**:
A module-boundary diagram that shows one enclosing component's boundary ports, internal components, internal ports, interface roles, and connector semantics so readers can see how exposed capabilities are delegated and assembled inside the boundary.
_Avoid_: UML-complete model, package dependency map, image-only architecture sketch

**Diagram Complexity Signal**:
The reader-facing interpretation that a dense or tangled Whitebox Component Diagram may indicate genuinely complex module logic or a potential refactoring opportunity, not merely a rendering failure. It is a review signal for human judgment, not a mechanical score.
_Avoid_: automatic refactor verdict, renderer defect by default, complexity metric

**Derived Whitebox View**:
An additional renderer-produced view generated from the same Diagram Source Model to make a dense Whitebox Component Diagram easier to read. It may focus on external boundary interactions, delegation, assembly, interface roles, or other renderer-defined slices, but it does not replace the complete Whitebox Component Diagram and never becomes a separate fact source. Derived views are generated automatically from renderer rules for dense diagrams; the Diagram Source Model does not contain `views` fields or author-selected view lists. The first standard derived views are `boundary`, `delegation`, and `assembly`, with `interfaces` generated only when interface roles exist. Empty derived views are not generated or embedded.
_Avoid_: second source model, partial truth source, source-level layout hint, manual diagram fork, source-level view selection

**Whitebox Layout Backend**:
The renderer-owned automatic layout engine that converts a Diagram Source Model into concrete node positions, port positions, edge routing, canvas size, and derived view geometry. For the free and open-source path, ELK is the preferred backend because it is designed for layered diagrams with ports, compound nodes, labels, and orthogonal routing. The enclosing Whitebox Component Diagram boundary is modeled as a real layout compound node so the backend can place boundary ports and internal parts together. The renderer does not pre-assign boundary port sides by default; free port placement belongs to the layout backend, while repeatability comes from stable ids, stable ordering, and fixed backend options. A layout backend is replaceable renderer infrastructure, not a diagram fact source, and it does not own the final Whitebox Component Diagram notation.
_Avoid_: source model field, layout intent in YAML, generated fact, manual coordinate editor, final notation owner, renderer-owned port side rule

**Simple Whitebox Layout Backend**:
The legacy deterministic renderer layout backend kept only as an explicitly selected diagnostic or migration comparison path while the ELK backend becomes the default. It is not the normal Skill execution path and must not be used as a silent fallback when ELK is unavailable.
_Avoid_: default renderer, silent fallback, production-quality layout target

**Whitebox Layout Failure**:
The fail-fast renderer outcome when the preferred Whitebox Layout Backend is unavailable or cannot produce a valid layout. The renderer reports the backend problem instead of silently falling back to a lower-quality layout. A simpler layout backend may exist only as an explicitly selected diagnostic or compatibility mode.
_Avoid_: silent fallback, fake successful ELK rendering, hidden quality downgrade

**Whitebox Layout Quality Check**:
The renderer verification practice for generated Whitebox Component Diagram output. It combines structural checks, geometry/readability checks, and visual snapshot review without treating pixel-perfect equality as the only signal of correctness.
_Avoid_: YAML-only validation, pixel-perfect theater, unchecked visual regressions

**Whitebox Renderer Dependency Boundary**:
The rule that layout/rendering dependencies such as `elkjs` are installed only while developing or upgrading the Repo Wiki Skill Suite itself, not during ordinary Skill execution against a Target Repository. A renderer may check for required dependencies and fail loudly with a setup diagnostic, but it must not run package installation as part of rendering.
_Avoid_: Skill initialization phase, runtime npm install, renderer-managed dependency mutation

**Semantic SVG Renderer**:
The renderer layer that turns laid-out Whitebox Component Diagram geometry into reader-facing SVG using the suite's own notation, labels, accessibility text, evidence-friendly metadata, interface-role symbols, connector styles, and derived-view framing. It consumes layout geometry from the Whitebox Layout Backend, but owns the final diagram semantics and visual notation.
_Avoid_: layout engine, fact source, ELK output as final notation, image-only rendering

**Diagram Source Model**:
The structured YAML or JSON file that acts as the only modifiable fact source for an agent-owned diagram. It records only topology and semantic relationships; renderer-owned layout algorithms decide grouping, ordering, coordinates, and routing, while generated SVG, PNG, Mermaid, PlantUML, or draw.io files remain derived renderings unless explicitly promoted.
It contains only explicit facts confirmed by code, documentation, or the user; unresolved questions must be resolved by further inspection or user clarification before entering the model.
_Avoid_: generated image as truth, draw.io XML as truth, Markdown prose as truth, source-level coordinates, source-level layout hints, question backlog

**Component Port**:
A named interaction point on a component boundary. It identifies where a component interacts, while interface roles identify the contracts available or needed at that point.
Port direction is not a port attribute in the Diagram Source Model; interaction direction is expressed only by connectors.
_Avoid_: interface, method, required port, provided port, port direction

**Interface Role**:
A provided or required interface contract attached to a component port. Interface assembly connects interface roles, not ports themselves.
_Avoid_: port, required port, provided port

**Delegation Connector**:
A connector from an enclosing component's boundary port to an internal component port, meaning the enclosing boundary capability is delegated inward.
_Avoid_: generic dependency, internal assembly

**Assembly Connector**:
A connector between internal component ports, meaning internal components collaborate through those ports.
_Avoid_: delegation connector, interface role connector, generic dependency

**Interface Assembly Connector**:
A connector from a required interface role to a provided interface role, meaning one component's required contract is satisfied by another component's provided contract.
_Avoid_: required port to provided port, generic dependency

**Stable Anchor**:
A reader-facing stable name, short alias, or local node label used to keep diagrams, tables, drill-down notes, evidence, and related pages pointing to the same concept.
_Avoid_: machine ID requirement, invented numbering, throwaway label drift

**Traceability Root**:
The main diagram or owner page that downstream diagrams, tables, and drill-down sections return to when explaining a narrower scenario. For complex flows, the Activity Map usually acts as the traceability root.
_Avoid_: competing mainline, duplicate truth source, disconnected drill-down

**Canonical Subject**:
The confirmed system context node, role, external system, runtime unit, page, module, model, or page-local declared subject that can validly appear as the subject of an activity, fact source, navigation edge, participant, owner, or public surface. The target system itself may be a Canonical Subject when an activity is genuinely system-initiated, but it is not a Canonical Role.
_Avoid_: payload as actor, adapter as business role, route file as page name, target system as role

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
