# State Transition Block

用于解释核心对象、流程或页面背后的稳定状态集合和状态变化。

## 适合使用时机

- 某个 model 有明确状态。
- 流程中存在重要终态、异常态或回退。
- 状态变化影响用户体验、业务规则或系统协作。
- 读者需要理解哪些 event 会改变状态，以及 guard 条件为什么会阻止变化。
- 当前 wiki 已经提到状态，但没有说明 terminal states 或不确定状态来源。

## 推荐表达

可以使用 Mermaid `stateDiagram-v2` 或状态表。状态少且 guard 重要时优先用表格，状态多且路径重要时使用图。

```md
| State | Event | Guard | Next state | Terminal? | Evidence or uncertainty |
| --- | --- | --- | --- | --- | --- |
| Draft | Submit | Required fields are valid | Submitted | No | `src/order/OrderState.ts` |
| Submitted | Cancel | Before fulfillment starts | Cancelled | Yes | `src/order/OrderService.ts` |
```

## 写作要求

- 列出稳定状态，而不是临时变量。
- 说明触发状态变化的 event，例如用户动作、系统回调、定时任务或人工处理。
- 说明 guard 条件，例如权限、时间窗口、前置校验、库存状态或外部系统结果。
- 说明变化后的业务结果。
- 标出终态、异常态、回退或不可逆状态。
- 终态要说明为什么不会继续流转，或者说明只能通过人工或补偿流程重新开始。
- 对证据不足的状态、event 或 guard 标出 uncertainty，不要把候选枚举写成稳定事实。
- 区分业务状态和 UI 展示状态。
- 如果 UI 展示态只是对业务状态的映射，写成 display note，不要和业务状态混在同一状态集合里。
- 状态表或图必须保留现有 unique facts、evidence anchors、限制条件和例外。

## 示例使用条件

当一个 model page 写到 `Pending`、`Approved`、`Rejected`，但代码还显示 `Expired` 是定时任务触发的终态时，可以增加 State Transition Block：

- States: `Pending`、`Approved`、`Rejected`、`Expired`。
- Events: submit review、manual approve、manual reject、expiry job。
- Guards: reviewer permission、deadline reached。
- Terminal states: `Approved`、`Rejected`、`Expired`。
- Uncertainty: 如果 `Expired` 只在历史文档出现、当前代码未验证，就保留为 uncertainty 或 candidate note。

## 避免

- 把局部布尔值写成系统状态。
- 用状态图表达服务调用顺序。
- 没有证据地推断状态枚举。
- 把 UI 展示态直接当作业务状态，除非明确说明它只是展示态。
- 把 active decision 写成已经稳定的状态规则。
