# Whitebox Component Diagram Fixtures

These fixtures cover the initial Whitebox Component Diagram path: one enclosing
component boundary, boundary ports, optional one-level internal parts with
ports, interface roles, external nodes, and directed `external`, `delegation`,
`assembly`, and `interfaceAssembly` connectors rendered to SVG.

Run from the repository root:

```sh
python3 scripts/check_whitebox_fixtures.py
```

The checker validates `.whitebox.yaml` source models and compares the generated
SVG for valid fixtures with the committed expected SVG through the explicit
`simple` render backend. Backend selection is a renderer/runtime concern, so it
is passed to the checker or render command and is not represented in
`.whitebox.yaml`.

The checker also renders every valid complete-view fixture through the explicit
`elk` backend. ELK fixture checks are structural rather than snapshot-based:
they verify deterministic SVG output, reader-visible semantic text, connector
markers, provided/required interface-role symbols, numeric canvas dimensions,
nonnegative geometry, and dense-diagram complexity metadata. The ELK backend
uses the repo-declared `elkjs` dependency and fails fast if `npm ci` has not
installed dependencies during repo-wiki skill suite development or upgrade.

Dense fixtures also exercise renderer-owned Derived Whitebox Views generated
from the same `.whitebox.yaml` source model:

```sh
python3 scripts/check_whitebox_fixtures.py render-derived \
  tests/whitebox/fixtures/valid/dense-complexity-signal.whitebox.yaml \
  tests/whitebox/fixtures/valid
```

Generated fixture snapshots use `.whitebox.<view>.svg` names such as
`.whitebox.boundary.svg`, `.whitebox.delegation.svg`,
`.whitebox.assembly.svg`, and `.whitebox.interfaces.svg`. Empty derived views
are not generated, and the checker fails if a fixture includes a derived SVG
file for a view that has no renderer-owned content.

It covers internal parts, port-level connectors, global interface definitions,
provided/required interface roles, interface assembly, UML lollipop/socket
notation, dense-diagram raw complexity metrics, and rejection of source-model
layout/view-selection fields. Guidance integration belongs to later issues.
