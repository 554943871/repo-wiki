# Whitebox Component Diagram Fixtures

These fixtures cover the initial Whitebox Component Diagram path: one enclosing
component boundary, boundary ports, optional one-level internal parts with
ports, external nodes, and directed `external`, `delegation`, and `assembly`
connectors rendered to SVG.

Run from the repository root:

```sh
python3 scripts/check_whitebox_fixtures.py
```

The checker validates `.whitebox.yaml` source models and compares the generated
SVG for valid fixtures with the committed expected SVG. It covers internal parts
and port-level connectors, while interfaces, interface assembly, UML
lollipop/socket notation, dense-diagram warnings, and guidance integration
belong to later issues.
