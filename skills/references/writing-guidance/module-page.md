# Module Page Guidance

Module 页面解释人类可理解的能力和职责边界。Module 不等于代码目录、页面、服务进程或 package。

## 应该帮助读者回答

- 这个 module 负责什么。
- 它明确不负责什么。
- 它为哪些 flow 提供能力。
- 它依赖谁，被谁依赖。
- 它对外暴露哪些稳定入口、行为或能力。
- 当前代码中哪些位置能帮助验证这个理解。

## 适合写

- 能力定位。
- 负责 / 不负责边界。
- 上游、下游和协作关系。
- 对外入口或关键行为；当多个 APIs、tools、routes、events、entry points 或 capabilities 共同定义 module 边界时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- 内部重要能力的自然语言说明。
- 相关 flows、pages 和 models。
- 仓库相对代码锚点。

## 避免写

- 直接复制 package tree。
- 服务进程或部署单元清单。
- 页面清单。
- 普通 helper 方法说明。
- 把 public surface 写成 controller、helper、adapter、文件树或完整方法索引；这些只作为 secondary code evidence。
- 未确认的 owner 或职责归属。

## 推荐表达

Module 页面可以自然组合：

- 模块定位。
- Owns / Does not own。
- Public Surface table 或关键入口。
- Collaborates with。
- Important internal capabilities。
- Related flows。
- Related pages。
- Related models。
- Code anchors。

这些是写作建议，不是固定字段。

## LLM 语义检查问题

- 页面是否能让读者判断某个责任该不该归这个 module？
- 是否区分了 module 边界和代码目录结构？
- 协作关系是否说明方向和原因？
- Public surfaces 是否说明 stable interaction points、使用者、稳定行为和 owner boundary，而不是列举 private helpers 或文件？
- 代码锚点是否支撑了页面里的主要判断？
- 是否把实现细节写得超过了理解 module 所需的程度？
