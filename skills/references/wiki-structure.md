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

## 初始正文

### wiki/README.md

```md
# Wiki

这个 wiki 记录当前系统中值得长期复用的理解材料。

## Reading Order

- [System](./01-system.md): 系统上下文和主要运行单元。
- [Flows](./02-flows/README.md): 关键用户、业务和系统流程。
- [Pages](./03-pages/README.md): 用户可见页面、入口、导航和页面状态。
- [Modules](./04-modules/README.md): 人类可理解的能力和职责边界。
- [Models](./05-models/README.md): 理解系统所需的核心模型、状态和关系。
- [Decisions](./06-decisions.md): 当前仍影响系统理解的重要取舍。
- [Drift](./07-drift.md): 当前待治理的 wiki/code 不一致和覆盖缺口。

## What Belongs Here

- 当前系统事实。
- 已确认或有证据支撑的长期知识。
- 帮助人理解系统的流程、页面、模块、模型和决策。

## What Does Not Belong Here

- 原始聊天记录。
- 一次性排查日志。
- 未确认的猜测。
- 只对局部实现有意义的临时代码细节。
```

### wiki/01-system.md

```md
# System

本页解释系统上下文和主要运行单元。它覆盖 C1/C2 级别的信息：系统是什么、服务谁、和外部世界如何交互、主要运行单元如何协作。

## Guidance

适合写：
- 系统目标和责任边界。
- 外部用户、外部系统和主要交互入口。
- 主要运行单元以及它们之间的大关系。
- 读者应该继续查看哪些 flow、page、module 或 model 页面。

避免写：
- 组件内部结构。
- 类、函数、SQL 或字段全集。
- 详细流程步骤。
- 每个模块的完整职责。
```

### wiki/02-flows/README.md

```md
# Flows

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
# Pages

本目录解释用户可见页面、入口、导航、页面状态，以及页面如何承接 flow、module 和 model。

适合写：
- 关键页面的目标和用户可见入口。
- 页面之间的跳转关系。
- 页面可见状态和关键展示条件。
- 页面依赖的 flows、modules 和 models。
- 理解页面行为所需的关键接口、路由或数据来源。

避免写：
- 完整 DOM 树。
- CSS 和组件库细节。
- 组件清单式盘点。
- 后端调用链。
- 每个字段的展示规则全集。
```

### wiki/04-modules/README.md

```md
# Modules

本目录解释人类可理解的能力和职责边界。Module 可以和代码目录一致，也可以不一致。

适合写：
- 模块负责什么。
- 模块不负责什么。
- 上游、下游和协作关系。
- 对外能力或入口。
- 重要代码锚点。

避免写：
- 直接复制 package tree。
- 运行单元清单。
- 页面清单。
- 只有局部实现意义的 helper 说明。
```

### wiki/05-models/README.md

```md
# Models

本目录解释理解系统所需的核心模型、状态、关系和规则。这里的 model 不是严格 DDD 分类，也不是数据库结构目录。

适合写：
- 核心对象或概念的含义。
- 模型边界。
- 状态和生命周期。
- 模型之间的引用、组成、衍生或事实来源关系。
- 会影响协作理解的关键字段。

避免写：
- 完整数据库表结构。
- Redis key 清单。
- ORM 映射细节。
- 临时变量或局部布尔状态。
```

### wiki/06-decisions.md

```md
# Decisions

本页记录当前仍影响系统理解的重要决策和取舍。它不是历史决策归档。

## Guidance

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
# Drift

No active drift or coverage gaps.
```
