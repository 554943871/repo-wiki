# Decision Tradeoff Block

用于解释一个当前仍重要的取舍。适合放在 `06-decisions.md`，也可以嵌入 flow、page、module 或 model 页面。

## 适合使用时机

- 有多个合理选择。
- 选择结果会影响未来维护。
- 如果不解释，读者容易把它改回另一种做法。

## 推荐表达

```md
### {Decision title}

Decision:
...

Reason:
...

Rejected alternatives:
- ...

Consequences:
- ...

Related pages:
- ...
```

## 避免

- 没有取舍的普通事实。
- 纯历史讨论。
- 把局部实现偏好包装成系统决策。
- 只写“因为这样更好”而不说明具体原因。
