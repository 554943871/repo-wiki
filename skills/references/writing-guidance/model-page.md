# Model Family Page Guidance

Model family 页面解释一组高度相关的系统理解模型，重点呈现它们之间的关系，并在同一页说明这些 model 的定义、关键字段和 demo/example。这里的 model 是系统理解模型，不是严格 DDD 分类，也不是数据库结构目录。

每个 `wiki/05-models/*.md` 页面默认是一个 Model Family Page：它承载一个有共同语境、共同 reader question 或共同事实链路的 model 组。不要把它机械理解成“一个 model 一页”。如果单个 model 只有少量字段说明，通常应并入更高相关度的 model family 页面，而不是单独建页。

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

1. 从关键 flow、module、page、系统事实或已有 wiki 中抽出重要名词、持久事实和容易混淆的字段。
2. 标出它们之间的 `组成`、`引用`、`衍生`、`事实源` 和状态转换关系。
3. 用一个核心 reader question 命名候选 model family。
4. 如果一张关系图和一个 demo/example 能自然解释这组 model，就放同一页。
5. 如果出现多个互不相干的 reader question，拆成多个 model family pages。
6. 如果某个 model 只是旁支、字段说明或证据，不单独建页；把它放进成员定义、关键字段、demo 或 uncertainty 中。

## 极简页面 Pattern

Model family page 默认从极简骨架开始。不要为了完整感先制造很多 section；只有当读者理解确实需要时，才增加关键字段、生命周期、demo 或事实来源等扩展章节。

极简版使用这四个二级章节：

```md
# <Model Family Name>

## 定位与边界
本页回答：...
包含：...
不包含：...

## 模型关系
使用 model-relation block 表达这些 model 之间的 `泛化`、`组成`、`引用`、`衍生` 或 `事实源` 关系。

## 成员模型
### <Model A>
说明这个 model 的定义、边界、关键字段摘要和证据。

### <Model B>
说明这个 model 的定义、边界、关键字段摘要和证据。

## 相关页面
链接相关 flow / page / module / decision。
```

`定位与边界` 合并 reader question 和 family boundary。它应该先说明本页回答什么读者问题，再列出哪些 model 属于本页、哪些相邻概念不属于本页。

`模型关系` 是极简版的主表达，必须使用 `skills/references/writing-blocks/model-relation.md` 定义的 model-relation block。关系少时可以用关系表；多节点、多方向、事实源、`引用` / `衍生` 容易混淆时，默认用 Mermaid 关系图表达关系本体，再用关系表补 evidence 和 uncertainty。

`成员模型` 不使用总表承载所有 model。每个成员 model 使用一个三级标题，下面用短段落或短列表说明定义、边界、关键字段摘要和证据。这样避免把 model 定义挤进表格，也避免退化成字段清单。

## 应该帮助读者回答

- 这一组 model 共同解释什么业务或系统事实。
- 哪些 model 属于本页，哪些相邻概念不属于本页。
- 这些 model 之间是什么关系：泛化、组成、引用、衍生、事实源。
- 每个成员 model 的定义、边界和读者容易混淆的点是什么。
- 哪些字段或属性对理解这组 model 的关系、生命周期、事实来源或协作约定重要。
- 这些 model 在 demo/example 中如何一起出现，读者能从例子里看懂什么。
- 这组 model 什么时候产生、变化、失效或终止。

## 适合写

- Model family 的定位、范围和排除项。
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
- 范围与排除项：哪些 model 在页内，哪些相邻概念应去其他页面。
- `model-relation` block：使用 Mermaid 模型关系图或关系表表达关系本体；必要时用关系表补充 meaning、evidence 和 uncertainty。
- 成员模型：每个 model 使用三级标题，下面写定义、边界、关键字段摘要和证据。
- 关键字段表，按 model 说明 field meaning、source of truth、evidence 和 uncertainty。
- Demo/example 表或短场景，说明这些 model 如何一起出现。
- 生命周期或状态转换。
- 相关 flows / pages / modules。
- 证据和代码锚点。

这些是写作建议，不是固定字段。

### 成员 Model 定义

