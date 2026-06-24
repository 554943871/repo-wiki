# Wiki Guidance Principles

本文件是所有 repo-wiki skills 的第一层 reader-quality guidance。每个 skill 都先按这里的原则判断信息是否应该保留、如何组织、能否写成稳定 wiki 知识，然后才使用具体 page-family guidance 或 writing blocks。

这些原则是自然语言 guidance，不是 schema、validator、lint、PASS/FAIL 或 compliance gate。语义质量只能靠证据、读者视角和 LLM 语义判断来检查。

## Priority

Information Preservation 是最高优先级。

任何 readability rewrite、结构调整、拆分、合并、移动、删减、表格化或图示化，都不能丢失 unique information、evidence anchors、canonical names、责任边界、decision meaning、例外条件或不确定性。

如果更易读的表达会改变含义、压掉证据、消除不确定性、合并两个不同概念、或让读者无法追溯原始判断，就停止改写并报告风险。不要用“整理”“精简”“标准化”当作删除信息的理由。

## Reader-First Structure

wiki 先服务读者理解，再服务文件整齐。

优先让读者知道：

- 这段内容解释什么系统事实或判断。
- 为什么它值得长期保留。
- 它属于哪个 owner page 或 canonical index。
- 它和相关 flow、page、module、model、decision 的关系。
- 读者下一步应该去哪里继续看。

可以把 dense prose 改成短段落、表格、列表或 Mermaid 图，但只有在这些表达让含义更清楚时才使用。不要为了填满固定字段而制造空内容，也不要把自然段机械拆成模板。

## Reader-Facing Heading Language

最终写入目标 repo 的 `wiki/**/*.md` 面向中文母语读者，页面标题、目录入口和正文小节标题默认使用中文。固定 page family 或长期复用的 block 语义可以在中文标题后保留英文别名，例如 `系统总览（System）`、`关键流程（Flows）`、`模块边界（Modules）`、`模型关系（Relationships）`。

文件名、目录名、skill 名、finding type、action vocabulary、代码符号、API path、class name、配置 key、事件名、表名、字段名和 repo 里的 canonical business term 不要为了中文化而强行翻译。需要同时服务读者和 LLM 锚点时，用“中文标题 + 英文别名”的方式，而不是替换掉稳定英文锚点。

生成或重写 wiki 时复用这组固定读者标题：

- `Wiki` -> `项目 Wiki`
- `Reading Order` -> `阅读顺序`
- `What Belongs Here` -> `收录范围`
- `What Does Not Belong Here` -> `不收录内容`
- `System` -> `系统总览（System）`
- `Flows` -> `关键流程（Flows）`
- `Pages` -> `页面与入口（Pages）`
- `Modules` -> `模块边界（Modules）`
- `Models` -> `核心模型（Models）`
- `Decisions` -> `设计决策（Decisions）`
- `Drift` -> `漂移治理（Drift）`
- `Guidance` -> `写作指引`

如果已有 wiki 使用英文标题，`wiki-doctor` 可以在不改变 meaning、link、anchor 和 canonical name 的前提下把 reader-facing 标题改成上述中文标题；如果标题本身是 repo 里的 confirmed product / domain name，则保留原名或作为别名，不要机械翻译。

## Evidence-Aware Writing

稳定 wiki 内容需要清楚区分：

- repo 证据支持的当前系统事实。
- 用户明确确认的业务意图、命名、边界或设计 rationale。
- 从代码中能观察到、但还不能证明意图的候选说明。
- 仍需确认的不确定性、冲突或风险。

写证据时优先使用仓库相对路径、符号名、路由、配置、测试、文档位置或明确用户确认。不要把长推理过程、原始聊天记录或大段日志塞进稳定 wiki。需要治理的问题放进 Drift Page；需要确认的问题以问题或风险形式保留，而不是伪装成事实。

## Canonical Naming

复用 repo-local wiki 已经确认的 canonical names。V1 不创建单独的 wiki glossary page；canonical names 分布在 owner pages 和 catalog README 中。优先从这些位置取名：

- Roles、External Systems、Main Runtime Units: `wiki/01-system.md`
- Flows: `wiki/02-flows/README.md`
- Pages: `wiki/03-pages/README.md`
- Modules: `wiki/04-modules/README.md`
- Models: `wiki/05-models/README.md`
- Decisions: `wiki/06-decisions.md`

