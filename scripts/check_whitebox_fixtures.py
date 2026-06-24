#!/usr/bin/env python3
"""Validate and render Whitebox Component Diagram fixtures."""

from __future__ import annotations

from dataclasses import dataclass
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised only on lean hosts.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "whitebox" / "fixtures"

REQUIRED_VALID_FIXTURES = {
    "both-interface-roles.whitebox.yaml",
    "dense-complexity-signal.whitebox.yaml",
    "delegation-input.whitebox.yaml",
    "delegation-output.whitebox.yaml",
    "file-evidence-lines-symbol.whitebox.yaml",
    "interface-assembly.whitebox.yaml",
    "internal-assembly.whitebox.yaml",
    "minimal-empty.whitebox.yaml",
    "multiple-interfaces.whitebox.yaml",
    "provided-interface.whitebox.yaml",
    "required-interface.whitebox.yaml",
    "user-evidence.whitebox.yaml",
}
REQUIRED_INVALID_FIXTURES = {
    "absolute-evidence-path.whitebox.yaml",
    "assembly-boundary-port.whitebox.yaml",
    "connector-direction-field.whitebox.yaml",
    "delegation-external-to-part.whitebox.yaml",
    "external-to-internal.whitebox.yaml",
    "invalid-interface-assembly-endpoints.whitebox.yaml",
    "invalid-interface-role-references.whitebox.yaml",
    "malformed-evidence-lines.whitebox.yaml",
    "missing-component-evidence.whitebox.yaml",
    "missing-connector-evidence.whitebox.yaml",
    "missing-evidence-note.whitebox.yaml",
    "missing-required-label.whitebox.yaml",
    "mixed-evidence-shape.whitebox.yaml",
    "non-snake-case-id.whitebox.yaml",
    "nonexistent-evidence-path.whitebox.yaml",
    "source-layout-hint.whitebox.yaml",
    "source-view-selection.whitebox.yaml",
    "source-complexity-conclusion.whitebox.yaml",
    "unconnected-port.whitebox.yaml",
    "unsupported-top-level-field.whitebox.yaml",
    "whole-component-connector.whitebox.yaml",
    "whole-part-connector.whitebox.yaml",
}
ALLOWED_TOP_LEVEL = {"kind", "version", "interfaces", "component", "parts", "externals", "connectors"}
ALLOWED_INTERFACE_FIELDS = {"id", "label", "description"}
ALLOWED_COMPONENT_FIELDS = {"id", "label", "evidence", "ports"}
ALLOWED_PART_FIELDS = {"id", "label", "evidence", "ports"}
ALLOWED_PORT_FIELDS = {"id", "label", "evidence", "provides", "requires"}
ALLOWED_EXTERNAL_FIELDS = {"id", "label", "evidence"}
ALLOWED_CONNECTOR_FIELDS = {"id", "type", "from", "to", "label", "evidence"}
ALLOWED_FILE_EVIDENCE_FIELDS = {"path", "note", "lines", "symbol"}
ALLOWED_USER_EVIDENCE_FIELDS = {"source", "note"}
ALLOWED_INTERFACE_ROLE_ENDPOINT_FIELDS = {"owner", "port", "interface", "role"}
CONNECTOR_TYPES = {"external", "delegation", "assembly", "interfaceAssembly"}
INTERFACE_ROLES = {"provided", "required"}
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
COMPLEXITY_CONCLUSION_FIELDS = {
    "complexity",
    "complexity_score",
    "complexity_signal",
    "diagram_complexity",
    "diagram_complexity_signal",
    "refactor",
    "refactor_conclusion",
    "refactor_verdict",
    "refactoring",
}
VIEW_SELECTION_FIELDS = {
    "derivedViews",
    "include_connectors",
    "include_parts",
    "views",
}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
LINE_RANGE = re.compile(r"^([1-9][0-9]*)(?:-([1-9][0-9]*))?$")
DENSE_PORT_THRESHOLD = 10
DENSE_INTERFACE_ROLE_THRESHOLD = 8
DENSE_CONNECTOR_THRESHOLD = 10
DENSE_PART_THRESHOLD = 6
APPROX_TEXT_CHAR_WIDTH = 7
SIMPLE_RENDER_BACKEND = "simple"
ELK_RENDER_BACKEND = "elk"
AVAILABLE_RENDER_BACKENDS = frozenset({SIMPLE_RENDER_BACKEND, ELK_RENDER_BACKEND})
ELK_LAYOUT_HELPER = ROOT / "scripts" / "elk_whitebox_layout.mjs"
ELK_PACKAGE_ENTRY = ROOT / "node_modules" / "elkjs" / "lib" / "elk.bundled.js"


@dataclass(frozen=True)
class Endpoint:
    kind: str
    owner_id: str
    port_id: str | None = None
    owner_kind: str | None = None
    interface_id: str | None = None
    role: str | None = None


@dataclass(frozen=True)
class DiagramComplexity:
    component_ports: int
    part_ports: int
    parts: int
    externals: int
    interfaces: int
    interface_roles: int
    connectors: int
    warnings: tuple[str, ...]

    @property
    def total_ports(self) -> int:
        return self.component_ports + self.part_ports

    @property
    def dense(self) -> bool:
        return bool(self.warnings)


@dataclass(frozen=True)
class RenderBackend:
    name: str


class WhiteboxRenderError(RuntimeError):
    """Raised when a selected Whitebox render backend cannot produce SVG."""


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


