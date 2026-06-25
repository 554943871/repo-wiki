# Module Overview Guidance

A Module Overview page explains how confirmed modules in `wiki/04-modules/` fit together. It is a directory-level reader entry for cross-module topology, not a canonical module owner page.

Common filenames include `module-map.md` or another explicitly named overview page under `wiki/04-modules/`.

## Page-Family Contract

Module Overview is a distinct page family. It covers directory-level or cross-module topology pages that help readers see how confirmed canonical modules and supporting participants collaborate, while canonical module owner pages still own individual module responsibility boundaries.

Module Overview pages serve two readers in one natural document:

- Human readers get the scan path first: scope, canonical modules in view, key topology, supporting participants, and where to drill down.
- Code Agents get stable programming context downstream: structured interpretation of nodes, collaboration direction, evidence, boundaries, reader routes, and explicit non-goals that code alone does not carry.

This is an ordering and responsibility model, not a rigid template. Do not force fixed `Human View` and `Agent Context` headings, parallel halves, or any other hard split. Use headings that fit the page, but make sure fast human orientation comes before detailed structured context.

## Should Help Readers Answer

- Which confirmed canonical modules are in scope.
- How those modules collaborate at a stable responsibility-boundary level.
- Which supporting participants, internal layers, stores, adapters, runtimes, or queues help explain the topology.
- Which supporting participants are not canonical modules.
- Where to drill down for each module's owner page, related flows, related pages, related models, or decisions.
- Which boundaries are overview-only and must not be read as complete request sequence, deployment topology, package dependency, or ownership promotion.
- Which downstream context Code Agents can rely on when planning or changing code, including confirmed collaboration direction, stable names, boundary interpretations, evidence anchors, and non-goals.

## Suitable Content

- A short opening statement that names the overview scope and says it does not create canonical modules.
- A link back to `wiki/04-modules/README.md` as the canonical module index.
- A short list or table of canonical modules shown in the map.
- Cross-module topology, dependency direction, or collaboration relationships that are already confirmed.
- Supporting participants such as stores, adapters, queues, runtimes, tools, or internal layers when they are needed to understand module collaboration.
- A table that separates map nodes from owner pages and states how readers should and should not interpret each node.
- Reader routes to related flows, pages, models, and decisions.
- Boundary rules that prevent common misreadings.
- Structured downstream context for Code Agents, such as collaboration tables, node interpretation tables, evidence anchors, and non-goal notes that preserve programming context after the initial human scan path.

## Avoid

- Treating the overview page as a new canonical module.
- Adding modules to the canonical module set without updating `wiki/04-modules/README.md` from confirmed owner and boundary evidence.
- Promoting supporting participants to canonical modules just because they appear in the map.
- Replacing concrete module owner pages; each canonical module still needs its own owner page.
- Turning the overview into a package tree, service inventory, deployment map, or complete request sequence.
- Using private helpers, DTOs, SQL objects, files, or adapter internals as stable module concepts.
- Splitting the page into mandatory `Human View` and `Agent Context` sections instead of choosing natural headings that preserve the human-first scan path and downstream structured context.
- Restating Whitebox mechanics instead of referring to `skills/references/writing-blocks/whitebox-component.md`.

## Recommended Shape

A useful Module Overview page usually combines:

- Scope note: what system or subsystem this overview explains.
- Canonical modules in scope.
- Supporting participants in scope, explicitly marked as non-canonical modules.
- Overview topology diagram or map.
- Node interpretation table.
- Collaboration relationship table.
- Reader routes to flows, pages, models, decisions, and module owner pages.
- Boundary rules and known non-goals.

These are writing suggestions, not fixed fields. Put the fastest human scan path before denser interpretation, evidence, and programming context. The downstream structured context still matters; it is what lets Code Agents reuse the overview safely without treating diagram nodes as new module ownership.

## Whitebox Use On Overview Pages

Module Overview pages may use the Whitebox Component Diagram block when the overview needs to show one confirmed enclosing system or subsystem boundary.

Follow `skills/references/writing-blocks/whitebox-component.md` for all Whitebox mechanics.

When a Module Overview page uses Whitebox:

- The page remains a Module Overview page; the enclosing component is an overview boundary, not automatically a canonical module.
- The page must state the overview scope and point canonical module ownership back to `wiki/04-modules/README.md`.
- Supporting participants can appear only when they help explain collaboration; their appearance must not promote them into canonical modules.
- If the existing evidence is not strong enough for Whitebox, do not invent a placeholder diagram. Use a Dependency Map, prose, table, or report the gap instead.

## Relationship To Module Owner Pages

- `wiki/04-modules/README.md` owns the canonical module index.
- A Module Overview page explains cross-module topology and reader routing.
- A canonical module owner page explains one module's responsibility boundary, public surfaces, internal capabilities, module rules, related flows/pages/models, code anchors, and required Module Boundary Map.
- The overview can link to owner pages, but it must not duplicate or override their ownership decisions.

## LLM Semantic Checks

- Does the page clearly say it is an overview and not a canonical module owner page?
- Does the page give humans a fast scan path before detailed context?
- Does the page still preserve structured downstream Code Agent context such as node meaning, collaboration direction, evidence, boundaries, routes, and non-goals?
- Does the page avoid mandatory `Human View` / `Agent Context` headings or another hard split while still serving both readers?
- Does it link to the canonical module index instead of creating a parallel module list?
- Are canonical modules and supporting participants visually or textually distinguished?
- Does every supporting participant have a clear "do not read as canonical module" interpretation when promotion would be tempting?
- If a Whitebox Component Diagram is present, does the page point to `skills/references/writing-blocks/whitebox-component.md` instead of restating Whitebox mechanics?
- Does the overview preserve cross-module direction and evidence without becoming a request sequence, deployment topology, package dependency graph, or helper inventory?
- Does the page point readers to the concrete owner pages and related flows/pages/models/decisions for detail?
