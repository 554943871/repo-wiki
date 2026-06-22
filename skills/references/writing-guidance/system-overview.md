# System Overview Guidance

本文件是 `wiki/01-system.md` 的唯一详细写作规范来源。`wiki-structure.md` 只提供可初始化的最小骨架，`wiki-suite-design.md` 只记录 suite 级设计定位。

`wiki/01-system.md` 帮助读者快速理解系统是什么、服务谁、边界在哪里、主要运行单元如何协作，以及被说明的运行范围在运行上如何连起来。

默认结构使用固定小节标题：

```md
## C1：系统上下文（System Context）

1-3 句系统边界说明。外部上下文节点较多、或关系方向只靠表格不直观时，可以补一张 C1 context Mermaid 图；简单系统不要为了模板强行画图。

### 标准角色索引（Canonical Roles）

| 标准名称 | 类型与边界 | 证据 |
| --- | --- | --- |

### 标准外部系统索引（Canonical External Systems）

| 标准名称 | 类型与边界 | 交互方向 | 证据 |
| --- | --- | --- | --- |

## C2：主要运行单元（Container）

1-3 句主要运行单元说明。

### 标准运行单元索引（Canonical Main Runtime Units）

| 标准名称 | 类型与边界 | 主要协作对象 | 证据 |
| --- | --- | --- | --- |

## 运行拓扑（Runtime Topology）

Mermaid `flowchart`，图中实体节点必须 100% 复用 C1 roles、C1 external systems 和 C2 main runtime units 这三类 canonical names；协议、读写方式、文件、持久化介质、module、page、flow、model、decision 等非 C1/C2 信息放在边标签、图后 2-5 条 bullet 短说明或继续阅读中。Runtime Topology 必须画图；如果信息不足或部分关系不能稳定表达，图中只画已确认的 C1/C2 节点和关系，并在图后说明问题，不通过省略图来规避。

## 继续阅读

- 关键流程：...
- 页面与入口：...
- 模块边界：...
- 核心模型：...
- 设计决策：...
```

这个结构可以略呆板一些，以减少 Skill 写作和人工 review 的判断分叉；但不要为了凑模板保留没有实际内容的空小节。C1 说明系统上下文节点：本系统、外部角色，以及和系统边界高度相关的外部系统或平台；`标准角色索引（Canonical Roles）` 和 `标准外部系统索引（Canonical External Systems）` 默认归入 C1。C2 说明主要运行单元；`标准运行单元索引（Canonical Main Runtime Units）` 默认归入 C2。角色只收外部行为主体，不收主要运行单元；本系统可以作为 activity subject，但不写进 Canonical Roles；不要把 C1 本身当成实体。

## 写作判定规则：C1/C2

本节是 Skill 写作判定规则，不是 `wiki/01-system.md` 的输出小节。不要在目标 wiki 中生成 `C1/C2 判定表` 或类似元信息。

C1 external system 的硬条件是目标系统边界外的独立系统、平台、服务或组织系统，并且和目标系统存在运行时交互、数据交换、调用关系或明确依赖边界。外部来源不等于外部系统；library、SDK、runtime framework 和 protocol 默认不是 C1 external system。

C2 的硬条件是独立运行时/独立进程边界。两个 C2 之间的数据交换必须跨进程或跨运行时边界，不能依赖共享内存。不能满足这个条件的概念默认不是 `Canonical Main Runtime Unit`。

