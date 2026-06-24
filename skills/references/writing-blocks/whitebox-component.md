# Whitebox Component Diagram Block

Whitebox Component Diagram 是 module 页面的必备 Module Boundary Map。它解释一个 enclosing module 如何通过 boundary ports 暴露能力、如何把这些能力委派给内部 components、内部 components 如何协作，以及哪些 interface roles 被满足。

它不是 UML 完整模型、package dependency map、调用链、文件树或截图式架构图。它只记录已经确认的 module 边界事实。

## Fact Source And Derived Output

- `.whitebox.yaml` 是唯一可修改的 diagram fact source。Agent 修改 diagram 时只改 source model，再重新生成 SVG。
- `.whitebox.svg` 是 reader-facing rendering，必须从同一份 `.whitebox.yaml` 派生。SVG 和其他生成图片都不是事实源。
- Mermaid、PlantUML、draw.io XML、Markdown prose、截图、手绘图片和生成图片都不能作为 Whitebox Component Diagram 的 diagram fact source。它们可以作为旧草图、临时说明或迁移输入，但不能替代 `.whitebox.yaml`。
- Source model 只写 topology 和语义关系；不要写坐标、布局、排序、routing、canvas size、样式或 renderer hints。布局由 renderer 决定。
- Source model 不写 `views`、`derivedViews`、`include_parts`、`include_connectors` 或其他展示选择字段。Derived views 由 renderer 根据拓扑和 connector 类型自动生成。
- 如果 source model 和 SVG 不一致，以 `.whitebox.yaml` 为准，并重新渲染 SVG。

## Markdown Linking Convention

Module 页面在 Module Boundary Map 位置同时链接 SVG 和 source model。优先把两者放在 module 页面旁边，使用稳定的相对路径：

```md
## 模块边界图（Module Boundary Map）

![Checkout Module whitebox component diagram](./checkout.whitebox.svg)

Source model: [`checkout.whitebox.yaml`](./checkout.whitebox.yaml) for the complete diagram and any derived views below.
```

For dense diagrams, keep the complete view first, keep the source model link visible beside the generated diagrams, and embed only non-empty generated Derived Whitebox Views immediately after the complete diagram and source model link:

```md
### Boundary Derived Whitebox View

![Checkout Module Boundary Derived Whitebox View](./checkout.whitebox.boundary.svg)

### Delegation Derived Whitebox View

![Checkout Module Delegation Derived Whitebox View](./checkout.whitebox.delegation.svg)

### Assembly Derived Whitebox View

![Checkout Module Assembly Derived Whitebox View](./checkout.whitebox.assembly.svg)
```

Derived views are reader aids from the same source model. They do not replace the complete diagram, do not introduce additional source models, and must never be treated as fact sources.

The first standard derived views are:

- `boundary`: external nodes, enclosing component boundary ports, and `external` connectors.
- `delegation`: enclosing component boundary ports, internal part ports, and `delegation` connectors.
- `assembly`: internal parts, internal part ports, and `assembly` connectors.
- `interfaces`: generated only when `interfaceAssembly`, `provides`, or `requires` is present.

Do not generate or embed an empty derived view. A derived view exists only when its connector or interface-role content exists in the source model.

如果目标仓库约定把图片放到 assets 目录，也必须保持 source model 和 SVG 的关系清楚，让读者和后续 agent 能从 Markdown 同时找到渲染图和事实源。

## Source Model Semantics

Use the current Whitebox Component Diagram source model:

- `kind: whitebox_component_diagram` and `version: 1`.
- `component`: the enclosing module boundary. It owns boundary `ports` and must have evidence.
- `parts`: optional internal components inside the enclosing boundary. Use only for confirmed internal responsibilities that help explain how public capability is assembled.
- `ports`: named interaction points. Port direction is not a field; interaction direction is expressed by connectors.
- `interfaces`: optional interface contracts that can be attached to ports as `provides` or `requires`.
- `externals`: actors, modules, pages, flows, runtime units, or systems outside this enclosing module boundary when they are needed to explain the boundary interaction.
- `connectors`: directed, typed relationships with evidence.

