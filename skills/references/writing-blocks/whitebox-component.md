# Whitebox Component Diagram Block

Whitebox Component Diagram 是 canonical module owner page 的必备 Module Boundary Map。它解释一个 enclosing module 如何通过 boundary ports 暴露能力、如何把这些能力委派给内部 components、内部 components 如何协作，以及哪些 interface roles 被满足。

Module Overview / Module Map pages may also use a Whitebox Component Diagram when they need to show one confirmed enclosing system or subsystem boundary across multiple modules and supporting participants. In that case, the page remains an overview page: the enclosing component is an overview boundary, not a canonical module unless `wiki/04-modules/README.md` already names it as one.

它不是 UML 完整模型、package dependency map、调用链、文件树或截图式架构图。它只记录已经确认的 module 边界事实。

## Fact Source And Derived Output

- `.whitebox.yaml` 是唯一可修改的 diagram fact source。Agent 修改 diagram 时只改 source model，再重新生成 SVG。
- `.whitebox.svg` 是 reader-facing rendering，必须从同一份 `.whitebox.yaml` 派生。SVG 和其他生成图片都不是事实源。
- Generated SVGs belong in an `assets/` subdirectory beside the module or module-overview page, not beside the Markdown page itself. Keep the `.whitebox.yaml` source model beside the Markdown page so agents can find the fact source directly, and keep complete/derived `.whitebox*.svg` files under `./assets/`.
- Mermaid、PlantUML、draw.io XML、Markdown prose、截图、手绘图片和生成图片都不能作为 Whitebox Component Diagram 的 diagram fact source。它们可以在转换过程中作为输入，但 Whitebox adoption 之后不能继续作为旧草图、迁移说明或并行事实源留在 wiki。
- Source model 只写 topology 和语义关系；不要写坐标、布局、排序、routing、canvas size、样式或 renderer hints。布局由 renderer 决定。
- Source model 不写 aspect ratio、direction、wrapping、candidate selection 或 viewport-readability fields。Viewport-readable layout belongs to the renderer policy and generated SVG metadata only.
- Source model 不写 `views`、`derivedViews`、`include_parts`、`include_connectors` 或其他展示选择字段。Derived views 由 renderer 根据拓扑和 connector 类型自动生成。
- 如果 source model 和 SVG 不一致，以 `.whitebox.yaml` 为准，并重新渲染 SVG。

## Current Artifact Policy

Wiki content reflects the current understanding of the module or overview boundary, not the migration process that produced it.

When a `.whitebox.yaml` source model supersedes an older Mermaid block, PlantUML file, draw.io export, PNG, screenshot, hand-drawn image, generated image, or manual diagram file, delete the superseded artifact from the repo-local wiki unless the user explicitly says that older artifact remains current.

Do not leave superseded diagrams in the page, beside the page, under `assets/`, or as unlinked archive files. Even when labelled `legacy`, `old`, `before`, or `migration`, they become competing fact sources for later readers and agents.

Do not add migration notes such as "converted from Mermaid" or "old diagram replaced by Whitebox" to reader-facing wiki pages. If an older artifact remains current, state its current reader purpose and keep it consistent with the `.whitebox.yaml`; otherwise remove it.

## Markdown Caption And Linking Convention

Module owner pages and Module Overview pages that use Whitebox both link SVG and source model at the diagram location. Source model 与 Markdown page 平级；完整图和派生 SVG 放在同目录的 `assets/` 子目录，使用稳定的相对路径。

The source model link must appear as a short, low-friction caption immediately beside the diagram. Prefer `图源：[...]` or another equally short caption. Do not put source/rendering mechanics in the reader scan path; keep those rules in this block instead.

```md
## 模块边界图（Module Boundary Map）

![Checkout Module whitebox component diagram](./assets/checkout.whitebox.svg)

图源：[`checkout.whitebox.yaml`](./checkout.whitebox.yaml)
```

The complete Whitebox Component Diagram is the primary reader-facing view by default. Keep it first, keep the short source-model caption visible beside the diagram, and do not let derived views replace or precede the complete view.