| 候选概念 | 通常处理方式 | 不要直接写成 | 进入 C1/C2 的条件或处理 |
| --- | --- | --- | --- |
| runtime framework or library | evidence、dependency note 或实现说明 | C1 external system、C2 main runtime unit | 只有它本身是系统边界外的托管平台或独立服务，并和本系统跨边界交互时，才可能是 C1 external system |
| H5 frontend running in browser | C2 main runtime unit | 普通页面说明或内部组件 | 它运行在浏览器 JavaScript runtime 中，和后端跨运行时通信，不共享内存 |
| formal CLI entry | C2 main runtime unit | 临时脚本、开发辅助命令 | 它是目标系统正式或常规使用入口，并作为独立命令进程运行 |
| backend service, worker, or job | C2 main runtime unit | module、helper、接口集合 | 它是目标系统正式运行面的一部分，以独立服务、worker、scheduled job、queue worker 或 batch job 进程运行，并承载稳定运行职责 |
| migration script, debug script, or local helper command | evidence 或 implementation detail | C2 main runtime unit | 只有目标 wiki 明确要解释它作为系统正式运行面的组成部分时，才可考虑进入 C2；临时维护和开发辅助默认不进入 C2 |
| Web API, route, or controller layer | public surface | C2 main runtime unit | 只有项目把它作为独立启动、部署和命名的 API 服务进程时才可进入 C2；此时名称应表达运行单元而不是接口集合 |
| Skill, Tool, plugin, or adapter | module detail、public surface 或 evidence | C2 main runtime unit | 只有它是本系统边界内独立 MCP server、worker 或服务进程时才可进入 C2；第三方托管 tool service 属于 C1 external system |
| data store | implementation detail、C2 data service 或 C1 external system | C2 main runtime unit | 只有它属于目标系统边界内，并且是独立运行的数据服务进程时才可进入 C2；边界外托管数据服务属于 C1 external system |
| SQLite file, local file, embedded library, or in-process store | evidence、persistence note 或 implementation detail | C1 external system、C2 main runtime unit | 无例外；如果没有独立运行时/独立进程边界，不进入 C2 |
| package, helper, runtime object, or in-process store | module detail 或 evidence | C2 main runtime unit | 无例外；共享宿主进程内存或运行上下文的内部对象不进入 C2 |
| domain model, state model, DTO, entity, or database table | model detail 或 evidence | C2 main runtime unit | 无例外；模型、状态、DTO、entity 和表不是运行时进程边界，只有承载它们的独立服务进程才可能进入 C2 |
| flow, scenario, or activity path | Flow Catalog content | C2 main runtime unit、Runtime Topology node | 无例外；flow 是跨角色、页面、运行单元、模块或模型的行为路径，不是独立运行时 |
| decision, tradeoff, or architecture rationale | Decision Map content | C1 external system、C2 main runtime unit、Runtime Topology node | 无例外；decision 解释当前取舍和约束，可能影响边界命名，但不是系统边界节点或运行节点 |

如果某个概念必须先通过 slash、or、`或` 等混名写法才能进入 canonical table，说明 stable name 尚未确认，应报告风险或询问用户，不要写成 canonical name。

不同 canonical indexes 可以共享自然领域词根，但不要为不同概念使用完全相同的 canonical name。C2 名称要表达独立运行边界，其他 index 名称也要表达各自概念类型；如果只能用同一个名字，应报告命名和边界风险，而不是同时写入多个 index。

同一个 canonical name 只归一个 owner index。`wiki/01-system.md` 可以引用其他 index 的 canonical names，但不要把 flow、page、module、model 或 decision 的 canonical entry 复制进 C1/C2 表；如果一个名称看起来需要双归属，先确认 owner index 和概念边界。

## 应该帮助读者回答

- 这个系统解决什么问题。
- 主要用户、外部系统或外部平台是谁。
- C1 系统上下文里的外部角色是谁，哪些名称需要作为 Canonical Roles 复用。
- C1 系统上下文里哪些外部系统或平台和本 repo 边界高度相关。
- 本系统负责什么，不负责什么。
- 主要入口、出口和交互方向是什么。
- 系统由哪些主要运行单元组成。
- C2 里的哪些名称需要作为 Canonical Main Runtime Units 复用。
- 稳定入口如何把主要运行单元、外部依赖和持久化读写关系连起来。
- 读者接下来应该查看哪些 flow、page、module 或 model 页面。
- `继续阅读` 是否按关键流程、页面与入口、模块边界、核心模型、设计决策的顺序路由读者。

## 适合写

### 读者入口与页面结构

- 系统目标和当前状态。
- 系统责任边界。
- 关键入口、协议或外部依赖。
- 多个稳定入口可以先放在一张拓扑图里；只有一张图读不清真实运行差异时才拆分。
- `继续阅读` 使用固定顺序：关键流程、页面与入口、模块边界、核心模型、设计决策；没有实际关联的项可以省略。

### C1 / C2 canonical tables

