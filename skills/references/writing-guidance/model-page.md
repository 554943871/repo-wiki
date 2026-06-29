# Model Family Page Guidance

Model family 页面解释一组高度相关的系统理解模型，先给读者一个动态使用语境入口，再呈现它们之间的静态关系，并在同一页说明这些 model 的定义、关键字段和 demo/example。这里的 model 是系统理解模型，不是严格 DDD 分类，也不是数据库结构目录。

`wiki/05-models/README.md` 是 Model Catalog README，不是 Model Family Page。非 README 的 `wiki/05-models/<topic>.md` 页面默认是 Model Family Page：它承载一个有共同语境、共同 reader question 或共同事实链路的 model 组。不要把它机械理解成“一个 model 一页”。如果单个 model 只有少量字段说明，通常应并入更高相关度的 model family 页面，而不是单独建页。

## Model Catalog README

`wiki/05-models/README.md` 的主要职责是解释当前目录下其它 model family pages 各自承载什么内容，并把读者路由到正确详情页。它不是写作规范页、字段目录页，也不是把所有 model family 的关系、生命周期和关键字段集中重写一遍的总览页。

当目录下已有详情页时，README 优先使用这个结构：

```md
# 核心模型（Models）

本目录解释理解系统所需的 model families。每个详情页围绕一个稳定读者问题，说明一组相关 model 的边界、关系、关键字段摘要、demo/example 和事实来源。

## 模型目录

| 页面 | 承载内容 | 先看它的情况 | 相关页面 / 证据 |
| --- | --- | --- | --- |
| [<Model Family>](./<page>.md) | 说明这页解释的 model family 和主要关系。 | 当读者需要回答某个具体问题时。 | ... |

## 读者路线

| 读者问题 | 先看 | 再看 |
| --- | --- | --- |
| ... | ... | ... |
```

`模型目录` 是 README 的主表达。每一行应该概括一个详情页“承载什么”：共同 reader question、包含的 model family、最重要的关系或事实来源，以及读者什么时候应该先看它。表格不展开成员 model 定义、字段全集、生命周期步骤或 demo 细节；这些属于详情页。

`页面` 列的链接文字应使用简洁概括名，例如 `<业务对象>模型`、`<能力>编排模型` 或 `<场景>参考模型`。不要把所有覆盖对象写进标题，也不要用顿号、`与`、`和`、`and` 或长括号翻译串成并列清单；这些细节应留给 `承载内容`、`先看它的情况` 和 `相关页面 / 证据` 列。

可以保留简短的 `标准模型索引`，但它必须服务于 page routing：稳定名称、边界短句、owner page、少量 related pages / evidence。不要把 canonical index 写成每个 model、字段、状态和 source-of-truth 的总清单。若一个 canonical entry 已经等同于某个详情页主题，优先让行指向该 owner page，而不是在 README 里复述详情页正文。

当目录还没有详情页时，README 可以保留极短的收录边界说明。只要目录下已经有详情页，就应把泛化的“适合写 / 避免写”压缩或移出正文，把篇幅让给 `模型目录` 和读者路线。

README 应避免写：

- 详情页级别的 `模型关系` block、Mermaid 关系图或关系证据表。
- 成员 model 的定义、关键字段、生命周期、状态转换、demo/example 或 source-of-truth facts。
- 长篇写作指引、规则解释或模板说明。
- 按代码类、DTO、表、字段或缓存 key 列出的模型总清单。
- 与详情页重复的边界解释；README 只保留足以选页的短句。

## Model Family Boundary

Model family 的边界由共同 reader question、稳定事实链路或生命周期驱动，而不是由代码目录、类名、表名、DTO 名、字段相似度或“都是核心对象”驱动。

一组 model 应该放进同一个 model family page，当且仅当它们共同回答同一个读者问题，并且拆开后会损失关系理解。

### 同页信号

- 它们一起解释同一个稳定业务或系统事实，例如“候选集如何形成并被消费”。
- 它们之间存在稳定的 `组成`、`引用`、`衍生`、`事实源` 或状态转换关系。
- 它们在同一条生命周期里产生、变化、失效或终止。
- 一个 model 的关键字段、状态或解释来自另一个 model，或来自同一个权威事实来源。
- 一个 demo/example 可以自然串起这组 model，并帮助读者理解关系和字段含义。
- 拆成多页后，读者容易混淆 current fact / snapshot、`引用` / `衍生`、source / derived model、base / overlay 等关系。

