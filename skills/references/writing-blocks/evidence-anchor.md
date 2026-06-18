# Evidence Anchor Block

用于在稳定 wiki 页面里保留短、可追溯的证据锚点。Evidence anchor 支撑页面里的事实、边界、关系、状态、surface、decision 或不确定性，但它不是原始日志归档、测试报告全集、聊天记录或完整代码索引。

## 适合使用时机

- 页面声明了当前系统事实、边界、状态、跳转、surface、dependency、model relation 或 decision。
- 读者需要知道这个结论能从哪里复核。
- 证据只支持“观察到的行为”，还不能支持业务意图、owner 或 rationale，需要保留 uncertainty。
- 同一页面有多类证据，需要避免长段落里混淆事实、推断和待确认项。

## 推荐表达

Evidence anchor 可以是行内短锚点、表格列、图下注释或短列表。优先短，不要把页面变成证据仓库。

```md
Evidence:
- Route: `src/routes/orders.ts`
- State source: `OrderStatus` enum
- Test: `order-status.spec.ts`
- User confirmation: 2026-06-18 discussion, checkout owner confirmed
```

如果证据和结论需要横向对照，可以使用小表：

```md
| Claim | Evidence anchor | Supports | Uncertainty |
| --- | --- | --- | --- |
| Checkout page starts payment recovery | `src/routes/checkout.ts` | Route and visible entry exist | Owner rationale not confirmed |
```

## 写作要求

- 使用仓库相对路径、符号名、路由、配置、测试名、已有 wiki 页面、产品材料或明确用户确认。
- 写清证据支持什么：当前事实、存在性、调用关系、状态含义、边界、用户可见行为，还是只支持候选解释。
- 证据不足时保留 uncertainty，不要把“代码里看到”改写成业务意图或 owner decision。
- 用户确认可以作为 evidence，但应简短说明确认的内容；不要粘贴长聊天记录。
- 原始日志、截图、curl、长输出、接口字段全集或完整 diff 只作为外部材料入口；稳定 wiki 页面保留可复核锚点和结论。
- 不写本机绝对路径。必要时使用 repo-relative path、文档相对链接或稳定符号。

## 与其他 Blocks 的关系

- Activity Map、Sequence、State Transition、Page Navigation、Page Layout、Module Boundary、Model Relation、Public Surface 和 Decision Tradeoff 都可以带 evidence anchors。
- Drift Page 的 Evidence Note 用于治理队列；Evidence Anchor Block 用于稳定页面里的短证据支撑。
- Evidence anchor 不替代 owner page、canonical index 或 module/model/flow/page 正文。证据证明不了边界时，留下 uncertainty 或 drift item。

## 避免

- 把完整日志、完整测试输出、聊天流水或大段代码贴进稳定 wiki。
- 只列文件路径，不说明它支撑哪个事实。
- 把临时 debug 证据写成长期系统事实。
- 用本机绝对路径、一次性截图文件或不可复核链接作为唯一证据。
- 因为 evidence 列存在就删除原有 uncertainty、限制条件、反例或 unresolved question。
