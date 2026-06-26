# Wiki Root Page Guidance

`wiki/README.md` 是 repo-local wiki 的顶层阅读入口。它帮助读者判断这个 wiki 记录什么、先读哪里、每个顶层 section 负责什么；它不是具体知识家族的 canonical index，也不是所有页面的汇总目录。

## 应该帮助读者回答

- 这个 wiki 的用途是什么。
- 推荐阅读顺序是什么。
- 每个顶层 section 承接哪类知识。
- 哪些内容适合进入稳定 wiki，哪些不适合。
- 读者下一步应该进入哪个 section。

## 适合写

- 1-2 句 wiki 定位。
- 顶层阅读顺序，链接到 `01-system.md`、`02-flows/README.md`、`03-pages/README.md`、`04-modules/README.md`、`05-models/README.md`、`06-decisions.md` 和 `07-drift.md`。
- 顶层收录范围和不收录内容。
- 非常短的 reader route 说明。

## 避免写

- 具体 flow、page、module、model 或 decision 的详细事实。
- 替代各 catalog README 的 canonical index。
- 原始聊天记录、排查日志或一次性 SOP。
- 为了完整感复制其它页面的正文。
- 把 `README.md` 变成 glossary 或所有页面的扁平目录。

## 推荐表达

`wiki/README.md` 可以保持略固定：

- 项目 Wiki 标题。
- 一句用途说明。
- 阅读顺序。
- 收录范围。
- 不收录内容。

这些是 reader-entry guidance，不是字段完整性检查。若目标 repo 需要额外入口说明，也应保持短，并把具体事实路由到对应 owner page 或 catalog README。

## LLM 语义检查问题

- 顶层阅读顺序是否覆盖所有固定 section？
- 每个 section 的说明是否只是路由摘要，而不是重复具体页面正文？
- `wiki/README.md` 是否没有承担 canonical index、glossary 或 drift history 职责？
- 收录范围是否强调当前系统事实、已确认或有证据支撑的长期知识？
- 不收录内容是否排除了原始聊天记录、一次性日志、未确认猜测和局部临时细节？
