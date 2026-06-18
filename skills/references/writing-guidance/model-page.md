# Model Page Guidance

Model 页面解释理解系统所需的核心对象、状态、关系和规则。这里的 model 是系统理解模型，不是严格 DDD 分类，也不是数据库结构目录。

## 应该帮助读者回答

- 这个 model 表达什么概念。
- 它为什么值得被稳定记录。
- 它的边界是什么。
- 它什么时候产生、变化、失效或终止。
- 它和其他 model、角色或系统事实有什么关系。
- 哪些字段或属性对协作理解重要。

## 适合写

- 模型含义和边界。
- 关键生命周期。
- 关键状态和状态转换。
- 重要关系：泛化、组成、引用、衍生、事实源。
- 影响协作理解的字段或属性。
- 相关 flows、pages 和 modules。
- 代码、接口或用户确认等证据。

## 避免写

- 完整数据库表结构。
- Redis key 或缓存清单。
- ORM 映射细节。
- 临时变量、局部布尔值或一次性 helper 状态。
- 把 model 强行分类为 DDD Entity / Value Object / Aggregate。

## 推荐表达

Model 页面可以自然组合：

- 模型定位。
- 模型边界。
- 生命周期或状态转换。
- Mermaid 模型关系图；必要时用关系表补充证据和不确定性。
- 关键字段。
- 相关 flows / pages / modules。
- 证据和代码锚点。

这些是写作建议，不是固定字段。

## 选择表达方式

按实际信息选择最能帮助读者理解的表达，不要为了统一样式制造空 section。

- 使用 model-relation block：当 model 有多个关系、方向重要、关系标签容易混淆，或需要同时保留 evidence anchors 和 uncertainty 时。多节点、多方向或事实源关系默认用 Mermaid 关系图表达关系本体，再用关系表补充 evidence 和 uncertainty。关系标签使用 `泛化`、`组成`、`引用`、`衍生`、`事实源`，细节见 `skills/references/writing-blocks/model-relation.md`。
- 使用 state-transition block：当 model 有稳定状态集合、明确触发条件、终态、异常态、回退或不可逆状态时。不要把临时变量或 UI 展示态直接写成业务状态，细节见 `skills/references/writing-blocks/state-transition.md`。
- 使用 lifecycle section：当读者需要知道 model 什么时候产生、变化、失效或终止，但没有明确状态集合或转换触发器时。lifecycle 可以用短步骤、时间线或 prose，重点是起点、变化点、终止点和证据。
- 使用 source-of-truth facts 小表：当页面需要说明某个字段、规则、计算结果或解释以哪里为准时。表格应该写清 fact、source of truth、适用范围、evidence 和 uncertainty。
- 使用 prose：当只有一个简单关系、一个边界说明或一个短规则时。prose 仍然要保留证据和不确定性，不要把多个方向不同的关系塞进一句话。

## 模型关系（Relationships）

Model relationships 应该让读者看清“谁指向谁、谁由谁组成、谁从谁衍生、哪个事实由哪里说了算”。

优先使用 `model-relation` block，而不是把关系埋在长段落里。尤其要保留 `引用` 和 `衍生` 的区别：`引用` 是 identity、上下文或当前事实的直接指向；`衍生` 是计算、复制、聚合、规范化或快照后的事实。两者同时存在时拆成两行。

关系图下的补充表可以承载 evidence anchors，例如代码路径、符号名、路由、配置、测试、已有 wiki 页面或用户确认。证据不足时把 uncertainty 写在关系旁边，而不是补成确定结论。

## 生命周期与状态（Lifecycle and State）

Lifecycle 解释 model 从产生到变化、失效或终止的读者路径。它适合表达 creation、mutation、expiration、archival、deletion、manual override 等长期有意义的阶段。

State transition 解释稳定状态之间的变化。只有当状态集合和触发条件对理解系统有帮助时才使用 `state-transition` block。若只有“创建后可以被更新”这种普通生命周期说明，用 lifecycle prose 或短步骤即可。

生命周期和状态转换可以同时出现，但不要互相重复：lifecycle 给读者完整路径，state transition 只承接状态名、trigger、result 和 exception。

## 事实来源（Source-of-Truth Facts）

当 model 页面包含容易被多个地方重复、覆盖或误解的事实时，写清 source-of-truth facts。

适合记录：

- 某个计算结果由哪个服务、规则、文档、用户确认或外部系统说了算。
- 某个 snapshot、derived field 或展示字段从哪个 source 得来。
- 某个业务规则当前只能被证据支持到什么程度。

避免把每个字段都写成 source-of-truth fact。只有当“哪里说了算”会影响协作理解、更新风险或读者判断时才写。

## LLM 语义检查问题

- 页面是否解释了这个 model 的业务或系统含义，而不是只列字段？
- 是否清楚说明范围内和范围外？
- 状态和生命周期是否有证据或用户确认？
- 模型关系是否使用清楚的关系标签，并保留 `引用` 和 `衍生` 的区别？
- 关系、lifecycle、state transitions 和 source-of-truth facts 是否保留 evidence anchors 和 uncertainty？
- 模型关系是否避免把数据依赖误写成运行时调用？
- 是否避免把存储实现当成 model 本身？