Connector types:

- `external`: connects an external node and an enclosing boundary port. The connector `from` and `to` fields express the interaction direction.
- `delegation`: connects an enclosing boundary port and an internal part port. The connector direction shows whether the boundary capability is delegated inward or an internal capability is exposed outward.
- `assembly`: connects one internal part port and another internal part port.
- `interfaceAssembly`: connects a required interface role to a provided interface role.

Connectors must terminate at legal endpoints. Ordinary endpoints are strings: use the external id for an external node, and use `owner.port` for an enclosing component port or internal part port. Interface-role endpoints are structured objects with `owner`, `port`, `interface`, and `role`. Do not connect whole components, whole parts, arbitrary files, packages, helpers, DTOs, SQL objects, or prose-only concepts. `interfaceAssembly` connects interface roles, not ports themselves.

## Evidence Expectations

- The enclosing component and every connector need short evidence. Prefer repo-relative paths, line ranges, symbols, routes, tests, docs, existing wiki content, or explicit user confirmation.
- A node, port, interface, or part may exist only when its meaning is confirmed by evidence or user confirmation. Do not introduce a part just because a class or package exists.
- Evidence explains why the fact belongs in the diagram; it should not become a long call-chain transcript.
- Unconfirmed ownership, unclear direction, candidate module names, or possible interface contracts stay out of the source model until confirmed.

## Simple Modules And Empty Whiteboxes

Simple modules may use an empty whitebox: the source model can omit `parts` and internal connectors when no internal component structure is needed.

Even an empty whitebox must still show the enclosing component boundary, at least one confirmed boundary port, at least one external node, and an `external` connector between that external node and the boundary port. Do not create a content-free diagram with only a component box.

If no boundary port or external interaction is confirmed, the module page is not ready for a complete Whitebox Component Diagram. Ask for confirmation, inspect allowed evidence, or report the gap instead of inventing a placeholder.

## Refreshing Older Module Maps

When converting an older Module Boundary block, Mermaid diagram, table, prose map, PlantUML sketch, draw.io export, or image into a Whitebox Component Diagram:

- Preserve every unique boundary fact, evidence anchor, uncertainty, and naming clue from the old map.
- Convert only facts that already identify legal whitebox concepts: boundary ports, externals, internal parts, part ports, interface roles, and typed connectors.
- If the old map combines multiple concepts in one arrow or row, split only when the split is explicit in the old content.
- If conversion would choose a new owner, hide uncertainty, drop evidence, or turn private implementation details into stable contracts, report `meaning_loss_risk`.
- If conversion appears to require current-code comparison or missing coverage classification, report `drift_or_coverage_suspect` and recommend the drift workflow.

## Diagram Complexity Signal

Dense or tangled SVG output is a reader signal, not automatically a renderer defect or refactor verdict. Preserve the complete view when the source model is semantically correct. Add a short note only when density affects reader interpretation, for example: this diagram may indicate genuinely complex module assembly or a possible refactoring opportunity that needs human judgment.

## Layout Quality Checks

Whitebox rendering needs more than source-model validation:

- Structural checks: all confirmed nodes, ports, connector labels, interface roles, and derived-view contents are present.
- Geometry/readability checks: generated SVGs avoid extreme aspect ratios, overlapping node boxes, overflowing port labels, and obvious routed-edge regressions.
- Visual snapshot checks: representative fixtures should be visually reviewable or compared with tolerant expectations; pixel-perfect equality is not the only correctness signal.

## Avoid

- Treating generated SVG, generated images, Markdown prose, Mermaid, PlantUML, or draw.io XML as the modifiable fact source.
- Adding layout hints or source-level coordinates to `.whitebox.yaml`.
- Drawing package trees, complete class lists, helper inventories, or deployment inventories.
- Using private helpers, DTOs, SQL, adapters, or local files as public boundary concepts.
- Guessing parts, ports, externals, connector direction, interface roles, or evidence to make the diagram look complete.
- Publishing a module boundary diagram that has no confirmed boundary port connected to an external node.
