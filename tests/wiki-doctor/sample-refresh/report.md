# Wiki Doctor Sample Refresh Report

This report is demonstration evidence for GitHub issue #11. It documents how a
wiki-doctor refresh could improve a generated wiki sample's reader-facing
structure without losing original information. It is not a universal quality
benchmark and it did not rewrite the target repository's wiki.

## Run Shape

- Mode: demonstration-only safe rewrite sample.
- Gate note: target `wiki/07-drift.md` was in the standard empty state.
- Source read scope: markdown files under `/Users/god/project_jdx/agent_pjt_auto_select/wiki`.
- Target write scope: none.
- Code lookup: none in this demonstration. A real `wiki-doctor` run may inspect target source, docs, config, and other local evidence, then write direct evidence-grounded stable facts when the evidence is clear enough to cite.

## Preserved Facts

- DeepAgent native runtime is the production path.
- External entries remain FastAPI, SSE, H5 pages, and replay interfaces.
- Skill is the business-procedure instruction layer; Tool is the real-action layer; UI Tool is the user-visible interaction layer.
- `slots.sqlite` stores confirmed purchasing conditions by user.
- `conversations.sqlite` stores turn/event replay data.
- DeepAgent checkpoint stores execution state, not business facts.
- Registered Tools or UI confirmation paths mediate candidate retrieval, profit analysis, visual calibration, memory save, and simulated order-draft actions.
- A message turn creates a response backlog turn, enforces previous-turn consumption, uses a user-level lock, resolves active Skills, emits `skill_activation` and progress events, calls Tools through ToolRuntime, persists events, and streams SSE.
- Message turn branches for keepalive/progress, waiting UI, public error, and client disconnect are preserved.
- H5 route entries remain `/h5/`, `/h5/demo`, `/h5/demo/visual-v2`, and `/h5/dev/replay`.
- API surfaces remain `/api/start`, `/api/message`, `/api/ui-response`, `/api/turns/{turn_id}/events`, and `/api/conversations/{turn_id}/replay`.
- Web event surfaces own HTTP/SSE, response backlog, UI request/response transport, and replay reads; they do not own purchase strategy, direct slot writes, or replay re-execution.
- Turn, Event, Response backlog, Candidate set, and Slots distinctions are preserved.
- `profits_analysis` reuses `candidate_set_id` rather than re-running `structured_search`.
- `qualityNames`, `levelNames`, replacement semantics, and `condition_grade_group` rules stay visible.

## Changed Pages And Actions

These are demonstration changes only. They were not applied to the target wiki.

| Page | Classification | Actions | Demonstrated change |
| --- | --- | --- | --- |
| `wiki/README.md` | `safe_guidance_rewrite` | `add_reader_entry` | Convert current seeds into reader questions and next-page routes. |
| `wiki/02-flows/message-turn.md` | `safe_guidance_rewrite` | `rewrite_page`, `add_table_or_diagram` | Convert dense flow prose into phase and branch tables. |
| `wiki/03-pages/h5-surfaces.md` | `safe_guidance_rewrite` | `rewrite_page`, `add_table_or_diagram` | Keep page routes while making navigation/data ownership clearer. |
| `wiki/04-modules/web-event-surfaces.md` | `safe_guidance_rewrite` | `rewrite_page`, `add_table_or_diagram` | Expand surfaces into stable capability and owner-boundary rows. |
| `wiki/05-models/turn-event-and-candidate-set.md` | `safe_guidance_rewrite` | `rewrite_page`, `add_table_or_diagram` | Preserve Turn/Event/backlog/candidate facts as relationship and source-of-truth tables. |
| `wiki/05-models/slots.md` | `safe_guidance_rewrite` | `rewrite_page`, `add_table_or_diagram` | Preserve base slots, overlay, lifecycle, and field rules as source-of-truth facts. |

## Skipped Risks

| Risk | Classification | Action | Reason |
| --- | --- | --- | --- |
| Merge `H5 Surfaces` and `Web Event Surfaces` because both mention routes. | `meaning_loss_risk` | `risk_report_only` | The existing wiki separates user-visible page entry from protocol/module boundary. Merging could lose owner-page meaning. |
| Rename `Runtime And Tooling` or split it into runtime, skill, tool, and storage pages. | `meaning_loss_risk` | `risk_report_only` | The current wiki does not prove a safer canonical owner split. |
| Split `Turn Event And Candidate Set` into separate model pages. | `meaning_loss_risk` | `risk_report_only` | The page explicitly groups models that are easy to confuse; splitting may hide that teaching purpose. |
| Add new API, event, Tool, or Skill names from current code. | `evidence_grounded_update` when direct evidence is inspected; otherwise `drift_or_coverage_suspect` | `write_evidence_grounded_fact` or `recommend_drift_radar` | A real `wiki-doctor` run may write direct repo evidence; this demo did not inspect current code. |

## Suspected Drift Or Coverage Items

These are not findings from a code comparison in this demonstration. In a real
`wiki-doctor` run, direct inspected evidence can be written into stable wiki
pages; broader comparison or unresolved coverage should still use
`wiki-drift-radar`.

| Suspect area | Classification | Recommended route |
| --- | --- | --- |
| `SELECT_AGENT_RUNTIME` values and DeepAgent runtime creation behavior may change over time. | `evidence_grounded_update` if direct evidence is inspected; otherwise `drift_or_coverage_suspect` | Write with Evidence Anchors when clear; use `wiki-drift-radar` for broad comparison. |
| Registered Tool names under `SELECT_TOOL_NAMES` may change over time. | `evidence_grounded_update` if direct evidence is inspected; otherwise `drift_or_coverage_suspect` | Write with Evidence Anchors when clear; do not guess from this demo. |
| H5 route list, API route list, and event-name list may drift as Web surfaces evolve. | `evidence_grounded_update` if direct evidence is inspected; otherwise `drift_or_coverage_suspect` | Write scoped route facts when clear; use `wiki-drift-radar` for broad route inventory. |
| Candidate-set retention count and expiration behavior may drift. | `evidence_grounded_update` if direct evidence is inspected; otherwise `drift_or_coverage_suspect` | Write direct evidence when clear; use `wiki-drift-radar` for broad lifecycle audit. |
| Visual calibration and order-draft coverage may need more reader pages if maintainers want deeper documentation. | `drift_or_coverage_suspect` | Treat as possible Coverage Gap through `wiki-drift-radar`, not as wiki-doctor rewrite scope. |

## Out Of Scope

- Rewriting files under `/Users/god/project_jdx/agent_pjt_auto_select/wiki`.
- Inspecting target source code, tests, docs, root README, or skill files was out of scope for this demonstration only.
- Resolving suspected drift or coverage items in this slice.
- Treating this sample as a universal benchmark for all generated wikis.
- Turning the demonstration into mechanical quality scoring.

## Self-Review Notes

- The after demonstration preserves all facts listed in the before snippets.
- The rewrite changes presentation, not source-of-truth claims.
- Unverified current-system questions are either direct evidence-grounded update
  candidates for a real `wiki-doctor` run or broader `wiki-drift-radar` work.
- Target wiki files were not modified.
