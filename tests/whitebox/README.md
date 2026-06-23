# Whitebox Component Diagram Fixtures

These fixtures cover the first minimal Whitebox Component Diagram tracer bullet:
one enclosing component boundary, one boundary port, one external node, and one
directed external connector rendered to SVG.

Run from the repository root:

```sh
python3 scripts/check_whitebox_fixtures.py
```

The checker validates `.whitebox.yaml` source models and compares the generated
SVG for valid fixtures with the committed expected SVG. It only covers the
minimal external-connector slice; internal parts, interfaces, delegation,
assembly, and interface assembly belong to later issues.
