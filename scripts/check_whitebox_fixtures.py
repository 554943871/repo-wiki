#!/usr/bin/env python3
"""Validate and render minimal Whitebox Component Diagram fixtures."""

from __future__ import annotations

from dataclasses import dataclass
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

REQUIRED_VALID_FIXTURES = {
    "both-interface-roles.whitebox.yaml",
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
ALLOWED_CONNECTOR_FIELDS = {"id", "type", "source", "target", "label", "evidence"}
ALLOWED_FILE_EVIDENCE_FIELDS = {"path", "note", "lines", "symbol"}
ALLOWED_USER_EVIDENCE_FIELDS = {"source", "note"}
ALLOWED_PART_PORT_ENDPOINT_FIELDS = {"part", "port"}
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
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
LINE_RANGE = re.compile(r"^([1-9][0-9]*)(?:-([1-9][0-9]*))?$")


@dataclass(frozen=True)
class Endpoint:
    kind: str
    owner_id: str
    port_id: str | None = None
    owner_kind: str | None = None
    interface_id: str | None = None
    role: str | None = None


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
    endpoint = expect_mapping(value, field_path, errors)
    if endpoint is None:
        return None
    if len(endpoint) != 1:
        errors.append(f"{field_path} must name exactly one endpoint")
        return None

    endpoint_type, endpoint_value = next(iter(endpoint.items()))
    if endpoint_type == "part_port":
        part_port = expect_mapping(endpoint_value, f"{field_path}.part_port", errors)
        if part_port is None:
            return None
        check_allowed_fields(part_port, ALLOWED_PART_PORT_ENDPOINT_FIELDS, f"{field_path}.part_port", errors)
        part_id = require_string(part_port, "part", f"{field_path}.part_port", errors)
        port_id = require_string(part_port, "port", f"{field_path}.part_port", errors)
        if part_id and part_id not in part_ids:
            errors.append(f"{field_path}.part_port.part references unknown part: {part_id}")
            return None
        if part_id and port_id and (part_id, port_id) not in part_port_ids:
            errors.append(f"{field_path}.part_port.port references unknown port on part {part_id}: {port_id}")
            return None
        if part_id and port_id:
            return Endpoint(kind="part_port", owner_id=part_id, port_id=port_id)
        return None

    if endpoint_type == "interface_role":
        interface_role = expect_mapping(endpoint_value, f"{field_path}.interface_role", errors)
        if interface_role is None:
            return None
        check_allowed_fields(
            interface_role,
            ALLOWED_INTERFACE_ROLE_ENDPOINT_FIELDS,
            f"{field_path}.interface_role",
            errors,
        )
        owner_id = require_string(interface_role, "owner", f"{field_path}.interface_role", errors)
        port_id = require_string(interface_role, "port", f"{field_path}.interface_role", errors)
        interface_id = require_string(interface_role, "interface", f"{field_path}.interface_role", errors)
        role = require_string(interface_role, "role", f"{field_path}.interface_role", errors)

        owner_kind: str | None = None
        if owner_id:
            if owner_id == component_id:
                owner_kind = "component"
                if port_id and port_id not in component_port_ids:
                    errors.append(
                        f"{field_path}.interface_role.port references unknown port on component {owner_id}: {port_id}"
                    )
                    return None
            elif owner_id in part_ids:
                owner_kind = "part"
                if port_id and (owner_id, port_id) not in part_port_ids:
                    errors.append(
                        f"{field_path}.interface_role.port references unknown port on part {owner_id}: {port_id}"
                    )
                    return None
            else:
                errors.append(f"{field_path}.interface_role.owner references unknown owner: {owner_id}")
                return None

        if interface_id:
            check_snake_case(interface_id, f"{field_path}.interface_role.interface", errors)
            if interface_id not in interface_ids:
                errors.append(f"{field_path}.interface_role.interface references unknown interface: {interface_id}")
                return None

        if role and role not in INTERFACE_ROLES:
            errors.append(f"{field_path}.interface_role.role must be provided or required")
            return None

        if owner_id and port_id and interface_id and role:
            role_key = (owner_id, port_id, interface_id, role)
            if role_key not in interface_roles:
                errors.append(
                    f"{field_path}.interface_role references undeclared {role} interface role: "
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

    if not isinstance(endpoint_value, str) or not endpoint_value.strip():
        errors.append(f"{field_path}.{endpoint_type} is required")
        return None
    if endpoint_type == "external":
        if endpoint_value not in external_ids:
            errors.append(f"{field_path}.external references unknown external: {endpoint_value}")
            return None
        return Endpoint(kind="external", owner_id=endpoint_value)
    if endpoint_type == "port":
        if endpoint_value not in component_port_ids:
            errors.append(f"{field_path}.port references unknown component port: {endpoint_value}")
            return None
        return Endpoint(kind="component_port", owner_id=endpoint_value)
    if endpoint_type == "component":
        errors.append(f"{field_path}.component cannot target a whole component; use a component port endpoint")
        return None
    if endpoint_type == "part":
        errors.append(f"{field_path}.part cannot target a whole part; use a part_port endpoint")
        return None

    errors.append(f"{field_path} uses unsupported endpoint type: {endpoint_type}")
    return None


def mark_connected_port(
    endpoint: Endpoint,
    connected_component_ports: set[str],
    connected_part_ports: set[tuple[str, str]],
) -> None:
    if endpoint.kind == "component_port":
        connected_component_ports.add(endpoint.owner_id)
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

    check_layout_hints(root, "", errors)

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
                connector.get("source"),
                f"{connector_path}.source",
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
                connector.get("target"),
                f"{connector_path}.target",
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
    endpoint: dict[str, object],
    component: dict[str, object],
    interfaces: dict[str, dict[str, object]],
    ports: dict[str, dict[str, object]],
    parts: dict[str, dict[str, object]],
    part_ports: dict[tuple[str, str], dict[str, object]],
    externals: dict[str, dict[str, object]],
) -> str:
    if "external" in endpoint:
        return str(externals[str(endpoint["external"])]["label"])
    if "part_port" in endpoint:
        part_port = endpoint["part_port"]
        assert isinstance(part_port, dict)
        part_id = str(part_port["part"])
        port_id = str(part_port["port"])
        return f'{parts[part_id]["label"]}.{part_ports[(part_id, port_id)]["label"]}'
    if "interface_role" in endpoint:
        interface_role = endpoint["interface_role"]
        assert isinstance(interface_role, dict)
        owner_id = str(interface_role["owner"])
        port_id = str(interface_role["port"])
        interface_id = str(interface_role["interface"])
        role = str(interface_role["role"])
        if owner_id == str(component["id"]):
            owner_label = str(component["label"])
            port_label = str(ports[port_id]["label"])
        else:
            owner_label = str(parts[owner_id]["label"])
            port_label = str(part_ports[(owner_id, port_id)]["label"])
        interface_label = str(interfaces[interface_id]["label"])
        return f"{owner_label}.{port_label} {role} {interface_label}"
    return str(ports[str(endpoint["port"])]["label"])


def port_interface_ids(port: dict[str, object], field: str) -> list[str]:
    value = port.get(field, [])
    if not isinstance(value, list):
        return []
    return [str(interface_id) for interface_id in value if isinstance(interface_id, str)]


def port_interface_count(port: dict[str, object]) -> int:
    return len(port_interface_ids(port, "provides")) + len(port_interface_ids(port, "requires"))


def render_svg(model: dict[str, object]) -> str:
    component, interfaces, ports, parts, part_ports, externals = model_index(model)
    connectors = model.get("connectors", [])
    assert isinstance(connectors, list)

    max_component_interface_count = max((port_interface_count(port) for port in ports.values()), default=0)
    component_port_gap = max(70, 58 + max(0, max_component_interface_count - 1) * 26)
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
    part_port_slot_height = max(48, 34 + max(0, max_part_interface_count - 1) * 26)
    part_width = 190
    part_height = max(118, 72 + max_part_port_count * part_port_slot_height)
    part_gap_x = 80
    part_gap_y = 48
    canvas_width = 960 if has_parts else 720
    canvas_height = max(
        360,
        290 + (rows - 1) * component_port_gap,
        170 + part_rows * part_height + (part_rows - 1) * part_gap_y if has_parts else 360,
    )
    component_x = 250
    component_y = 70
    component_width = 650 if has_parts else 390
    component_height = canvas_height - 140
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
        port_positions[port_id] = (port_x, 160 + index * component_port_gap)

    external_positions: dict[str, tuple[int, int]] = {}
    for index, external_id in enumerate(externals):
        external_positions[external_id] = (external_x, 150 + index * component_port_gap)

    part_positions: dict[str, tuple[int, int]] = {}
    part_port_positions: dict[tuple[str, str], tuple[int, int]] = {}
    for index, (part_id, part) in enumerate(parts.items()):
        row = index // part_columns
        column = index % part_columns
        part_x = 410 + column * (part_width + part_gap_x)
        part_y = 135 + row * (part_height + part_gap_y)
        part_positions[part_id] = (part_x, part_y)
        part_ports_for_part = [
            port for port in part.get("ports", []) if isinstance(port, dict) and "id" in port
        ]
        for port_index, port in enumerate(part_ports_for_part):
            port_x_in_part = part_x + (part_width - part_port_width) // 2
            port_y_in_part = part_y + 54 + port_index * part_port_slot_height
            part_port_positions[(part_id, str(port["id"]))] = (port_x_in_part, port_y_in_part)

    direction_labels = [
        f"{endpoint_label(connector['source'], component, interfaces, ports, parts, part_ports, externals)} -> "
        f"{endpoint_label(connector['target'], component, interfaces, ports, parts, part_ports, externals)}"
        for connector in connectors
        if isinstance(connector, dict)
    ]

    interface_role_positions: dict[tuple[str, str, str, str], tuple[int, int, int, int]] = {}

    def role_offsets(count: int) -> list[int]:
        if count <= 0:
            return []
        first_offset = -((count - 1) * 26) // 2
        return [first_offset + index * 26 for index in range(count)]

    def endpoint_box(endpoint: dict[str, object]) -> tuple[int, int, int, int]:
        if "external" in endpoint:
            external_id = str(endpoint["external"])
            x, y = external_positions[external_id]
            return x, y, external_width, external_height
        if "part_port" in endpoint:
            part_port = endpoint["part_port"]
            assert isinstance(part_port, dict)
            part_id = str(part_port["part"])
            port_id = str(part_port["port"])
            x, y = part_port_positions[(part_id, port_id)]
            return x, y, part_port_width, part_port_height
        if "interface_role" in endpoint:
            interface_role = endpoint["interface_role"]
            assert isinstance(interface_role, dict)
            key = (
                str(interface_role["owner"]),
                str(interface_role["port"]),
                str(interface_role["interface"]),
                str(interface_role["role"]),
            )
            return interface_role_positions[key]
        port_id = str(endpoint["port"])
        x, y = port_positions[port_id]
        return x, y, port_width, port_height

    def endpoint_anchors(
        source: dict[str, object],
        target: dict[str, object],
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
        "  <defs>",
        '    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#1f2937" />',
        "    </marker>",
        "  </defs>",
        f'  <rect x="{component_x}" y="{component_y}" width="{component_width}" height="{component_height}" rx="8" fill="#ffffff" stroke="#1f2937" stroke-width="2" />',
        f'  <text x="{component_x + component_width // 2}" y="{component_y + 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#111827">{html.escape(str(component["label"]))}</text>',
    ]

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
        source = connector["source"]
        target = connector["target"]
        assert isinstance(source, dict)
        assert isinstance(target, dict)
        source_label = endpoint_label(source, component, interfaces, ports, parts, part_ports, externals)
        target_label = endpoint_label(target, component, interfaces, ports, parts, part_ports, externals)
        direction_label = f"{source_label} -> {target_label}"
        start_x, start_y, end_x, end_y = endpoint_anchors(source, target)

        label_x = (start_x + end_x) // 2
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
    svg = render_svg(model)
    expected_svg_path = path.with_suffix(".svg")
    if not expected_svg_path.exists():
        errors.append(f"{rel(expected_svg_path)} is missing")
    elif svg != read_text(expected_svg_path):
        errors.append(f"{rel(path)} rendered SVG differs from {rel(expected_svg_path)}")

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
        assert isinstance(connector["source"], dict)
        assert isinstance(connector["target"], dict)
        required_text.append(
            f"{endpoint_label(connector['source'], component, interfaces, ports, parts, part_ports, externals)} -> "
            f"{endpoint_label(connector['target'], component, interfaces, ports, parts, part_ports, externals)}"
        )
        label = connector.get("label")
        if isinstance(label, str) and label.strip():
            required_text.append(label)

    for text in required_text:
        if html.escape(text) not in svg:
            errors.append(f"{rel(path)} SVG must contain reader-visible text {text!r}")

    connector_count = len([connector for connector in model["connectors"] if isinstance(connector, dict)])
    if svg.count('marker-end="url(#arrowhead)"') < connector_count:
        errors.append(f"{rel(path)} SVG must contain a direction marker for every connector")
    if svg.count('data-interface-role="provided"') < provided_role_count:
        errors.append(f"{rel(path)} SVG must contain a lollipop marker for every provided interface")
    if svg.count('data-interface-role="required"') < required_role_count:
        errors.append(f"{rel(path)} SVG must contain a socket marker for every required interface")

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
