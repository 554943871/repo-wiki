#!/usr/bin/env python3
"""Validate and render minimal Whitebox Component Diagram fixtures."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised only on lean hosts.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "whitebox" / "fixtures"

REQUIRED_VALID_FIXTURES = {"minimal-empty.whitebox.yaml"}
REQUIRED_INVALID_FIXTURES = {
    "missing-component-evidence.whitebox.yaml",
    "missing-connector-evidence.whitebox.yaml",
    "missing-required-label.whitebox.yaml",
    "non-snake-case-id.whitebox.yaml",
    "source-layout-hint.whitebox.yaml",
    "unconnected-port.whitebox.yaml",
    "unsupported-top-level-field.whitebox.yaml",
}
ALLOWED_TOP_LEVEL = {"kind", "version", "component", "externals", "connectors"}
ALLOWED_COMPONENT_FIELDS = {"id", "label", "evidence", "ports"}
ALLOWED_PORT_FIELDS = {"id", "label", "evidence"}
ALLOWED_EXTERNAL_FIELDS = {"id", "label", "evidence"}
ALLOWED_CONNECTOR_FIELDS = {"id", "type", "source", "target", "label", "evidence"}
LAYOUT_HINT_FIELDS = {
    "canvas",
    "coordinate",
    "coordinates",
    "height",
    "layout",
    "order",
    "position",
    "rank",
    "route",
    "routing",
    "width",
    "x",
    "y",
}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_source_model(path: Path) -> tuple[Any | None, list[str]]:
    if yaml is None:
        return None, ["PyYAML is required to read .whitebox.yaml files"]

    try:
        return yaml.safe_load(read_text(path)), []
    except yaml.YAMLError as exc:
        return None, [f"{rel(path)} is not valid YAML: {exc}"]


def type_name(value: object) -> str:
    return type(value).__name__


def expect_mapping(value: object, field_path: str, errors: list[str]) -> dict[str, object] | None:
    if isinstance(value, dict):
        return value
    errors.append(f"{field_path} must be a mapping, got {type_name(value)}")
    return None


def expect_list(value: object, field_path: str, errors: list[str]) -> list[object] | None:
    if isinstance(value, list):
        return value
    errors.append(f"{field_path} must be a list, got {type_name(value)}")
    return None


def require_string(mapping: dict[str, object], key: str, field_path: str, errors: list[str]) -> str | None:
    value = mapping.get(key)
    if isinstance(value, str) and value.strip():
        return value
    errors.append(f"{field_path}.{key} is required")
    return None


def check_allowed_fields(
    mapping: dict[str, object],
    allowed: set[str],
    field_path: str,
    errors: list[str],
) -> None:
    for key in sorted(mapping):
        if key not in allowed:
            errors.append(f"{field_path} unsupported field: {key}")


def check_layout_hints(value: object, field_path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{field_path}.{key}" if field_path else str(key)
            if key in LAYOUT_HINT_FIELDS:
                errors.append(f"source model must not contain layout hint field: {child_path}")
            check_layout_hints(child, child_path, errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_layout_hints(child, f"{field_path}[{index}]", errors)


def check_snake_case(value: str | None, field_path: str, errors: list[str]) -> None:
    if value is not None and not SNAKE_CASE.fullmatch(value):
        errors.append(f"{field_path} must be snake_case")


def check_evidence(value: object, field_path: str, errors: list[str]) -> None:
    entries = expect_list(value, field_path, errors)
    if entries is None:
        return
    if not entries:
        errors.append(f"{field_path} is required")
        return

    for index, entry in enumerate(entries):
        entry_path = f"{field_path}[{index}]"
        evidence = expect_mapping(entry, entry_path, errors)
        if evidence is None:
            continue
        evidence_type = require_string(evidence, "type", entry_path, errors)
        if evidence_type == "file":
            path_value = require_string(evidence, "path", entry_path, errors)
            if path_value:
                evidence_path = Path(path_value)
                if evidence_path.is_absolute() or ".." in evidence_path.parts:
                    errors.append(f"{entry_path}.path must be repo-relative")
                elif not (ROOT / evidence_path).exists():
                    errors.append(f"{entry_path}.path does not exist: {path_value}")
        elif evidence_type == "user":
            require_string(evidence, "note", entry_path, errors)
        elif evidence_type is not None:
            errors.append(f"{entry_path}.type must be file or user")


def parse_endpoint(
    value: object,
    field_path: str,
    external_ids: set[str],
    port_ids: set[str],
    errors: list[str],
) -> tuple[str, str] | None:
    endpoint = expect_mapping(value, field_path, errors)
    if endpoint is None:
        return None
    if len(endpoint) != 1:
        errors.append(f"{field_path} must name exactly one endpoint")
        return None

    endpoint_type, endpoint_id = next(iter(endpoint.items()))
    if not isinstance(endpoint_id, str) or not endpoint_id.strip():
        errors.append(f"{field_path}.{endpoint_type} is required")
        return None
    if endpoint_type == "external":
        if endpoint_id not in external_ids:
            errors.append(f"{field_path}.external references unknown external: {endpoint_id}")
            return None
        return ("external", endpoint_id)
    if endpoint_type == "port":
        if endpoint_id not in port_ids:
            errors.append(f"{field_path}.port references unknown component port: {endpoint_id}")
            return None
        return ("port", endpoint_id)

    errors.append(f"{field_path} uses unsupported endpoint type: {endpoint_type}")
    return None


def validate_source_model(model: object) -> list[str]:
    errors: list[str] = []
    root = expect_mapping(model, "source model", errors)
    if root is None:
        return errors

    check_layout_hints(root, "", errors)

    for key in sorted(root):
        if key not in ALLOWED_TOP_LEVEL:
            errors.append(f"unsupported top-level field: {key}")

    if root.get("kind") != "whitebox_component_diagram":
        errors.append("kind must be whitebox_component_diagram")
    if root.get("version") != 1:
        errors.append("version must be 1")

    component = expect_mapping(root.get("component"), "component", errors)
    port_ids: set[str] = set()
    if component is not None:
        check_allowed_fields(component, ALLOWED_COMPONENT_FIELDS, "component", errors)
        component_id = require_string(component, "id", "component", errors)
        check_snake_case(component_id, "component.id", errors)
        require_string(component, "label", "component", errors)
        if "evidence" not in component:
            errors.append("component.evidence is required")
        else:
            check_evidence(component.get("evidence"), "component.evidence", errors)

        ports = expect_list(component.get("ports"), "component.ports", errors)
        if ports is not None:
            if not ports:
                errors.append("component.ports must include at least one boundary port")
            for index, port_value in enumerate(ports):
                port_path = f"component.ports[{index}]"
                port = expect_mapping(port_value, port_path, errors)
                if port is None:
                    continue
                check_allowed_fields(port, ALLOWED_PORT_FIELDS, port_path, errors)
                port_id = require_string(port, "id", port_path, errors)
                check_snake_case(port_id, f"{port_path}.id", errors)
                require_string(port, "label", port_path, errors)
                if port_id:
                    if port_id in port_ids:
                        errors.append(f"{port_path}.id duplicates component port: {port_id}")
                    port_ids.add(port_id)

    externals = expect_list(root.get("externals"), "externals", errors)
    external_ids: set[str] = set()
    if externals is not None:
        if not externals:
            errors.append("externals must include at least one external node")
        for index, external_value in enumerate(externals):
            external_path = f"externals[{index}]"
            external = expect_mapping(external_value, external_path, errors)
            if external is None:
                continue
            check_allowed_fields(external, ALLOWED_EXTERNAL_FIELDS, external_path, errors)
            external_id = require_string(external, "id", external_path, errors)
            check_snake_case(external_id, f"{external_path}.id", errors)
            require_string(external, "label", external_path, errors)
            if external_id:
                if external_id in external_ids:
                    errors.append(f"{external_path}.id duplicates external: {external_id}")
                external_ids.add(external_id)

    connectors = expect_list(root.get("connectors"), "connectors", errors)
    connected_ports: set[str] = set()
    connector_ids: set[str] = set()
    if connectors is not None:
        if not connectors:
            errors.append("connectors must include at least one directed external connector")
        for index, connector_value in enumerate(connectors):
            connector_path = f"connectors[{index}]"
            connector = expect_mapping(connector_value, connector_path, errors)
            if connector is None:
                continue
            check_allowed_fields(connector, ALLOWED_CONNECTOR_FIELDS, connector_path, errors)
            connector_id = require_string(connector, "id", connector_path, errors)
            check_snake_case(connector_id, f"{connector_path}.id", errors)
            if connector_id:
                if connector_id in connector_ids:
                    errors.append(f"{connector_path}.id duplicates connector: {connector_id}")
                connector_ids.add(connector_id)

            connector_type = connector.get("type")
            if connector_type != "external":
                errors.append(f"{connector_path}.type must be external in this minimal slice")

            source = parse_endpoint(connector.get("source"), f"{connector_path}.source", external_ids, port_ids, errors)
            target = parse_endpoint(connector.get("target"), f"{connector_path}.target", external_ids, port_ids, errors)
            if source is not None and target is not None:
                endpoint_types = {source[0], target[0]}
                if endpoint_types != {"external", "port"}:
                    errors.append(f"{connector_path} must connect one external and one component port")
                for endpoint_type, endpoint_id in (source, target):
                    if endpoint_type == "port":
                        connected_ports.add(endpoint_id)

            if "evidence" not in connector:
                errors.append(f"{connector_path}.evidence is required")
            else:
                check_evidence(connector.get("evidence"), f"{connector_path}.evidence", errors)

    for port_id in sorted(port_ids - connected_ports):
        errors.append(f"component port {port_id} must participate in a connector")

    return errors


def model_index(model: dict[str, object]) -> tuple[dict[str, object], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    component = model["component"]
    assert isinstance(component, dict)
    ports = {
        str(port["id"]): port
        for port in component.get("ports", [])
        if isinstance(port, dict) and "id" in port
    }
    externals = {
        str(external["id"]): external
        for external in model.get("externals", [])
        if isinstance(external, dict) and "id" in external
    }
    return component, ports, externals


def endpoint_label(
    endpoint: dict[str, object],
    ports: dict[str, dict[str, object]],
    externals: dict[str, dict[str, object]],
) -> str:
    if "external" in endpoint:
        return str(externals[str(endpoint["external"])]["label"])
    return str(ports[str(endpoint["port"])]["label"])


def render_svg(model: dict[str, object]) -> str:
    component, ports, externals = model_index(model)
    connectors = model.get("connectors", [])
    assert isinstance(connectors, list)

    rows = max(len(ports), len(externals), 1)
    canvas_width = 720
    canvas_height = max(360, 290 + (rows - 1) * 70)
    component_x = 250
    component_y = 70
    component_width = 390
    component_height = canvas_height - 140
    port_x = 220
    external_x = 60
    port_width = 120
    port_height = 44
    external_width = 130
    external_height = 64

    port_positions: dict[str, tuple[int, int]] = {}
    for index, port_id in enumerate(ports):
        port_positions[port_id] = (port_x, 160 + index * 70)

    external_positions: dict[str, tuple[int, int]] = {}
    for index, external_id in enumerate(externals):
        external_positions[external_id] = (external_x, 150 + index * 70)

    direction_labels = [
        f"{endpoint_label(connector['source'], ports, externals)} -> "
        f"{endpoint_label(connector['target'], ports, externals)}"
        for connector in connectors
        if isinstance(connector, dict)
    ]

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">Whitebox Component Diagram: {html.escape(str(component["label"]))}</title>',
        f'  <desc id="desc">{html.escape("; ".join(direction_labels))}</desc>',
        "  <defs>",
        '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#1f2937" />',
        "    </marker>",
        "  </defs>",
        f'  <rect x="{component_x}" y="{component_y}" width="{component_width}" height="{component_height}" rx="8" fill="#ffffff" stroke="#1f2937" stroke-width="2" />',
        f'  <text x="{component_x + component_width // 2}" y="{component_y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#111827">{html.escape(str(component["label"]))}</text>',
    ]

    for port_id, port in ports.items():
        x, y = port_positions[port_id]
        lines.extend(
            [
                f'  <rect x="{x}" y="{y}" width="{port_width}" height="{port_height}" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2" />',
                f'  <text x="{x + port_width // 2}" y="{y + 27}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#1e3a8a">{html.escape(str(port["label"]))}</text>',
            ]
        )

    for external_id, external in externals.items():
        x, y = external_positions[external_id]
        lines.extend(
            [
                f'  <rect x="{x}" y="{y}" width="{external_width}" height="{external_height}" rx="8" fill="#f9fafb" stroke="#4b5563" stroke-width="2" />',
                f'  <text x="{x + external_width // 2}" y="{y + 37}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#111827">{html.escape(str(external["label"]))}</text>',
            ]
        )

    for connector in connectors:
        assert isinstance(connector, dict)
        source = connector["source"]
        target = connector["target"]
        assert isinstance(source, dict)
        assert isinstance(target, dict)
        source_label = endpoint_label(source, ports, externals)
        target_label = endpoint_label(target, ports, externals)
        direction_label = f"{source_label} -> {target_label}"

        if "external" in source:
            external_id = str(source["external"])
            port_id = str(target["port"])
            start_x = external_positions[external_id][0] + external_width
            start_y = external_positions[external_id][1] + external_height // 2
            end_x = port_positions[port_id][0]
            end_y = port_positions[port_id][1] + port_height // 2
        else:
            port_id = str(source["port"])
            external_id = str(target["external"])
            start_x = port_positions[port_id][0]
            start_y = port_positions[port_id][1] + port_height // 2
            end_x = external_positions[external_id][0] + external_width
            end_y = external_positions[external_id][1] + external_height // 2

        label_x = (start_x + end_x) // 2
        label_y = min(start_y, end_y) - 37
        connector_label_y = max(start_y, end_y) + 50
        lines.extend(
            [
                f'  <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="#1f2937" stroke-width="2" marker-end="url(#arrowhead)" />',
                f'  <text x="{label_x}" y="{label_y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#374151">{html.escape(direction_label)}</text>',
            ]
        )
        label = connector.get("label")
        if isinstance(label, str) and label.strip():
            lines.append(
                f'  <text x="{label_x}" y="{connector_label_y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">{html.escape(label)}</text>'
            )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def check_valid_fixture(path: Path) -> list[str]:
    errors: list[str] = []
    model, load_errors = load_source_model(path)
    if load_errors:
        return load_errors

    validation_errors = validate_source_model(model)
    if validation_errors:
        return [f"{rel(path)} should be valid but failed: {error}" for error in validation_errors]

    assert isinstance(model, dict)
    svg = render_svg(model)
    expected_svg_path = path.with_suffix(".svg")
    if not expected_svg_path.exists():
        errors.append(f"{rel(expected_svg_path)} is missing")
    elif svg != read_text(expected_svg_path):
        errors.append(f"{rel(path)} rendered SVG differs from {rel(expected_svg_path)}")

    component, ports, externals = model_index(model)
    required_text = [str(component["label"])]
    required_text.extend(str(port["label"]) for port in ports.values())
    required_text.extend(str(external["label"]) for external in externals.values())
    for connector in model["connectors"]:
        assert isinstance(connector, dict)
        assert isinstance(connector["source"], dict)
        assert isinstance(connector["target"], dict)
        required_text.append(
            f"{endpoint_label(connector['source'], ports, externals)} -> "
            f"{endpoint_label(connector['target'], ports, externals)}"
        )

    for text in required_text:
        if html.escape(text) not in svg:
            errors.append(f"{rel(path)} SVG must contain reader-visible text {text!r}")

    return errors


def check_invalid_fixture(path: Path) -> list[str]:
    model, load_errors = load_source_model(path)
    if load_errors:
        return load_errors

    validation_errors = validate_source_model(model)
    if not validation_errors:
        return [f"{rel(path)} should be invalid but passed validation"]

    expected_errors_path = path.parent / path.name.replace(".whitebox.yaml", ".errors.txt")
    if not expected_errors_path.exists():
        return [f"{rel(expected_errors_path)} is missing"]

    actual = "\n".join(validation_errors)
    errors: list[str] = []
    for expected in read_text(expected_errors_path).splitlines():
        if expected and expected not in actual:
            errors.append(f"{rel(path)} validation errors must contain {expected!r}")
    return errors


def check_fixtures() -> int:
    errors: list[str] = []
    valid_paths = sorted((FIXTURE_ROOT / "valid").glob("*.whitebox.yaml"))
    invalid_paths = sorted((FIXTURE_ROOT / "invalid").glob("*.whitebox.yaml"))
    valid_names = {path.name for path in valid_paths}
    invalid_names = {path.name for path in invalid_paths}

    if not valid_paths:
        errors.append(f"{rel(FIXTURE_ROOT / 'valid')} must include at least one valid fixture")
    if not invalid_paths:
        errors.append(f"{rel(FIXTURE_ROOT / 'invalid')} must include invalid fixtures")
    for fixture_name in sorted(REQUIRED_VALID_FIXTURES - valid_names):
        errors.append(f"missing required valid Whitebox fixture: {fixture_name}")
    for fixture_name in sorted(REQUIRED_INVALID_FIXTURES - invalid_names):
        errors.append(f"missing required invalid Whitebox fixture: {fixture_name}")

    for path in valid_paths:
        errors.extend(check_valid_fixture(path))
    for path in invalid_paths:
        errors.extend(check_invalid_fixture(path))

    if errors:
        print("Whitebox fixture check found problems:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Checked {len(valid_paths)} valid Whitebox fixture(s).")
    print(f"Checked {len(invalid_paths)} invalid Whitebox fixture(s).")
    print("Validated minimal topology-only source models and SVG rendering.")
    return 0


def validate_command(source_path: Path) -> int:
    model, load_errors = load_source_model(source_path)
    errors = load_errors or validate_source_model(model)
    if errors:
        print(f"{rel(source_path)} is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{rel(source_path)} is valid.")
    return 0


def render_command(source_path: Path, output_path: Path) -> int:
    model, load_errors = load_source_model(source_path)
    errors = load_errors or validate_source_model(model)
    if errors:
        print(f"{rel(source_path)} is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    assert isinstance(model, dict)
    svg = render_svg(model)
    if str(output_path) == "-":
        sys.stdout.write(svg)
    else:
        output_path.write_text(svg, encoding="utf-8")
        print(f"Wrote {rel(output_path)}")
    return 0


def usage() -> None:
    print(
        "Usage:\n"
        "  python3 scripts/check_whitebox_fixtures.py\n"
        "  python3 scripts/check_whitebox_fixtures.py validate <source.whitebox.yaml>\n"
        "  python3 scripts/check_whitebox_fixtures.py render <source.whitebox.yaml> <output.svg|->"
    )


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        return check_fixtures()
    if len(argv) == 3 and argv[1] == "validate":
        return validate_command(Path(argv[2]))
    if len(argv) == 4 and argv[1] == "render":
        return render_command(Path(argv[2]), Path(argv[3]))
    usage()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
