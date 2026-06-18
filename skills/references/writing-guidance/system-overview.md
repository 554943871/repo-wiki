# System Overview Guidance

本文件是 `wiki/01-system.md` 的唯一详细写作规范来源。`wiki-structure.md` 只提供可初始化的最小骨架，`wiki-suite-design.md` 只记录 suite 级设计定位。

`wiki/01-system.md` 帮助读者快速理解系统是什么、服务谁、边界在哪里、主要运行单元如何协作，以及被说明的运行范围在运行上如何连起来。

默认结构使用固定小节标题：

```md
## C1：系统上下文（System Context）

1-3 句系统边界说明。外部上下文节点较多、或关系方向只靠表格不直观时，可以补一张 C1 context Mermaid 图；简单系统不要为了模板强行画图。

### 标准角色索引（Canonical Roles）

| 标准名称 | 类型 / 边界 | 证据 |
| --- | --- | --- |

### 标准外部系统索引（Canonical External Systems）

| 标准名称 | 类型 / 边界 | 交互方向 | 证据 |
| --- | --- | --- | --- |

## C2：主要运行单元（Container）

1-3 句主要运行单元说明。

### 标准运行单元索引（Canonical Main Runtime Units）

| 标准名称 | 类型 / 边界 | 主要协作对象 | 证据 |
| --- | --- | --- | --- |

## Deployment：部署/运行拓扑（Runtime Topology）

Mermaid `flowchart`，图后保留 2-5 条 bullet 短说明，解释入口、共享路径、持久化点或外部依赖边界。

## 继续阅读

- 关键流程：...
- 页面与入口：...
- 模块边界：...
- 核心模型：...
- 设计决策：...
```

这个结构可以略呆板一些，以减少 Skill 写作和人工 review 的判断分叉；但不要为了凑模板保留没有实际内容的空小节。C1 说明系统上下文节点：本系统、外部角色，以及和系统边界高度相关的外部系统或平台；`标准角色索引（Canonical Roles）` 和 `标准外部系统索引（Canonical External Systems）` 默认归入 C1。C2 说明主要运行单元；`标准运行单元索引（Canonical Main Runtime Units）` 默认归入 C2。角色只收外部行为主体，不收主要运行单元；不要把 C1 本身当成实体。

## 应该帮助读者回答

- 这个系统解决什么问题。
- 主要用户、外部系统或外部平台是谁。
- C1 系统上下文里的外部角色是谁，哪些名称需要作为 Canonical Roles 复用。
- C1 系统上下文里哪些外部系统或平台和本 repo 边界高度相关。
- 本系统负责什么，不负责什么。
- 主要入口、出口和交互方向是什么。
- 系统由哪些主要运行单元组成。
- C2 里的哪些名称需要作为 Canonical Main Runtime Units 复用。
- 稳定入口如何把主要运行单元、持久化点和外部依赖连起来。
- 读者接下来应该查看哪些 flow、page、module 或 model 页面。
- `继续阅读` 是否按关键流程、页面与入口、模块边界、核心模型、设计决策的顺序路由读者。

## 适合写

- 系统目标和当前状态。
- 外部参与方与外部系统。
- C1 下的标准角色索引。
- C1 下的标准外部系统索引。
- 外部上下文节点较多、或关系方向只靠表格不直观时的 C1 context Mermaid 图。
- 系统责任边界。
- 主要运行单元和大粒度协作关系。
- C2 下的标准运行单元索引。
- 稳定入口和被说明运行范围的轻量部署/运行拓扑；默认用 Mermaid `flowchart` 表达连接关系。
- Deployment 图后的 2-5 条 bullet 短说明，用于解释入口、共享路径、持久化点或外部依赖边界。
- 初始化骨架可以用 `TBD` Mermaid 占位图；稳定成文后必须替换为真实拓扑或明确省略原因。
- 信息不足以稳定描述 Deployment / Runtime Topology 时，不猜图、不保留 `TBD`；写明不足以稳定描述，并交给用户确认、wiki-sink 后续补充，或由 wiki-drift-radar 记录 Coverage Gap。
- `wiki-doctor` 刷新旧版 `01-system.md` 时，可以默认迁移到 C1 / C2 / Deployment 结构，但只限无损保留现有信息、命名、边界、证据和不确定性的 `safe_guidance_rewrite`。
- Deployment 图节点优先复用 C1/C2 的 canonical 名称；支撑性持久化点或基础设施节点需要明确其边界。
- 多个稳定入口可以先放在一张拓扑图里；只有一张图读不清真实运行差异时才拆分。
- 关键入口、协议或外部依赖。
- 当读者需要比较系统级 APIs、tools、routes、page entries、events 或 capabilities 时，使用 Public Surface table 说明 stable interaction points、使用者、稳定行为和 owner boundary。
- 支撑这些判断的代码锚点或文件证据。
- 三张 canonical 表的 `证据` 列使用短 Evidence Anchor。
- 三张 canonical 表的 `标准名称` 列使用读者可见稳定名；代码类名、文件名、接口名默认放在 `证据`，除非它本身就是系统实际识别的名称。
- 三张 canonical 表的 `类型 / 边界` 列用一句短语或短句说明类型和边界，不使用枚举标签堆，也不写成长段落。
- 外部系统表的 `交互方向` 列使用方向短语，例如 `本系统 -> 外部系统：查询候选`、`外部系统 -> 本系统：回调结果` 或 `双向：认证 / 数据同步`。
- 运行单元表的 `主要协作对象` 列使用 C1/C2 canonical 名称列表加简短关系，说明这个运行单元主要和谁协作。
- `继续阅读` 使用固定顺序：关键流程、页面与入口、模块边界、核心模型、设计决策；没有实际关联的项可以省略。

