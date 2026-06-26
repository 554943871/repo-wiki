# Decision Tradeoff Block

用于解释一个当前仍重要的取舍。适合放在 `06-decisions.md`，也可以嵌入 flow、page、module 或 model family 页面。

## 适合使用时机

- 有多个合理选择。
- 选择结果会影响未来维护。
- 如果不解释，读者容易把它改回另一种做法。
- 需要把 stable facts、active decision、rejected alternatives 和 consequences 分开写。
- 决策仍影响 page navigation、module boundary、model lifecycle、dependency direction 或 flow behavior。

## 推荐表达

```md
### {Decision title}

Status:
Active decision / Confirmed decision / Candidate decision needing confirmation

Stable facts:
- ...

Decision:
...

Reason:
...

Rejected alternatives:
- ...

Consequences:
- ...

Uncertainty or guardrails:
- ...

Evidence anchors:
- ...

Related pages:
- ...
```

## 写作要求

- 先列 stable facts，再写 active decision，避免把证据事实和取舍判断混在一起。
- Decision 必须说明选择了什么，也说明排除了什么。
- Reason 写具体约束、读者影响或维护影响，不写空泛的“更好”“更清晰”。
- Consequences 写未来维护者需要承担的后果，例如 owner page、routing、dependency direction、migration cost 或 reader path。
- Evidence anchors 使用已有 wiki、repo 路径、符号名、路由、测试、用户确认或外部材料。
- 如果证据只支持事实、不支持意图或 rationale，把 rationale 写成 uncertainty，不要补成稳定决策。
- 当前仍未定的选择要标成 Active decision 或 Candidate decision needing confirmation，不要伪装成已确认事实。
- 不要为了压缩 decision block 删除 unique facts、rejected alternatives、限制条件或证据来源。

## V1 边界

- V1 不新增 `reader-map` block。读者选择下一页的内容属于 Page Navigation Block 或 README / catalog guidance。
- V1 不新增 `caliber-map` block。字段级重要性排序不写成独立 block；只有字段取舍本身是当前决策时，才作为 decision 的 stable fact、reason 或 consequence 保留。

## 示例使用条件

当 dependency map 显示 `Checkout flow` 当前调用 `Pricing module`，但团队还在决定 tax ownership 时，用 Decision Tradeoff Block：

- Stable fact: checkout total currently comes from `PricingClient`，证据是源码路径。
- Active decision: tax policy owner 是 Pricing 还是 Compliance。
- Rejected alternatives: 把 tax policy 分散到每个 checkout step。
- Consequences: owner page、dependency map 和 reader route 都要跟随这个选择。
- Uncertainty: 如果只有旧文档提到 Compliance，保留为待确认，不写成已定 ownership。

## 避免

- 没有取舍的普通事实。
- 纯历史讨论。
- 把局部实现偏好包装成系统决策。
- 只写“因为这样更好”而不说明具体原因。
- 把 active decision 混进 dependency map 作为稳定关系，或把稳定事实包装成决策。
