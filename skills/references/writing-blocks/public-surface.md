# Public Surface Block

用于解释系统、module 或 page 对外稳定暴露的交互点。Public surface 是读者可以依赖、比较或用来判断责任边界的 visible contract，不是代码文件、类、helper 或函数清单。

## 适合使用时机

- 读者需要比较多个稳定入口、出口或能力边界。
- 页面需要说明系统、module 或 page 如何被外部用户、外部系统、相邻 module、工具调用者或事件订阅方使用。
- APIs、tools、routes、page entries、events、commands、configured entry points 或 confirmed capabilities 能帮助解释 owner boundary。
- 单纯代码锚点不足以说明“谁能从哪里进入、能依赖什么行为、边界在哪里”。

## 推荐表达

优先使用紧凑表格。表格行应该是稳定 interaction point，而不是实现文件。

```md
| Surface | Kind | Used by | Stable capability or promise | Owner boundary | Evidence |
| --- | --- | --- | --- | --- | --- |
| ... | API / tool / route / page entry / event / capability | ... | ... | ... | ... |
```

列的含义：

- `Surface`: 读者可识别的稳定入口、出口、能力或事件名，例如 route、API operation、tool command、page entry、event topic、extension point 或 confirmed capability。
- `Kind`: 表面类型，用来跨 APIs、tools、routes、pages、events 和 capabilities 做横向比较。
- `Used by`: 使用者或调用方，可以是 human role、external system、neighboring module、page、flow 或 subscriber。
- `Stable capability or promise`: 这个 surface 对使用者稳定提供什么行为、数据、导航、触发或通知。
- `Owner boundary`: 谁拥有该 surface 的语义，明确它不代表哪些下游实现职责。
- `Evidence`: 简短证据锚点。优先给 route/config/test/doc/symbol 等能验证 surface 存在和语义的仓库相对锚点。

## Secondary Code Evidence

代码证据应该支撑 public surface，而不是替代表格主体。把以下内容作为 secondary evidence、短 code anchors 或后续 drill-down，不要把它们扩展成 public surface 行：

- private helpers、internal classes、adapter internals、DTO field lists、SQL details 或完整 call chain。
- 文件树、package tree、controller/service/repository 清单。
- 只因当前实现存在、但没有稳定交互含义的函数或组件。
- 过长参数、响应字段或事件 payload 全集。

如果实现细节本身就是稳定 contract，例如 CLI command、documented config key、public SDK method 或 route parameter，再把它作为 surface 写入表格。

## Representative Example

```md
| Surface | Kind | Used by | Stable capability or promise | Owner boundary | Evidence |
| --- | --- | --- | --- | --- | --- |
| `GET /orders/{id}` | API route | Order detail page, support tools | Read the current order summary for a known order id | Order Query owns read shape; payment capture remains outside this boundary | `routes/orders.*`, order query handler |
| `order.status.changed` | Event | Fulfillment and notification subscribers | Notify that an order status crossed a stable lifecycle boundary | Order Lifecycle owns event meaning; subscribers own their reactions | event registry, status transition tests |
| `/checkout` | Page entry | Shopper | Start checkout from an active cart and return to cart on recoverable failure | Checkout page owns user journey; pricing rules are owned by Pricing | app route table, checkout page tests |
| `export-invoices` | Tool command | Finance operator | Export confirmed invoices for a selected period | Invoice Reporting owns export semantics; storage delivery is secondary | tool manifest, export command docs |
```

This example lists stable interaction points. It does not list helper methods, DTO fields, private adapters, every file touched by checkout, or subscriber implementation classes.

## 写作要求

- 使用 repo-neutral 名称；不要假设所有 repo 都有 HTTP API、React page 或 message bus。
- 一行只表达一个 stable interaction point。
- 同时说明使用者、稳定行为和 owner boundary。
- 保留 evidence，但保持 evidence 简短；详细实现放到 code anchors 或相关 module/page/flow。
- 未确认的 business intent、owner 或 capability 不要写成稳定事实；标成 candidate note、问题或 drift item。

## 避免

- 把 public surface 变成代码索引。
- 把 private helper、内部组件、DTO 字段或 call chain 写成对外 surface。
- 因为某个文件名包含 Controller、Page、Tool 或 Event 就自动认定它是稳定边界。
- 只列 route/API/event 名称，不说明使用者、稳定行为或 owner boundary。
- 为了表格完整而发明 capability、owner 或外部使用者。
