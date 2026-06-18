# Before Snippets

These are minimal excerpts copied from the generated target wiki. They show the
reader-facing structure before a wiki-doctor style refresh. The snippets are
trimmed to only the lines needed for this demonstration.

## Overview Seeds

Source: `wiki/README.md`, lines 30-35.

```md
当前已沉淀的稳定理解包括：

- DeepAgent native runtime 是当前生产主线，外部入口保持 FastAPI、SSE、H5 页面和回放接口。
- Skill 是业务流程指令层，Tool 是真实执行动作层，UI Tool 是用户可见交互层。
- `slots.sqlite` 保存按用户维度沉淀的采购条件，`conversations.sqlite` 保存 turn/event 回放，DeepAgent checkpoint 保存执行态。
- 候选检索、利润分析、视觉校准、记忆保存和模拟订单草稿都必须通过注册 Tool 或 UI 确认链路推进。
```

## Message Turn Flow

Source: `wiki/02-flows/message-turn.md`, lines 11-27.

```md
1. Web API 接收请求，创建 response backlog turn。
2. Response backlog 要求同一用户上一个 turn 已被消费；未消费时返回冲突，避免前端漏读事件后继续推进。
3. `DeepAgentRuntimeStore` 获取用户级锁，取消该用户旧的 waiting turn，并创建新的 `turn_id`。
4. Runtime store 读取当前 slots、知识来源和上一轮 active Skill，解析本轮 active Skills。
5. Store 先发出知识来源、`skill_activation` 和进度事件，并把 running turn 保存到 `conversations.sqlite`。
6. `DeepAgentRuntime` 为本轮构造 DeepAgent graph run：注入 user、turn、thread、current message、候选集 scope、active Skill ids 和允许 Tool 集。
7. DeepAgent graph 通过 ToolRuntime 调用 select Tool。Observed Tool wrapper 会发出 `tool_call` 和 `tool_output` 事件。
8. Runtime 把 DeepAgent graph 输出桥接成标准事件，并识别是否有 pending UI request。
9. Store 将前缀事件、Tool 事件、assistant 文本、UI 请求和终止事件保存成 turn/event 回放。
10. Web 用 SSE 把 backlog 里的事件流式返回给前端。

- 如果 runtime 仍在执行，store 会定期发 keepalive/progress 事件，前端可继续显示“处理中”状态。
- 如果结果包含 pending UI request，turn 状态进入 waiting UI，后续由 UI response resume 继续。
- 如果 DeepAgent 或 Tool 抛出异常，系统输出公开错误文本，并保存 error 状态。
- 如果客户端断开，store 保存已发出的前缀事件，并把该 turn 标为 interrupted。
```

## H5 Navigation And Web Surfaces

Source: `wiki/03-pages/h5-surfaces.md`, lines 9-19.

```md
| `/h5/` | 主 H5 控制台：对话、实时事件流、slots 面板、工具事件、视觉标尺和历史回放入口。 | `src/select_agent/web/static/index.html` |
| `/h5/demo` | 拍机堂移动端 AI 版 demo：商品列表、聊天抽屉、实时事件、证据卡、利润对比、回复选项和 Agent 结论卡。 | `src/select_agent/web/static/demo.html` |
| `/h5/demo/visual-v2` | 视觉校准 V2 独立页面。 | `src/select_agent/web/static/demo_visual_v2.html` |
| `/h5/dev/replay` | 前端回放工作台：读取保存的 conversation events，离线回放，不重新调用 Agent。 | `src/select_agent/web/static/replay.html` |

- 页面通过 Web API 发起 `/api/start`、`/api/message`、`/api/ui-response`、`/api/uploads`、会话列表和回放请求。
- SSE 事件是页面主要运行时输入，页面不应从 assistant 文本里解析结构化业务状态。
- 回放工作台读取 `conversation_events` 中保存的事件，用于复现 UI 行为和比较历史 turn。
- 视觉校准页面依赖 `attribute_visual_calibration` Skill 的 UI metadata 和 `request_visual_calibration` / `image_recognize` 工具链。
```

Source: `wiki/04-modules/web-event-surfaces.md`, lines 29-38.

```md
| `/api/start` | 新会话默认 Skill 开场。 | `src/select_agent/web/app.py` |
| `/api/message` | 普通文本消息入口，返回 SSE。 | `src/select_agent/web/app.py` |
| `/api/ui-response` | UI Tool 结构化反馈入口，返回 SSE。 | `src/select_agent/web/app.py` |
| `/api/turns/{turn_id}/events` | 按 seq 续读 response backlog 事件。 | `src/select_agent/web/app.py`, `src/select_agent/web/response_backlog.py` |
| `/api/conversations/{turn_id}/replay` | 读取已保存 turn 的事件流用于回放。 | `src/select_agent/web/app.py`, `src/select_agent/storage/conversations_db.py` |
| `/h5/`, `/h5/demo`, `/h5/demo/visual-v2`, `/h5/dev/replay` | 用户和开发可见页面入口。 | `src/select_agent/web/app.py`, `src/select_agent/web/static/*` |

Runtime events 保持 dict 形态进入 Web。`normalize_runtime_event` 当前只做复制，不改变语义。共享事件表面包括 `skill_activation`、`status`、`assistant_text`、`tool_call`、`tool_output`、`ui_request`、`ui_response`、`waiting_for_ui`、`done` 和 `error`。
```

## Runtime Models

Source: `wiki/05-models/turn-event-and-candidate-set.md`, lines 7-39, trimmed.

```md
Turn 是一次用户输入、系统开场、reset、UI resume 或保存动作产生的对话单元。它保存到 `conversation_turns`，包含 `turn_id`、`user_id`、`user_message`、开始和完成时间、状态、事件数量、结果和 metadata。

Event 是 turn 内按 seq 排列的运行时输出，保存到 `conversation_events`。事件用于 SSE、H5 展示、历史详情和离线回放。

Response backlog 是 Web 层的内存缓冲，不是长期事实源。它为每个用户保存最新 turn 的事件、seq、消费进度和 terminal 状态。前端通过 ack 或携带已消费 turn 信息告诉后端自己已经读完，后端才接受下一轮消息。

Candidate set 是 `structured_search` 返回给后续 Tool 的会话级候选集指针。它包含：

- `candidate_set_id`
- `applied_filters`
- `goods`

`profits_analysis` 不重新搜索，它通过 `candidate_set_id` 找到同一会话 scope 内保存的候选集，再按客户预期出货价计算物品编号级利润。
```

Source: `wiki/05-models/slots.md`, lines 30-40.

```md
1. 新用户或 reset 后，slots 为空。
2. 用户给出明确采购条件时，Agent 必须调用 `update_slots`。
3. `slots_db.apply_patch` 只接受基础采购条件 patch；场景和记忆 overlay 必须走更窄的 state patch 入口。
4. `reset_slots` 或 `/api/reset` 会清空当前用户 slots。
5. 下一轮消息读取 slots，并把非空基础条件作为可信业务状态注入 runtime context。

- `qualityNames` 和 `levelNames` 是对外公共键名；内部模型会迁移旧字段名。
- 列表和字典类条件采用替换语义，避免用户多轮修改后旧值越积越多。
- `condition_grade_group` 只支持“靓机”和“非靓机”。
```
