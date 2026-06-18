# Drift Page Rules

`wiki/07-drift.md` 是当前漂移治理队列。它承接 `wiki-drift-radar` 的结果，并由 `wiki-drift-govern` 治理完成后清空回 empty state。

## Empty State

```md
# 漂移治理（Drift）

No active drift or coverage gaps.
```

## Drift Page Ownership

`wiki/07-drift.md` is owned by the drift workflow, with narrow permissions per skill:

| Skill | Permission |
| --- | --- |
| `wiki-drift-radar` | May refresh active findings or write the standard empty state when it owns the radar pass. It still writes only `wiki/07-drift.md`. |
| `wiki-drift-govern` | May resolve and remove active items. It must write the standard empty state when the queue is cleared. |
| `wiki-sink` | May create the standard empty state during wiki initialization or explicit skeleton completion. Otherwise it only reads the gate and reports non-standard empty formatting. |
| `wiki-doctor` | Reader-refresh skill. It only reads the gate, except it may create a missing `wiki/07-drift.md` empty state as part of `complete_skeleton` for an existing wiki. It does not rewrite an existing Drift Page. |

Do not use `wiki/07-drift.md` as resolved history, raw chat storage, doctor audit output, or stable wiki content. Doctor ownership is documented here only to define Drift Page permissions; the `wiki-doctor` skill implements its reader-refresh workflow separately.

## Radar 启动门禁

`wiki-drift-radar` 启动前只检查 `wiki/07-drift.md`：

- 如果是 empty state，可以开始新一轮 radar。
- 如果包含 active items，停止并要求先运行 `wiki-drift-govern`。
- 不检查 git 工作区是否 clean。当前 working tree 就是当前系统事实。

## Radar 可写范围

`wiki-drift-radar` 只能刷新 `wiki/07-drift.md`。

它不能写：

- `wiki/01-system.md`
- `wiki/02-flows/**`
- `wiki/03-pages/**`
- `wiki/04-modules/**`
- `wiki/05-models/**`
- `wiki/06-decisions.md`
- 源代码或测试代码

## Finding Types

### Wiki Drift

wiki 写错或过期，当前系统事实更可信，因此应该改 wiki。

### Code Drift

代码偏离了用户确认仍正确的 wiki 描述，因此应该改代码。

### Coverage Gap

当前系统里有重要知识，但 wiki 没覆盖，因此应该补 wiki。

### Wiki Too Thin

wiki 内容太薄，无法进行有意义的 radar 对照。此时 `wiki-drift-radar` 写入 `Wiki Too Thin` 状态和需要补充的 wiki seeds，不输出 drift/gap 清单。

## Active Item Shape

```md
### {Finding title}
- Type: Wiki Drift | Code Drift | Coverage Gap
- Wiki text or missing coverage: ...
- Current evidence: ...
- Evidence: path/to/file
- Suggested owner page: wiki/...
- Candidate wiki note: ...
```

`Candidate wiki note` 是候选内容，不是稳定事实。只有 `wiki-drift-govern` 或 `wiki-sink` 写入稳定页面后，才算进入 wiki 正文。

## Governance Lifecycle

`wiki-drift-govern` 按 active item 类型治理：

- `Wiki Drift`: 更新对应 wiki 页面。
- `Coverage Gap`: 补充对应 wiki 页面。
- `Code Drift`: 修改代码，使实现回到用户确认仍正确的 wiki 描述。

如果 active item 缺少明确类型或仍然 ambiguous，`wiki-drift-govern` 直接询问用户把它分类为 `Wiki Drift`、`Code Drift`、`Coverage Gap`，或从治理队列移除。不要在 `07-drift.md` 仍有 active items 时要求重新运行 `wiki-drift-radar`。

治理完单条后，从 `07-drift.md` 删除该条。全部治理完成后，将文件改回 empty state。

`07-drift.md` 不保存 resolved history。治理历史交给 git commit 或 PR。

## Evidence Notes

每个 active item 都应该有精简证据：

- 指明相关 wiki 文本或缺失覆盖。
- 指明当前系统证据。
- 使用仓库相对路径、符号名或明确用户确认。
- 不保存完整推理过程。
- 不保存原始聊天记录。