### 拆页信号

- 这些 model 只是名字相似、字段相似、同目录、同表前缀、同 DTO 包或同一接口里出现。
- 它们只是在运行时偶尔一起出现，没有稳定概念关系或共同事实链路。
- 需要多个互不相关的 reader question 才能解释清楚。
- 生命周期、事实来源和主要 demo 都互相独立。
- 放在同一页会把页面变成大对象清单、表结构目录或领域词典。

### 生成流程

1. 从关键 flow、module、page、系统事实、当前 repo 证据或已有 wiki 中抽出重要名词、持久事实和容易混淆的字段。
2. 标出它们之间的 `组成`、`引用`、`衍生`、`事实源` 和状态转换关系。
3. 用一个核心 reader question 命名候选 model family。
4. 如果一张关系图和一个 demo/example 能自然解释这组 model，就放同一页。
5. 如果出现多个互不相干的 reader question，拆成多个 model family pages。
6. 如果某个 model 只是旁支、字段说明或证据，不单独建页；把它放进成员定义、关键字段、demo 或 uncertainty 中。

## 极简页面 Pattern

Model family page 默认从极简骨架开始。不要为了完整感先制造很多 section；只有当读者理解确实需要时，才增加关键字段、生命周期、demo 或事实来源等扩展章节。

极简版使用这四个二级章节：

````md
# <Model Family Name>

## 定位与边界
本页帮助读者回答：<核心 reader question>。

### <使用路径标题>

```mermaid
flowchart LR
  A["角色 / 页面 / 模块动作"] -->|"创建 / 读取 / 衍生 <ModelA>"| B["下一步活动"]
  B -->|"引用 <ModelB> / 展示 <ModelC>"| C["结果或后续处理"]
```

范围：本页只展开 <member models>；相邻模型通过“模型关系”或“相关页面”跳转。

## 模型关系
使用 model-relation block 表达这些 model 之间的 `泛化`、`组成`、`引用`、`衍生` 或 `事实源` 关系。

## 成员模型
### <Model A>
**定义：** 用一句话突出说明这个 model 表达什么事实、在本页关系里负责什么。

```jsonc
{
  "field": "mock value" // 字段含义
}
```

补充说明：只写会帮助理解 demo 字段、边界差异或事实来源的短说明。

### <Model B>
**定义：** ...

```jsonc
{
  "field": "mock value" // 字段含义
}
```

## 相关页面
链接相关 flow / page / module / decision。
````

`定位与边界` 合并 reader question、family boundary 和 reader entry。它应该先说明本页帮助读者回答哪个核心问题，再用使用语境图展示这些 model 在实际场景、执行链路或代码路径中如何被创建、读取、引用、衍生、展示、校验、失效或终止，最后最多用一句范围说明交代本页只展开哪些 member models。

这个章节要短。优先用 1-2 句话加一张使用语境图，让读者快速知道“什么场景下该看这页”和“这组 model 在链路里怎样被使用”。不要把它写成大段概念解释、术语定义、成员模型声明、`包含` 清单、完整排除项清单、字段目录或静态模型关系正文。覆盖场景只写已有 wiki、页面正文、相关 flow/module/decision、直接 repo evidence 或用户确认已经支撑的事实；如果需要 broad comparison、证据冲突或重新判断执行链路，写成 uncertainty 或转给 drift/radar，而不是在 model page 里猜。

使用语境图只承担入口职责，不替代 flow page、sequence、lifecycle 或 model-relation block。图只画读者理解 model usage 必需的关键路径：哪个角色、页面、模块、运行单元或外部系统触发了哪段活动，边上标注创建、读取、引用、衍生、展示、校验、失效或终止了哪些 model，以及后续应跳到哪个 flow / module / decision / model page。