如果命名、边界或 owner page 不清楚，先问用户或报告 `meaning_loss_risk` / candidate note。不要为了让文档看起来统一而发明同义词、重命名业务概念、把代码目录名直接提升为 module 名，或把局部实现名当成外部系统名。

Canonical name 必须是单一稳定名称。不要在 canonical name 里用 `A / B`、`A or B`、`A 或 B` 或类似混名写法来包住多个候选名、别名或不同概念；这些信息只能放在 alias、candidate note、证据或待确认问题里。

## Stable Anchors And Traceability

图、表和短段落都应该能让读者追溯到同一组稳定概念。复杂图里的节点、参与方、页面、model、module、flow、decision 或 public surface，如果会被图下表、下钻段落、相关页面或后续维护反复引用，应使用稳定名称、稳定别名或短编号。

稳定锚点是 reader-facing 约定，不是机器 ID 体系。它的目的只是避免同一个概念在主图、补充表、证据和相关页面之间漂移。不要为了形式统一给一次性说明、候选事实或证据不足的节点硬造编号。

主图和下钻内容的关系要清楚：

- Flow 的 activity map 是复杂 flow 的主线图；sequence、state transition、page navigation、dependency map 和 evidence table 只能补充主图中的关键节点，不应重新定义另一条主业务链路。
- Drill-down 图或定位图应复用主图中的稳定节点名、边或连续子链，并说明它聚焦哪一段；它可以补充细节，但不能悄悄改写主图语义。
- Model relation、dependency map 和 page navigation 如果有总览图和局部图，局部图应说明来自哪个总览关系或 reader route，避免读者看到两套互相竞争的拓扑。

## Canonical Subjects

涉及“谁做了什么”的图和表，主语必须来自已经确认的 system context node、canonical roles、external systems、main runtime units、pages、modules，或来自当前页面先声明且有证据支撑的 subject list。Canonical Roles 只要参与该流程，就天然适合作为 Subject。目标系统本身可以在确实由系统发起的活动里作为 subject，但不要因此写进 Canonical Roles。

Canonical Models 不适合作为 Activity Subject：model 通常是被创建、读取、更新、终止、展示或引用的对象、状态载体或事实来源，而不是“谁做了什么”的执行者。需要表达 model 变化时，把 model 写在 SVO 的 Object、状态结果、相关模型、state transition 或 evidence anchor 中；不要把 model 名称硬提升成主语。主语不能是 payload、DTO、SQL、record、adapter、helper、method、临时状态名或文件路径。

同一张 Activity Map 里的 Subject 应保持抽象层次一致。Canonical Roles 代表参与者，可以和其他 subject family 共存；除 Roles 之外，同一张图里的其他 Subject 应尽量来自同一种 canonical index 类型或同一种页面声明的 flow-local 抽象层，例如全是 External Systems、全是 Main Runtime Units、全是 Pages、全是 Modules，或全是同一运行单元内部的 flow-local participants。不要在同一张主活动图里把 Page、Module、Runtime Unit、External System 和实现组件混成同级主语。如果确实需要解释跨层交接，应拆成主 activity map 加 drill-down / sequence，或把较低层内容放到 Object、条件、证据或相关页面中。

如果写不出清楚主语，说明当前内容可能不是稳定业务活动、事实来源、页面跳转或 public surface；应改成证据说明、候选说明、source-of-truth note，或保留为问题，不要把实现名硬提升成 reader-facing 概念。

Activity map 的活动节点必须显式写出 Subject，并使用 SVO 业务动作短句。多 Subject activity map 应用 Mermaid `class` / `classDef` 或等价样式区分 Subject；颜色只表达 Subject / perspective，不表达状态、风险、优先级或 Component 归属。

## No Guessing Stable Knowledge

不要把猜测写成稳定 wiki 知识。

可以直接写入的内容通常需要至少一种支撑：

- 当前 repo 里能明确证明的系统事实。
- 用户确认。
- 已有 wiki 页面中可保留、可追溯的信息。
- 明确引用的外部材料。

业务意图、设计 rationale、页面命名、module 边界、model 含义、跨团队责任和“应该如此”的判断，只有在证据或用户确认足够时才能写成稳定事实。证据不足时，保留为问题、candidate wiki note、drift item 或 intentionally left out。

## No Mechanical Correctness Theater

不要用机械正确性替代语义正确性。

