# Wiki Doctor Sample Refresh Selection

This directory records demonstration evidence for GitHub issue #11. It is a
hand-authored sample refresh based on a generated wiki from another repository.
It is not a rewrite of that repository and not a universal quality benchmark.

## Target Sample

- Target wiki read path: `/Users/god/project_jdx/agent_pjt_auto_select/wiki`
- Source type: existing generated wiki sample only.
- Target write scope: none. No files under the target wiki were changed.
- Drift gate observed: `wiki/07-drift.md` contains the standard empty state.

## Read Boundary

The sample refresh intentionally used only markdown files under the target
`wiki/` directory. It did not inspect the target repository's source code,
tests, root README, docs, AGENTS files, or skill source files.

Existing wiki pages contain code anchors such as paths and symbols. The
demonstration preserves those anchors as copied wiki facts, but does not open
the referenced target files to verify them.

## Selected Pages

| Sample page | Why selected | Demonstrated wiki-doctor behavior |
| --- | --- | --- |
| `wiki/README.md` | Its current seeds are useful but do not route readers by task. | `add_reader_entry` for overview and navigation. |
| `wiki/02-flows/message-turn.md` | It has a dense numbered flow and branch list that can be easier to scan as phases. | `rewrite_page`, `add_table_or_diagram` for flow readability. |
| `wiki/03-pages/h5-surfaces.md` | It lists visible page entries and navigation/data rules. | Page navigation and public-surface shaping. |
| `wiki/04-modules/web-event-surfaces.md` | It overlaps with H5 surfaces but owns the protocol/module boundary. | Public-surface table with owner boundary preserved. |
| `wiki/04-modules/runtime-and-tooling.md` | It names the Skill/Tool/runtime boundary and stable tool set. | Public-surface and module-boundary preservation. |
| `wiki/05-models/turn-event-and-candidate-set.md` | It explains multiple related runtime models in prose. | Model relationship and source-of-truth readability. |
| `wiki/05-models/slots.md` | It separates confirmed purchasing conditions from scenario/memory overlay. | Model boundary and lifecycle readability. |

## Not Selected For Rewrite

The other target wiki pages were either catalog pages used for context or
already clear enough for this slice. The demonstration keeps the sample small:
it shows representative reader-facing improvements without copying the full
generated wiki into this repository.
