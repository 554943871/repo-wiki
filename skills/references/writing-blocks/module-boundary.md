# Module Boundary Block

用于解释一个 module 的稳定能力边界：它对外承诺什么、内部有哪些值得命名的能力、和相邻 module 如何协作，以及哪些规则限制它的责任范围。

Module boundary 不是 package tree、service process、deployment unit、page inventory 或 helper list。它服务读者判断“这个责任该不该归这个 module”“相邻 module 可以依赖什么稳定行为”“哪些实现细节只是证据”。

## 适合使用时机

- 一个 module 的职责边界容易和代码目录、运行单元、页面或相邻 module 混淆。
- 多个 public surfaces、routes、events、tools、commands 或 capabilities 共同定义 module 对外边界。
- 读者需要知道内部稳定能力如何支撑 public surfaces，但不需要完整实现调用链。
- module 之间存在稳定引用、调用、依赖或 owner 关系，需要区分方向、关系类型和证据。
- 已有说明只列文件、类、Controller、Service 或 helper，无法判断业务责任归属。

## 推荐表达

先用短段落说明 module 的 reader-facing boundary，再按需要组合 public surface table、internal capability table、dependency map 和规则说明。不要为了凑结构而填空表。

```md
| Capability / surface | Kind | Used by | Stable promise | Owner boundary | Evidence |
| --- | --- | --- | --- | --- | --- |
| Quote price | Public capability | Checkout flow | Returns a price quote for a cart snapshot | Pricing owns quote semantics, not payment capture | `src/pricing/**` |
| Normalize tax inputs | Internal capability | Quote price | Prepares tax inputs before quote calculation | Internal to Pricing; not a cross-module contract | `TaxInputNormalizer` |
```

当引用关系本身重要时，使用 Mermaid 或依赖表补充：

```md
| From | To | Entry / surface | Relationship | Why it matters | Evidence |
| --- | --- | --- | --- | --- | --- |
| Checkout | Pricing | Quote price | Runtime call | Checkout total depends on current quote result | checkout pricing gateway |
```

## 写作要求

- 明确 `Owns` 和 `Does not own`。边界说明应能帮助读者判断责任归属，而不是只描述代码位置。
- Public surface 行只写稳定可依赖的入口、能力、事件、route、tool 或 command；private helper、DTO、SQL 和 adapter internals 只能作为 evidence anchors。
- Internal capability 只记录 module 内部稳定、可复用、能解释边界的能力；不要把每个函数或类都命名成能力。
- 如果一个内部能力支撑多个 public surfaces，可以说明支撑关系；但内部能力不能被当成跨 module contract。
- 协作关系要写清方向、关系类型和证据。区分 runtime call、data reference、ownership dependency、fact source 和 active decision。
- 一个 surface、capability 或 dependency 行只表达一个稳定行为；多个能力不要压成一行或一条箭头。
- Module rules 应写当前仍有效的边界约束、must / must not、owner decision 或非显然约定；过期历史讨论不进入规则。
- 保留 related flows / pages / models，让读者知道这个 module 被哪些业务主线、页面和模型使用。

## 与其他 Blocks 的关系

- Whitebox Component Diagram 是 canonical module owner page 的必备 Module Boundary Map，并由 `.whitebox.yaml` 作为 diagram fact source。Module Boundary Block 可以补充 owns / does-not-own、public surface table、internal capability 说明和 module rules，但不能替代 Whitebox Component Diagram，也不能把 prose、Mermaid、PlantUML、draw.io XML 或生成图片当作 diagram fact source。
- Public Surface Block 解释对外稳定入口；Module Boundary Block 用它作为 module 边界的一部分，而不是替代整个 module 页面。
- Dependency Map Block 解释 module 与其他对象的关系方向、类型、稳定性和证据。
- Activity Map 和 Sequence 可以引用 module 的 public surface 或 stable capability，但不能把 private helper 当成业务活动或主要 participant。
- Model Relation 解释模型之间的事实关系；不要把模型关系直接推断成 module runtime call。
- Decision Tradeoff 记录仍影响 module boundary 的当前取舍；未拍板边界应指向 decision 或 uncertainty，不写成稳定事实。

## 避免

- 把 module boundary 写成 package tree、文件树、Controller / Service / Repository 清单。
- 把 deployment unit、进程、页面或目录名直接当成 module，除非 owner boundary 已确认。
- 把 private helper、adapter internals、DTO 字段、SQL 或完整 call chain 写成 public contract。
- 把内部能力 ID、内部函数名或局部实现当成跨 module 调用入口。
- 只写“负责 X”，不写不负责什么、谁使用、稳定承诺和证据。
- 把 active decision、候选 ownership 或边界争议写成稳定 module fact。