当一个页面包含多个 model 时，`成员模型` 章节下每个 model 使用一个三级标题。不要用一张总表把所有 model 的定义、边界、字段和证据塞在一起；这种表通常过挤，也容易让页面变成对象清单。

```md
## 成员模型

### <ModelName>

定义：...

边界：...

关键字段摘要：...

证据：...
```

这些标签是写作提示，不是固定 schema。`关键字段摘要` 只写会影响理解的字段，不写字段全集。如果一个字段只是持久化细节、传输细节或局部实现细节，除非它影响 model 关系、事实来源或协作规则，否则不要放进 model family page。

### Demo / Examples

Demo 的作用是把关系和字段放回一个可理解的场景，不是堆原始数据。

```md
| Demo / Example | Involved models | What it demonstrates | Evidence |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
```

如果 demo 需要样例 payload、样例记录或界面状态，只保留最小片段，并解释它证明了哪个 model 定义、关系、字段含义或事实来源。

## 选择表达方式

按实际信息选择最能帮助读者理解的表达，不要为了统一样式制造空 section。

- 使用 model-relation block：`模型关系` 章节必须使用该 block。当 model family 内有多个成员、方向重要、关系标签容易混淆，或需要同时保留 evidence anchors 和 uncertainty 时，多节点、多方向或事实源关系默认用 Mermaid 关系图表达关系本体，再用关系表补充 evidence 和 uncertainty。关系标签使用 `泛化`、`组成`、`引用`、`衍生`、`事实源`，细节见 `skills/references/writing-blocks/model-relation.md`。
- 使用 member model subsections：当页面包含多个 model，读者需要先知道每个 model 表达什么、边界在哪里、哪些字段最重要时，在 `成员模型` 下为每个 model 建三级标题并写短说明，不使用总表。
- 使用 key fields table：当字段含义会影响协作理解、事实来源、生命周期、关系判断或 demo 解释时。不要把它扩展成完整 schema。
- 使用 demo/example table：当一组 model 的关系需要通过典型样例才能看懂，或字段含义离开样例容易误读时。
- 使用 state-transition block：当这组 model 中有稳定状态集合、明确触发条件、终态、异常态、回退或不可逆状态时。不要把临时变量或 UI 展示态直接写成业务状态，细节见 `skills/references/writing-blocks/state-transition.md`。
- 使用 lifecycle section：当读者需要知道这组 model 什么时候产生、变化、失效或终止，但没有明确状态集合或转换触发器时。lifecycle 可以用短步骤、时间线或 prose，重点是起点、变化点、终止点和证据。
- 使用 source-of-truth facts 小表：当页面需要说明某个字段、规则、计算结果或解释以哪里为准时。表格应该写清 fact、source of truth、适用范围、evidence 和 uncertainty。
- 使用 prose：当只有一个简单关系、一个边界说明或一个短规则时。prose 仍然要保留证据和不确定性，不要把多个方向不同的关系塞进一句话。

## 模型关系（Relationships）

Model family page 的主表达通常是 relationships。它应该让读者看清“谁指向谁、谁由谁组成、谁从谁衍生、哪个事实由哪里说了算”。

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
- `定位与边界` 是否同时说明本页回答的问题、包含的 model 和不包含的相邻概念？
- 成员 model 的定义、边界和排除项是否清楚？
- `模型关系` 是否使用了 `model-relation` block，而不是普通 prose？
- `成员模型` 是否按每个 model 的三级标题展开，而不是使用拥挤总表？
- 是否清楚说明范围内和范围外？
- 关键字段是否服务于 model 定义、关系、事实来源、生命周期或 demo，而不是完整 schema？
- Demo/example 是否解释了这些 model 如何一起出现，而不是只贴原始数据？
- 状态和生命周期是否有证据或用户确认？
- 模型关系是否使用清楚的关系标签，并保留 `引用` 和 `衍生` 的区别？
- 关系、lifecycle、state transitions 和 source-of-truth facts 是否保留 evidence anchors 和 uncertainty？
- 模型关系是否避免把数据依赖误写成运行时调用？
- 是否避免把存储实现当成 model 本身？
