# Module Overview Guidance

`module-overview.md` is kept only as a compatibility note for older skill-suite references.

The current Wiki Guidance System no longer treats Module Overview as a separate page family. A page under `wiki/04-modules/` that draws a confirmed C2 runtime unit or stable subsystem as the enclosing component is a canonical module owner page and must follow [`module-page.md`](./module-page.md). The enclosing component must be named and owned in `wiki/04-modules/README.md`.

`wiki/04-modules/README.md` remains the flat Canonical Module Index and reader route. It should not become a forced module tree. Parent/child drill-down, collaborating-module jumps, and cross-module topology belong in the relevant module owner pages.

When refreshing an older `module-map.md` or Module Overview page:

- If it already names a confirmed enclosing C2 runtime unit or stable subsystem, migrate it to a canonical module owner page shape using `module-page.md` and the Whitebox rules in `../writing-blocks/whitebox-component.md`.
- If the enclosing boundary is unclear, ownerless, or not confirmed as a canonical module, report `meaning_loss_risk` instead of preserving an ownerless overview page family.
- Preserve supporting participants as supporting participants. Do not promote stores, adapters, queues, helper layers, or runtime participants into canonical modules just because they appear in a map.
- Preserve reader routes as module-to-module drill-down links or related-module links inside owner pages, not as a separate overview-page ownership model.

Avoid creating new pages whose only role is "directory-level overview". Create or update a canonical module owner page instead, once the module name, owner page, and boundary are confirmed.