每张使用语境图都必须有明确入口和可观察出口。入口可以是角色动作、页面入口、模块触发、运行单元处理或外部系统事件；出口可以是读者能看到的结果、后续处理、稳定状态、异常终止、下一页/下一 flow/module/decision，或一个有边界的持续态。Mermaid `flowchart` 可以包含回退边或重试边，但每条回环边都必须写清业务条件、用户动作或系统动作，例如“校验失败，返回编辑”“用户修改后重新提交”“超时后重试”。不要留下无标签、无条件、无起点终点的闭环；如果补不出语义，改成 uncertainty、短 prose 或删除该边。

图形选择规则：

- 逻辑分叉、异常路径、回退或多种结果多时，优先用 Mermaid `flowchart`。
- 跨端、跨模块、跨系统、异步回调或时间顺序是理解重点时，优先用 Mermaid `sequenceDiagram`。
- 如果一个 `flowchart` 回环实际表达的是参与方消息往返、调用返回、异步回调、轮询或重试顺序，改用 `sequenceDiagram`；如果表达的是稳定状态变化，改用 state-transition / lifecycle；如果表达的是 model 间互相引用或衍生，移到 `模型关系`。
- 多个核心使用路径可以放多张图，但每张图必须有清楚标题，例如 `创建路径`、`展示路径`、`失效路径`；不要为了覆盖所有代码调用而堆图。
- 简单场景或证据不足以安全画图时，可以退回短 prose 或小表；表格仍只承担 reader entry，不替代动态图、flow page 或 `模型关系`。

使用语境图的节点和参与方不能把 model 当执行者。Model 是被创建、读取、引用、衍生、展示、校验、失效或终止的对象，应放在边标签、message 文本或 note 中；图节点 / participant 应优先使用已确认的角色、页面、模块、运行单元、外部系统，或当前页面先声明且有证据的 page-local subject。`sequenceDiagram` 的 header 必须遵守 `skills/references/writing-blocks/sequence.md` 的 participant header 规则：同一张图里的系统参与方保持同一抽象层级，结果卡片、状态变化、model、payload 或事实结论不做 header，除非它们已被确认成会主动发送/接收消息的 page、module、runtime unit 或 page-local active participant。Controller、Service、adapter、DTO、payload、表、字段、日志和临时 helper 通常只作为 evidence 或边标签的实现锚点，不应被提升成读者入口图的稳定主体。

使用语境图之后不要再重复解释同一批概念。`user_purchase_context 指代...`、`本页展开的成员模型是...`、`包含：...`、`不等同于：...` 这类内容只有在图、简短入口和范围说明没有覆盖且读者确实会误解时，才压缩成一句范围说明；否则应迁移到 `成员模型`、`模型关系`、`相关页面` 或直接删除重复表述。

`模型关系` 是极简版的主表达，必须使用 `skills/references/writing-blocks/model-relation.md` 定义的 model-relation block。关系少时可以用关系表；多节点、多方向、事实源、`引用` / `衍生` 容易混淆时，默认用 Mermaid 关系图表达关系本体，再用关系表补 evidence 和 uncertainty。

关系图和 `成员模型` 必须能互相对上。Mermaid 关系图中出现的每个 Model 节点，都要在本页有明确处理：本页主角 model 在 `成员模型` 下用三级标题、醒目定义句和符合 `skills/references/writing-blocks/structured-example.md` 的精简 `jsonc` mock data 展开；相邻但不归本页完整展开的 model 也要在 `成员模型` 下给出关系锚点级定义、为什么出现在图里、继续阅读路线，以及只展示本页已经支撑的最小字段。不要出现关系图画了多个 Model 节点，但 `成员模型` 只解释其中一部分且没有说明剩余节点的情况；如果不准备解释相邻节点，就把它移出关系图或改到 prose / 相关页面中。

`成员模型` 不使用总表承载所有 model。每个成员 model 使用一个三级标题，先用醒目的定义句说明这个 model 表达什么事实，再紧跟一个 `jsonc` 代码块展示精简 mock data，让读者快速看到字段组成。边界、字段说明和证据是辅助信息，不要把成员模型写成 `定义 / 边界 / 关键字段摘要 / 证据` 四行模板。

## 应该帮助读者回答

