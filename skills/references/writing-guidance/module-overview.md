# Module Overview Guidance

A Module Overview page explains how confirmed modules in `wiki/04-modules/` fit together. It is a directory-level reader entry for cross-module topology, not a canonical module owner page.

Common filenames include `module-map.md` or another explicitly named overview page under `wiki/04-modules/`.

## Page-Family Contract

Module Overview is a distinct page family. It covers directory-level or cross-module topology pages that help readers see how confirmed canonical modules and supporting participants collaborate, while canonical module owner pages still own individual module responsibility boundaries.

Module Overview pages serve two readers in one natural document:

- Human readers get the scan path first: scope, canonical modules in view, key topology, supporting participants, and where to drill down.
- Code Agents get stable programming context downstream: structured interpretation of nodes, collaboration direction, evidence, boundaries, reader routes, and explicit non-goals that code alone does not carry.

This is an ordering and responsibility model, not a rigid template. Do not force fixed `Human View` and `Agent Context` headings, parallel halves, or any other hard split. Use headings that fit the page, but make sure fast human orientation comes before detailed structured context.

## Human Scan Path

Open with a short scope statement before the main map. In one to three sentences, name the system, subsystem, or directory-level relationship being explained, link canonical module ownership back to `wiki/04-modules/README.md` when useful, and say that the overview does not create canonical modules.

Place the primary topology map, dependency map, Whitebox view, or equivalent structural table near the top, immediately after the scope statement and any short canonical-index pointer. The primary visual comes before detailed context, caveats, evidence, source mechanics, node tables, or long explanatory prose.

Give the primary visual a compact legend or caption for high-impact semantics. Define distinctions readers could otherwise misread, such as canonical module versus supporting participant, direction of collaboration, external boundary, store, adapter, queue, runtime, or overview-only grouping. Do not make readers infer those semantics later from dense prose.

After the primary visual, give reader routes to the concrete places they should drill into next: module owner pages, related flows, related pages, related models, decisions, or source-backed evidence sections. Then add denser node interpretation, collaboration details, boundaries, evidence anchors, and non-goals.

Prose supports the visual path; it does not replace it. Keep pre-map prose short, and use later prose to explain how to read the map, preserve programming context, and prevent common misreadings.

## Downstream Code Agent Context

Module Overview pages are responsible for retaining Code Agent context. Do not leave stable programming interpretation only in source code, generated diagrams, local fixtures, skill notes, or issue discussion when the overview needs that context to be reused safely.

Place detailed Code Agent context downstream of the human scan path: after the short scope statement, primary visual or structural table, compact legend or caption, and immediate reader routes. This keeps the page scannable for humans while still preserving the structured context that Code Agents need for planning and code changes.

Use structured semantic blocks where they help, without requiring fixed heading names. Useful blocks can include diagram fact source, boundary rules, evidence anchors, node notes, collaboration notes, reader routes, provenance notes, and anti-misread notes. Name, merge, split, or reorder those blocks to fit the page as long as the human-first scan path stays first and the Code Agent context remains easy to find.

Keep primary visual explanation distinct from evidence, provenance, and anti-misread support. The map legend or caption should explain the visible topology just enough for fast reading; downstream evidence and provenance should show why the map is trustworthy, and downstream anti-misread notes should state what the map must not be taken to mean.

Preserve context that code alone does not contain, such as confirmed boundary interpretation, why a supporting participant is not canonical, collaboration direction, overview-only groupings, source-backed naming decisions, evidence anchors, reader routes, and non-goals.

## Should Help Readers Answer

- Which confirmed canonical modules are in scope.
- How those modules collaborate at a stable responsibility-boundary level.
- Which supporting participants, internal layers, stores, adapters, runtimes, or queues help explain the topology.
- Which supporting participants are not canonical modules.
- Where to drill down for each module's owner page, related flows, related pages, related models, or decisions.
- Which boundaries are overview-only and must not be read as complete request sequence, deployment topology, package dependency, or ownership promotion.
- Which downstream context Code Agents can rely on when planning or changing code, including confirmed collaboration direction, stable names, boundary interpretations, evidence anchors, and non-goals.
- Which evidence, provenance, and anti-misread notes support the map without replacing the primary visual explanation.

## Suitable Content

- A short opening statement that names the overview scope and says it does not create canonical modules.
- A link back to `wiki/04-modules/README.md` as the canonical module index.
- A short list or table of canonical modules shown in the map.
- Cross-module topology, dependency direction, or collaboration relationships that are already confirmed.
- A compact legend or caption beside the primary map or structural table when map semantics carry ownership, direction, boundary, or supporting-participant meaning.
- Supporting participants such as stores, adapters, queues, runtimes, tools, or internal layers when they are needed to understand module collaboration.
- A table that separates map nodes from owner pages and states how readers should and should not interpret each node.
- Reader routes to related flows, pages, models, and decisions.
- Boundary rules that prevent common misreadings.
- Structured downstream context for Code Agents, such as diagram fact source, collaboration tables, node interpretation tables, evidence anchors, provenance notes, boundary rules, reader routes, and non-goal or anti-misread notes that preserve programming context after the initial human scan path.

## Avoid

