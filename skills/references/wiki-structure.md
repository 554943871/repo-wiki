# Wiki Structure

本文件定义 `wiki-sink` 初始化到目标仓库的固定 `wiki/` 骨架，以及每个固定入口的最小初始正文。它是给人和 LLM 使用的结构说明，不是机器检查规则。

## 固定结构

```text
wiki/
  README.md
  01-system.md
  02-flows/
    README.md
  03-pages/
    README.md
  04-modules/
    README.md
  05-models/
    README.md
  06-decisions.md
  07-drift.md
```

顶层内容页和目录使用数字前缀控制阅读顺序。`README.md` 不加数字。子目录内的内容页不加数字。

最终 wiki 的 reader-facing 标题使用中文为主，并在固定 page family 标题中保留英文别名作为稳定锚点。文件名和目录名继续使用英文。

## 目录与页面归属

本文件只固定顶层目录、README 入口和每个目录的最小初始正文。它不预先规定每个目录下必须有哪些子页面，也不把 child page 变成固定模板。

每个 active page family 的详细写作规则由 `skills/references/writing-guidance/` 下唯一、独占的元知识文档维护。`wiki-structure.md` 不承担详细 page-family 规范；它只提供初始化骨架和目录归属。

目录下是否新增页面，取决于是否存在已经确认、值得长期维护的主题或边界。`04-modules` 例外更严格：第一层生成入口来自 `wiki/01-system.md` 的 confirmed C2 runtime units，而不是任意看起来可独立维护的代码对象。

- `wiki/02-flows/`: 放关键 flow owner pages，例如关键用户旅程、跨模块业务流程、异步处理、回调、重试或工具调用链路。
- `wiki/03-pages/`: 放用户可见 page owner pages，例如关键页面、入口、导航、页面状态和页面级交互。
- `wiki/04-modules/`: 放 canonical module owner pages。`README.md` 是平铺 Canonical Module Index，不维护强制模块树；confirmed C2 runtime unit 默认生成 root module owner page。stable subsystem、代码模块或其他 lower-level module 只在从 C2 root page 的 Whitebox internal parts、既有 wiki、repo 证据或用户确认中明确需要下钻时，才拥有自己的 owner page。
- `wiki/05-models/`: 放 model family pages。每个页面先给出这组 model 在重要场景或代码路径中的动态使用入口，再呈现高度相关 model 之间的静态关系，并说明涉及 model 的定义、关键字段、demo/example、事实来源和证据。

如果名称、边界、owner page 或长期价值不清楚，先保留为候选说明、drift item 或待确认问题，不要为了填目录而创建页面。

## 初始正文

### wiki/README.md

```md
# 项目 Wiki

这个 wiki 记录当前系统中值得长期复用的理解材料。

## 阅读顺序

- [系统总览（System）](./01-system.md): 系统上下文和主要运行单元。
- [关键流程（Flows）](./02-flows/README.md): 关键用户、业务和系统流程。
- [页面与入口（Pages）](./03-pages/README.md): 用户可见页面、入口、导航、页面状态和页面级交互。
- [模块边界（Modules）](./04-modules/README.md): 人类可理解的能力和职责边界。
- [核心模型（Models）](./05-models/README.md): 理解系统所需的一组组核心模型、关系、关键字段和示例。
- [设计决策（Decisions）](./06-decisions.md): 当前仍影响系统理解的重要取舍。
- [漂移治理（Drift）](./07-drift.md): 当前待治理的 wiki/code 不一致和覆盖缺口。

## 收录范围

- 当前系统事实。
- 已确认或有证据支撑的长期知识。
- 帮助人理解系统的流程、页面、模块、模型和决策。

## 不收录内容

- 原始聊天记录。
- 一次性排查日志。
- 未确认的猜测。
- 只对局部实现有意义的临时代码细节。
```

### wiki/01-system.md

````md
# 系统总览（System）

本页解释系统上下文、主要运行单元和运行拓扑。

## C1：系统上下文（System Context）

待补充 1-3 句系统边界说明。

### 标准角色索引（Canonical Roles）

| 标准名称 | 类型与边界 | 证据 |
| --- | --- | --- |

### 标准外部系统索引（Canonical External Systems）

| 标准名称 | 类型与边界 | 交互方向 | 证据 |
| --- | --- | --- | --- |

## C2：主要运行单元（Container）

待补充 1-3 句主要运行单元说明。

### 标准运行单元索引（Canonical Main Runtime Units）

| 标准名称 | 类型与边界 | 主要协作对象 | 证据 |
| --- | --- | --- | --- |

## 运行拓扑（Runtime Topology）

```mermaid
flowchart LR
  TBD[待补充运行拓扑]
```