- 这一组 model 共同解释什么业务或系统事实。
- 读者在哪些活动场景、执行链路、代码路径或排查任务中应该先看这页。
- 这些 model 在实际链路里什么时候被创建、读取、引用、衍生、展示、校验、失效或终止。
- 哪些 model 是本页主角，哪些相邻概念只通过关系或相关页面跳转。
- 这些 model 之间是什么关系：泛化、组成、引用、衍生、事实源。
- 每个成员 model 的定义、边界和读者容易混淆的点是什么。
- 每个成员 model 的字段大概长什么样，哪些字段最能解释它的含义和关系。
- 哪些字段或属性对理解这组 model 的关系、生命周期、事实来源或协作约定重要。
- 这些 model 在 demo/example 中如何一起出现，读者能从例子里看懂什么。
- 这组 model 什么时候产生、变化、失效或终止。

## 适合写

- Model family 的定位、主角 model 和必要范围说明。
- 帮助读者进入页面的 model usage 语境图，说明 model 在关键场景或执行链路里如何被使用。
- 成员 model 清单，以及每个 model 的定义和边界。
- 成员 model 之间的重要关系：泛化、组成、引用、衍生、事实源。
- 影响协作理解的关键字段或属性，不追求字段全集。
- 能把多个 model 串起来的 demo、example、样例数据或典型场景说明。
- 这组 model 的关键生命周期、状态和状态转换。
- 相关 flows、pages 和 modules。
- 代码、接口或用户确认等证据。

## 避免写

- 为每个琐碎 model 单独建页，只得到字段清单。
- 完整数据库表结构。
- 完整 DTO、API payload 或 ORM 映射清单。
- Redis key 或缓存清单。
- 临时变量、局部布尔值或一次性 helper 状态。
- 把 model 强行分类为 DDD Entity / Value Object / Aggregate。
- 把 demo 写成无解释的日志、截图或原始 JSON dump。

## 推荐表达

Model family page 可以自然组合：

- Model family 定位：本页解释哪组 model、回答哪个 reader question。
- 使用语境图：在 `定位与边界` 中用 Mermaid `flowchart` 或 `sequenceDiagram` 展示关键使用路径，并把 model 放在边标签、message 或 note 中。
- 范围说明：哪些 model 是本页主角，哪些相邻概念通过关系或相关页面跳转。
- `model-relation` block：使用 Mermaid 模型关系图或关系表表达关系本体；必要时用关系表补充 meaning、evidence 和 uncertainty。
- 成员模型：每个 model 使用三级标题，先写醒目的定义句，再用一个符合 structured-example block 的精简 `jsonc` mock data 代码块展示字段组成；边界和证据作为短补充。
- 关键字段表，按 model 说明 field meaning、source of truth、evidence 和 uncertainty。
- Demo/example 表或短场景，说明这些 model 如何一起出现。
- 生命周期或状态转换。
- 相关 flows / pages / modules。
- 证据和代码锚点。

这些是写作建议，不是固定字段。

### 成员 Model 定义

当一个页面包含多个 model 时，`成员模型` 章节下每个 model 使用一个三级标题。不要用一张总表把所有 model 的定义、边界、字段和证据塞在一起；这种表通常过挤，也容易让页面变成对象清单。

````md
## 成员模型

### <ModelName>

**定义：** 一句话说明这个 model 表达什么事实、在当前 model family 里负责什么。

```jsonc
{
  "stable_field": "mock value",   // 稳定字段的示例值
  "related_field": {              // 与当前 model 关系相关的字段组
    "nested_field": "mock value"  // 嵌套字段的示例值
  }
}
```

补充说明：
- 只解释 demo 中最影响理解的字段、关系或事实来源。
- 边界和排除项只写读者容易误解的点。
- 证据用短锚点放在段末或页面末尾，不抢占定义和 demo 的阅读位置。
````

每个成员 model 默认应有一个符合 `skills/references/writing-blocks/structured-example.md` 的 `jsonc` mock data 代码块。这个代码块是人类理解用的 mock data，不是完整 schema、真实生产记录、接口契约或数据库结构。每个可见字段 key 必须有行尾注释，且同一代码块内的 `//` 注释应形成稳定的视觉列。字段只选能解释 model 定义、关系、生命周期、事实来源或协作规则的最小集合；不要为了显得完整而补全所有字段。

