# Wiki Guidance Principles

本文件是所有 repo-wiki skills 的第一层 reader-quality guidance。每个 skill 都先按这里的原则判断信息是否应该保留、如何组织、能否写成稳定 wiki 知识，然后才使用具体 page-family guidance 或 writing blocks。

这些原则是自然语言 guidance，不是 schema、validator、lint、PASS/FAIL 或 compliance gate。语义质量只能靠证据、读者视角和 LLM 语义判断来检查。

## Priority

Information Preservation 是最高优先级。

任何 readability rewrite、结构调整、拆分、合并、移动、删减、表格化或图示化，都不能丢失 unique information、evidence anchors、canonical names、责任边界、decision meaning、例外条件或不确定性。

如果更易读的表达会改变含义、压掉证据、消除不确定性、合并两个不同概念、或让读者无法追溯原始判断，就停止改写并报告风险。不要用“整理”“精简”“标准化”当作删除信息的理由。

## Reader-First Structure

wiki 先服务读者理解，再服务文件整齐。

优先让读者知道：

- 这段内容解释什么系统事实或判断。
- 为什么它值得长期保留。
- 它属于哪个 owner page 或 canonical index。
- 它和相关 flow、page、module、model、decision 的关系。
- 读者下一步应该去哪里继续看。

可以把 dense prose 改成短段落、表格、列表或 Mermaid 图，但只有在这些表达让含义更清楚时才使用。不要为了填满固定字段而制造空内容，也不要把自然段机械拆成模板。

## Evidence-Aware Writing

稳定 wiki 内容需要清楚区分：

- repo 证据支持的当前系统事实。
- 用户明确确认的业务意图、命名、边界或设计 rationale。
- 从代码中能观察到、但还不能证明意图的候选说明。
- 仍需确认的不确定性、冲突或风险。

写证据时优先使用仓库相对路径、符号名、路由、配置、测试、文档位置或明确用户确认。不要把长推理过程、原始聊天记录或大段日志塞进稳定 wiki。需要治理的问题放进 Drift Page；需要确认的问题以问题或风险形式保留，而不是伪装成事实。

## Canonical Naming

复用 repo-local wiki 已经确认的 canonical names。V1 不创建单独的 wiki glossary page；canonical names 分布在 owner pages 和 catalog README 中。优先从这些位置取名：

- Roles、External Systems、Main Runtime Units: `wiki/01-system.md`
- Flows: `wiki/02-flows/README.md`
- Pages: `wiki/03-pages/README.md`
- Modules: `wiki/04-modules/README.md`
- Models: `wiki/05-models/README.md`
- Decisions: `wiki/06-decisions.md`

如果命名、边界或 owner page 不清楚，先问用户或报告 `meaning_loss_risk` / candidate note。不要为了让文档看起来统一而发明同义词、重命名业务概念、把代码目录名直接提升为 module 名，或把局部实现名当成外部系统名。

## No Guessing Stable Knowledge

不要把猜测写成稳定 wiki 知识。

可以直接写入的内容通常需要至少一种支撑：

- 当前 repo 里能明确证明的系统事实。
- 用户确认。
- 已有 wiki 页面中可保留、可追溯的信息。
- 明确引用的外部材料。

业务意图、设计 rationale、页面命名、module 边界、model 含义、跨团队责任和“应该如此”的判断，只有在证据或用户确认足够时才能写成稳定事实。证据不足时，保留为问题、candidate wiki note、drift item 或 intentionally left out。

## No Mechanical Correctness Theater

不要用机械正确性替代语义正确性。

禁止把 schema、validator、lint、PASS/FAIL、compliance、字段齐全、标题齐全、表格齐全，包装成 wiki 质量已经正确的证明。一个页面可以格式完整但事实错误、边界错、命名错、读者入口错或丢失关键不确定性。

报告质量时使用自然语言说明：保留了什么、改清楚了什么、还有什么证据不足、哪里有 meaning loss risk、哪里可能需要 drift radar 或用户确认。

## Skill Responsibilities

这些原则适用于所有 wiki skills，但不同 skill 不能互相越界。

- Reader-facing rewrite work, such as `wiki-doctor`, 只改善已有 wiki 的格式、结构和表达。它必须保留原信息，不能发明新稳定事实，不能做 drift classification。
- Drift detection, `wiki-drift-radar`, 对照 current working tree 和 wiki，分类 Wiki Drift、Code Drift、Coverage Gap 或 Wiki Too Thin，只刷新 `wiki/07-drift.md`。Candidate wiki note 不是稳定事实。
- Drift resolution, `wiki-drift-govern`, 只治理已经分类的 Drift Page items。它可以更新 wiki、补 coverage gap、或在确认的 Code Drift 下改代码，并在治理完成后清空 drift queue。
- New stable knowledge capture, `wiki-sink`, 只在没有 active drift items 时初始化 wiki 或写入 confirmed / evidence-grounded stable knowledge。它不能持久化原始聊天记录，不能把猜测写进稳定页面。

## Dense Prose Rewrite Example

Dense input:

```md
Checkout total comes from PricingClient in src/checkout/PricingGateway.ts now, not CartStore, but the old wiki says CartStore owns totals; admins can still override tax from /admin/orders/:id according to routes/admin.ts; refunds are described as manual in docs/refunds.md, but I did not verify current code.
```

Reader-first rewrite that preserves information:

```md
## Checkout Total Ownership

- Current evidence: checkout totals are read through `PricingClient` in `src/checkout/PricingGateway.ts`.
- Wiki conflict: the existing wiki says `CartStore` owns totals, so this may be Wiki Drift unless the wiki describes an intended behavior that should still hold.
- Admin tax override: admins can still override tax from `/admin/orders/:id`; evidence is `routes/admin.ts`.
- Refund uncertainty: `docs/refunds.md` describes refunds as manual, but current code has not been verified. Keep this as an uncertainty or candidate note, not as stable current behavior.
```

The rewrite is easier to scan, but it keeps every unique fact, evidence anchor, conflict, and uncertainty from the dense note.