Generated Derived Whitebox Views may exist under `assets/` as renderer-produced artifacts, but artifact existence is not the same as reader-facing embedding. Embed a derived view only when it answers a clear reader question or materially improves understanding, such as isolating external boundary contracts, delegation paths, internal assembly, or interface-role relationships in a dense diagram.

Do not mechanically embed every generated derived view. If the complete view is readable enough, or if a generated slice does not add a distinct reader benefit, leave the derived SVG as an artifact and show only the complete diagram. When derived views do meet the reader-benefit threshold, embed only those non-empty views immediately after the complete diagram and caption. For example, if boundary, delegation, and assembly views each answer a distinct reader question:

```md
### Boundary Derived Whitebox View

![Checkout Module Boundary Derived Whitebox View](./assets/checkout.whitebox.boundary.svg)

### Delegation Derived Whitebox View

![Checkout Module Delegation Derived Whitebox View](./assets/checkout.whitebox.delegation.svg)

### Assembly Derived Whitebox View

![Checkout Module Assembly Derived Whitebox View](./assets/checkout.whitebox.assembly.svg)
```

Derived views are reader aids from the same source model. They do not replace the complete diagram, do not introduce additional source models, and must never be treated as fact sources.

The first standard derived views are:

- `boundary`: external nodes, enclosing component boundary ports, and `external` connectors.
- `delegation`: enclosing component boundary ports, internal part ports, and `delegation` connectors.
- `assembly`: internal parts, internal part ports, and `assembly` connectors.
- `interfaces`: generated only when `interfaceAssembly`, `provides`, or `requires` is present.

Do not generate or embed an empty derived view. A derived view exists only when its connector or interface-role content exists in the source model.

Do not put generated Whitebox SVGs beside the Markdown page. Use page-local `assets/`: for `wiki/04-modules/checkout.md`, use `wiki/04-modules/checkout.whitebox.yaml` and `wiki/04-modules/assets/checkout.whitebox.svg`.

## Source Model Semantics

Use the current Whitebox Component Diagram source model:

- `kind: whitebox_component_diagram` and `version: 1`.
- `component`: the enclosing boundary. On a canonical module owner page this is the module boundary. On a Module Overview page this may be a confirmed system or subsystem overview boundary. It owns boundary `ports` and must have evidence.
- `parts`: optional internal components inside the enclosing boundary. Use only for confirmed internal responsibilities that help explain how public capability is assembled. On Module Overview pages, parts may include confirmed canonical modules and supporting participants, but supporting participants must not be promoted into canonical modules by appearing in the diagram.
- `ports`: named interaction points. Port direction is not a field; interaction direction is expressed by connectors.
- `interfaces`: optional interface contracts that can be attached to ports as `provides` or `requires`.
- `externals`: actors, modules, pages, flows, runtime units, or systems outside this enclosing module boundary when they are needed to explain the boundary interaction.
- `connectors`: directed, typed relationships with evidence.

Renderer notation: a port is a boundary interaction point, so the rendered port rectangle must straddle the border of its owning component or internal part. It should not float entirely outside the owner, sit entirely inside the owner, or become an ordinary child node. The renderer may choose the side and ordering from topology, but the source model must not store coordinates, side hints, or layout intent.

Connector types:

- `external`: connects an external node and an enclosing boundary port. The connector `from` and `to` fields express the interaction direction.
- `delegation`: connects an enclosing boundary port and an internal part port. The connector direction shows whether the boundary capability is delegated inward or an internal capability is exposed outward.
- `assembly`: connects one internal part port and another internal part port.
- `interfaceAssembly`: connects a required interface role to a provided interface role.

Connectors must terminate at legal endpoints. Ordinary endpoints are strings: use the external id for an external node, and use `owner.port` for an enclosing component port or internal part port. Interface-role endpoints are structured objects with `owner`, `port`, `interface`, and `role`. Do not connect whole components, whole parts, arbitrary files, packages, helpers, DTOs, SQL objects, or prose-only concepts. `interfaceAssembly` connects interface roles, not ports themselves.

