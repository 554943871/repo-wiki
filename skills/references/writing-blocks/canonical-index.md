# Canonical Index Block

用于维护 repo-local wiki 中稳定名称的 owner index。Canonical index 不是单独的 glossary page，而是分布在已经解释该知识家族的 owner page 或 catalog README 中，让读者和 agent 能用同一套名称继续阅读、写入和治理。

V1 不新增单独的 wiki glossary page。不要创建 `wiki/glossary.md`、`wiki/00-glossary.md` 或类似集中词表来承接这些名字。

## Canonical Index Owner

| Knowledge kind | Canonical index owner | What the index owns |
| --- | --- | --- |
| Roles | `wiki/01-system.md` | 人或组织角色的稳定称呼，以及它们和系统的关系。 |
| External Systems | `wiki/01-system.md` | 系统边界外的平台、服务、团队系统或第三方能力。 |
| Main Runtime Units | `wiki/01-system.md` | 读者理解系统运行形态所需的主要进程、应用、worker、job 或服务单元。 |
| Flows | `wiki/02-flows/README.md` | flow 名称、reader route、owner flow page 和关键相关对象。 |
| Pages | `wiki/03-pages/README.md` | 用户可见 page 名称、入口定位、owner page 和相关 flow/module/model。 |
| Modules | `wiki/04-modules/README.md` | 人类可理解的能力边界、owner module page 和主要责任。 |
| Models | `wiki/05-models/README.md` | model family 名称、包含的系统理解模型、owner model family page、边界和关键关系。 |
| Decisions | `wiki/06-decisions.md` | 当前仍有效的 decision 名称、取舍含义和相关页面。 |

`wiki/README.md` 只做顶层阅读入口，不承担具体知识家族的 canonical index。子页面可以解释细节，但稳定名称应回到上表中的 owner index。

一个 canonical name 只归一个 owner index。其他页面或 index 需要使用它时，应通过 related pages、related models、related flows、evidence 或正文引用指向 owner index，而不是新增同名 canonical entry。如果一个名称看起来需要双归属，先确认 owner index 和概念边界。

## 推荐表达

Canonical index 可以用短表、短列表或 catalog entry 表达。关键是帮助读者判断“这个名字指向哪个概念、边界是什么、继续读哪一页”。

```md
| Canonical name | Meaning and boundary | Owner page | Related pages | Evidence |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |
```

这些列不是固定 schema。只保留能减少歧义的列；没有证据或没有相关页时不要为了填表而编造。

Catalog README 里的 canonical index 应保持目录路由职责。对 `wiki/05-models/README.md` 来说，index 行优先说明 model family 名称、短边界、owner page 和何时阅读；不要在 README 里展开详情页级别的成员定义、关系图、关键字段、生命周期、demo/example 或 source-of-truth facts。

Canonical name 必须是一个单一稳定名称，不得使用 `A / B`、`A or B`、`A 或 B` 或类似混名写法承接多个候选名、别名或不同概念。别名和候选名称可以写在 alias、candidate note、证据或待确认问题中，但不能占用 canonical name。

Catalog / README 中显示的 page label 应是简洁概括名，而不是把页面承载的多个概念串成标题。避免用顿号、`与`、`和`、`and` 或长括号翻译堆出并列清单；并列内容放进 `Meaning and boundary`、`承载内容`、`Use when`、related pages 或 evidence 列。

## 何时可以维护

- `wiki-sink` 写入新稳定知识时，如果 name、owner page 和 boundary 已由 repo 证据、已有 wiki 或用户确认支撑，必须同步维护对应 canonical index。
- `wiki-doctor` 做 reader-facing refresh 时，可以从已有 wiki 内容或直接 target-repository evidence 重建、补齐或调整 canonical index。它可以写入 `safe_guidance_rewrite` 和 `evidence_grounded_update`，但不能凭代码相似度发明新名称，不能在证据冲突时猜哪个名称正确。
- `wiki-drift-radar` 读取 canonical index 来判断 coverage、owner page 和 suggested owner，但只能写 `wiki/07-drift.md`。它不能维护 canonical index；发现缺口或冲突时写成 finding、candidate wiki note 或需要确认的风险。
- `wiki-drift-govern` 治理 `Wiki Drift` 或 `Coverage Gap` 并写入稳定 wiki 内容时，必须同步更新受影响的 canonical index。治理 `Code Drift` 只改代码且不改变稳定 wiki 内容时，通常不改 canonical index。

## 必须报告的 meaning-loss risk

遇到下面情况，停止 canonicalize，报告 `meaning_loss_risk` 或询问用户，不要自动改名、合并、搬家或建新 owner page：

- 同一概念有多个候选名称，但证据不能证明它们完全等价。
- 同一名称可能指向不同概念，例如角色、页面、module 或外部系统重名。
- 不同 canonical indexes 会为不同概念使用完全相同的 canonical name。可以共享自然领域词根，但不能完全同名。
- 同一个 canonical name 看起来需要同时归入多个 owner indexes。
- 代码目录、类名、adapter 名或部署名看起来像 module / external system / runtime unit，但人类边界没有确认。
- SDK、client、adapter 或 protocol 名称看起来像 external system，但实际外部服务、平台或组织系统名称未确认。
- 需要用 slash、or、`或` 等混名写法才能表达一个 canonical name，说明稳定名称尚未确认。
- owner page 不清楚，或者一个条目可能属于多个 index owner。
- 改名会丢失已有 wiki 中的别名、边界说明、决策含义、证据锚点或不确定性。

可以保留 alias 或 candidate note，但要明确它还不是 canonical name。

不同 canonical indexes 可以共享自然领域词根，但不要为不同概念使用完全相同的 canonical name。名称应通过后缀、限定语或项目已确认的稳定叫法区分概念类型，例如运行边界、能力边界、页面、模型或流程。

同一个概念不要复制成多个同名 canonical entries。只保留一个 owner index，其它位置引用它。

## 示例

安全的 index update:

```md
已有 `wiki/04-modules/pricing.md` 明确说明 `Pricing` module 负责报价和税费计算，列出 `src/pricing/PricingGateway.ts` 作为证据，并链接到 Checkout Flow。

可以在 `wiki/04-modules/README.md` 增加：

| Canonical name | Boundary | Owner page | Related flows | Evidence |
| --- | --- | --- | --- | --- |
| Pricing | Owns quote and tax calculation boundaries. | `./pricing.md` | `../02-flows/checkout.md` | `src/pricing/PricingGateway.ts` |
```

这个更新只把已确认的名称和 owner route 放进 catalog，没有新增边界判断，也没有删除原页面里的证据。

应报告而不是猜的 case:

```md
代码里同时出现 `PaymentGateway` adapter、`Gateway` runtime unit 和 wiki 页面里的 `Payment Platform` external system。现有 wiki 没说明它们是否是同一概念，也没有确认哪个名字应对外展示。
```

此时不要把三者统一改成 `Payment Gateway`。应报告 `meaning_loss_risk`：名称冲突、external system 和 runtime unit 边界不清、canonical owner 未确认。需要用户确认或 drift governance 后，才能维护 `wiki/01-system.md` 的 canonical external systems / runtime units。