如果现有 wiki 没有足够信息支撑某个字段，不要凭代码名或想象补字段。可以在 demo 前后明确写“示例只展示已确认字段”，或把缺口报告为 uncertainty / coverage gap。不要把 mock data 伪装成事实证据。

避免把成员模型写成四个机械标签段落：`定义：...`、`边界：...`、`关键字段摘要：...`、`证据：...`。这些内容可以保留，但应服务于定义和 structured example，而不是成为主要版式。

### Demo / Examples

Demo 的作用是把关系和字段放回一个可理解的场景，不是堆原始数据。成员模型下的 `jsonc` mock data 用来解释单个 model 的字段组成；本节的 demo/example 表或短场景用来解释多个 model 如何一起出现。

```md
| Demo / Example | Involved models | What it demonstrates | Evidence |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
```

如果 demo 需要样例 payload、样例记录或界面状态，只保留最小片段，并解释它证明了哪个 model 定义、关系、字段含义或事实来源。不要粘贴无解释的日志、截图或原始 JSON dump；示例数据必须经过裁剪、命名清楚，并能辅助读者理解。

## 选择表达方式

按实际信息选择最能帮助读者理解的表达，不要为了统一样式制造空 section。

- 使用 model-relation block：`模型关系` 章节必须使用该 block。当 model family 内有多个成员、方向重要、关系标签容易混淆，或需要同时保留 evidence anchors 和 uncertainty 时，多节点、多方向或事实源关系默认用 Mermaid 关系图表达关系本体，再用关系表补充 evidence 和 uncertainty。关系标签使用 `泛化`、`组成`、`引用`、`衍生`、`事实源`，细节见 `skills/references/writing-blocks/model-relation.md`。
- 使用 usage context diagram：`定位与边界` 优先用 Mermaid `flowchart` 或 `sequenceDiagram` 表达 model 在关键场景、执行链路或代码路径里的动态使用入口。图里的主体是角色、页面、模块、运行单元或外部系统；model 放在边标签、message 或 note 中。图只画 reader entry 所需关键路径，不展开完整调用链。
- 使用 member model subsections：当页面包含多个 model，读者需要先知道每个 model 表达什么、字段如何组成、边界在哪里、哪些字段最重要时，在 `成员模型` 下为每个 model 建三级标题、醒目定义句和符合 structured-example block 的精简 `jsonc` mock data，不使用总表。
- 使用 key fields table：当字段含义会影响协作理解、事实来源、生命周期、关系判断或 demo 解释时。不要把它扩展成完整 schema。
- 使用 demo/example table：当一组 model 的关系需要通过典型样例才能看懂，或字段含义离开样例容易误读时。
- 使用 state-transition block：当这组 model 中有稳定状态集合、明确触发条件、终态、异常态、回退或不可逆状态时。不要把临时变量或 UI 展示态直接写成业务状态，细节见 `skills/references/writing-blocks/state-transition.md`。
- 使用 lifecycle section：当读者需要知道这组 model 什么时候产生、变化、失效或终止，但没有明确状态集合或转换触发器时。lifecycle 可以用短步骤、时间线或 prose，重点是起点、变化点、终止点和证据。
- 使用 source-of-truth facts 小表：当页面需要说明某个字段、规则、计算结果或解释以哪里为准时。表格应该写清 fact、source of truth、适用范围、evidence 和 uncertainty。
- 使用 prose：当只有一个简单关系、一个边界说明或一个短规则时。prose 仍然要保留证据和不确定性，不要把多个方向不同的关系塞进一句话。

## 模型关系（Relationships）

`模型关系` 章节的主表达是 relationships。它应该让读者看清“谁指向谁、谁由谁组成、谁从谁衍生、哪个事实由哪里说了算”。

`模型关系` 章节必须使用 `model-relation` block，而不是把关系埋在长段落里。尤其要保留 `引用` 和 `衍生` 的区别：`引用` 是 identity、上下文或当前事实的直接指向；`衍生` 是计算、复制、聚合、规范化或快照后的事实。两者同时存在时拆成两行。

关系图下的补充表可以承载 evidence anchors，例如代码路径、符号名、路由、配置、测试、已有 wiki 页面或用户确认。证据不足时把 uncertainty 写在关系旁边，而不是补成确定结论。