- 外部参与方与外部系统。
- C1 下的标准角色索引。
- C1 下的标准外部系统索引。
- 外部上下文节点较多、或关系方向只靠表格不直观时的 C1 context Mermaid 图。
- 主要运行单元和大粒度协作关系。
- C2 下的标准运行单元索引。
- 三张 canonical 表的 `标准名称` 列使用读者可见稳定名；代码类名、文件名、接口名默认放在 `证据`，除非它本身就是系统实际识别的名称。
- 三张 canonical 表的 `标准名称` 列必须是单一稳定名称；不要用 `A / B`、`A or B`、`A 或 B` 或类似混名写法承接多个候选名、别名或不同概念。
- `Canonical Main Runtime Units` 中的名称不要和其他 canonical indexes 中的不同概念完全重名；可以共享自然领域词根，但要用名称或边界说明区分概念类型。
- 同一个 canonical name 只维护在一个 owner index；`wiki/01-system.md` 引用其它 index 名称时，不把它复制成 C1/C2 canonical entry。
- C1 external system 的 canonical name 指向系统边界外实际交互的独立服务、平台或组织系统；SDK、client、adapter、protocol 只作为 evidence 或交互说明，不占 canonical name。
- C1 external system 可以使用 `LLM Provider`、`Payment Provider` 等泛化稳定名，但只能在系统确实抽象支持多个 provider、用户确认不绑定具体厂商、或泛化名比厂商名更适合读者理解边界时使用；不能用泛化名遮蔽不确定性。
- 如果证据只能证明代码里存在 SDK、client 或 adapter，不能确认外部服务边界，`wiki-doctor` 应报告 `meaning_loss_risk` 并避免改 canonical external system；`wiki-drift-radar` 可记录为待确认候选；`wiki-sink` 需要用户确认或更强证据后才能写入。
- Data store 是否进入 C2 取决于它是否属于目标系统边界内且有独立运行时/进程边界；边界外托管数据库或数据平台属于 C1 external system，本地文件和 embedded library 不属于 C1/C2。
- 三张 canonical 表的 `类型与边界` 列用一句短语或短句说明类型和边界，不使用枚举标签堆，也不写成长段落。
- 外部系统表的 `交互方向` 列使用方向短语，例如 `本系统 -> 外部系统：查询候选`、`外部系统 -> 本系统：回调结果` 或 `双向：认证 / 数据同步`。
- 运行单元表的 `主要协作对象` 列使用 C1/C2 canonical 名称列表加简短关系，说明这个运行单元主要和谁协作。

### Runtime Topology

- 稳定入口和被说明运行范围的运行拓扑；默认用 Mermaid `flowchart` 表达 C1/C2 canonical names 之间的运行连接关系。
- Runtime Topology 图后的 2-5 条 bullet 短说明，用于解释入口、跨运行时交互路径、持久化读写关系、协议或外部依赖边界。
- 初始化骨架可以用 `TBD` Mermaid 占位图；稳定成文后必须替换为真实 Runtime Topology 图，不能保留占位图。
- 信息不足以完整稳定描述 Runtime Topology 时，不猜关系、不保留 `TBD`、不省略图；先画已确认的 C1/C2 canonical 节点和关系，再在图后说明缺口、问题或待确认事项，并交给用户确认、wiki-sink 后续补充，或由 wiki-drift-radar 记录 Coverage Gap。
- Runtime Topology 的边只画 confirmed runtime interaction。节点已确认但关系不清时，可以保留节点、不硬连边，并在图后说明关系缺口或待确认问题。
- Runtime Topology 不要求覆盖 C1/C2 表的全部条目，只覆盖被说明运行范围内相关的 C1/C2 canonical nodes。主 C2 运行单元如果未出现在图中，图后说明它为什么不在当前运行范围；C1 roles 和 external systems 按当前运行关系需要入图。
- Runtime Topology 中的 role 节点只用于表达用户或外部角色如何进入或触发运行链路；不参与当前运行链路的 role 留在 Canonical Roles 表或 C1 context 图中。
- C1 context 图不强制；只有外部角色或外部系统较多，或仅靠表格不够直观时才画。Runtime Topology 必须画 Mermaid `flowchart`，但不能为了补全画面而发明非 C1/C2 节点或未确认关系。
- Runtime Topology 图中每个实体节点都必须复用 C1 roles、C1 external systems 和 C2 main runtime units 这三类 canonical 名称；不得为持久化介质、协议、文件、配置、基础设施细节、module、page、flow、model 或 decision 另造 topology-local node。
- Runtime Topology 默认不把“本系统”画成节点；C1 context 图可以用本系统节点，activity map 可以在确实系统发起时用本系统 subject，但运行拓扑应展开为 C2 main runtime units。
- 如果 Runtime Topology 图确实需要一个尚未进入 C1/C2 canonical indexes 的实体，先补齐或确认对应 canonical index；不能在图里临时写新节点。

