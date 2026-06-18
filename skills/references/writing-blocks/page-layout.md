# Page Layout Block

用于解释用户可见页面或页面局部的稳定空间结构：页面区域、主要组件、弹窗、抽屉、tab、占位区、操作区、覆盖层，以及这些元素在不同业务条件下如何组合。

Page layout 只回答“用户在这个页面看到哪些稳定区域，它们如何排列，哪些条件会改变页面形态”。它不是 DOM 树、CSS 还原图、组件库用法、真实截图归档或后端调用链。

## 适合使用时机

- 页面有多个稳定区域、组件、弹窗、抽屉、tab、固定区或占位区。
- 页面存在业务可见的多态，例如登录 / 未登录、空列表 / 有数据、审核中 / 已通过、可编辑 / 只读。
- 读者需要知道哪些页面区域承接哪些 flow、module、model、public surface 或用户动作。
- 页面状态、可操作项或出口路由随页面形态变化。
- 单纯用 prose 或导航表会丢失区域层级、覆盖关系、并列 / 堆叠关系或下钻边界。

## 推荐表达

空间关系重要时，优先使用轻量 SVG、线框图或等价图形表达页面布局；如果当前环境不适合产出图形，可以先用区域表保存稳定事实和不确定性。图形用于表达布局，不用于还原视觉稿。

```md
| Region / component | Visible when | Role on page | Key actions | Drill-down / evidence |
| --- | --- | --- | --- | --- |
| Header | Always | Shows order title and return entry | Back to order list | route config |
| Payment banner | Payment pending | Explains pending payment state | Continue payment | payment status model |
| Support drawer | Risk flagged | Lets Support Agent review exception | Approve / reject | support workflow |
```

## 写作要求

- 使用 canonical page names、已确认的 stable component / region names，或当前页面先声明且有证据支撑的局部名称。
- 表达相邻层级即可：页面 -> 区域 / 组件 -> 直接子区域。更深层细节写成“下钻到 X”，不要在一张图里展开完整组件树。
- 标明 visible conditions：哪些业务条件、权限、状态、入口或数据结果让某个区域出现、隐藏、禁用或替换。
- 标明 page variants：当页面形态变化会影响区域组合、可操作项、出口路由或页面级交互时，说明变化条件和可见差异。
- 标明 page-level actions：只写用户可感知动作和页面级结果；组件内部事件链、hook、handler 和方法名只作为 evidence anchors。
- 保留 evidence anchors：路由、页面文件、测试、产品材料、截图标注、设计稿或用户确认都可以作为证据，但证据应短而可追溯。
- 如果使用 SVG / 线框图，图中标签应清楚、文字不溢出、不遮挡区域边界；这只是可读性检查，不是机械正确性证明。

## 与其他 Blocks 的关系

- Page Navigation Block 解释页面之间怎么跳转；Page Layout Block 解释单个页面或局部页面里看得见的区域如何组织。
- Activity Map 解释业务主链路；Page Layout 只解释页面如何承接该链路的可见部分。
- Sequence Block 解释跨参与方或跨组件的交互顺序；Page Layout 不表达事件回调链或后端调用链。
- State Transition Block 解释核心对象或流程状态如何变化；Page Layout 只说明状态如何投射为可见区域、禁用态、空态或异常态。
- Public Surface table 解释页面入口、route、action、event 或 exposed capability 的稳定行为；Page Layout 可以引用这些 surface，但不替代其 owner boundary。

## 避免

- 把 DOM 树、React component tree、CSS box model 或组件库 API 当成 page layout。
- 为了显得完整而列出所有低价值组件、字段、按钮和样式 token。
- 用真实截图、视觉稿还原或装饰图替代稳定区域和布局层级说明。
- 把页面跳转、业务流程、后端调用链、接口字段全集或组件内部事件链画进 layout。
- 在一张图里展开超过页面、区域 / 组件、直接子区域三层的结构。
- 把没有证据的区域名、组件名或页面形态写成 canonical fact。