Connector `label` is optional, but when present it must add relationship meaning: action, data exchanged, protocol, contract, ownership, buffering, persistence, or another reason the dependency matters. Do not write visible labels that only restate endpoints, such as `A -> B`, `External -> port`, or `part.port -> other.port`; the diagram already shows endpoints and direction. If no meaningful relation phrase is confirmed, omit the visible connector label instead of adding endpoint noise.

## Evidence Expectations

- The enclosing component and every connector need short evidence. Prefer repo-relative paths, line ranges, symbols, routes, tests, docs, existing wiki content, or explicit user confirmation.
- A node, port, interface, or part may exist only when its meaning is confirmed by evidence or user confirmation. Do not introduce a part just because a class or package exists.
- Evidence explains why the fact belongs in the diagram; it should not become a long call-chain transcript.
- Unconfirmed ownership, unclear direction, candidate module names, or possible interface contracts stay out of the source model until confirmed.

## Simple Modules And Empty Whiteboxes

Simple modules may use an empty whitebox: the source model can omit `parts` and internal connectors when no internal component structure is needed.

Even an empty whitebox must still show the enclosing component boundary, at least one confirmed boundary port, at least one external node, and an `external` connector between that external node and the boundary port. Do not create a content-free diagram with only a component box.

If no boundary port or external interaction is confirmed, the canonical module owner page or Module Overview page is not ready for a complete Whitebox Component Diagram. Ask for confirmation, inspect allowed evidence, or report the gap instead of inventing a placeholder.

## Refreshing Older Module Maps

When converting an older Module Boundary block, Mermaid diagram, table, prose map, PlantUML sketch, draw.io export, or image into a Whitebox Component Diagram:

- Preserve every unique boundary fact, evidence anchor, uncertainty, and naming clue from the old map by moving it into the current Whitebox source model or current page text, not by retaining the old artifact.
- Convert only facts that already identify legal whitebox concepts: boundary ports, externals, internal parts, part ports, interface roles, and typed connectors.
- If the old map combines multiple concepts in one arrow or row, split only when the split is explicit in the old content.
- If conversion would choose a new owner, hide uncertainty, drop evidence, or turn private implementation details into stable contracts, report `meaning_loss_risk`.
- If conversion appears to require current-code comparison or missing coverage classification, report `drift_or_coverage_suspect` and recommend the drift workflow.

## Diagram Complexity Signal

Dense or tangled SVG output is a reader signal, not automatically a renderer defect or refactor verdict. Preserve the complete view when the source model is semantically correct. Add a short note only when density affects reader interpretation, for example: this diagram may indicate genuinely complex module assembly or a possible refactoring opportunity that needs human judgment.

## Layout Quality Checks

Whitebox rendering needs more than source-model validation:

- Structural checks: all confirmed nodes, ports, connector labels, interface roles, and derived-view contents are present.
- Connector label checks: visible connector labels carry relationship semantics and do not repeat the generated endpoint direction text.
- Viewport-readability checks: the ELK renderer may generate multiple candidate layouts, prefer fixed-browser-width readability over strict squareness, and write selected-candidate metadata to SVG without modifying the source model.
- Geometry/readability checks: generated SVGs render ports straddling owner boundaries, avoid extreme aspect ratios, overlapping node boxes, overflowing port labels, connector lines crossing port labels, arrowheads landing over port text, and obvious routed-edge regressions.
- Visual snapshot checks: representative fixtures should be visually reviewable or compared with tolerant expectations; pixel-perfect equality is not the only correctness signal.

## Avoid

- Treating generated SVG, generated images, Markdown prose, Mermaid, PlantUML, or draw.io XML as the modifiable fact source.
- Adding layout hints or source-level coordinates to `.whitebox.yaml`.
- Drawing package trees, complete class lists, helper inventories, or deployment inventories.
- Using private helpers, DTOs, SQL, adapters, or local files as public boundary concepts.
- Guessing parts, ports, externals, connector direction, interface roles, or evidence to make the diagram look complete.
- Publishing a module boundary diagram that has no confirmed boundary port connected to an external node.
