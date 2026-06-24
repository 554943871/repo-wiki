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

It covers internal parts, port-level connectors, global interface definitions,
provided/required interface roles, interface assembly, UML lollipop/socket
notation, dense-diagram raw complexity metrics, and rejection of source-model
layout/view-selection fields. Guidance integration belongs to later issues.