### Public Surface 与非 C2 概念

- 当读者需要比较系统级 APIs、tools、routes、page entries、events 或 capabilities 时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- Public Surface 是系统、module、page 或 C2 对外暴露的稳定交互点，不是运行单元本身；API route、tool call、event、page entry、command option 等默认不进入 C2。
- CLI 应用作为正式入口并以独立命令进程运行时可以进入 C2；具体 subcommand、flag、参数或一次动作默认是 Public Surface，不是新的 C2。
- Page 属于用户可见页面、入口和导航结构，不进入 C2；page route 属于 Public Surface 或 page entry，组件树属于 implementation detail，只有承载页面的独立 frontend app/runtime unit 才可能进入 C2。
- Model 属于系统理解模型、状态、关系或事实源，不进入 C2；DTO、entity class、database table 和 model object 只作为 model detail 或 evidence，只有承载模型读写、计算或同步的独立服务进程才可能进入 C2。
- Flow 属于跨角色、页面、运行单元、模块或模型的行为路径，不进入 C2，也不作为 Runtime Topology 节点；flow 可以引用 C1/C2 canonical names 作为 subject 或 participant。
- Decision 属于当前取舍、约束和 rationale，不进入 C1/C2，也不作为 Runtime Topology 节点；decision 可以解释为什么某个边界或命名存在。

### Evidence

- 支撑这些判断的代码锚点或文件证据。
- C2 evidence 优先指向能证明独立运行时/进程边界的启动入口、CLI entry、server main、worker entry、job config、deployment config、package script 或 README usage；证据不足时不要猜 C2。
- C1 evidence 优先证明外部服务、平台或组织系统边界，例如 endpoint、provider config、外部依赖说明、contract、mock、integration test 或调用文档；SDK、adapter、client 文件只能作为辅助证据。
- 三张 canonical 表的 `证据` 列使用短 Evidence Anchor。

### 旧文档迁移

- `wiki-doctor` 刷新旧版 `01-system.md` 时，可以默认迁移到 C1 / C2 / Runtime Topology 结构，但只限无损保留现有信息、命名、边界、证据和不确定性的 `safe_guidance_rewrite`。
- `wiki-doctor` 发现旧文档把 Web API、Skills、Store、tool、page、model、flow 或内部组件误列为 C2 时，不要直接删除；能无损重分类时移到 Public Surface、module detail、model detail、evidence 或图后说明，不能判断去向时报告 `meaning_loss_risk`。

## 避免写

### 粒度越界

- C3 组件内部结构。
- 类、函数、SQL 或字段全集。
- 详细业务流程步骤。
- 请求级时序细节。
- 完整模块职责说明。
- 页面布局或前端组件细节。
- 完整基础设施清单或环境配置清单。

### Canonical naming 与 evidence

- 把 `证据` 列写成长分析或源码路径全集。
- 把代码类名、文件名或接口名直接当作 canonical `标准名称`。
- 把 canonical `标准名称` 写成 slash/or/或 拼接的候选名或混合概念。
- 让不同 canonical indexes 中的不同概念使用完全相同的 canonical name。
- 把同一个 canonical name 复制到多个 owner indexes。
- 把 SDK、client、adapter 或 protocol 名称当作 C1 external system 的 canonical name。
- 用泛化 external-system 名称遮蔽尚未确认的具体外部边界。
- 只因为数据存储是独立服务进程就写入 C2，而没有判断它是否属于目标系统边界内。
- 把 `类型与边界` 写成标签堆或完整段落。
- 把 `交互方向` 写成完整流程、接口字段清单或调用细节。
- 把 `主要协作对象` 写成 package/class 依赖、完整调用链或 Runtime Topology 替代品。

### Runtime Topology