## 关键字段（Key Fields）

Model family page 的字段说明服务于理解，不服务于 schema 完整性。

适合记录：

- 会影响 model 定义或边界的字段。
- 会影响 `引用` / `衍生` / `事实源` 判断的字段。
- 会影响状态、生命周期、demo 或协作规则的字段。
- 容易被多个页面、接口、存储结构或角色误读的字段。

推荐表达：

```md
| Model | Field | Meaning | Source of truth | Evidence | Uncertainty |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |
```

避免把字段表写成数据库字段全集。字段类型、长度、索引、ORM 注解和缓存 key 只有在影响 reader understanding 时才写。

## 生命周期与状态（Lifecycle and State）

Lifecycle 解释一组 model 从产生到变化、失效或终止的读者路径。它适合表达 creation、mutation、expiration、archival、deletion、manual override 等长期有意义的阶段。

State transition 解释稳定状态之间的变化。只有当状态集合和触发条件对理解系统有帮助时才使用 `state-transition` block。若只有“创建后可以被更新”这种普通生命周期说明，用 lifecycle prose 或短步骤即可。

生命周期和状态转换可以同时出现，但不要互相重复：lifecycle 给读者完整路径，state transition 只承接状态名、trigger、result 和 exception。

## 事实来源（Source-of-Truth Facts）

当 model family page 包含容易被多个地方重复、覆盖或误解的事实时，写清 source-of-truth facts。

适合记录：

- 某个计算结果由哪个服务、规则、文档、用户确认或外部系统说了算。
- 某个 snapshot、derived field 或展示字段从哪个 source 得来。
- 某个业务规则当前只能被证据支持到什么程度。

避免把每个字段都写成 source-of-truth fact。只有当“哪里说了算”会影响协作理解、更新风险或读者判断时才写。

## LLM 语义检查问题

- 页面是否解释了一组高度相关 model 的共同语境和关系，而不是只列单个字段？
- `定位与边界` 是否先给出核心 reader question，再用 usage context diagram 或安全退路说明活动场景、执行链路、代码路径或读者任务入口？
- `定位与边界` 的图是否根据场景选择了合适表达：分支多用 `flowchart`，跨端 / 跨模块 / 跨系统 / 时间顺序重要时用 `sequenceDiagram`？
- `定位与边界` 的图是否有明确入口和可观察出口；若存在回退或重试边，是否标明业务条件或动作，并避免无语义闭环？
- `定位与边界` 的图是否把 model、结果卡片、状态变化或事实结论放在边标签、message、note、outcome、state-transition 或 `模型关系` 中，而不是把它们当执行者、participant header 或 activity node？
- `定位与边界` 是否只画理解 model usage 必需的关键路径，没有退化成完整代码调用链？
- `定位与边界` 是否避免长篇概念定义、成员声明、`包含` 清单和过长排除项清单？
- 成员 model 的定义、边界和排除项是否清楚？
- 每个成员 model 是否有醒目的定义句，并紧跟一个能展示字段组成、字段 key 带行尾注释的精简 `jsonc` mock data 代码块？
- 成员模型是否避免退化成 `定义 / 边界 / 关键字段摘要 / 证据` 的机械标签清单？
- `模型关系` 是否使用了 `model-relation` block，而不是普通 prose？
- 关系图中的每个 Model 节点是否都能在 `成员模型` 中找到主角模型定义或关系锚点级说明？
- `成员模型` 是否按每个 model 的三级标题展开，而不是使用拥挤总表？
- 是否清楚说明范围内和范围外？
- 关键字段是否服务于 model 定义、关系、事实来源、生命周期或 demo，而不是完整 schema？
- Demo/example 是否解释了这些 model 如何一起出现，而不是只贴原始数据？
- 状态和生命周期是否有证据或用户确认？
- 模型关系是否使用清楚的关系标签，并保留 `引用` 和 `衍生` 的区别？
- 关系、lifecycle、state transitions 和 source-of-truth facts 是否保留 evidence anchors 和 uncertainty？
- 模型关系是否避免把数据依赖误写成运行时调用？
- 是否避免把存储实现当成 model 本身？
