# Page Navigation Block

用于解释页面之间的用户可见入口、跳转关系、返回路径，以及 README / catalog 页面如何按读者问题或任务路由。

## 适合使用时机

- 一个页面有多个入口或出口。
- 用户路径需要跨多个页面理解。
- 页面跳转容易被误写成后端调用链或内部组件交互。
- README 或 catalog 页面需要帮读者选择下一页，而不只是列出文件名。
- 读者常见问题可以对应到不同 flow、page、module、model 或 decision 页面。

## 推荐表达

页面之间的跳转优先使用 Mermaid `flowchart` 或简洁导航表。

```md
| From page | User-visible action | To page | Return or next step | Evidence |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |
```

README / catalog 页面优先使用按 question 或 task 路由的表格。

```md
| Reader question or task | Start here | Then read | Use when | Evidence anchor |
| --- | --- | --- | --- | --- |
| Where does checkout start? | `02-flows/checkout.md` | `03-pages/cart.md` | Reader needs user path first | Route config in `src/routes/cart.ts` |
| Who owns pricing behavior? | `04-modules/pricing.md` | `06-decisions.md#pricing-owner` | Reader is checking ownership or tradeoff | Module boundary note in existing wiki |
```

## 写作要求

- 每条边说明用户可见动作或入口。
- 区分页面跳转、页面内部状态变化和后端调用。
- 路由参数只在影响读者理解目标页面时写。
- 入口、路由和目标页面要有代码、路由配置、产品材料或用户确认支撑。
- README 和 catalog 不只做文件索引，要按读者的问题、任务或下一步选择来路由。
- 每条 reader route 说明适合什么时候使用，避免读者不知道先看哪页。
- 如果某个入口、页面名或目标页只有候选证据，标出 uncertainty，不要把候选页面写成 canonical route。
- 保留 unique facts 和 evidence anchors；重排为导航表时不要删除特殊入口、权限限制、返回路径或异常跳转。

## V1 边界

- V1 不新增单独的 `reader-map` block。读者路由写在 Page Navigation Block、README / catalog guidance 和 Reader-First Structure 原则里。
- V1 不新增 `caliber-map` block。字段级重要性治理不属于本 block；只有当字段、权限或路由参数影响读者选择下一页时才简短说明。

## 示例使用条件

当 `02-flows/README.md` 已经列出多个 flow，但读者仍不知道“我要排查支付失败应该看哪里”时，用 Page Navigation Block 增加 question/task 路由：

- Question: 支付失败从哪个用户页面开始？
- Start here: 支付 flow。
- Then read: 支付结果页、退款 decision 或订单状态 model。
- Use when: 读者按用户任务排查，不是按目录浏览。
- Evidence anchor: 页面路由、已有 wiki 页面、产品材料或用户确认。

## 避免

- 把页面跳转图画成业务流程主活动图。
- 把后端接口调用画成页面跳转。
- 把组件内部交互提升成页面跳转。
- 把完整路由参数、接口字段或展示条件都塞进边标签。
- 只列文件名，不说明读者问题、任务或下一步。