- 把 Runtime Topology 写成请求时序图。
- 把 Runtime Topology 图后的短说明扩展成第二张索引表。
- 在 Runtime Topology 图里新增没有进入 C1/C2 canonical indexes 的实体节点。
- 把协议、文件、持久化介质、配置或基础设施细节画成 topology-local entity node；这些信息应放在边标签或图后短说明。
- 把 module、page、flow、model 或 decision 画成 Runtime Topology entity node；它们应通过图后说明、相关页面或继续阅读路由出现。
- 在 Runtime Topology 里用“本系统”节点包住 C2 main runtime units，导致系统边界和运行边界混在一起。
- 绕过 canonical index，直接在 Runtime Topology 图里临时命名新实体。
- 完整模块职责说明。
- 页面布局或前端组件细节。
- 完整基础设施清单或环境配置清单。
- 因固定偏好排除真实存在的稳定入口。
- Runtime Topology 图重新发明已经在 canonical indexes 里存在的名称，或为非 C1/C2 概念另造节点。
- 为了凑模板保留没有实际内容的空小节。
- 把 C1 或 C2 开头说明写成长篇解释。
- 为了模板完整性强行添加没有信息增益的 C1 context 图。
- 稳定页面保留 `TBD` 占位图或占位说明。
- 信息不足时编造看似完整的 Runtime Topology 图，或用省略图来回避应说明的问题。
- 为了让 Runtime Topology 连成完整图而硬画未确认的边。
- 为了覆盖全集而把当前运行范围无关的 C1/C2 节点塞进 Runtime Topology。
- 把不参与当前运行链路的 roles 塞进 Runtime Topology，导致它退化成 C1 context 图。

### Public Surface 与非 C2 概念

- 把 public surface 写成 controller、helper、组件、文件树或完整接口字段索引；这些只作为 secondary code evidence。
- 把 API route、tool call、event、page entry 或 command option 这类 public surface 直接写成 C2 main runtime unit。
- 把 CLI subcommand、flag 或参数当成独立 C2 main runtime unit。
- 把 page、page route 或前端组件树写成 C2 main runtime unit。
- 把 domain model、state model、DTO、entity class 或 database table 写成 C2 main runtime unit。
- 把 flow、scenario 或 activity path 写成 C2 main runtime unit 或 Runtime Topology node。
- 把 decision、tradeoff 或 architecture rationale 写成 C1/C2 节点或 Runtime Topology node。

### 迁移与导航

- 为了套用新结构而丢失旧 `01-system.md` 里的唯一信息、证据或不确定性。
- 为了清理 C1/C2 表而删除旧文档里的唯一信息；应先无损重分类，无法重分类则报告风险。
- 自由改写 `继续阅读` 的顺序，导致系统总览和 wiki 阅读顺序不一致。

## LLM 语义检查问题