禁止把 schema、validator、lint、PASS/FAIL、compliance、字段齐全、标题齐全、表格齐全，包装成 wiki 质量已经正确的证明。一个页面可以格式完整但事实错误、边界错、命名错、读者入口错或丢失关键不确定性。

报告质量时使用自然语言说明：保留了什么、改清楚了什么、还有什么证据不足、哪里有 meaning loss risk、哪里可能需要 drift radar 或用户确认。

## Semantic Review Checklist

每次重写或写入稳定 wiki 内容后，用自然语言做一次语义自检。这个 checklist 不是 validator，也不能产生 PASS/FAIL；它只帮助写作者发现是否还需要保留不确定性或停止改写。

- Reader question: 这段内容正在回答哪个读者问题？主表达是图、表还是 prose，为什么这个表达最清楚？
- Main expression: 如果内容有拓扑、顺序、分支、跳转、状态或关系，是否优先用了 Mermaid 或等价图形表达？如果用了表格作为主表达，是否确实是短线性或横向对照信息？
- Stable anchors: 图中节点、表格行和相关段落是否复用同一组 stable names / aliases？下钻内容是否明确回到主图或 owner page？
- Canonical subjects: 活动主语、事实来源、页面来源、参与方和 owner 是否来自 confirmed canonical concepts 或当前页面声明的 subject list，而不是 model / runtime helper / adapter / payload / DTO / SQL / helper？Canonical Roles 是否优先保留为 Subject，Canonical Models 是否只作为对象、状态或相关模型出现？除 Roles 外，同一张 Activity Map 的其他 Subject 是否来自同一种 canonical index 或同一种 flow-local 抽象层？Activity map 是否使用 SVO label，并对不同 Subject 分色？
- Evidence and uncertainty: 每个关键事实、边、状态、跳转、surface 或 decision 是否有短证据锚点；证据不足处是否保留 uncertainty，而不是补成稳定结论？
- Boundary fit: 信息是否写在正确 owner page 或 canonical index 附近；是否把 model 关系、dependency、sequence、page navigation、public surface 或 decision 混成一种表达？
- Preservation: 重排成图、表或短段落后，是否丢失了 unique facts、异常、限制条件、反例、证据或 unresolved question？
- Diagram readability: 中心 Mermaid 图是否可读、边标签是否过长、节点是否拥挤；如果工具环境能方便预览，可以做一次人工阅读/渲染检查，但这只是可读性检查，不是机械正确性证明。

## Skill Responsibilities

这些原则适用于所有 wiki skills，但不同 skill 不能互相越界。

- Reader-facing rewrite work, such as `wiki-doctor`, 只改善已有 wiki 的格式、结构和表达。它必须保留原信息，不能发明新稳定事实，不能做 drift classification。
- Drift detection, `wiki-drift-radar`, 对照 current working tree 和 wiki，分类 Wiki Drift、Code Drift、Coverage Gap 或 Wiki Too Thin，只刷新 `wiki/07-drift.md`。Candidate wiki note 不是稳定事实。
- Drift resolution, `wiki-drift-govern`, 只治理已经分类的 Drift Page items。它可以更新 wiki、补 coverage gap、或在确认的 Code Drift 下改代码，并在治理完成后清空 drift queue。
- New stable knowledge capture, `wiki-sink`, 只在没有 active drift items 时初始化 wiki 或写入 confirmed / evidence-grounded stable knowledge。它不能持久化原始聊天记录，不能把猜测写进稳定页面。

## Dense Prose Rewrite Example

Dense input:

```md
Checkout total comes from PricingClient in src/checkout/PricingGateway.ts now, not CartStore, but the old wiki says CartStore owns totals; admins can still override tax from /admin/orders/:id according to routes/admin.ts; refunds are described as manual in docs/refunds.md, but I did not verify current code.
```

Reader-first rewrite that preserves information:

```md
## Checkout Total Ownership

- Current evidence: checkout totals are read through `PricingClient` in `src/checkout/PricingGateway.ts`.
- Wiki conflict: the existing wiki says `CartStore` owns totals, so this may be Wiki Drift unless the wiki describes an intended behavior that should still hold.
- Admin tax override: admins can still override tax from `/admin/orders/:id`; evidence is `routes/admin.ts`.
- Refund uncertainty: `docs/refunds.md` describes refunds as manual, but current code has not been verified. Keep this as an uncertainty or candidate note, not as stable current behavior.
```

The rewrite is easier to scan, but it keeps every unique fact, evidence anchor, conflict, and uncertainty from the dense note.