## 避免写

- C3 组件内部结构。
- 类、函数、SQL 或字段全集。
- 把 `证据` 列写成长分析或源码路径全集。
- 把代码类名、文件名或接口名直接当作 canonical `标准名称`。
- 把 `类型 / 边界` 写成标签堆或完整段落。
- 把 `交互方向` 写成完整流程、接口字段清单或调用细节。
- 把 `主要协作对象` 写成 package/class 依赖、完整调用链或 deployment 拓扑替代品。
- 详细业务流程步骤。
- 请求级时序细节。
- 把 Deployment 写成请求时序图。
- 把 Deployment 图后的短说明扩展成第二张索引表。
- 完整模块职责说明。
- 页面布局或前端组件细节。
- 完整基础设施清单或环境配置清单。
- 因固定偏好排除真实存在的稳定入口。
- Deployment 图重新发明已经在 canonical indexes 里存在的名称。
- 为了凑模板保留没有实际内容的空小节。
- 把 C1 或 C2 开头说明写成长篇解释。
- 为了模板完整性强行添加没有信息增益的 C1 context 图。
- 稳定页面保留 `TBD` 占位图或占位说明。
- 信息不足时编造看似完整的 Deployment 图。
- 为了套用新结构而丢失旧 `01-system.md` 里的唯一信息、证据或不确定性。
- 自由改写 `继续阅读` 的顺序，导致系统总览和 wiki 阅读顺序不一致。
- 把 public surface 写成 controller、helper、组件、文件树或完整接口字段索引；这些只作为 secondary code evidence。

## LLM 语义检查问题

- 读者能否只看本页就知道系统和外部世界的边界？
- 页面是否默认使用固定小节标题 `C1：系统上下文（System Context）`、`C2：主要运行单元（Container）`、`Deployment：部署/运行拓扑（Runtime Topology）`，除非这样会产生空话或重复内容？
- 每个小节是否使用默认 block：边界说明、索引表、Deployment Mermaid flowchart、短说明和继续阅读？
- C1 和 C2 的开头说明是否控制在 1-3 句，把细节留给表格、图和后续页面？
- C1 context 图是否只在外部上下文节点较多或关系方向不直观时出现，而不是强制样板？
- 三张 canonical 表是否使用固定中文列名，并且没有强制保留重复的 `Owner 页面` 列？
- 三张 canonical 表的 `标准名称` 是否是读者可见稳定名，而不是实现符号？
- 三张 canonical 表的 `类型 / 边界` 是否用短语或短句同时说明类型和边界，而不是标签堆或长段落？
- 外部系统表的 `交互方向` 是否是方向短语，而不是完整流程或接口细节？
- 运行单元表的 `主要协作对象` 是否复用 C1/C2 canonical 名称并说明简短关系，而不是 package/class 依赖或完整调用链？
- 三张 canonical 表的 `证据` 列是否是短 Evidence Anchor，而不是长解释或源码路径全集？
- `标准角色索引（Canonical Roles）` 是否归入 C1，并且只收录外部行为主体而不是主要运行单元？
- `标准外部系统索引（Canonical External Systems）` 是否归入 C1，并只收录和系统边界高度相关的外部系统或平台？
- `标准运行单元索引（Canonical Main Runtime Units）` 是否归入 C2，并作为后续 deployment、flow、page、module、model 复用的运行单元命名来源？
- 本页是否停留在 C4 C1（System Context，系统上下文）、C2（Container，容器/主要运行单元）和轻量 Deployment / Runtime Topology（部署/运行拓扑）粒度，没有下钻到组件或代码层？
- 首次出现 C2 时是否展开为 `Container`，后文是否优先使用“主要运行单元”而不是容易误读的“容器”？
- Deployment / Runtime Topology 是否默认使用 Mermaid `flowchart` 表达被选运行范围内的真实稳定入口和运行连接关系，而不是复写请求时序或模块细节？
- 稳定页面中是否已经替换初始化骨架里的 `TBD` Mermaid 占位图？
- 信息不足时是否避免猜图，并把缺口留给确认、后续写入或 drift/radar 处理？
- 从旧结构迁移时是否属于无损 `safe_guidance_rewrite`；如果需要判断现状或改变含义，是否停在风险报告？
- Deployment 图后的说明是否是 2-5 条有信息量的 bullet，而不是第二张索引表？
- Deployment 图节点是否优先复用 `Canonical Roles`、`Canonical External Systems` 和 `Canonical Main Runtime Units` 中的名称？
- 多入口拓扑是否仍然清楚；如果拆图，是否因为真实运行差异而不是入口偏好？
- 每个外部交互是否说明了方向和关系？
- 系统级 public surfaces 是否只列 stable interaction points，并把实现细节留作 secondary code evidence？
- 责任边界是否同时说明了负责和不负责的部分？
- 是否给出了继续阅读的入口，而不是把所有细节塞在本页？
- `继续阅读` 是否按固定顺序呈现，并省略没有实际关联的项？
