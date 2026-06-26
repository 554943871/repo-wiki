# After Demonstration

This is a hand-authored demonstration of a wiki-doctor style reader refresh.
It was not applied to the target wiki. It only restructures information already
present in the target wiki sample and keeps code anchors as existing wiki facts.

## Overview And Reader Navigation

Suggested shape for `wiki/README.md` and catalog entries:

| Reader question | Start here | Then read | Preserved sample facts |
| --- | --- | --- | --- |
| What system is this and where are its boundaries? | `01-system.md` | `04-modules/runtime-and-tooling.md`, `04-modules/web-event-surfaces.md` | DeepAgent native runtime is the production path; external entries include FastAPI, SSE, H5, and replay. |
| How does one user message become streamed output and replay data? | `02-flows/message-turn.md` | `05-models/turn-event-and-candidate-set.md` | A request creates a response backlog turn, activates Skills, calls Tools, stores turn/events, and streams SSE. |
| What happens after a user confirms a UI Tool card? | `02-flows/ui-response-resume.md` | `03-pages/h5-surfaces.md`, `04-modules/web-event-surfaces.md` | UI response carries structured feedback and resumes a pending DeepAgent turn. |
| Which visible H5 pages exist? | `03-pages/h5-surfaces.md` | `04-modules/web-event-surfaces.md` | The sample names `/h5/`, `/h5/demo`, `/h5/demo/visual-v2`, and `/h5/dev/replay`. |
| Who owns business procedure versus real actions? | `04-modules/runtime-and-tooling.md` | `06-decisions.md` | Skill owns business procedure, Tool owns real execution, and UI Tool owns visible interaction. |
| Which runtime facts are persisted? | `05-models/slots.md`, `05-models/turn-event-and-candidate-set.md` | `01-system.md` | `slots.sqlite` stores confirmed purchasing conditions; `conversations.sqlite` stores turn/event replay; checkpoint stores execution state. |

Reader-facing improvement: the original seeds are preserved, but the reader now
chooses a page by task instead of scanning a list of dense facts.

## Message Turn Flow Readability

Suggested shape for `wiki/02-flows/message-turn.md`:

| Phase | Owner / actor | Action and outcome | Preserved branch or guard |
| --- | --- | --- | --- |
| Entry | Web API | Receives `/api/start` or `/api/message` and creates a response backlog turn. | If the previous turn for the same user has not been consumed, the backlog rejects the next message to avoid missed frontend events. |
| Turn ownership | `DeepAgentRuntimeStore` | Takes the user-level lock, cancels the user's old waiting turn, and creates a new `turn_id`. | This keeps one user flow serialized. |
| Skill setup | Runtime store | Reads current slots, knowledge sources, and previous active Skill; resolves active Skills for the new turn. | It emits knowledge-source, `skill_activation`, and progress events, then saves the running turn to `conversations.sqlite`. |
| DeepAgent run | `DeepAgentRuntime` | Builds the graph run with user, turn, thread, current message, candidate-set scope, active Skill ids, and allowed Tool set. | The allowed Tool set remains scoped to active Skills and runtime context. |
| Tool bridge | DeepAgent graph and observed Tool wrapper | Calls select Tools through ToolRuntime; emits `tool_call` and `tool_output` events. | Tool execution remains the real action boundary. |
| Runtime output | Runtime store and Web API | Bridges graph output into standard events, detects pending UI request, saves prefix/tool/assistant/UI/terminal events, and streams backlog events over SSE. | Pending UI request moves the turn to waiting UI; completion or error is persisted for replay. |

Branch table preserved from the same page:

| Condition | Reader-visible result | Preserved action |
| --- | --- | --- |
| Runtime is still executing | Frontend can keep showing processing state. | Store emits keepalive/progress events. |
| Result includes pending UI request | Turn waits for structured UI response. | Continue through the UI Response Resume flow. |
| DeepAgent or Tool raises an exception | User receives public error text. | Error status is saved. |
| Client disconnects | The turn is not treated as normally completed. | Prefix events are saved and the turn is marked interrupted. |

Reader-facing improvement: the long numbered list becomes phases and branches
without changing ordering, actors, event names, storage facts, or exception
behavior.

## Public Surface And Navigation

Suggested shape across `wiki/03-pages/h5-surfaces.md` and
`wiki/04-modules/web-event-surfaces.md`:

