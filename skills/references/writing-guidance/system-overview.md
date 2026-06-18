# System Overview Guidance

`wiki/01-system.md` 帮助读者快速理解系统是什么、服务谁、边界在哪里，以及主要运行单元如何协作。

## 应该帮助读者回答

- 这个系统解决什么问题。
- 主要用户、外部系统或外部平台是谁。
- 本系统负责什么，不负责什么。
- 主要入口、出口和交互方向是什么。
- 系统由哪些主要运行单元组成。
- 读者接下来应该查看哪些 flow、page、module 或 model 页面。

## 适合写

- 系统目标和当前状态。
- 外部参与方与外部系统。
- 系统责任边界。
- 主要运行单元和大粒度协作关系。
- 关键入口、协议或外部依赖。
- 当读者需要比较系统级 APIs、tools、routes、page entries、events 或 capabilities 时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- 支撑这些判断的代码锚点或文件证据。

## 避免写

- C3 组件内部结构。
- 类、函数、SQL 或字段全集。
- 详细业务流程步骤。
- 完整模块职责说明。
- 页面布局或前端组件细节。
- 把 public surface 写成 controller、helper、组件、文件树或完整接口字段索引；这些只作为 secondary code evidence。

## LLM 语义检查问题

- 读者能否只看本页就知道系统和外部世界的边界？
- 本页是否停留在 C1/C2 粒度，没有下钻到组件或代码层？
- 每个外部交互是否说明了方向和关系？
- 系统级 public surfaces 是否只列 stable interaction points，并把实现细节留作 secondary code evidence？
- 责任边界是否同时说明了负责和不负责的部分？
- 是否给出了继续阅读的入口，而不是把所有细节塞在本页？
