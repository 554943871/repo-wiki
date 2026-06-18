# Repo Wiki Skill Suite

This context describes a skill suite for helping teams maintain human-readable, repository-local system knowledge.

For the operational design, see [Wiki Skill Suite Design](./wiki-suite-design.md).

## Language

**Repo Wiki Skill Suite**:
A set of agent skills that help create, inspect, diagnose, and update a repository-local wiki for a target repository.
_Avoid_: raw archive workflow

**Local Skill Suite**:
A group of ordinary local agent skills maintained together without packaging them as a plugin bundle.
_Avoid_: plugin bundle

**Skill Suite Source Repository**:
The repository that contains the skill suite's own source, instructions, templates, and supporting assets.
_Avoid_: target repo, repo-local wiki

**Target Repository**:
The product or application repository that the Repo Wiki Skill Suite is applied to.
_Avoid_: skill suite repository

**Repo-Local Wiki**:
Human-readable system knowledge stored in a top-level `wiki/` directory inside a target repository alongside its code.
_Avoid_: raw conversation archive, nested wiki directory

**Numbered Wiki Structure**:
A repo-local wiki layout where top-level content pages and folders use numeric prefixes for reading order, while README files stay unnumbered and child content pages stay unnumbered.
_Avoid_: numbered README files, numbered child pages

**Guidance**:
Human-readable writing and reading guidance for wiki sections, intended for people and LLM semantic judgment rather than mechanical checking.
_Avoid_: schema, validator, lint, compliance, PASS

**Wiki Guidance System**:
The complete guidance set used by the Repo Wiki Skill Suite, including Wiki Structure, Writing Guidance, Writing Blocks, and Drift Page Rules.
_Avoid_: schema system, validator suite, template framework

**Drift Page**:
The top-level numbered repo-local wiki file that records the current active semantic drift and coverage gaps while they are being governed; a new wiki-radar check must not start while it still contains active items.
_Avoid_: drift directory, drift backlog archive, append-only drift history

**Evidence Note**:
A short citation in the Drift Page that names the relevant wiki text or missing coverage, the current system evidence, the suggested owner page, and any candidate wiki note without preserving the full radar analysis or treating candidates as stable facts.
_Avoid_: full reasoning transcript, raw conversation archive, stable wiki fact

**Decision Map**:
The repo-local wiki page that summarizes current active decisions and tradeoffs for human understanding.
_Avoid_: history archive, decision inbox

**System Overview**:
The top-level repo-local wiki page for human-readable system context and major runtime-unit overview, roughly covering C4 C1 and C2 without going into component or code-level detail.
_Avoid_: component map, class documentation

**Flow Catalog**:
The repo-local wiki section that explains key user, business, and system flows before readers inspect page behavior or module boundaries.
_Avoid_: ordinary call chain, implementation trace log, test scenario dump, troubleshooting SOP

**Page Catalog**:
The repo-local wiki section that explains user-visible pages, entry points, navigation, visible states, and how pages connect to flows, modules, and models.
_Avoid_: DOM tree, CSS detail, component inventory, backend call chain

**Module Catalog**:
The repo-local wiki section that explains human-meaningful capability and responsibility boundaries after key flows are understood, even when those boundaries do not match code directories.
_Avoid_: package tree, runtime unit inventory, page inventory

**Model Catalog**:
The repo-local wiki section that explains important system-understanding models, including their meaning, state, and relationships, without requiring strict DDD classification or focusing on persistence technology.
_Avoid_: strict DDD model, database table catalog, storage inventory

**wiki-radar**:
The radar skill that compares the target repository's current working-tree system with its repo-local wiki across the whole project by default or a user-specified scope, classifies each finding as wiki drift, code drift, or coverage gap, asks the user to resolve ambiguity before writing, and may refresh the Drift Page without confirmation after classification when the Drift Page has no active items.
_Avoid_: wiki-xray, validator, stable wiki page writer, ambiguous drift handoff, git clean gate

**wiki-govern**:
The governance skill used when the Drift Page has active items; it resolves classified Drift Page items by updating wiki pages for wiki drift or coverage gaps, or by changing code when code drift means the implementation should return to the wiki-described behavior; after all active items are resolved, it clears the Drift Page to its empty state.
_Avoid_: ambiguous drift resolver, open-ended refactor skill, guessing intent from code

**wiki-sink**:
The write skill used when the Drift Page has no active items; it initializes the fixed repo-local wiki skeleton and records confirmed or evidence-grounded reusable knowledge into it, including system, flow, page, module, model, and decision knowledge, while excluding radar findings persisted to the Drift Page.
_Avoid_: wiki-update, wiki-adr, raw archive, agent-doc sync, radar result persistence, guessed stable knowledge, drift governance

**Coverage Gap**:
Important current system knowledge that exists in the target repository but is missing from the repo-local wiki.
_Avoid_: every undocumented implementation detail

**Wiki Drift**:
A mismatch where wiki content is outdated or wrong compared with the current system, so the wiki should change.
_Avoid_: code drift

**Code Drift**:
A mismatch where the current implementation diverges from wiki-described behavior that the user confirms should still hold, so code should change.
_Avoid_: wiki drift, open-ended refactor

**Wiki Too Thin**:
A repo-local wiki with too little relevant content for meaningful radar comparison; wiki-radar may stop and refresh the Drift Page with this status instead of producing drift or coverage-gap findings.
_Avoid_: pretending a meaningful comparison is possible
