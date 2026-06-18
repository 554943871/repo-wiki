# Module Page Guidance

Module 页面解释人类可理解的能力和职责边界。Module 不等于代码目录、页面、服务进程或 package。

## 应该帮助读者回答

- 这个 module 负责什么。
- 它明确不负责什么。
- 它为哪些 flow 提供能力。
- 它依赖谁，被谁依赖。
- 它对外暴露哪些稳定入口、行为或能力。
- 哪些内部稳定能力支撑这些对外行为，但不应被外部直接依赖。
- 哪些边界规则、must / must not、owner decision 或 active uncertainty 会影响后续修改。
- 当前代码中哪些位置能帮助验证这个理解。

## 适合写

- 能力定位。
- 负责 / 不负责边界。
- 上游、下游和协作关系。
- 对外入口或关键行为；当多个 APIs、tools、routes、events、entry points 或 capabilities 共同定义 module 边界时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- 内部重要能力的自然语言说明；当内部能力和 public surfaces 的支撑关系会影响理解时，使用 Module Boundary block。
- Module rules：当前仍有效的边界约束、必须遵守 / 不应做、owner decision 或非显然约定。
- 协作关系的方向、类型、稳定性和证据；关系复杂时使用 Dependency Map block。
- 相关 flows、pages 和 models。
- 仓库相对代码锚点。

## 避免写

- 直接复制 package tree。
- 服务进程或部署单元清单。
- 页面清单。
- 普通 helper 方法说明。
- 把内部能力当成跨 module contract。
- 把多个 public surfaces、内部能力或依赖关系合并成一条含糊行。
- 过期历史讨论或未拍板 ownership。
- 把 public surface 写成 controller、helper、adapter、文件树或完整方法索引；这些只作为 secondary code evidence。
- 未确认的 owner 或职责归属。

## 推荐表达

Module 页面可以自然组合：

- 模块定位。
- 负责 / 不负责（Owns / Does not own）。
- 模块边界（Module Boundary block）：当 public surface、内部能力、协作关系和规则共同定义边界时。
- 对外入口（Public Surface table）或关键入口。
- 协作对象（Collaborates with）。
- 重要内部能力（Important internal capabilities）。
- 模块规则（Module rules）。
- 相关流程（Related flows）。
- 相关页面（Related pages）。
- 相关模型（Related models）。
- 代码锚点（Code anchors）。

这些是写作建议，不是固定字段。

## LLM 语义检查问题

- 页面是否能让读者判断某个责任该不该归这个 module？
- 是否区分了 module 边界和代码目录结构？
- 协作关系是否说明方向和原因？
- Public surfaces 是否说明 stable interaction points、使用者、稳定行为和 owner boundary，而不是列举 private helpers 或文件？
- 内部能力是否只解释 module 内部稳定能力，没有被误写成跨 module contract？
- Module rules 是否记录当前仍有效的边界约束或 owner decision，而不是历史讨论流水？
- 复杂依赖是否用 Dependency Map 区分 runtime call、data reference、owner dependency、fact source 和 active decision？
- 代码锚点是否支撑了页面里的主要判断？
- 是否把实现细节写得超过了理解 module 所需的程度？
