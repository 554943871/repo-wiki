# Flow Page Guidance

Flow 页面解释关键用户、业务或系统流程。它关注“谁在什么条件下做了什么，系统如何推进”，而不是普通调用链。

## 应该帮助读者回答

- 这个流程从哪里开始，到哪里结束。
- 参与者是谁。
- 关键步骤、分支、异常和终止点是什么。
- 哪些 module 承接了流程中的责任。
- 哪些 page 承接了流程中的用户可见步骤。
- 哪些 model 在流程中被创建、读取、更新或终止。
- 哪些调用、事件或状态变化有代码或用户确认支撑。

## 适合写

- 用户旅程和业务主链路。
- 跨模块系统流程。
- 关键异步链路、回调、重试、调度或工具调用流程。
- 重要分支、异常路径和不可逆节点。
- 与 page/module/model family 页面的导航关系。

## 避免写

- Controller -> Service -> Repository 这类普通调用链。
- 测试步骤。
- 日志排查路径。
- 一次性操作 SOP。
- 没有证据的运行时调用关系。

## 推荐表达

Flow 页面可以自然组合：

- 简短流程定位。
- 参与者和触发条件。
- 活动图（Activity map），用 Mermaid 主活动图表达业务主链路、confirmed subjects、SVO activity labels、conditions、branches、joins、exceptions 和 cross-role handoffs；很短的线性 flow 才用步骤表作为主表达。
- 时序图（Sequence diagram），用来解释关键场景中的参与方协作和调用顺序；很短的线性序列才用步骤表作为主表达。
- 状态表或状态图（State table / state diagram），用来解释核心对象、流程或页面背后的稳定状态变化。
- 关键分支和异常。
- 相关 pages。
- 相关 modules。
- 相关 models。
- 代码锚点或证据。

这些不是固定字段。按实际内容选择最能帮助读者理解的表达。

具体写法可参考 `writing-blocks/activity-map.md`、`writing-blocks/sequence.md` 和 `writing-blocks/state-transition.md`。

## 表达选择

优先从读者问题选择表达，不要为了凑结构而重复同一信息。

| 表达 | 适合回答 | 何时使用 | 不适合 |
| --- | --- | --- | --- |
| Activity map | 谁在什么条件下做什么，主链路如何分支、汇合、异常退出和跨角色交接 | flow 有多个 confirmed subject、业务条件、异常路径、人工介入或跨系统/跨角色交接时；复杂 flow 默认用 Mermaid `flowchart`，活动节点使用 SVO label，不同 Subject 分色 | 普通 Controller -> Service -> Repository 调用链，或只能列出文件和 payload 的实现说明 |
| Sequence | 关键场景中参与方按什么顺序交互 | 某个 activity 需要说明调用顺序、消息往返、回调、重试或异步协作时 | 替代整条业务主链路，或把实现类画成主要参与方 |
| State table | 核心对象有哪些稳定状态，什么触发状态变化，结果是什么 | model、flow 或 page 有明确终态、异常态、回退或不可逆状态时 | 表达服务调用顺序、临时变量或纯 UI 展示态 |
| Steps table / prose | 范围、背景、证据限制、导航关系或很短的线性流程 | 信息简单，或需要保留不确定性、证据说明和读者下一步时 | 承载复杂分支、异常路径和跨角色交接 |

Activity map 通常是复杂 flow 的第一层 reader-facing 结构。Sequence 和 state table 应该补充 activity map 中的关键节点，而不是把业务主链路拆散成技术调用图。Prose 应保留 evidence anchors、限制条件和异常说明，但不要用 dense prose 掩盖主线和分支。

## 可追溯下钻（Traceability）

复杂 flow 页面应让读者先看到一张主 activity map，再通过 sequence、state transition、page navigation、dependency map、相关 pages/modules/models 和证据锚点下钻。下钻内容应复用主 activity map 的稳定节点名、短编号或连续子链，不要重新定义一套竞争的主链路。

当某个局部场景只覆盖主链路的一段时，说明它从哪个活动节点、哪条边、哪个异常出口或哪段连续子链展开。共享节点在局部场景中是入口、出口、前置条件、投射点还是异常处理点，也应写清楚。

## LLM 语义检查问题

- 页面是否说明了流程的起点、终点和触发条件？
- 活动描述是否是业务或系统动作，而不是技术名词堆叠？
- 复杂 flow 是否用 Mermaid activity map 表达了 business mainline、confirmed subjects、SVO activity labels、conditions、branches、joins、exceptions 和 cross-role handoffs？
- 每个 activity node 的 Subject 是否已经存在于 canonical names 或当前页面声明的 subject list，而不是在节点里临时发明？
- 同一 Subject 的节点是否使用同一 Mermaid class；不同 Subject 是否用不同 class / classDef 或等价样式分色？
- 下钻 sequence、state、page navigation 或 dependency 是否明确回到主 activity map 的节点、边或子链？
- 如果复杂 flow 使用步骤表或 prose 作为主表达，是否有明确理由；它是否丢失了分支、汇合、异常或交接关系？
- 实现层项目是否只作为 evidence anchors，而不是 activity labels？
- 运行时调用关系是否有代码、接口、路由或用户确认支撑？
- 是否把普通调用链误写成关键 flow？
- 是否链接到相关 page、module 和 model，而不是重复它们的完整内容？
