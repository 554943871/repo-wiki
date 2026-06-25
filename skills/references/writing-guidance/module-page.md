# Module Page Guidance

Module 页面解释一个 canonical module 的人类可理解能力和职责边界。Module 不等于代码目录、页面、服务进程或 package；它也可以是一个已经确认的 C2 runtime unit 或 stable subsystem，只要它在 `wiki/04-modules/README.md` 中拥有 canonical name 和 owner page。

This guidance is for all canonical module owner pages under `wiki/04-modules/`. A former directory-level `module-map.md` becomes a module owner page when it draws a confirmed C2 runtime unit or subsystem as the enclosing component. `wiki/04-modules/README.md` remains the flat Canonical Module Index and reader route; module-to-module hierarchy and cross-jumps belong inside the relevant owner pages.

## 应该帮助读者回答

- 这个 module 负责什么。
- 它明确不负责什么。
- 它为哪些 flow 提供能力。
- 它依赖谁，被谁依赖。
- 它对外暴露哪些稳定入口、行为或能力。
- 它的 Module Boundary Map 如何展示 confirmed boundary ports、external interactions、internal parts 和 connector direction。
- 图中的哪些 internal parts 是内部 canonical modules，读者应该去哪里下钻。
- 每个重要 boundary port 聚合了哪些高度相关的 contracts。
- 哪些内部稳定能力支撑这些对外行为，但不应被外部直接依赖。
- 它和其他 module page 如何下钻或横向跳转。
- 哪些边界规则、must / must not、owner decision 或 active uncertainty 会影响后续修改。
- 当前代码中哪些位置能帮助验证这个理解。

## 适合写

- 能力定位，尤其说明这个 module 是代码模块、C2 runtime unit、stable subsystem，还是其他人类可理解能力边界。
- 负责 / 不负责边界。
- 上游、下游和协作关系。
- 对外入口或关键行为；当多个 APIs、tools、routes、events、entry points 或 capabilities 共同定义 module 边界时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- Module Boundary Map：每个 canonical module owner page 都必须包含完整的 Whitebox Component Diagram，并以 owner page 平级的 `.whitebox.yaml` 作为 diagram fact source、同目录 `assets/` 子目录里的 generated `.whitebox.svg` 作为 reader-facing rendering。Generated derived SVGs 仍放在同一个 `assets/` 目录，但 Markdown 只按 `skills/references/writing-blocks/whitebox-component.md` 的 reader-purpose threshold 选择性嵌入；不要机械地嵌入所有 generated derived views。细节见 `skills/references/writing-blocks/whitebox-component.md`。
- 内部模块：当 Whitebox 图中的 internal part 是 canonical module 时，用 `模块 | 图中节点 | 摘要 | 下钻页面` 表给出一两句话和跳转。完整职责、ports、contracts、证据由下钻 module owner page 维护。
- Port contract tables：当一个 boundary port 聚合多个相关 contracts 时，为这个 port 单独使用 `Contract | 输入 | 输出 | 简介 | 副作用` 表。输入/输出是读者级摘要，不是完整字段 schema；内部 part port 通常留给对应下钻 module page 解释。
- 内部重要能力的自然语言说明；当 internal part 不是 canonical module 但会影响理解时，用短段落、图例、节点说明或 Module Boundary block 解释它是 supporting participant，不要把它写进内部模块表。
- Module rules：当前仍有效的边界约束、必须遵守 / 不应做、owner decision 或非显然约定。
- 协作关系的方向、类型、稳定性和证据；关系复杂时使用 Dependency Map block。
- 相关 flows、pages 和 models。
- 下钻模块和相关模块的 reader routes。
- 仓库相对代码锚点。

## 避免写

- 直接复制 package tree。
- 服务进程或部署单元清单。
- 把 C2 runtime unit 页面写成部署 inventory，而不是人类可理解的 module boundary。
- 页面清单。
- 普通 helper 方法说明。
- 把内部能力当成跨 module contract。
- 把 supporting participants 写进内部模块表，或因为它们出现在 Whitebox 图中就提升为 canonical module。
- 在 `wiki/04-modules/README.md` 中强行维护模块树；README 是平铺 Canonical Module Index，不是唯一父级树。
- 在上层 module page 中复制下钻 module 的完整 ports、contracts、内部结构或证据。
- 把多个 public surfaces、内部能力或依赖关系合并成一条含糊行。
- 过期历史讨论或未拍板 ownership。
- 把 public surface 写成 controller、helper、adapter、文件树或完整方法索引；这些只作为 secondary code evidence。
- 未确认的 owner 或职责归属。
- 把 Mermaid、PlantUML、draw.io XML、Markdown prose、生成 SVG 或其他生成图片当作 Module Boundary Map 的事实源。
- 为了让图看起来完整而发明 boundary port、external node、internal part、interface role、connector direction 或 evidence。