| Surface | Kind | Used by | Stable capability or promise | Owner boundary | Existing wiki evidence |
| --- | --- | --- | --- | --- | --- |
| `/api/start` | API route | H5 pages and clients starting a new session | Starts a new conversation with the default Skill and returns SSE. | Web event surfaces own the HTTP/SSE entry; business strategy comes from active Skill and Agent. | `src/select_agent/web/app.py` |
| `/api/message` | API route | CLI, H5 console, and demo user-message paths | Accepts ordinary text and streams runtime events. | Web owns transport and backlog turn creation; runtime owns execution. | `src/select_agent/web/app.py` |
| `/api/ui-response` | API route | UI Tool cards rendered in H5 pages | Sends structured user feedback back to a waiting turn and returns SSE. | UI response does not directly write slots; Tool/runtime path owns state mutation. | `src/select_agent/web/app.py` |
| `/api/turns/{turn_id}/events` | API route | Frontend recovery / continuation | Reads response backlog events by seq. | Backlog is an in-memory delivery buffer, not the long-term replay source. | `src/select_agent/web/app.py`, `src/select_agent/web/response_backlog.py` |
| `/api/conversations/{turn_id}/replay` | API route | Replay workbench and historical inspection | Reads stored turn events for offline replay. | Replay reads saved events and does not re-run the Agent. | `src/select_agent/web/app.py`, `src/select_agent/storage/conversations_db.py` |
| `/h5/` | Page entry | Main H5 console users | Conversation, real-time events, slots panel, tool events, visual ruler, and replay entry. | Page owns user-visible entry and state display, not backend business ownership. | `src/select_agent/web/static/index.html` |
| `/h5/demo` | Page entry | Mobile demo users | Goods list, chat drawer, real-time events, evidence card, profit comparison, reply options, and Agent conclusion card. | Page renders visible experience from Web events and Tool metadata. | `src/select_agent/web/static/demo.html` |
| `/h5/demo/visual-v2` | Page entry | Visual calibration workflow users | Standalone visual calibration page. | Depends on visual calibration Skill metadata and visual Tool chain. | `src/select_agent/web/static/demo_visual_v2.html` |
| `/h5/dev/replay` | Page entry | Developers inspecting saved turns | Reads saved conversation events and replays UI behavior offline. | Replay does not call the Agent again. | `src/select_agent/web/static/replay.html` |
| Runtime event names | Event surface | H5 pages and replay | Shared event shape includes `skill_activation`, `status`, `assistant_text`, `tool_call`, `tool_output`, `ui_request`, `ui_response`, `waiting_for_ui`, `done`, and `error`. | `normalize_runtime_event` keeps dict semantics instead of changing event meaning. | `src/select_agent/web/events.py` |

Reader-facing improvement: the sample already had route tables, but the refreshed
shape adds `Kind`, `Used by`, stable capability, and owner boundary so readers
can compare pages, APIs, SSE, replay, and UI response without reading a code
index.

## Model Relationship And Source-Of-Truth Readability

Suggested shape for `wiki/05-models/turn-event-and-candidate-set.md`:

| From | Relationship | To | Meaning | Existing wiki evidence | Uncertainty |
| --- | --- | --- | --- | --- | --- |
| `Event` | 组成 | `Turn` | Events are ordered by `seq` inside one conversation turn. | `conversation_events` stores turn events for SSE, H5, history, and replay. | None introduced by this rewrite. |
| `Response backlog` | 引用 | `TurnEvent` | Backlog keeps latest per-user turn events, seq, consume progress, and terminal state for delivery. | The existing wiki says it is a Web-layer memory buffer. | It is not a long-term fact source. |
| `TurnEvent` | 衍生 | `ReplayEventStream` | Replay reads saved turn events and produces replayable UI event output without re-running the Agent. | The sample says replay uses saved turn/event data and does not re-run the Agent. | None introduced by this rewrite. |
| `Candidate set` | 引用 | `StructuredSearchResult` | A candidate set points to returned goods and applied filters for later Tools. | The page names `candidate_set_id`, `applied_filters`, and `goods`. | The retention count should be checked by drift radar if current code changes. |
| `ProfitAnalysis` | 引用 | `Candidate set` | Profit analysis uses `candidate_set_id` in the same session scope instead of searching again. | Existing wiki explicitly says `profits_analysis` does not re-search. | None introduced by this rewrite. |

Suggested source-of-truth table across `slots.md` and
`turn-event-and-candidate-set.md`:

| Fact | Source of truth | Applies to | Preserved rule |
| --- | --- | --- | --- |
| Confirmed purchasing conditions | `slots.sqlite` plus `update_slots` / `reset_slots` Tool path | Cross-turn user purchasing state | Frontend UI response cannot directly write business state. |
| Scenario and memory overlay | Narrow state patch / `state_snapshot()` path | Trial or overlay state around base slots | `slots_db.apply_patch` only accepts base purchasing-condition patches. |
| Replay data | `conversations.sqlite` turn/event records | H5 history, detail, and offline replay | Replay reads saved events and does not calculate candidate sets again. |
| Execution recovery | DeepAgent checkpoint | Runtime execution state | Checkpoint is not a business fact source. |
| Candidate-set reuse | Session-scope candidate-set memory | Follow-up Tools such as profit analysis | Expired or evicted `candidate_set_id` requires another `structured_search`. |

Reader-facing improvement: prose about Turn, Event, backlog, candidate set, slots,
and checkpoint becomes relationship/source-of-truth tables. The rewrite keeps
the original distinctions between replay source, delivery buffer, business
state, candidate pointer, and execution state.