- 读者能否只看本页就知道系统和外部世界的边界？
- 页面是否默认使用固定小节标题 `C1：系统上下文（System Context）`、`C2：主要运行单元（Container）`、`运行拓扑（Runtime Topology）`，除非这样会产生空话或重复内容？
- 每个小节是否使用默认 block：边界说明、索引表、Runtime Topology Mermaid flowchart、短说明和继续阅读？
- C1 和 C2 的开头说明是否控制在 1-3 句，把细节留给表格、图和后续页面？
- C1 context 图是否只在外部上下文节点较多或关系方向不直观时出现，而不是强制样板？
- 三张 canonical 表是否使用固定中文列名，并且没有强制保留重复的 `Owner 页面` 列？
- 三张 canonical 表的 `标准名称` 是否是读者可见稳定名，而不是实现符号？
- 三张 canonical 表的 `标准名称` 是否是单一稳定名称，没有用 slash/or/或 拼接候选名、别名或不同概念？
- C2 main runtime unit 名称是否避免和其他 canonical indexes 中的不同概念完全重名，并能表达运行边界？
- 同一个 canonical name 是否只归一个 owner index，其他位置只是引用而不是复制？
- 三张 canonical 表的 `类型与边界` 是否用短语或短句同时说明类型和边界，而不是标签堆或长段落？
- 外部系统表的 `交互方向` 是否是方向短语，而不是完整流程或接口细节？
- 运行单元表的 `主要协作对象` 是否复用 C1/C2 canonical 名称并说明简短关系，而不是 package/class 依赖或完整调用链？
- 三张 canonical 表的 `证据` 列是否是短 Evidence Anchor，而不是长解释或源码路径全集？
- `标准角色索引（Canonical Roles）` 是否归入 C1，并且只收录外部行为主体而不是主要运行单元？
- 本系统是否只在确实需要表达系统发起活动时作为 subject 使用，而没有被写进 Canonical Roles？
- `标准外部系统索引（Canonical External Systems）` 是否归入 C1，并只收录和系统边界高度相关的外部系统或平台？
- C1 external system 的 canonical name 是否指向真实外部服务、平台或组织系统，而不是 SDK、client、adapter 或 protocol？
- 泛化 external-system 名称是否有抽象层、用户确认或读者边界理由支撑，而不是用来遮蔽不确定性？
- Data store 是否同时满足目标系统边界内和独立运行时/进程边界两个条件，才被写入 C2？
- C2 evidence 是否优先证明独立运行时/进程边界；证据不足时是否避免猜测 C2？
- C1 evidence 是否优先证明外部服务、平台或组织系统边界，而不是只给 SDK、adapter 或 client 文件？
- `标准运行单元索引（Canonical Main Runtime Units）` 是否归入 C2，并作为后续 Runtime Topology、flow、page、module、model 复用的运行单元命名来源？
- 本页是否停留在 C4 C1（System Context，系统上下文）、C2（Container，容器/主要运行单元）和轻量 Runtime Topology（运行拓扑）粒度，没有下钻到组件或代码层？
- 首次出现 C2 时是否展开为 `Container`，后文是否优先使用“主要运行单元”而不是容易误读的“容器”？
- Runtime Topology 是否默认使用 Mermaid `flowchart` 表达 C1/C2 canonical names 之间的真实稳定入口和运行连接关系，而不是复写请求时序或模块细节？
- 稳定页面中是否已经替换初始化骨架里的 `TBD` Mermaid 占位图？
- 信息不足时是否仍画出已确认的 Runtime Topology，并把缺口留给确认、后续写入或 drift/radar 处理，而不是猜关系或省略图？
- Runtime Topology 是否只画 confirmed edges；节点已确认但关系不清时，是否在图后说明而不是硬连？
- Runtime Topology 是否覆盖当前运行范围，而不是强行画全集；主 C2 缺席时是否说明原因？
- Runtime Topology 中的 role 节点是否只表达进入或触发运行链路的外部角色？
- 从旧结构迁移时是否属于无损 `safe_guidance_rewrite`；如果需要判断现状或改变含义，是否停在风险报告？
- 旧文档中错放到 C1/C2 的信息是否被无损重分类或报告风险，而不是直接删除？
- Runtime Topology 图后的说明是否是 2-5 条有信息量的 bullet，而不是第二张索引表？
- Runtime Topology 图节点是否 100% 复用 `Canonical Roles`、`Canonical External Systems` 和 `Canonical Main Runtime Units` 中的名称，没有新增 topology-local entity node，也没有把 module、page、flow、model 或 decision 画成节点？
- Runtime Topology 是否展开到 C2 main runtime units，而不是用“本系统”节点代替内部运行边界？
- 如果图中需要新实体，是否先维护或确认了对应 C1/C2 canonical index，而不是直接在图里命名？
- 多入口拓扑是否仍然清楚；如果拆图，是否因为真实运行差异而不是入口偏好？
- 每个外部交互是否说明了方向和关系？
- 系统级 public surfaces 是否只列 stable interaction points，并把实现细节留作 secondary code evidence？
- Public Surface 是否作为交互点解释，而没有被直接升格成 C2 main runtime unit？
- CLI 是否按应用进程和具体命令面分层：CLI 应用可为 C2，subcommand、flag 和参数属于 Public Surface？
- Page 是否停留在 Page Catalog 或 Public Surface 层，没有被写成 C2；只有承载页面的独立 frontend runtime unit 才进入 C2？
- Model 是否停留在 Model Catalog 或 evidence 层，没有因为核心或重要就被写成 C2？
- Flow 是否停留在 Flow Catalog 层，并只引用 C1/C2 作为主体或参与方，而没有被写成 C2 或 Runtime Topology 节点？
- Decision 是否停留在 Decision Map 或 rationale 层，没有被写成 C1/C2 或 Runtime Topology 节点？
- 责任边界是否同时说明了负责和不负责的部分？
- 是否给出了继续阅读的入口，而不是把所有细节塞在本页？
- `继续阅读` 是否按固定顺序呈现，并省略没有实际关联的项？
