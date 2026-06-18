# Repo Wiki Skill Suite

Repo Wiki Skill Suite is a local skill suite for maintaining a human-readable `wiki/` inside a target repository.

The suite is intentionally small:

- `wiki-sink` initializes and writes stable wiki knowledge.
- `wiki-doctor` refreshes existing wiki pages against the latest Wiki Guidance System without losing original information.
- `wiki-drift-radar` compares the current working tree with the wiki and refreshes `wiki/07-drift.md`.
- `wiki-drift-govern` resolves active drift items by updating wiki pages or changing code.

For the full design, see [wiki-suite-design.md](./wiki-suite-design.md). For the glossary, see [CONTEXT.md](./CONTEXT.md).

## Target Wiki Shape

`wiki-sink` creates this top-level wiki structure in a target repository:

```text
wiki/
  README.md
  01-system.md
  02-flows/
    README.md
  03-pages/
    README.md
  04-modules/
    README.md
  05-models/
    README.md
  06-decisions.md
  07-drift.md
```

## Skill Flow

```text
wiki-sink
  -> create or update stable wiki pages

wiki-doctor
  -> check existing wiki pages against the latest guidance
  -> rewrite formatting, structure, and expression without losing original information

wiki-drift-radar
  -> compare current working tree with wiki
  -> write current findings to wiki/07-drift.md

wiki-drift-govern
  -> resolve wiki/07-drift.md items
  -> clear wiki/07-drift.md when done
```

`wiki-drift-radar` does not require a clean git working tree. The current working tree is the current system being compared.

## User Guide

Use `wiki-sink` first when a target repository has no repo-local wiki, or when you want to write confirmed, reusable system knowledge into stable wiki pages.

Use `wiki-doctor` when an existing repo-local wiki should be refreshed against the latest Wiki Guidance System. It rewrites formatting, structure, and expression only when the original information can be preserved.

Use `wiki-drift-radar` when the target repository already has a wiki and you want to compare the current working tree with it. `wiki-drift-radar` only refreshes `wiki/07-drift.md`. If that file already contains active items, resolve them with `wiki-drift-govern` before starting another radar pass.

Use `wiki-drift-govern` when `wiki/07-drift.md` contains active items. It resolves each item by updating wiki pages for Wiki Drift or Coverage Gap, or by changing code for confirmed Code Drift. When all active items are resolved, it clears `wiki/07-drift.md` back to the empty state.

Typical workflow:

```text
1. Create or seed wiki knowledge with wiki-sink.
2. Run wiki-doctor when existing pages need guidance refresh without changing meaning.
3. Run wiki-drift-radar to find current drift and coverage gaps.
4. Run wiki-drift-govern until wiki/07-drift.md is empty.
5. Repeat radar only after the previous drift queue is cleared.
```

Do not use the suite as a raw archive. Stable wiki pages should contain current, evidence-grounded knowledge. Unclear business intent, naming, responsibility boundaries, or design rationale should be confirmed by a human before being written as stable wiki fact.

## Glossary

| Term | Meaning |
| --- | --- |
| Repo Wiki Skill Suite | The local skill suite in this repository. It helps create, inspect, govern, and update repo-local wiki knowledge. |
| Skill Suite Source Repository | This repository: the source for the skills and their shared references. |
| Target Repository | The product or application repository where the suite creates and maintains a top-level `wiki/`. |
| Repo-Local Wiki | The target repository's top-level `wiki/` directory. |
| Wiki Guidance System | The complete guidance set used by the suite: Wiki Guidance Principles, Wiki Structure, Writing Guidance, Writing Blocks, and Drift Page Rules. |
| Wiki Guidance Principles | Shared natural-language reader-quality guidance that every wiki skill reads first: information preservation, reader-first structure, reader-facing Chinese headings with stable English aliases, evidence-aware writing, canonical naming, no guessing stable knowledge, and no mechanical correctness theater. |
| Wiki Structure | The fixed target wiki layout and minimal initial page text, defined in `skills/references/wiki-structure.md`. |
| Writing Guidance | Page-family guidance for system, flow, page, module, model, decision, and drift pages. |
| Writing Blocks | Reusable semantic writing patterns for activity maps, canonical indexes, decisions, dependencies, evidence anchors, model relations, module boundaries, page layout, page navigation, public surfaces, sequence, and state transitions. |
| Drift Page Rules | Rules for `wiki/07-drift.md`, including radar gating, finding types, evidence notes, and governance lifecycle. |
| Information Preservation | A global principle: readability work must not lose unique information, evidence anchors, naming, boundaries, decision meaning, or uncertainty. |
| Canonical Index | The stable naming and navigation source for roles, external systems, flows, pages, modules, models, and decisions. |
| Public Surface | A stable visible entry point, capability, API, tool, route, page entry, or event surface that explains a system or module boundary. |
| Page Catalog | The repo-local wiki section for user-visible pages, entry points, navigation, visible regions, page variants, visible states, page-level interactions, and page-to-flow/module/model links. |
| Module Catalog | The repo-local wiki section for human-meaningful capability boundaries, stable public surfaces, internal capabilities, collaboration rules, and related flow/page/model links. |
| Wiki Drift | The wiki is outdated or wrong compared with the current system, so the wiki should change. |
| Code Drift | Code diverges from wiki-described behavior that the user confirms should still hold, so code should change. |
| Coverage Gap | Important current system knowledge exists in the target repository but is missing from the wiki. |
| Wiki Too Thin | The wiki has too little relevant content for meaningful radar comparison. |
| Evidence Note | A concise note in `wiki/07-drift.md` that links a finding to wiki text, current evidence, and a suggested owner page. |

## Quality Model

The suite uses human-readable guidance and LLM semantic judgment. It does not use mechanical validators, lint checks, or pass/fail compliance gates for wiki quality.

`skills/references/wiki-guidance-principles.md` is the shared first reference for all wiki skills. It treats Information Preservation as the highest-priority rule and distinguishes reader-facing rewrites from drift detection, drift resolution, and new stable knowledge capture.

Fine-grained guidance is still expected. The suite should borrow useful expression rules from mature documentation systems, but translate them into natural-language writing guidance and writing blocks instead of schemas or mechanical checks.