## 推荐表达

Module 页面可以自然组合：

- 模块定位。
- 负责 / 不负责（Owns / Does not own）。
- 模块边界图（Whitebox Component Diagram / Module Boundary Map）：必备。Markdown 必须先展示 `./assets/<name>.whitebox.svg`，紧挨着保留平级 `.whitebox.yaml` source model link，并从 `.whitebox.yaml` 重新渲染所有 SVG 到同目录 `assets/` 子目录。Derived Whitebox Views 只有在回答明确读者问题或显著降低 dense diagram 理解成本时才嵌入；每个嵌入的派生图使用清楚的 `... Derived Whitebox View` 标题、alt text 和 reader-purpose 说明，表明它们只是同一 source model 的派生阅读视图。
- 内部模块：只列图中的 canonical module internal parts，列为 `模块 | 图中节点 | 摘要 | 下钻页面`。支撑参与方不进入这张表。
- Boundary port contract tables：每个需要解释 contract 集合的 boundary port 单独一张表，列为 `Contract | 输入 | 输出 | 简介 | 副作用`。
- 对外入口（Public Surface table）或关键入口。
- 协作对象（Collaborates with）。
- 重要内部能力（Important internal capabilities）。
- 模块规则（Module rules）。
- 下钻模块 / 相关模块（Drill-down / Related modules）。
- 相关流程（Related flows）。
- 相关页面（Related pages）。
- 相关模型（Related models）。
- 代码锚点（Code anchors）。

这些是写作建议，不是固定字段。

简单 module 可以使用没有 internal parts 的 empty whitebox，但仍必须包含至少一个 confirmed boundary port、一个 external node，以及连接两者的 `external` connector。如果没有证据能确认 boundary port 或 external interaction，不要补占位图；先确认事实或报告缺口。

## LLM 语义检查问题

- 页面是否能让读者判断某个责任该不该归这个 module？
- 是否区分了 module 边界和代码目录结构？
- 是否包含 Whitebox Component Diagram 作为 Module Boundary Map，并同时链接 `./assets/` 下的 generated SVG 和平级 `.whitebox.yaml` source model？完整图是否永远排在第一位、没有被 Derived Whitebox Views 替代？如果页面嵌入 Derived Whitebox Views，是否是按 `skills/references/writing-blocks/whitebox-component.md` 的 reader-purpose threshold 选择性嵌入，且标题、alt text 和说明都表明它们只是同一 source model 的派生阅读视图？
- `.whitebox.yaml` 是否是唯一 fact source；SVG、Mermaid、PlantUML、draw.io XML、Markdown prose 或生成图片是否只作为 derived/rendered/sketch material？
- 图中是否至少有一个 confirmed boundary port 连接到 external node；simple module 是否使用合法 empty whitebox 而不是无事实空盒？
- 图中的 components、parts、ports、interfaces、externals 和 connectors 是否都有足够 evidence 或用户确认，没有把猜测写成稳定事实？
- 协作关系是否说明方向和原因？可见 connector label 是否表达动作、数据、协议、契约或责任关系，而不是只写 `A -> B` 这种端点复述？
- Public surfaces 是否说明 stable interaction points、使用者、稳定行为和 owner boundary，而不是列举 private helpers 或文件？
- `内部模块` 表是否只列 canonical module internal parts，并用一两句话加下钻页面，而不是复制下钻 module 的完整内容？
- Boundary port contract tables 是否按一个 port 一张表组织，列出 `Contract | 输入 | 输出 | 简介 | 副作用`，并避免完整函数清单或字段 schema？
- 内部能力是否只解释 module 内部稳定能力，没有被误写成跨 module contract？
- Supporting participants 是否被解释为支撑节点，而不是被内部模块表或正文提升成 canonical module？
- Module-to-module drill-down 是否放在 owner page 正文中，而不是把 `README.md` 变成唯一父级树？
- Module rules 是否记录当前仍有效的边界约束或 owner decision，而不是历史讨论流水？
- 复杂依赖是否用 Dependency Map 区分 runtime call、data reference、owner dependency、fact source 和 active decision？
- 代码锚点是否支撑了页面里的主要判断？
- 是否把实现细节写得超过了理解 module 所需的程度？
