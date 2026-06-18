# Wiki Skill Suite Design

This document records the current operating design for the Repo Wiki Skill Suite. `CONTEXT.md` remains the glossary; this file holds the workflow and output structure.

## Scope

The suite is a Local Skill Suite, not a plugin bundle.

The suite writes a Repo-Local Wiki into a Target Repository. The Repo-Local Wiki is the top-level `wiki/` directory only.

## Skill Set

V1 has three skills:

```text
wiki-radar
wiki-govern
wiki-sink
```

## Source Repository Layout

The Skill Suite Source Repository uses ordinary local skill directories:

```text
skills/
  wiki-radar/
    SKILL.md
    agents/
      openai.yaml
  wiki-govern/
    SKILL.md
    agents/
      openai.yaml
  wiki-sink/
    SKILL.md
    agents/
      openai.yaml
  references/
    wiki-structure.md
    drift-page-rules.md
    writing-guidance/
      system-overview.md
      flow-page.md
      page-page.md
      module-page.md
      model-page.md
      decision-map.md
      drift-page.md
    writing-blocks/
      decision-tradeoff.md
      dependency-map.md
      page-navigation.md
      sequence.md
      state-transition.md
```

This is the suite's source layout. It is separate from the `wiki/` output that `wiki-sink` creates inside a Target Repository.

Shared references stay thin and only hold stable cross-skill rules. Individual skill instructions should not duplicate the fixed wiki structure or Drift Page rules.

The suite deliberately avoids schema-oriented language. Do not introduce Doc Schema, Fragment Schema, page schema, validators, linters, compliance checks, or PASS/FAIL language. Wiki quality is judged through human-readable guidance and LLM semantic checking, not mechanical structure checks.

`wiki-structure.md` includes the fixed layout and minimal initial page text with human-readable guidance. It must not define rigid field templates for child pages.

`writing-guidance/` holds central quality guidance for each wiki page family. `writing-blocks/` holds reusable writing patterns for common explanatory blocks. These files are semantic standards for LLM writing and review, not schemas or mechanically checked templates.

Guidance and block files must be self-contained. They may be authored from prior documentation experience, but they must not advertise inheritance from another documentation system or create compatibility expectations.

Guidance and block files use Chinese prose by default, while keeping English file names and stable terms such as `wiki-radar`, `Wiki Drift`, and `Coverage Gap`.

### wiki-radar

`wiki-radar` compares the Target Repository's current working-tree system with its Repo-Local Wiki. It defaults to whole-project review and may accept a user-specified scope.

It classifies findings as:

- `Wiki Drift`: the wiki is outdated or wrong, so the wiki should change.
- `Code Drift`: code diverges from wiki-described behavior that the user confirms should still hold, so code should change.
- `Coverage Gap`: important current system knowledge is missing from the wiki.

If classification is ambiguous, `wiki-radar` must ask the user before writing. It must not hand ambiguous drift to `wiki-govern`.

`wiki-radar` may refresh only `wiki/07-drift.md`, and it may do so without confirmation after classification. It must not write stable wiki pages.

Before starting, `wiki-radar` checks only `wiki/07-drift.md`. If it contains active items, `wiki-radar` stops and asks the user to run governance first. It does not require a clean git working tree; the current working tree is the current system being compared.

If the wiki is too thin for meaningful comparison, `wiki-radar` stops normal checking and refreshes `wiki/07-drift.md` with a `Wiki Too Thin` status and needed wiki seeds.

### wiki-govern

`wiki-govern` is used when `wiki/07-drift.md` has active items.

It resolves classified items:

- For `Wiki Drift`, update the relevant wiki page.
- For `Coverage Gap`, add missing wiki coverage.
- For `Code Drift`, change code so implementation matches the wiki-described behavior.

For coverage gaps, code-proven facts may be written directly. Business intent, design rationale, page or module naming, and boundary decisions require user confirmation.

After an item is resolved, `wiki-govern` removes it from `wiki/07-drift.md`. When all active items are resolved, it writes the empty state.

`wiki-govern` is not an open-ended refactor skill. If a Drift Page item is ambiguous or lacks a clear type, `wiki-govern` asks the user to classify it as `Wiki Drift`, `Code Drift`, `Coverage Gap`, or remove it from the governance queue. It must not send the user back to `wiki-radar` while active items remain.

### wiki-sink

`wiki-sink` is used when `wiki/07-drift.md` has no active items.

It initializes the fixed Repo-Local Wiki skeleton and records confirmed or evidence-grounded reusable knowledge into stable wiki pages.

It must not write guessed stable knowledge. It must not persist raw conversation archives. It does not own radar result persistence.

When initializing an existing `wiki/`, `wiki-sink` must not overwrite existing files. It may create missing skeleton files only when the user explicitly asked to initialize or complete the skeleton; otherwise it reports the missing paths and asks first.

## Target Wiki Structure

`wiki-sink` initializes this fixed structure:

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

Top-level content pages and folders use numeric prefixes for reading order. `README.md` files are never numbered. Child content pages inside folders are not numbered.

### README.md

Explains how to read the wiki and what each top-level section contains.

### 01-system.md

Provides a human-readable system overview. It roughly covers C4 C1 and C2: system context and major runtime units. It does not enter component, class, or function-level detail.

### 02-flows/

Explains key user, business, and system flows before readers inspect pages and module boundaries. It excludes ordinary call chains, test steps, trace dumps, and troubleshooting SOPs.

### 03-pages/

Explains user-visible pages, entry points, navigation, visible states, and page relationships to flows, modules, and models. It excludes DOM trees, CSS details, component-library inventories, and backend call chains.

### 04-modules/

Explains human-meaningful capability and responsibility boundaries. A module may or may not match a code directory, page, service process, or package.

### 05-models/

Explains important system-understanding models: core objects, state, relationships, and rules. These are not strict DDD models and do not focus on persistence technology such as MySQL or Redis.

### 06-decisions.md

Summarizes current active decisions and tradeoffs for human understanding.

### 07-drift.md

Stores the current active radar findings while they are being governed. It is not a history archive.

## Drift Page Contract

`wiki/07-drift.md` represents the current governance queue.

Empty state:

```md
# Drift

No active drift or coverage gaps.
```

When non-empty, it may contain:

```md
# Drift

## Wiki Too Thin

## Active Drift

## Coverage Gaps
```

Each active item should include a short Evidence Note:

```md
### {Finding title}
- Type: Wiki Drift | Code Drift | Coverage Gap
- Wiki text or missing coverage: ...
- Current evidence: ...
- Evidence: path/to/file
- Suggested owner page: wiki/...
- Candidate wiki note: ...
```

`Candidate wiki note` is optional and is never a stable fact until `wiki-govern` or `wiki-sink` writes it into a stable page.

`wiki/07-drift.md` is refreshed for current state, not appended as history. Governance history belongs in git commits or pull requests.