- Treating the overview page as a new canonical module.
- Adding modules to the canonical module set without updating `wiki/04-modules/README.md` from confirmed owner and boundary evidence.
- Promoting supporting participants to canonical modules just because they appear in the map.
- Replacing concrete module owner pages; each canonical module still needs its own owner page.
- Turning the overview into a package tree, service inventory, deployment map, or complete request sequence.
- Using private helpers, DTOs, SQL objects, files, or adapter internals as stable module concepts.
- Splitting the page into mandatory `Human View` and `Agent Context` sections instead of choosing natural headings that preserve the human-first scan path and downstream structured context.
- Starting with long prose, node interpretation tables, evidence blocks, caveats, source model explanations, or rendering mechanics before the primary map or structural table.
- Letting prose-only description stand in for the main map when a topology map or compact structural table is needed for fast human orientation.
- Hiding Code Agent context outside the page when the overview relies on that context to prevent boundary, evidence, provenance, or ownership misreadings.
- Treating downstream semantic blocks as mandatory fixed headings or letting them interrupt the opening scope, primary visual, legend, or immediate reader routes.
- Restating Whitebox mechanics instead of referring to `skills/references/writing-blocks/whitebox-component.md`.

## Recommended Shape

A useful Module Overview page usually combines:

- Short scope note: what system or subsystem this overview explains, and that it does not create canonical modules.
- Primary overview topology diagram, dependency map, Whitebox view, or compact structural table near the top.
- Legend or caption for high-impact map semantics, especially ownership, direction, boundary, external, store, adapter, queue, runtime, or supporting-participant meaning.
- Reader routes to module owner pages, flows, pages, models, decisions, and evidence sections.
- Canonical modules in scope, if not already clear from the primary visual.
- Supporting participants in scope, explicitly marked as non-canonical modules.
- Node interpretation table.
- Collaboration relationship table.
- Diagram fact source, evidence anchors, provenance notes, or source-backed naming notes where they preserve meaning that code alone does not contain.
- Boundary rules and known non-goals.

These are writing suggestions, not fixed fields. Put the fastest human scan path before denser interpretation, evidence, and programming context, and keep prose in service of that visual route. The downstream structured context still matters; it is what lets Code Agents reuse the overview safely without treating diagram nodes as new module ownership.

## Whitebox Use On Overview Pages

Module Overview pages may use the Whitebox Component Diagram block when the overview needs to show one confirmed enclosing system or subsystem boundary.

Follow `skills/references/writing-blocks/whitebox-component.md` for all Whitebox mechanics.

When a Module Overview page uses Whitebox:

- The page remains a Module Overview page; the enclosing component is an overview boundary, not automatically a canonical module.
- The page must state the overview scope and point canonical module ownership back to `wiki/04-modules/README.md`.
- Supporting participants can appear only when they help explain collaboration; their appearance must not promote them into canonical modules.
- If the existing evidence is not strong enough for Whitebox, do not invent a placeholder diagram. Use a Dependency Map or compact structural table when another confirmed visual path is possible; otherwise report the gap and keep prose focused on what cannot yet be mapped.

## Relationship To Module Owner Pages

- `wiki/04-modules/README.md` owns the canonical module index.
- A Module Overview page explains cross-module topology and reader routing.
- A canonical module owner page explains one module's responsibility boundary, public surfaces, internal capabilities, module rules, related flows/pages/models, code anchors, and required Module Boundary Map.
- The overview can link to owner pages, but it must not duplicate or override their ownership decisions.

## LLM Semantic Checks

- Does the page clearly say it is an overview and not a canonical module owner page?
- Does the page open with a short scope statement before the primary map or structural table?
- Does the primary map or equivalent structural table appear near the top, before detailed context, caveats, evidence, source mechanics, or node tables?
- Does the primary visual include a compact legend or caption for high-impact semantics?
- Does the page give readers concrete routes after the primary visual?
- Does the page give humans a fast scan path before detailed context?
- Does the prose support the visual path instead of replacing it?
- Does the page itself preserve structured downstream Code Agent context such as node meaning, collaboration direction, evidence, provenance, boundaries, routes, anti-misread notes, and non-goals?
- Does detailed Code Agent context come after the short scope statement, primary visual or structural table, compact legend or caption, and immediate reader routes?
- Does the page allow useful semantic blocks without enforcing fixed heading names?
- Does it keep evidence, provenance, and anti-misread support distinct from the primary visual explanation?
- Does it retain context code alone does not contain?
- Does the page avoid mandatory `Human View` / `Agent Context` headings or another hard split while still serving both readers?
- Does it link to the canonical module index instead of creating a parallel module list?
- Are canonical modules and supporting participants visually or textually distinguished?
- Does every supporting participant have a clear "do not read as canonical module" interpretation when promotion would be tempting?
- If a Whitebox Component Diagram is present, does the page point to `skills/references/writing-blocks/whitebox-component.md` instead of restating Whitebox mechanics?
- Does the overview preserve cross-module direction and evidence without becoming a request sequence, deployment topology, package dependency graph, or helper inventory?
- Does the page point readers to the concrete owner pages and related flows/pages/models/decisions for detail?