- 待补充入口、跨运行时交互路径、持久化读写关系、协议或外部依赖边界。

## 继续阅读

- 关键流程：待补充。
- 页面与入口：待补充。
- 模块边界：待补充。
- 核心模型：待补充。
- 设计决策：待补充。
````

### wiki/02-flows/README.md

```md
# 关键流程（Flows）

本目录解释关键用户、业务和系统流程，让读者先理解系统如何运转，再查看页面行为和模块边界。

适合写：
- 关键用户旅程。
- 跨模块业务流程。
- 关键系统流程，例如异步处理、回调、重试或工具调用链路。
- 有证据支撑的关键流转。

避免写：
- 普通函数调用链。
- 测试步骤。
- 日志排查路径。
- 一次性操作 SOP。
```

### wiki/03-pages/README.md

```md
# 页面与入口（Pages）

本目录解释用户可见页面、入口、导航、页面状态、页面级交互，以及页面如何承接 flow、module 和 model。

适合写：
- 关键页面的目标和用户可见入口。
- 页面之间的跳转关系。
- 页面可见区域、主要组件、弹窗、抽屉、tab、占位区和页面级 layout。
- 页面多态、页面可见状态、空态、异常态、禁用态和关键展示条件。
- 页面级出口路由、关键用户动作和用户可见结果。
- 页面级后端交互的触发时机、接口 / 能力、入参来源、页面影响和证据。
- 页面依赖的 flows、modules 和 models。
- 理解页面行为所需的关键接口、路由或数据来源。

避免写：
- 完整 DOM 树。
- CSS 和组件库细节。
- 组件清单式盘点。
- 后端调用链。
- 每个字段的展示规则全集。
- 像素级视觉稿还原、截图归档或组件内部事件链。
```

### wiki/04-modules/README.md

```md
# 模块边界（Modules）

本目录解释人类可理解的能力、职责边界、稳定入口、内部能力和协作规则。Module 可以和代码目录一致，也可以不一致。

本 README 是平铺 Canonical Module Index，不维护强制模块树。confirmed C2 runtime unit 默认拥有 root module owner page；stable subsystem、代码模块或其他 lower-level module 只在从 root page 下钻或被明确确认时拥有自己的 owner page。module page 之间可以通过“内部模块”、相关模块和读者路线进行下钻或横向跳转。

适合写：
- 模块负责什么。
- 模块不负责什么。
- 上游、下游、内部模块和协作关系。
- 对外能力、入口和 boundary port contracts。
- 支撑对外行为的内部稳定能力与 module-to-module drill-down routes。
- 当前仍有效的边界规则、owner decision 或协作约束。
- 重要代码锚点。

避免写：
- 直接复制 package tree。
- 运行单元清单。
- 强制模块树。
- 页面清单。
- 只有局部实现意义的 helper 说明。
- 把内部能力当成跨 module contract。
- 未确认的 owner 或边界争议。
```

### wiki/05-models/README.md

```md
# 核心模型（Models）

本目录解释理解系统所需的 model families：每个页面先给出这组 model 在重要场景或代码路径中的动态使用入口，再呈现高度相关 model 之间的静态关系，并说明涉及 model 的定义、关键字段、demo/example 和事实来源。这里的 model 不是严格 DDD 分类，也不是数据库结构目录。

## 模型目录

当前还没有确认的 model family page。新增详情页后，本节用短表说明每个页面承载什么内容、读者什么时候应该先看它，以及它关联的 flow / module / decision / evidence。

| 页面 | 承载内容 | 先看它的情况 | 相关页面 / 证据 |
| --- | --- | --- | --- |

## 收录边界

- 每个详情页围绕一个共同 reader question、稳定事实链路、生命周期、事实来源关系或 demo/example explainability。
- 详情页说明成员 model 的定义、边界、关键字段摘要、关系和证据。
- 不按代码目录、DTO、数据库表、字段相似度或“每个 model 都很重要”来建页。
- 不收录完整数据库表结构、完整 DTO / API payload / ORM 映射、Redis key 清单、临时变量或局部布尔状态。
```

### wiki/06-decisions.md

```md
# 设计决策（Decisions）

本页记录当前仍影响系统理解的重要决策和取舍。它不是历史决策归档。

## 写作指引

适合写：
- 当前仍有效的系统约束。
- 重要设计取舍及其原因。
- 明确不做的事情。
- 容易被未来维护者误改的决定。

避免写：
- 已失效的历史讨论。
- 纯实现细节。
- 没有取舍的普通事实。
- 历史文件清单。
```

### wiki/07-drift.md

```md
# 漂移治理（Drift）

No active drift or coverage gaps.
```
