# Repo Wiki Skill Suite

Repo Wiki Skill Suite is a local skill suite for maintaining a human-readable `wiki/` inside a target repository.

The suite is intentionally small:

- `wiki-sink` initializes and writes stable wiki knowledge.
- `wiki-radar` compares the current working tree with the wiki and refreshes `wiki/07-drift.md`.
- `wiki-govern` resolves active drift items by updating wiki pages or changing code.

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

wiki-radar
  -> compare current working tree with wiki
  -> write current findings to wiki/07-drift.md

wiki-govern
  -> resolve wiki/07-drift.md items
  -> clear wiki/07-drift.md when done
```

`wiki-radar` does not require a clean git working tree. The current working tree is the current system being compared.

## User Guide

Use `wiki-sink` first when a target repository has no repo-local wiki, or when you want to write confirmed, reusable system knowledge into stable wiki pages.

Use `wiki-radar` when the target repository already has a wiki and you want to compare the current working tree with it. `wiki-radar` only refreshes `wiki/07-drift.md`. If that file already contains active items, resolve them with `wiki-govern` before starting another radar pass.

Use `wiki-govern` when `wiki/07-drift.md` contains active items. It resolves each item by updating wiki pages for Wiki Drift or Coverage Gap, or by changing code for confirmed Code Drift. When all active items are resolved, it clears `wiki/07-drift.md` back to the empty state.

Typical workflow:

```text
1. Create or seed wiki knowledge with wiki-sink.
2. Run wiki-radar to find current drift and coverage gaps.
3. Run wiki-govern until wiki/07-drift.md is empty.
4. Repeat radar only after the previous drift queue is cleared.
```

Do not use the suite as a raw archive. Stable wiki pages should contain current, evidence-grounded knowledge. Unclear business intent, naming, responsibility boundaries, or design rationale should be confirmed by a human before being written as stable wiki fact.

## Glossary

| Term | Meaning |
| --- | --- |
| Repo Wiki Skill Suite | The local skill suite in this repository. It helps create, inspect, govern, and update repo-local wiki knowledge. |
| Skill Suite Source Repository | This repository: the source for the skills and their shared references. |
| Target Repository | The product or application repository where the suite creates and maintains a top-level `wiki/`. |
| Repo-Local Wiki | The target repository's top-level `wiki/` directory. |
| Wiki Guidance System | The complete guidance set used by the suite: Wiki Structure, Writing Guidance, Writing Blocks, and Drift Page Rules. |
| Wiki Structure | The fixed target wiki layout and minimal initial page text, defined in `skills/references/wiki-structure.md`. |
| Writing Guidance | Page-family guidance for system, flow, page, module, model, decision, and drift pages. |
| Writing Blocks | Reusable semantic writing patterns for decisions, dependencies, page navigation, sequence, and state transitions. |
| Drift Page Rules | Rules for `wiki/07-drift.md`, including radar gating, finding types, evidence notes, and governance lifecycle. |
| Page Catalog | The repo-local wiki section for user-visible pages, entry points, navigation, visible states, and page-to-flow/module/model links. |
| Wiki Drift | The wiki is outdated or wrong compared with the current system, so the wiki should change. |
| Code Drift | Code diverges from wiki-described behavior that the user confirms should still hold, so code should change. |
| Coverage Gap | Important current system knowledge exists in the target repository but is missing from the wiki. |
| Wiki Too Thin | The wiki has too little relevant content for meaningful radar comparison. |
| Evidence Note | A concise note in `wiki/07-drift.md` that links a finding to wiki text, current evidence, and a suggested owner page. |

## Quality Model

The suite uses human-readable guidance and LLM semantic judgment. It does not use mechanical validators, lint checks, or pass/fail compliance gates for wiki quality.