def check_source_model_forbidden_fields(value: object, field_path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{field_path}.{key}" if field_path else str(key)
            if key in LAYOUT_HINT_FIELDS:
                errors.append(f"source model must not contain layout hint field: {child_path}")
            if key in COMPLEXITY_CONCLUSION_FIELDS:
                errors.append(f"source model must not contain complexity or refactor conclusion field: {child_path}")
            if key in VIEW_SELECTION_FIELDS:
                errors.append(f"source model must not contain view-selection field: {child_path}")
            check_source_model_forbidden_fields(child, child_path, errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_source_model_forbidden_fields(child, f"{field_path}[{index}]", errors)


def check_snake_case(value: str | None, field_path: str, errors: list[str]) -> None:
    if value is not None and not SNAKE_CASE.fullmatch(value):
        errors.append(f"{field_path} must be snake_case")


def check_line_range(value: object, field_path: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{field_path} must be a line string like '12' or '12-18'")
        return

    match = LINE_RANGE.fullmatch(value)
    if match is None:
        errors.append(f"{field_path} must be a line string like '12' or '12-18'")
        return

    start, end = match.groups()
    if end is not None and int(start) > int(end):
        errors.append(f"{field_path} must be a line string like '12' or '12-18'")


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

        if evidence.get("source") == "user":
            if any(key in evidence for key in ("path", "lines", "symbol")):
                errors.append(f"{entry_path} user evidence must not include path, lines, or symbol")
            check_allowed_fields(evidence, ALLOWED_USER_EVIDENCE_FIELDS, entry_path, errors)
            require_string(evidence, "note", entry_path, errors)
            continue

        if "source" in evidence:
            errors.append(f"{entry_path}.source must be user")
            check_allowed_fields(evidence, ALLOWED_USER_EVIDENCE_FIELDS | ALLOWED_FILE_EVIDENCE_FIELDS, entry_path, errors)
            continue

        if "path" not in evidence:
            errors.append(f"{entry_path} must include either path or source: user")
            check_allowed_fields(evidence, ALLOWED_USER_EVIDENCE_FIELDS | ALLOWED_FILE_EVIDENCE_FIELDS, entry_path, errors)
            continue

        check_allowed_fields(evidence, ALLOWED_FILE_EVIDENCE_FIELDS, entry_path, errors)
        path_value = require_string(evidence, "path", entry_path, errors)
        require_string(evidence, "note", entry_path, errors)
        if "lines" in evidence:
            check_line_range(evidence.get("lines"), f"{entry_path}.lines", errors)
        if "symbol" in evidence:
            require_string(evidence, "symbol", entry_path, errors)

        if path_value:
            evidence_path = Path(path_value)
            if evidence_path.is_absolute() or ".." in evidence_path.parts:
                errors.append(f"{entry_path}.path must be repo-relative")
            elif not (ROOT / evidence_path).exists():
                errors.append(f"{entry_path}.path does not exist: {path_value}")


def check_interface_references(
    value: object,
    field_path: str,
    interface_ids: set[str],
    errors: list[str],
) -> list[str]:
    entries = expect_list(value, field_path, errors)
    if entries is None:
        return []
    if not entries:
        errors.append(f"{field_path} must include at least one interface id")
        return []

    interface_refs: list[str] = []
    seen_refs: set[str] = set()
    for index, entry in enumerate(entries):
        entry_path = f"{field_path}[{index}]"
        if not isinstance(entry, str) or not entry.strip():
            errors.append(f"{entry_path} must be an interface id")
            continue
        interface_id = entry
        check_snake_case(interface_id, entry_path, errors)
        if interface_id not in interface_ids:
            errors.append(f"{entry_path} references unknown interface: {interface_id}")
            continue
        if interface_id in seen_refs:
            errors.append(f"{entry_path} duplicates interface role: {interface_id}")
            continue
        seen_refs.add(interface_id)
        interface_refs.append(interface_id)
    return interface_refs


def collect_port_interface_roles(
    port: dict[str, object],
    port_path: str,
    owner_id: str | None,
    port_id: str | None,
    interface_ids: set[str],
    interface_roles: set[tuple[str, str, str, str]],
    errors: list[str],
) -> None:
    if owner_id is None or port_id is None:
        return

    for role_field, role in (("provides", "provided"), ("requires", "required")):
        if role_field not in port:
            continue
        for interface_id in check_interface_references(
            port.get(role_field),
            f"{port_path}.{role_field}",
            interface_ids,
            errors,
        ):
            interface_roles.add((owner_id, port_id, interface_id, role))


def parse_endpoint(
    value: object,
    field_path: str,
    external_ids: set[str],
    component_id: str | None,
    component_port_ids: set[str],
    part_ids: set[str],
    part_port_ids: set[tuple[str, str]],
    interface_ids: set[str],
    interface_roles: set[tuple[str, str, str, str]],
    errors: list[str],
) -> Endpoint | None:
    if isinstance(value, str) and value.strip():
        endpoint_value = value
        if "." not in endpoint_value:
            if endpoint_value in external_ids:
                return Endpoint(kind="external", owner_id=endpoint_value)
            if endpoint_value == component_id:
                errors.append(f"{field_path} cannot target a whole component; use an owner.port endpoint")
                return None
            if endpoint_value in part_ids:
                errors.append(f"{field_path} cannot target a whole part; use an owner.port endpoint")
                return None
            errors.append(f"{field_path} references unknown external or owner.port endpoint: {endpoint_value}")
            return None

        owner_id, port_id = endpoint_value.split(".", 1)
        if owner_id == component_id:
            if port_id not in component_port_ids:
                errors.append(f"{field_path} references unknown port on component {owner_id}: {port_id}")
                return None
            return Endpoint(kind="component_port", owner_id=owner_id, port_id=port_id, owner_kind="component")
        if owner_id in part_ids:
            if (owner_id, port_id) not in part_port_ids:
                errors.append(f"{field_path} references unknown port on part {owner_id}: {port_id}")
                return None
            return Endpoint(kind="part_port", owner_id=owner_id, port_id=port_id, owner_kind="part")
        if owner_id in external_ids:
            errors.append(f"{field_path} cannot target a port on external {owner_id}")
            return None
        errors.append(f"{field_path} references unknown owner: {owner_id}")
        return None

    interface_role = expect_mapping(value, field_path, errors)
    if interface_role is None:
        return None
    check_allowed_fields(interface_role, ALLOWED_INTERFACE_ROLE_ENDPOINT_FIELDS, field_path, errors)
    owner_id = require_string(interface_role, "owner", field_path, errors)
    port_id = require_string(interface_role, "port", field_path, errors)
    interface_id = require_string(interface_role, "interface", field_path, errors)
    role = require_string(interface_role, "role", field_path, errors)

    owner_kind: str | None = None
    if owner_id:
        if owner_id == component_id:
            owner_kind = "component"
            if port_id and port_id not in component_port_ids:
                errors.append(f"{field_path}.port references unknown port on component {owner_id}: {port_id}")
                return None
        elif owner_id in part_ids:
            owner_kind = "part"
            if port_id and (owner_id, port_id) not in part_port_ids:
                errors.append(f"{field_path}.port references unknown port on part {owner_id}: {port_id}")
                return None
        elif owner_id in external_ids:
            errors.append(f"{field_path}.owner cannot reference external {owner_id}")
            return None
        else:
            errors.append(f"{field_path}.owner references unknown owner: {owner_id}")
            return None

    if interface_id:
        check_snake_case(interface_id, f"{field_path}.interface", errors)
        if interface_id not in interface_ids:
            errors.append(f"{field_path}.interface references unknown interface: {interface_id}")
            return None

    if role and role not in INTERFACE_ROLES:
        errors.append(f"{field_path}.role must be provided or required")
        return None

    if owner_id and port_id and interface_id and role:
        role_key = (owner_id, port_id, interface_id, role)
        if role_key not in interface_roles:
            errors.append(
                f"{field_path} references undeclared {role} interface role: "
                f"{owner_id}.{port_id}.{interface_id}"
            )
            return None
        return Endpoint(
            kind="interface_role",
            owner_id=owner_id,
            port_id=port_id,
            owner_kind=owner_kind,
            interface_id=interface_id,
            role=role,
        )
    return None


def mark_connected_port(
    endpoint: Endpoint,
    connected_component_ports: set[str],
    connected_part_ports: set[tuple[str, str]],
) -> None:
    if endpoint.kind == "component_port" and endpoint.port_id is not None:
        connected_component_ports.add(endpoint.port_id)
    elif endpoint.kind == "part_port" and endpoint.port_id is not None:
        connected_part_ports.add((endpoint.owner_id, endpoint.port_id))
    elif endpoint.kind == "interface_role" and endpoint.port_id is not None:
        if endpoint.owner_kind == "component":
            connected_component_ports.add(endpoint.port_id)
        elif endpoint.owner_kind == "part":
            connected_part_ports.add((endpoint.owner_id, endpoint.port_id))


def connector_endpoint_error(connector_type: object, connector_path: str) -> str:
    if connector_type == "external":
        return f"{connector_path} external connector must connect one external and one component port"
    if connector_type == "delegation":
        return f"{connector_path} delegation connector must connect one component port and one part port"
    if connector_type == "assembly":
        return f"{connector_path} assembly connector must connect two part ports"
    if connector_type == "interfaceAssembly":
        return f"{connector_path} interfaceAssembly connector must connect a required interface role to a provided interface role"
    return f"{connector_path}.type must be external, delegation, assembly, or interfaceAssembly"


def validate_source_model(model: object) -> list[str]:
    errors: list[str] = []
    root = expect_mapping(model, "source model", errors)
    if root is None:
        return errors

    check_source_model_forbidden_fields(root, "", errors)

    for key in sorted(root):
        if key not in ALLOWED_TOP_LEVEL:
            errors.append(f"unsupported top-level field: {key}")

    if root.get("kind") != "whitebox_component_diagram":
        errors.append("kind must be whitebox_component_diagram")
    if root.get("version") != 1:
        errors.append("version must be 1")

    interface_ids: set[str] = set()
    if "interfaces" in root:
        interfaces = expect_list(root.get("interfaces"), "interfaces", errors)
        if interfaces is not None:
            if not interfaces:
                errors.append("interfaces must include at least one interface definition")
            for index, interface_value in enumerate(interfaces):
                interface_path = f"interfaces[{index}]"
                interface = expect_mapping(interface_value, interface_path, errors)
                if interface is None:
                    continue
                check_allowed_fields(interface, ALLOWED_INTERFACE_FIELDS, interface_path, errors)
                interface_id = require_string(interface, "id", interface_path, errors)
                check_snake_case(interface_id, f"{interface_path}.id", errors)
                require_string(interface, "label", interface_path, errors)
                if "description" in interface:
                    require_string(interface, "description", interface_path, errors)
                if interface_id:
                    if interface_id in interface_ids:
                        errors.append(f"{interface_path}.id duplicates interface: {interface_id}")
                    interface_ids.add(interface_id)

    component = expect_mapping(root.get("component"), "component", errors)
    component_id: str | None = None
    component_port_ids: set[str] = set()
    interface_roles: set[tuple[str, str, str, str]] = set()
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
                    if port_id in component_port_ids:
                        errors.append(f"{port_path}.id duplicates component port: {port_id}")
                    component_port_ids.add(port_id)
                collect_port_interface_roles(
                    port,
                    port_path,
                    component_id,
                    port_id,
                    interface_ids,
                    interface_roles,
                    errors,
                )

    part_ids: set[str] = set()
    part_port_ids: set[tuple[str, str]] = set()
    if "parts" in root:
        parts = expect_list(root.get("parts"), "parts", errors)
        if parts is not None:
            if not parts:
                errors.append("parts must include at least one internal part")
            for index, part_value in enumerate(parts):
                part_path = f"parts[{index}]"
                part = expect_mapping(part_value, part_path, errors)
                if part is None:
                    continue
                check_allowed_fields(part, ALLOWED_PART_FIELDS, part_path, errors)
                part_id = require_string(part, "id", part_path, errors)
                check_snake_case(part_id, f"{part_path}.id", errors)
                require_string(part, "label", part_path, errors)
                if part_id:
                    if part_id in part_ids:
                        errors.append(f"{part_path}.id duplicates part: {part_id}")
                    part_ids.add(part_id)
                if "evidence" in part:
                    check_evidence(part.get("evidence"), f"{part_path}.evidence", errors)

                ports = expect_list(part.get("ports"), f"{part_path}.ports", errors)
                if ports is not None:
                    if not ports:
                        errors.append(f"{part_path}.ports must include at least one part port")
                    part_local_port_ids: set[str] = set()
                    for port_index, port_value in enumerate(ports):
                        port_path = f"{part_path}.ports[{port_index}]"
                        port = expect_mapping(port_value, port_path, errors)
                        if port is None:
                            continue
                        check_allowed_fields(port, ALLOWED_PORT_FIELDS, port_path, errors)
                        port_id = require_string(port, "id", port_path, errors)
                        check_snake_case(port_id, f"{port_path}.id", errors)
                        require_string(port, "label", port_path, errors)
                        if part_id and port_id:
                            if port_id in part_local_port_ids:
                                errors.append(f"{port_path}.id duplicates port on part {part_id}: {port_id}")
                            part_local_port_ids.add(port_id)
                            part_port_ids.add((part_id, port_id))
                        collect_port_interface_roles(
                            port,
                            port_path,
                            part_id,
                            port_id,
                            interface_ids,
                            interface_roles,
                            errors,
                        )

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
    connected_component_ports: set[str] = set()
    connected_part_ports: set[tuple[str, str]] = set()
    connector_ids: set[str] = set()
    if connectors is not None:
        if not connectors:
            errors.append("connectors must include at least one directed connector")
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
            if connector_type not in CONNECTOR_TYPES:
                errors.append(connector_endpoint_error(connector_type, connector_path))

            source = parse_endpoint(
                connector.get("from"),
                f"{connector_path}.from",
                external_ids,
                component_id,
                component_port_ids,
                part_ids,
                part_port_ids,
                interface_ids,
                interface_roles,
                errors,
            )
            target = parse_endpoint(
                connector.get("to"),
                f"{connector_path}.to",
                external_ids,
                component_id,
                component_port_ids,
                part_ids,
                part_port_ids,
                interface_ids,
                interface_roles,
                errors,
            )
            if source is not None and target is not None:
                endpoint_kinds = {source.kind, target.kind}
                connector_is_valid = False
                connector_error_reported = False
                if connector_type == "external":
                    connector_is_valid = endpoint_kinds == {"external", "component_port"}
                elif connector_type == "delegation":
                    connector_is_valid = endpoint_kinds == {"component_port", "part_port"}
                elif connector_type == "assembly":
                    connector_is_valid = source.kind == "part_port" and target.kind == "part_port"
                elif connector_type == "interfaceAssembly":
                    if source.kind == "interface_role" and target.kind == "interface_role":
                        connector_is_valid = (
                            source.role == "required"
                            and target.role == "provided"
                            and source.interface_id == target.interface_id
                        )
                        if (
                            source.role == "required"
                            and target.role == "provided"
                            and source.interface_id != target.interface_id
                        ):
                            errors.append(
                                f"{connector_path} interfaceAssembly connector must connect matching interface ids"
                            )
                            connector_error_reported = True

                if connector_is_valid:
                    mark_connected_port(source, connected_component_ports, connected_part_ports)
                    mark_connected_port(target, connected_component_ports, connected_part_ports)
                elif connector_type in CONNECTOR_TYPES and not connector_error_reported:
                    errors.append(connector_endpoint_error(connector_type, connector_path))

            if "evidence" not in connector:
                errors.append(f"{connector_path}.evidence is required")
            else:
                check_evidence(connector.get("evidence"), f"{connector_path}.evidence", errors)

    for port_id in sorted(component_port_ids - connected_component_ports):
        errors.append(f"component port {port_id} must participate in a connector")
    for part_id, port_id in sorted(part_port_ids - connected_part_ports):
        errors.append(f"part port {part_id}.{port_id} must participate in a connector")

    return errors


def model_index(
    model: dict[str, object],
) -> tuple[
    dict[str, object],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[tuple[str, str], dict[str, object]],
    dict[str, dict[str, object]],
]:
    component = model["component"]
    assert isinstance(component, dict)
    ports = {
        str(port["id"]): port
        for port in component.get("ports", [])
        if isinstance(port, dict) and "id" in port
    }
    interfaces = {
        str(interface["id"]): interface
        for interface in model.get("interfaces", [])
        if isinstance(interface, dict) and "id" in interface
    }
    parts = {
        str(part["id"]): part
        for part in model.get("parts", [])
        if isinstance(part, dict) and "id" in part
    }
    part_ports: dict[tuple[str, str], dict[str, object]] = {}
    for part_id, part in parts.items():
        for port in part.get("ports", []):
            if isinstance(port, dict) and "id" in port:
                part_ports[(part_id, str(port["id"]))] = port
    externals = {
        str(external["id"]): external
        for external in model.get("externals", [])
        if isinstance(external, dict) and "id" in external
    }
    return component, interfaces, ports, parts, part_ports, externals


def endpoint_label(
    endpoint: object,
    component: dict[str, object],
    interfaces: dict[str, dict[str, object]],
    ports: dict[str, dict[str, object]],
    parts: dict[str, dict[str, object]],
    part_ports: dict[tuple[str, str], dict[str, object]],
    externals: dict[str, dict[str, object]],
) -> str:
    if isinstance(endpoint, str):
        if "." not in endpoint:
            return str(externals[endpoint]["label"])
        owner_id, port_id = endpoint.split(".", 1)
        if owner_id == str(component["id"]):
            return str(ports[port_id]["label"])
        return f'{parts[owner_id]["label"]}.{part_ports[(owner_id, port_id)]["label"]}'

    assert isinstance(endpoint, dict)
    owner_id = str(endpoint["owner"])
    port_id = str(endpoint["port"])
    interface_id = str(endpoint["interface"])
    role = str(endpoint["role"])
    if owner_id == str(component["id"]):
        owner_label = str(component["label"])
        port_label = str(ports[port_id]["label"])
    else:
        owner_label = str(parts[owner_id]["label"])
        port_label = str(part_ports[(owner_id, port_id)]["label"])
    interface_label = str(interfaces[interface_id]["label"])
    return f"{owner_label}.{port_label} {role} {interface_label}"


def endpoint_role_key(endpoint: object) -> tuple[str, str, str, str]:
    assert isinstance(endpoint, dict)
    return (
        str(endpoint["owner"]),
        str(endpoint["port"]),
        str(endpoint["interface"]),
        str(endpoint["role"]),
    )


def port_interface_ids(port: dict[str, object], field: str) -> list[str]:
    value = port.get(field, [])
    if not isinstance(value, list):
        return []
    return [str(interface_id) for interface_id in value if isinstance(interface_id, str)]


def port_interface_count(port: dict[str, object]) -> int:
    return len(port_interface_ids(port, "provides")) + len(port_interface_ids(port, "requires"))


def diagram_complexity(model: dict[str, object]) -> DiagramComplexity:
    _, interfaces, ports, parts, part_ports, externals = model_index(model)
    connectors = model.get("connectors", [])
    connector_count = len([connector for connector in connectors if isinstance(connector, dict)])
    interface_role_count = sum(
        port_interface_count(port)
        for port in list(ports.values()) + list(part_ports.values())
    )
    total_ports = len(ports) + len(part_ports)
    warnings: list[str] = []
    if total_ports >= DENSE_PORT_THRESHOLD:
        warnings.append(f"ports>={DENSE_PORT_THRESHOLD}")
    if interface_role_count >= DENSE_INTERFACE_ROLE_THRESHOLD:
        warnings.append(f"interface_roles>={DENSE_INTERFACE_ROLE_THRESHOLD}")
    if connector_count >= DENSE_CONNECTOR_THRESHOLD:
        warnings.append(f"connectors>={DENSE_CONNECTOR_THRESHOLD}")
    if len(parts) >= DENSE_PART_THRESHOLD:
        warnings.append(f"parts>={DENSE_PART_THRESHOLD}")
    return DiagramComplexity(
        component_ports=len(ports),
        part_ports=len(part_ports),
        parts=len(parts),
        externals=len(externals),
        interfaces=len(interfaces),
        interface_roles=interface_role_count,
        connectors=connector_count,
        warnings=tuple(warnings),
    )


def format_complexity_metrics(complexity: DiagramComplexity) -> str:
    return (
        f"ports={complexity.total_ports}; "
        f"component_ports={complexity.component_ports}; "
        f"part_ports={complexity.part_ports}; "
        f"parts={complexity.parts}; "
        f"externals={complexity.externals}; "
        f"interfaces={complexity.interfaces}; "
        f"interface_roles={complexity.interface_roles}; "
        f"connectors={complexity.connectors}"
    )


def format_complexity_signal(complexity: DiagramComplexity) -> str:
    warnings = ",".join(complexity.warnings) if complexity.warnings else "none"
    return f"Diagram Complexity Signal raw metrics: {format_complexity_metrics(complexity)}; warnings={warnings}"


def svg_dimensions(svg: str) -> tuple[int, int] | None:
    match = re.search(r'<svg\b[^>]*\bwidth="([0-9]+)"\s+height="([0-9]+)"', svg)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2))


def select_render_backend(backend: str = SIMPLE_RENDER_BACKEND) -> RenderBackend:
    if backend not in AVAILABLE_RENDER_BACKENDS:
        available = ", ".join(sorted(AVAILABLE_RENDER_BACKENDS))
        raise ValueError(f"unsupported Whitebox render backend: {backend}; available backends: {available}")
    return RenderBackend(name=backend)


def render_svg(model: dict[str, object], backend: str = SIMPLE_RENDER_BACKEND) -> str:
    selected_backend = select_render_backend(backend)
    if selected_backend.name == SIMPLE_RENDER_BACKEND:
        return render_simple_svg(model)
    if selected_backend.name == ELK_RENDER_BACKEND:
        return render_elk_svg(model)
    raise AssertionError(f"unhandled Whitebox render backend: {selected_backend.name}")


def require_elk_runtime() -> None:
    missing: list[str] = []
    if not ELK_LAYOUT_HELPER.exists():
        missing.append(f"ELK layout helper is missing: {rel(ELK_LAYOUT_HELPER)}")
    if shutil.which("node") is None:
        missing.append("Node.js is required for the elk Whitebox render backend")
    if not ELK_PACKAGE_ENTRY.exists():
        missing.append(
            "elkjs dependency is not installed; run npm ci during repo-wiki skill suite development or upgrade before rendering with --backend elk"
        )
    if missing:
        raise WhiteboxRenderError("; ".join(missing))


def run_elk_layout(model: dict[str, object]) -> dict[str, object]:
    require_elk_runtime()
    command = ["node", str(ELK_LAYOUT_HELPER)]
    try:
        completed = subprocess.run(
            command,
            input=json.dumps(model, sort_keys=True),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
            check=False,
        )
    except OSError as exc:
        raise WhiteboxRenderError(f"failed to start ELK layout helper: {exc}") from exc

    if completed.returncode != 0:
        diagnostic = completed.stderr.strip() or completed.stdout.strip() or f"exit code {completed.returncode}"
        raise WhiteboxRenderError(f"ELK Whitebox layout failed: {diagnostic}")
    try:
        layout = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise WhiteboxRenderError(f"ELK Whitebox layout helper returned invalid JSON: {exc}") from exc
    if not isinstance(layout, dict):
        raise WhiteboxRenderError("ELK Whitebox layout helper returned a non-object layout")
    return layout


def layout_box(layout: dict[str, object], path: str) -> tuple[int, int, int, int]:
    current: object = layout
    for segment in path.split("."):
        if not isinstance(current, dict) or segment not in current:
            raise WhiteboxRenderError(f"ELK Whitebox layout is missing geometry for {path}")
        current = current[segment]
    if not isinstance(current, dict):
        raise WhiteboxRenderError(f"ELK Whitebox layout geometry for {path} is not an object")
    try:
        return (
            round(float(current["x"])),
            round(float(current["y"])),
            round(float(current["width"])),
            round(float(current["height"])),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise WhiteboxRenderError(f"ELK Whitebox layout geometry for {path} is incomplete") from exc


def layout_edge_points(layout: dict[str, object], connector_id: str) -> list[tuple[int, int]]:
    edges = layout.get("edges")
    if not isinstance(edges, dict):
        return []
    points = edges.get(connector_id)
    if not isinstance(points, list):
        return []
    parsed: list[tuple[int, int]] = []
    for point in points:
        if (
            isinstance(point, list)
            and len(point) == 2
            and isinstance(point[0], (int, float))
            and isinstance(point[1], (int, float))
        ):
            parsed.append((round(point[0]), round(point[1])))
    return parsed


def infer_port_side(port_box: tuple[int, int, int, int], owner_box: tuple[int, int, int, int]) -> str:
    port_x, port_y, port_width, port_height = port_box
    owner_x, owner_y, owner_width, owner_height = owner_box
    center_x = port_x + port_width / 2
    center_y = port_y + port_height / 2
    distances = {
        "left": abs(center_x - owner_x),
        "right": abs(center_x - (owner_x + owner_width)),
        "top": abs(center_y - owner_y),
        "bottom": abs(center_y - (owner_y + owner_height)),
    }
    return min(distances, key=distances.get)


def box_center(box: tuple[int, int, int, int]) -> tuple[int, int]:
    x, y, width, height = box
    return x + width // 2, y + height // 2


def connector_endpoint_point(
    endpoint: object,
    component: dict[str, object],
    layout: dict[str, object],
    interface_role_positions: dict[tuple[str, str, str, str], tuple[int, int, int, int]],
) -> tuple[int, int]:
    return box_center(endpoint_box_from_layout(endpoint, component, layout, interface_role_positions))


def endpoint_box_from_layout(
    endpoint: object,
    component: dict[str, object],
    layout: dict[str, object],
    interface_role_positions: dict[tuple[str, str, str, str], tuple[int, int, int, int]],
) -> tuple[int, int, int, int]:
    component_id = str(component["id"])
    if isinstance(endpoint, str):
        if "." not in endpoint:
            return layout_box(layout, f"externals.{endpoint}")
        owner_id, port_id = endpoint.split(".", 1)
        if owner_id == component_id:
            return layout_box(layout, f"componentPorts.{port_id}")
        return layout_box(layout, f"partPorts.{owner_id}.{port_id}")
    return interface_role_positions[endpoint_role_key(endpoint)]


def render_elk_svg(model: dict[str, object]) -> str:
    layout = run_elk_layout(model)
    component, interfaces, ports, parts, part_ports, externals = model_index(model)
    connectors = model.get("connectors", [])
    assert isinstance(connectors, list)

    canvas = layout.get("canvas")
    if not isinstance(canvas, dict):
        raise WhiteboxRenderError("ELK Whitebox layout is missing canvas geometry")
    try:
        canvas_width = max(360, round(float(canvas["width"])))
        canvas_height = max(240, round(float(canvas["height"])))
    except (KeyError, TypeError, ValueError) as exc:
        raise WhiteboxRenderError("ELK Whitebox layout canvas geometry is incomplete") from exc

    component_box = layout_box(layout, "component")
    complexity = diagram_complexity(model)
    direction_labels = [
        f"{endpoint_label(connector['from'], component, interfaces, ports, parts, part_ports, externals)} -> "
        f"{endpoint_label(connector['to'], component, interfaces, ports, parts, part_ports, externals)}"
        for connector in connectors
        if isinstance(connector, dict)
    ]

    interface_role_positions: dict[tuple[str, str, str, str], tuple[int, int, int, int]] = {}
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">Whitebox Component Diagram: {html.escape(str(component["label"]))}</title>',
        f'  <desc id="desc">{html.escape("; ".join(direction_labels))}</desc>',
    ]
    if complexity.dense:
        lines.append(
            f'  <metadata data-diagram-complexity-signal="dense">{html.escape(format_complexity_signal(complexity))}</metadata>'
        )
    lines.extend([
        "  <defs>",
        '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#1f2937" />',
        "    </marker>",
        "  </defs>",
    ])

    component_x, component_y, component_width, component_height = component_box
    lines.extend([
        f'  <rect x="{component_x}" y="{component_y}" width="{component_width}" height="{component_height}" rx="8" fill="#ffffff" stroke="#1f2937" stroke-width="2" />',
        f'  <text x="{component_x + component_width // 2}" y="{component_y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#111827">{html.escape(str(component["label"]))}</text>',
    ])

    def role_offsets(count: int) -> list[int]:
        if count <= 0:
            return []
        first_offset = -((count - 1) * 26) // 2
        return [first_offset + index * 26 for index in range(count)]

    def render_interface_role(
        owner_id: str,
        port_id: str,
        interface_id: str,
        role: str,
        side: str,
        port_box: tuple[int, int, int, int],
        offset: int,
    ) -> None:
        x, y, width, height = port_box
        if side in {"left", "right"}:
            role_y = y + height // 2 + offset
            if side == "right":
                stem_start_x = x + width
                symbol_x = x + width + 30
                stem_end_x = symbol_x - 10
                label_x = symbol_x + 16
                text_anchor = "start"
            else:
                stem_start_x = x
                symbol_x = x - 30
                stem_end_x = symbol_x + 10
                label_x = symbol_x - 16
                text_anchor = "end"
            stem = f'  <line x1="{stem_start_x}" y1="{role_y}" x2="{stem_end_x}" y2="{role_y}" stroke="#6b7280" stroke-width="2" />'
            label = f'  <text x="{label_x}" y="{role_y + 4}" text-anchor="{text_anchor}" font-family="Arial, sans-serif" font-size="11" fill="#374151">{html.escape(str(interfaces[interface_id]["label"]))}</text>'
            if role == "required":
                if side == "right":
                    socket_path = f"M {symbol_x - 10} {role_y - 10} A 10 10 0 0 1 {symbol_x - 10} {role_y + 10}"
                else:
                    socket_path = f"M {symbol_x + 10} {role_y - 10} A 10 10 0 0 0 {symbol_x + 10} {role_y + 10}"
        else:
            role_x = x + width // 2 + offset
            if side == "bottom":
                stem_start_y = y + height
                symbol_y = y + height + 30
                stem_end_y = symbol_y - 10
                label_y = symbol_y + 25
                socket_path = f"M {role_x - 10} {symbol_y - 10} A 10 10 0 0 0 {role_x + 10} {symbol_y - 10}"
            else:
                stem_start_y = y
                symbol_y = y - 30
                stem_end_y = symbol_y + 10
                label_y = symbol_y - 16
                socket_path = f"M {role_x - 10} {symbol_y + 10} A 10 10 0 0 1 {role_x + 10} {symbol_y + 10}"
            symbol_x = role_x
            role_y = symbol_y
            stem = f'  <line x1="{role_x}" y1="{stem_start_y}" x2="{role_x}" y2="{stem_end_y}" stroke="#6b7280" stroke-width="2" />'
            label = f'  <text x="{role_x}" y="{label_y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#374151">{html.escape(str(interfaces[interface_id]["label"]))}</text>'

        escaped_owner = html.escape(owner_id)
        escaped_port = html.escape(port_id)
        escaped_interface = html.escape(interface_id)
        interface_role_positions[(owner_id, port_id, interface_id, role)] = (symbol_x - 10, role_y - 10, 20, 20)
        lines.append(stem)
        if role == "provided":
            lines.append(
                f'  <circle data-interface-role="provided" data-owner="{escaped_owner}" data-port="{escaped_port}" data-interface="{escaped_interface}" data-symbol-cx="{symbol_x}" data-symbol-cy="{role_y}" cx="{symbol_x}" cy="{role_y}" r="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" />'
            )
        else:
            lines.append(
                f'  <path data-interface-role="required" data-owner="{escaped_owner}" data-port="{escaped_port}" data-interface="{escaped_interface}" data-symbol-cx="{symbol_x}" data-symbol-cy="{role_y}" d="{socket_path}" fill="none" stroke="#b45309" stroke-width="2" />'
            )
        lines.append(label)

    def render_port_interface_roles(
        owner_id: str,
        owner_kind: str,
        port_id: str,
        port: dict[str, object],
        port_box: tuple[int, int, int, int],
        owner_box: tuple[int, int, int, int],
    ) -> None:
        provided_ids = port_interface_ids(port, "provides")
        required_ids = port_interface_ids(port, "requires")
        side = infer_port_side(port_box, owner_box)
        if owner_kind == "component":
            roles = [("provided", interface_id) for interface_id in provided_ids]
            roles.extend(("required", interface_id) for interface_id in required_ids)
        else:
            roles = [("required", interface_id) for interface_id in required_ids]
            roles.extend(("provided", interface_id) for interface_id in provided_ids)
        for (role, interface_id), offset in zip(roles, role_offsets(len(roles))):
            render_interface_role(owner_id, port_id, interface_id, role, side, port_box, offset)

    for port_id, port in ports.items():
        x, y, width, height = layout_box(layout, f"componentPorts.{port_id}")
        lines.extend([
            f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2" />',
            f'  <text x="{x + width // 2}" y="{y + height // 2 + 5}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#1e3a8a">{html.escape(str(port["label"]))}</text>',
        ])
        render_port_interface_roles(str(component["id"]), "component", port_id, port, (x, y, width, height), component_box)

    for part_id, part in parts.items():
        part_box = layout_box(layout, f"parts.{part_id}")
        x, y, width, height = part_box
        lines.extend([
            f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="2" />',
            f'  <text x="{x + width // 2}" y="{y + 31}" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#334155">{html.escape(str(part["label"]))}</text>',
        ])
        for port in part.get("ports", []):
            if not isinstance(port, dict) or "id" not in port:
                continue
            port_id = str(port["id"])
            port_box = layout_box(layout, f"partPorts.{part_id}.{port_id}")
            port_x, port_y, port_width, port_height = port_box
            lines.extend([
                f'  <rect x="{port_x}" y="{port_y}" width="{port_width}" height="{port_height}" rx="6" fill="#ecfdf5" stroke="#059669" stroke-width="2" />',
                f'  <text x="{port_x + port_width // 2}" y="{port_y + port_height // 2 + 4}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#065f46">{html.escape(str(port["label"]))}</text>',
            ])
            render_port_interface_roles(part_id, "part", port_id, port, port_box, part_box)

    for external_id, external in externals.items():
        x, y, width, height = layout_box(layout, f"externals.{external_id}")
        lines.extend([
            f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="#f9fafb" stroke="#4b5563" stroke-width="2" />',
            f'  <text x="{x + width // 2}" y="{y + height // 2 + 5}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#111827">{html.escape(str(external["label"]))}</text>',
        ])

    for connector_index, connector in enumerate(connectors):
        assert isinstance(connector, dict)
        connector_id = str(connector["id"])
        source = connector["from"]
        target = connector["to"]
        source_label = endpoint_label(source, component, interfaces, ports, parts, part_ports, externals)
        target_label = endpoint_label(target, component, interfaces, ports, parts, part_ports, externals)
        direction_label = f"{source_label} -> {target_label}"
        routed_points = layout_edge_points(layout, connector_id)
        if (
            len(routed_points) >= 2
            and all(0 <= x <= canvas_width and 0 <= y <= canvas_height for x, y in routed_points)
        ):
            points = routed_points
        else:
            start = connector_endpoint_point(source, component, layout, interface_role_positions)
            end = connector_endpoint_point(target, component, layout, interface_role_positions)
            points = [start, end]
        if isinstance(source, dict):
            points[0] = connector_endpoint_point(source, component, layout, interface_role_positions)
        if isinstance(target, dict):
            points[-1] = connector_endpoint_point(target, component, layout, interface_role_positions)
        point_text = " ".join(f"{x},{y}" for x, y in points)
        midpoint = points[len(points) // 2]
        label_y = max(18, midpoint[1] - 18 - connector_index % 3 * 14)
        lines.extend([
            f'  <polyline data-connector="{html.escape(connector_id)}" points="{point_text}" fill="none" stroke="#1f2937" stroke-width="2" marker-end="url(#arrowhead)" />',
            f'  <text x="{midpoint[0]}" y="{label_y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#374151">{html.escape(direction_label)}</text>',
        ])
        label = connector.get("label")
        if isinstance(label, str) and label.strip():
            lines.append(
                f'  <text x="{midpoint[0]}" y="{midpoint[1] + 28 + connector_index % 3 * 14}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">{html.escape(label)}</text>'
            )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def coordinate_values(svg: str) -> list[int]:
    values: list[int] = []
    for match in re.finditer(r'\b(?:x|y|x1|y1|x2|y2|cx|cy|width|height)="(-?[0-9]+)"', svg):
        values.append(int(match.group(1)))
    for points in re.findall(r'\bpoints="([^"]+)"', svg):
        for value in re.findall(r"-?[0-9]+", points):
            values.append(int(value))
    return values


def svg_attributes(tag: str) -> dict[str, str]:
    return {
        match.group(1): html.unescape(match.group(2))
        for match in re.finditer(r'([A-Za-z_:][-A-Za-z0-9_:.]*)="([^"]*)"', tag)
    }


def svg_polyline_points(points: str) -> list[tuple[int, int]]:
    parsed: list[tuple[int, int]] = []
    for point in points.split():
        if "," not in point:
            continue
        x_value, y_value = point.split(",", 1)
        try:
            parsed.append((int(x_value), int(y_value)))
        except ValueError:
            continue
    return parsed


def interface_role_key_from_endpoint(endpoint: object) -> tuple[str, str, str, str] | None:
    if not isinstance(endpoint, dict):
        return None
    return endpoint_role_key(endpoint)


def check_elk_interface_assembly_symbol_endpoints(
    path: Path,
    model: dict[str, object],
    svg: str,
) -> list[str]:
    role_centers: dict[tuple[str, str, str, str], tuple[int, int]] = {}
    for tag_match in re.finditer(r'<(?:circle|path)\b[^>]*\bdata-interface-role="(?:provided|required)"[^>]*/>', svg):
        attributes = svg_attributes(tag_match.group(0))
        key = (
            attributes.get("data-owner", ""),
            attributes.get("data-port", ""),
            attributes.get("data-interface", ""),
            attributes.get("data-interface-role", ""),
        )
        try:
            role_centers[key] = (
                int(attributes["data-symbol-cx"]),
                int(attributes["data-symbol-cy"]),
            )
        except (KeyError, ValueError):
            continue

    connector_points: dict[str, list[tuple[int, int]]] = {}
    for tag_match in re.finditer(r'<polyline\b[^>]*/>', svg):
        attributes = svg_attributes(tag_match.group(0))
        connector_id = attributes.get("data-connector")
        points = attributes.get("points")
        if connector_id and points:
            connector_points[connector_id] = svg_polyline_points(points)

    errors: list[str] = []
    connectors = model.get("connectors", [])
    assert isinstance(connectors, list)
    for connector in connectors:
        if not isinstance(connector, dict) or connector.get("type") != "interfaceAssembly":
            continue
        connector_id = str(connector["id"])
        points = connector_points.get(connector_id, [])
        if len(points) < 2:
            errors.append(f"{rel(path)} elk SVG connector {connector_id} must expose rendered polyline points")
            continue
        source_key = interface_role_key_from_endpoint(connector["from"])
        target_key = interface_role_key_from_endpoint(connector["to"])
        if source_key is not None and role_centers.get(source_key) != points[0]:
            errors.append(
                f"{rel(path)} elk SVG connector {connector_id} must start at source interface-role symbol center"
            )
        if target_key is not None and role_centers.get(target_key) != points[-1]:
            errors.append(
                f"{rel(path)} elk SVG connector {connector_id} must end at target interface-role symbol center"
            )
    return errors


def check_rendered_svg_semantics(
    path: Path,
    model: dict[str, object],
    svg: str,
    backend: str,
) -> list[str]:
    errors: list[str] = []
    component, interfaces, ports, parts, part_ports, externals = model_index(model)
    required_text = [str(component["label"])]
    required_text.extend(str(port["label"]) for port in ports.values())
    required_text.extend(str(part["label"]) for part in parts.values())
    required_text.extend(str(port["label"]) for port in part_ports.values())
    required_text.extend(str(external["label"]) for external in externals.values())
    provided_role_count = 0
    required_role_count = 0
    for port in list(ports.values()) + list(part_ports.values()):
        for interface_id in port_interface_ids(port, "provides"):
            required_text.append(str(interfaces[interface_id]["label"]))
            provided_role_count += 1
        for interface_id in port_interface_ids(port, "requires"):
            required_text.append(str(interfaces[interface_id]["label"]))
            required_role_count += 1
    for connector in model["connectors"]:
        assert isinstance(connector, dict)
        required_text.append(
            f"{endpoint_label(connector['from'], component, interfaces, ports, parts, part_ports, externals)} -> "
            f"{endpoint_label(connector['to'], component, interfaces, ports, parts, part_ports, externals)}"
        )
        label = connector.get("label")
        if isinstance(label, str) and label.strip():
            required_text.append(label)

    for text in required_text:
        if html.escape(text) not in svg:
            errors.append(f"{rel(path)} {backend} SVG must contain reader-visible text {text!r}")

    connector_count = len([connector for connector in model["connectors"] if isinstance(connector, dict)])
    if svg.count('marker-end="url(#arrowhead)"') < connector_count:
        errors.append(f"{rel(path)} {backend} SVG must contain a direction marker for every connector")
    if svg.count('data-interface-role="provided"') < provided_role_count:
        errors.append(f"{rel(path)} {backend} SVG must contain a lollipop marker for every provided interface")
    if svg.count('data-interface-role="required"') < required_role_count:
        errors.append(f"{rel(path)} {backend} SVG must contain a socket marker for every required interface")

    dimensions = svg_dimensions(svg)
    if dimensions is None:
        errors.append(f"{rel(path)} {backend} SVG must expose numeric width and height")
    else:
        width, height = dimensions
        if width <= 0 or height <= 0:
            errors.append(f"{rel(path)} {backend} SVG must have positive canvas dimensions")
        values = coordinate_values(svg)
        if values and min(values) < 0:
            errors.append(f"{rel(path)} {backend} SVG must not render negative geometry coordinates")

    complexity = diagram_complexity(model)
    if complexity.dense:
        if 'data-diagram-complexity-signal="dense"' not in svg:
            errors.append(f"{rel(path)} {backend} SVG must emit raw Diagram Complexity Signal metrics")
        complexity_signal = format_complexity_signal(complexity)
        for fragment in (format_complexity_metrics(complexity), f"warnings={','.join(complexity.warnings)}"):
            if html.escape(fragment) not in svg:
                errors.append(f"{rel(path)} {backend} SVG complexity metrics must contain {fragment!r}")
        if dimensions is not None:
            width, height = dimensions
            base_width = 960 if parts else 720
            if width <= base_width and height <= 360:
                errors.append(f"{rel(path)} {backend} dense SVG must expand canvas instead of compacting semantics")
        if "refactor" in complexity_signal.lower():
            errors.append(f"{rel(path)} {backend} SVG complexity signal must not write refactor conclusions")

    if backend == ELK_RENDER_BACKEND:
        errors.extend(check_elk_interface_assembly_symbol_endpoints(path, model, svg))

    return errors


def render_simple_svg(model: dict[str, object]) -> str:
    component, interfaces, ports, parts, part_ports, externals = model_index(model)
    connectors = model.get("connectors", [])
    assert isinstance(connectors, list)

    complexity = diagram_complexity(model)
    connector_count = complexity.connectors
    total_ports = complexity.total_ports
    interface_role_count = complexity.interface_roles
    max_interface_label_length = max(
        (len(str(interface["label"])) for interface in interfaces.values()),
        default=0,
    )
    dense_interface_label_padding = max(60, max_interface_label_length * APPROX_TEXT_CHAR_WIDTH + 48)
    interface_label_padding = dense_interface_label_padding if complexity.dense else 60
    dense_connector_extra = max(0, connector_count - 8)
    dense_port_extra = max(0, total_ports - 10)
    dense_interface_extra = max(0, interface_role_count - 8)
    max_component_interface_count = max((port_interface_count(port) for port in ports.values()), default=0)
    component_port_gap = max(70, 58 + max(0, max_component_interface_count - 1) * 26 + dense_connector_extra * 3)
    rows = max(len(ports), len(externals), 1)
    has_parts = bool(parts)
    part_columns = 2
    part_rows = max((len(parts) + part_columns - 1) // part_columns, 1)
    max_part_port_count = max(
        (
            len([port for port in part.get("ports", []) if isinstance(port, dict)])
            for part in parts.values()
        ),
        default=0,
    )
    max_part_interface_count = max((port_interface_count(port) for port in part_ports.values()), default=0)
    part_port_slot_height = max(48, 34 + max(0, max_part_interface_count - 1) * 26 + dense_interface_extra * 2)
    part_width = 190
    part_height = max(118, 72 + max_part_port_count * part_port_slot_height)
    part_gap_x = 80 + dense_connector_extra * 8
    part_gap_y = 48 + dense_port_extra * 4
    if complexity.dense and has_parts:
        connector_label_top_stack = connector_count * 18
        connector_label_bottom_stack = connector_count * 16
    else:
        connector_label_top_stack = max(0, connector_count - 4) * 18 if has_parts else 0
        connector_label_bottom_stack = max(0, connector_count - 4) * 16 if has_parts else 0
    top_margin = 70 + connector_label_top_stack
    bottom_margin = 70 + connector_label_bottom_stack
    body_height = max(
        220,
        220 + (rows - 1) * component_port_gap,
        100 + part_rows * part_height + (part_rows - 1) * part_gap_y if has_parts else 220,
    )
    component_x = 250
    component_y = top_margin
    part_grid_right = 410 + (part_columns - 1) * (part_width + part_gap_x) + part_width if has_parts else 0
    component_width = max(
        650 if has_parts else 390,
        part_grid_right - component_x + max(0, interface_label_padding - 60) if has_parts else 390,
    )
    canvas_width = max(
        960 if has_parts else 720,
        component_x + component_width + interface_label_padding,
    )
    canvas_height = top_margin + body_height + bottom_margin
    component_height = body_height
    port_x = 220
    external_x = 60
    port_width = 120
    port_height = 44
    external_width = 130
    external_height = 64
    part_port_width = 138
    part_port_height = 34

    port_positions: dict[str, tuple[int, int]] = {}
    for index, port_id in enumerate(ports):
        port_positions[port_id] = (port_x, top_margin + 90 + index * component_port_gap)

    external_positions: dict[str, tuple[int, int]] = {}
    for index, external_id in enumerate(externals):
        external_positions[external_id] = (external_x, top_margin + 80 + index * component_port_gap)

    part_positions: dict[str, tuple[int, int]] = {}
    part_port_positions: dict[tuple[str, str], tuple[int, int]] = {}
    for index, (part_id, part) in enumerate(parts.items()):
        row = index // part_columns
        column = index % part_columns
        part_x = 410 + column * (part_width + part_gap_x)
        part_y = top_margin + 65 + row * (part_height + part_gap_y)
        part_positions[part_id] = (part_x, part_y)
        part_ports_for_part = [
            port for port in part.get("ports", []) if isinstance(port, dict) and "id" in port
        ]
        for port_index, port in enumerate(part_ports_for_part):
            port_x_in_part = part_x + (part_width - part_port_width) // 2
            port_y_in_part = part_y + 54 + port_index * part_port_slot_height
            part_port_positions[(part_id, str(port["id"]))] = (port_x_in_part, port_y_in_part)

    direction_labels = [
        f"{endpoint_label(connector['from'], component, interfaces, ports, parts, part_ports, externals)} -> "
        f"{endpoint_label(connector['to'], component, interfaces, ports, parts, part_ports, externals)}"
        for connector in connectors
        if isinstance(connector, dict)
    ]

    interface_role_positions: dict[tuple[str, str, str, str], tuple[int, int, int, int]] = {}

    def role_offsets(count: int) -> list[int]:
        if count <= 0:
            return []
        first_offset = -((count - 1) * 26) // 2
        return [first_offset + index * 26 for index in range(count)]

    def endpoint_box(endpoint: object) -> tuple[int, int, int, int]:
        if isinstance(endpoint, str):
            if "." not in endpoint:
                x, y = external_positions[endpoint]
                return x, y, external_width, external_height
            owner_id, port_id = endpoint.split(".", 1)
            if owner_id == str(component["id"]):
                x, y = port_positions[port_id]
                return x, y, port_width, port_height
            x, y = part_port_positions[(owner_id, port_id)]
            return x, y, part_port_width, part_port_height

        return interface_role_positions[endpoint_role_key(endpoint)]

    def endpoint_anchors(
        source: object,
        target: object,
    ) -> tuple[int, int, int, int]:
        source_x, source_y, source_width, source_height = endpoint_box(source)
        target_x, target_y, target_width, target_height = endpoint_box(target)
        if source_x < target_x:
            start_x = source_x + source_width
            end_x = target_x
        else:
            start_x = source_x
            end_x = target_x + target_width
        return start_x, source_y + source_height // 2, end_x, target_y + target_height // 2

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">Whitebox Component Diagram: {html.escape(str(component["label"]))}</title>',
        f'  <desc id="desc">{html.escape("; ".join(direction_labels))}</desc>',
    ]
    if complexity.dense:
        lines.append(
            f'  <metadata data-diagram-complexity-signal="dense">{html.escape(format_complexity_signal(complexity))}</metadata>'
        )
    lines.extend([
        "  <defs>",
        '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#1f2937" />',
        "    </marker>",
        "  </defs>",
        f'  <rect x="{component_x}" y="{component_y}" width="{component_width}" height="{component_height}" rx="8" fill="#ffffff" stroke="#1f2937" stroke-width="2" />',
        f'  <text x="{component_x + component_width // 2}" y="{component_y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#111827">{html.escape(str(component["label"]))}</text>',
    ])

    def render_interface_role(
        owner_id: str,
        port_id: str,
        interface_id: str,
        role: str,
        side: str,
        port_box: tuple[int, int, int, int],
        offset_y: int,
    ) -> None:
        x, y, width, height = port_box
        role_y = y + height // 2 + offset_y
        if side == "right":
            stem_start_x = x + width
            symbol_x = x + width + 30
            stem_end_x = symbol_x - 10
            label_x = symbol_x + 16
            text_anchor = "start"
        else:
            stem_start_x = x
            symbol_x = x - 30
            stem_end_x = symbol_x + 10
            label_x = symbol_x - 16
            text_anchor = "end"

        interface_label = html.escape(str(interfaces[interface_id]["label"]))
        escaped_owner = html.escape(owner_id)
        escaped_port = html.escape(port_id)
        escaped_interface = html.escape(interface_id)
        interface_role_positions[(owner_id, port_id, interface_id, role)] = (symbol_x - 10, role_y - 10, 20, 20)
        lines.append(
            f'  <line x1="{stem_start_x}" y1="{role_y}" x2="{stem_end_x}" y2="{role_y}" stroke="#6b7280" stroke-width="2" />'
        )
        if role == "provided":
            lines.append(
                f'  <circle data-interface-role="provided" data-owner="{escaped_owner}" data-port="{escaped_port}" data-interface="{escaped_interface}" cx="{symbol_x}" cy="{role_y}" r="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" />'
            )
        else:
            if side == "right":
                socket_path = f"M {symbol_x - 10} {role_y - 10} A 10 10 0 0 1 {symbol_x - 10} {role_y + 10}"
            else:
                socket_path = f"M {symbol_x + 10} {role_y - 10} A 10 10 0 0 0 {symbol_x + 10} {role_y + 10}"
            lines.append(
                f'  <path data-interface-role="required" data-owner="{escaped_owner}" data-port="{escaped_port}" data-interface="{escaped_interface}" d="{socket_path}" fill="none" stroke="#b45309" stroke-width="2" />'
            )
        lines.append(
            f'  <text x="{label_x}" y="{role_y + 4}" text-anchor="{text_anchor}" font-family="Arial, sans-serif" font-size="11" fill="#374151">{interface_label}</text>'
        )

    def render_port_interface_roles(
        owner_id: str,
        owner_kind: str,
        port_id: str,
        port: dict[str, object],
        port_box: tuple[int, int, int, int],
    ) -> None:
        provided_ids = port_interface_ids(port, "provides")
        required_ids = port_interface_ids(port, "requires")
        if owner_kind == "component":
            roles = [("provided", interface_id) for interface_id in provided_ids]
            roles.extend(("required", interface_id) for interface_id in required_ids)
            for (role, interface_id), offset_y in zip(roles, role_offsets(len(roles))):
                render_interface_role(owner_id, port_id, interface_id, role, "right", port_box, offset_y)
            return

        for interface_id, offset_y in zip(required_ids, role_offsets(len(required_ids))):
            render_interface_role(owner_id, port_id, interface_id, "required", "left", port_box, offset_y)
        for interface_id, offset_y in zip(provided_ids, role_offsets(len(provided_ids))):
            render_interface_role(owner_id, port_id, interface_id, "provided", "right", port_box, offset_y)

    for port_id, port in ports.items():
        x, y = port_positions[port_id]
        lines.extend(
            [
                f'  <rect x="{x}" y="{y}" width="{port_width}" height="{port_height}" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="2" />',
                f'  <text x="{x + port_width // 2}" y="{y + 27}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#1e3a8a">{html.escape(str(port["label"]))}</text>',
            ]
        )
        render_port_interface_roles(
            str(component["id"]),
            "component",
            port_id,
            port,
            (x, y, port_width, port_height),
        )

    for part_id, part in parts.items():
        x, y = part_positions[part_id]
        lines.extend(
            [
                f'  <rect x="{x}" y="{y}" width="{part_width}" height="{part_height}" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="2" />',
                f'  <text x="{x + part_width // 2}" y="{y + 31}" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#334155">{html.escape(str(part["label"]))}</text>',
            ]
        )
        for port in part.get("ports", []):
            if not isinstance(port, dict) or "id" not in port:
                continue
            port_id = str(port["id"])
            port_x_in_part, port_y_in_part = part_port_positions[(part_id, port_id)]
            lines.extend(
                [
                    f'  <rect x="{port_x_in_part}" y="{port_y_in_part}" width="{part_port_width}" height="{part_port_height}" rx="6" fill="#ecfdf5" stroke="#059669" stroke-width="2" />',
                    f'  <text x="{port_x_in_part + part_port_width // 2}" y="{port_y_in_part + 22}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#065f46">{html.escape(str(port["label"]))}</text>',
                ]
            )
            render_port_interface_roles(
                part_id,
                "part",
                port_id,
                port,
                (port_x_in_part, port_y_in_part, part_port_width, part_port_height),
            )

    for external_id, external in externals.items():
        x, y = external_positions[external_id]
        lines.extend(
            [
                f'  <rect x="{x}" y="{y}" width="{external_width}" height="{external_height}" rx="8" fill="#f9fafb" stroke="#4b5563" stroke-width="2" />',
                f'  <text x="{x + external_width // 2}" y="{y + 37}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#111827">{html.escape(str(external["label"]))}</text>',
            ]
        )

    for connector_index, connector in enumerate(connectors):
        assert isinstance(connector, dict)
        source = connector["from"]
        target = connector["to"]
        source_label = endpoint_label(source, component, interfaces, ports, parts, part_ports, externals)
        target_label = endpoint_label(target, component, interfaces, ports, parts, part_ports, externals)
        direction_label = f"{source_label} -> {target_label}"
        start_x, start_y, end_x, end_y = endpoint_anchors(source, target)

        label_x = (start_x + end_x) // 2
        if complexity.dense and has_parts:
            label_y = 36 + connector_index * 16
            connector_label_y = component_y + component_height + 32 + connector_index * 16
        else:
            label_offset = connector_index * 18 if has_parts else 0
            connector_label_offset = connector_index * 16 if has_parts else 0
            label_y = min(start_y, end_y) - 37 - label_offset
            connector_label_y = max(start_y, end_y) + 50 + connector_label_offset
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
    svg = render_svg(model, backend=SIMPLE_RENDER_BACKEND)
    expected_svg_path = path.with_suffix(".svg")
    if not expected_svg_path.exists():
        errors.append(f"{rel(expected_svg_path)} is missing")
    elif svg != read_text(expected_svg_path):
        errors.append(f"{rel(path)} rendered SVG differs from {rel(expected_svg_path)}")

    errors.extend(check_rendered_svg_semantics(path, model, svg, SIMPLE_RENDER_BACKEND))
    try:
        elk_svg = render_svg(model, backend=ELK_RENDER_BACKEND)
        second_elk_svg = render_svg(model, backend=ELK_RENDER_BACKEND)
    except WhiteboxRenderError as exc:
        errors.append(f"{rel(path)} elk backend failed: {exc}")
    else:
        errors.extend(check_rendered_svg_semantics(path, model, elk_svg, ELK_RENDER_BACKEND))
        if elk_svg != second_elk_svg:
            errors.append(f"{rel(path)} elk backend must produce deterministic SVG for stable input")

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
    print(
        "Validated topology-only source models and SVG rendering with "
        f"{SIMPLE_RENDER_BACKEND} snapshot checks and {ELK_RENDER_BACKEND} structural checks."
    )
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


def render_command(source_path: Path, output_path: Path, backend: str = SIMPLE_RENDER_BACKEND) -> int:
    try:
        selected_backend = select_render_backend(backend)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    model, load_errors = load_source_model(source_path)
    errors = load_errors or validate_source_model(model)
    if errors:
        print(f"{rel(source_path)} is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    assert isinstance(model, dict)
    try:
        svg = render_svg(model, backend=selected_backend.name)
    except WhiteboxRenderError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    complexity = diagram_complexity(model)
    if str(output_path) == "-":
        sys.stdout.write(svg)
    else:
        output_path.write_text(svg, encoding="utf-8")
        print(f"Wrote {rel(output_path)}")
    if complexity.dense:
        print(f"{rel(source_path)}: {format_complexity_signal(complexity)}", file=sys.stderr)
    return 0


def usage() -> None:
    print(
        "Usage:\n"
        "  python3 scripts/check_whitebox_fixtures.py\n"
        "  python3 scripts/check_whitebox_fixtures.py validate <source.whitebox.yaml>\n"
        "  python3 scripts/check_whitebox_fixtures.py render [--backend simple|elk] <source.whitebox.yaml> <output.svg|->"
    )


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        return check_fixtures()
    if len(argv) == 3 and argv[1] == "validate":
        return validate_command(Path(argv[2]))
    if len(argv) in (4, 6) and argv[1] == "render":
        if len(argv) == 4:
            return render_command(Path(argv[2]), Path(argv[3]))
        if argv[2] == "--backend":
            return render_command(Path(argv[4]), Path(argv[5]), backend=argv[3])
    usage()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
