#!/usr/bin/env python3
"""Check wiki-doctor regression fixture coverage and boundary wording."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from check_whitebox_fixtures import (
    DEFAULT_RENDER_BACKEND,
    DERIVED_VIEW_LABELS,
    DERIVED_VIEW_NAMES,
    build_derived_view_models,
    derived_svg_file_name,
    load_source_model,
    render_svg,
    validate_source_model,
    whitebox_view,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "wiki-doctor" / "fixtures"
DOC_ROOT = ROOT / "tests" / "wiki-doctor"

REQUIRED_BEHAVIORS = {
    "active_drift_page_stops_before_audit_or_rewrite",
    "existing_incomplete_wiki_completes_skeleton_without_new_facts",
    "duplicate_same_concept_pages_preserve_unique_info_and_links",
    "naming_conflicts_report_meaning_loss_risk",
    "suspected_code_wiki_mismatch_recommends_drift_radar",
    "audit_only_does_not_rewrite_stable_pages",
    "old_module_map_refreshes_to_whitebox_source_and_svg",
    "old_module_map_insufficient_evidence_reports_meaning_loss_risk",
    "old_module_map_needing_code_comparison_recommends_drift_radar",
}

ALLOWED_GATES = {
    "active_drift_blocks",
    "empty_drift_allows_default",
    "empty_drift_allows_audit_only",
}

ALLOWED_CLASSIFICATIONS = {
    "safe_guidance_rewrite",
    "meaning_loss_risk",
    "drift_or_coverage_suspect",
}

ALLOWED_ACTIONS = {
    "rewrite_page",
    "add_reader_entry",
    "add_table_or_diagram",
    "update_canonical_index",
    "relocate_content",
    "split_page",
    "deduplicate_content",
    "safe_page_delete",
    "safe_file_rename",
    "safe_page_merge",
    "complete_skeleton",
    "risk_report_only",
    "recommend_drift_radar",
}

BOUNDARY_WORDING_PATTERNS = [
    re.compile(r"\bvalidator(s)?\b", re.IGNORECASE),
    re.compile(r"\blint(s|ing)?\b", re.IGNORECASE),
    re.compile(r"\bcompliance\b", re.IGNORECASE),
    re.compile(r"\bPASS\b"),
    re.compile(r"\bFAIL\b"),
    re.compile(r"\bpass\s*/\s*fail\b", re.IGNORECASE),
    re.compile(r"\bsemantic correctness\b", re.IGNORECASE),
    re.compile(r"\bproves? wiki meaning\b", re.IGNORECASE),
]
MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def markdown_images(markdown: str) -> list[tuple[str, str, int, int]]:
    return [
        (match.group(1), match.group(2), match.start(), match.end())
        for match in MARKDOWN_IMAGE.finditer(markdown)
    ]


def markdown_target_file_name(target: str) -> str:
    return Path(target.strip("<>")).name


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_case(case_dir: Path) -> tuple[dict[str, object] | None, list[str]]:
    errors: list[str] = []
    metadata_path = case_dir / "case.json"
    if not metadata_path.exists():
        return None, [f"{rel(case_dir)} is missing case.json"]

    try:
        metadata = json.loads(read_text(metadata_path))
    except json.JSONDecodeError as exc:
        return None, [f"{rel(metadata_path)} is not JSON: {exc}"]

    if not isinstance(metadata, dict):
        return None, [f"{rel(metadata_path)} must contain a JSON object"]

    if metadata.get("id") != case_dir.name:
        errors.append(f"{rel(metadata_path)} id must match directory name")

    return metadata, errors


def expect_list(metadata: dict[str, object], key: str) -> list[str]:
    value = metadata.get(key, [])
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return []


def check_basic_contract(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    report_path = case_dir / "expected" / "report.md"
    input_wiki = case_dir / "input" / "wiki"

    if not input_wiki.exists():
        errors.append(f"{rel(case_dir)} must contain input/wiki")

    if not report_path.exists():
        errors.append(f"{rel(case_dir)} must contain expected/report.md")
        report = ""
    else:
        report = read_text(report_path)

    behavior = metadata.get("behavior")
    if not isinstance(behavior, str) or not behavior:
        errors.append(f"{rel(case_dir / 'case.json')} must name one behavior")

    gate = metadata.get("gate")
    if gate not in ALLOWED_GATES:
        errors.append(f"{rel(case_dir / 'case.json')} has unknown gate {gate!r}")

    stable_pages_rewritten = metadata.get("stable_pages_rewritten")
    if not isinstance(stable_pages_rewritten, bool):
        errors.append(
            f"{rel(case_dir / 'case.json')} must set stable_pages_rewritten to true or false"
        )

    for classification in expect_list(metadata, "classifications"):
        if classification not in ALLOWED_CLASSIFICATIONS:
            errors.append(
                f"{rel(case_dir / 'case.json')} has unknown classification {classification!r}"
            )

    for action in expect_list(metadata, "actions"):
        if action not in ALLOWED_ACTIONS:
            errors.append(f"{rel(case_dir / 'case.json')} has unknown action {action!r}")

    for phrase in expect_list(metadata, "report_must_contain"):
        if phrase not in report:
            errors.append(f"{rel(report_path)} must contain {phrase!r}")

    for phrase in expect_list(metadata, "report_must_not_contain"):
        if phrase in report:
            errors.append(f"{rel(report_path)} must not contain {phrase!r}")

    return errors


def all_markdown_text(root: Path) -> str:
    parts: list[str] = []
    if root.exists():
        for path in sorted(root.rglob("*.md")):
            parts.append(read_text(path))
    return "\n".join(parts)


def all_expected_wiki_text(case_dir: Path) -> str:
    parts: list[str] = []
    expected_dir = case_dir / "expected" / "wiki"
    if expected_dir.exists():
        for path in sorted(p for p in expected_dir.rglob("*") if p.is_file()):
            if path.suffix in {".md", ".svg", ".yaml"}:
                parts.append(read_text(path))
    return "\n".join(parts)


def check_expected_text_requirements(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    expected_text = all_expected_wiki_text(case_dir)

    for phrase in expect_list(metadata, "expected_wiki_must_contain"):
        if phrase not in expected_text:
            errors.append(f"{rel(case_dir / 'expected')} must preserve {phrase!r}")

    for phrase in expect_list(metadata, "expected_wiki_must_not_contain"):
        if phrase in expected_text:
            errors.append(f"{rel(case_dir / 'expected')} must not contain {phrase!r}")

    return errors


def check_unchanged_wiki_paths(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for path_name in expect_list(metadata, "unchanged_wiki_paths"):
        input_path = case_dir / "input" / "wiki" / path_name
        expected_path = case_dir / "expected" / "wiki" / path_name
        if not input_path.exists():
            errors.append(f"{rel(input_path)} must exist for unchanged wiki comparison")
            continue
        if not expected_path.exists():
            errors.append(f"{rel(expected_path)} must exist for unchanged wiki comparison")
            continue
        if read_text(input_path) != read_text(expected_path):
            errors.append(f"{rel(expected_path)} must match input for no-write behavior")
    return errors


def check_no_expected_whitebox_files(case_dir: Path) -> list[str]:
    expected_wiki = case_dir / "expected" / "wiki"
    if not expected_wiki.exists():
        return []

    errors: list[str] = []
    for path in sorted(expected_wiki.rglob("*.whitebox.*")):
        errors.append(f"{rel(path)} must not exist for report-only old module map behavior")
    return errors


def check_module_page_whitebox_embeds(
    module_page_path: Path,
    module_page: str,
    source_name: str,
    complete_svg_name: str,
    expected_derived_views: dict[str, str],
    generated_derived_views: set[str],
) -> list[str]:
    errors: list[str] = []
    images = markdown_images(module_page)
    whitebox_images = [
        (alt, target, start, end)
        for alt, target, start, end in images
        if ".whitebox" in markdown_target_file_name(target) and markdown_target_file_name(target).endswith(".svg")
    ]

    if not whitebox_images:
        errors.append(f"{rel(module_page_path)} must embed the complete Whitebox SVG")
        return errors

    first_alt, first_target, first_start, first_end = whitebox_images[0]
    if markdown_target_file_name(first_target) != complete_svg_name:
        errors.append(f"{rel(module_page_path)} must embed the complete Whitebox SVG before derived views")

    complete_images = [
        (alt, target, start, end)
        for alt, target, start, end in whitebox_images
        if markdown_target_file_name(target) == complete_svg_name
    ]
    if not complete_images:
        errors.append(f"{rel(module_page_path)} must link the rendered complete Whitebox SVG")
        complete_start = first_start
        complete_end = first_end
    else:
        _, _, complete_start, complete_end = complete_images[0]

    source_link = f"[`{source_name}`](./{source_name})"
    source_index = module_page.find(source_link)
    if source_index == -1:
        errors.append(f"{rel(module_page_path)} must link the Whitebox source model")
    elif source_index < complete_end:
        errors.append(f"{rel(module_page_path)} must keep the source model link after the complete diagram")

    first_derived_start: int | None = None
    for view_name, path_value in expected_derived_views.items():
        derived_name = Path(path_value).name
        derived_images = [
            (alt, target, start, end)
            for alt, target, start, end in whitebox_images
            if markdown_target_file_name(target) == derived_name
        ]
        if not derived_images:
            errors.append(f"{rel(module_page_path)} must embed the {view_name} Derived Whitebox View")
            continue

        label = DERIVED_VIEW_LABELS[view_name]
        alt, _, image_start, _ = derived_images[0]
        first_derived_start = image_start if first_derived_start is None else min(first_derived_start, image_start)
        heading = f"### {label}"
        heading_index = module_page.find(heading)
        if heading_index == -1:
            errors.append(f"{rel(module_page_path)} must head the {view_name} derived view as {heading!r}")
        elif not (complete_start < heading_index < image_start):
            errors.append(f"{rel(module_page_path)} must place {heading!r} before its derived SVG and after the complete diagram")
        if label not in alt:
            errors.append(f"{rel(module_page_path)} {view_name} derived SVG alt text must include {label!r}")

    if source_index != -1 and first_derived_start is not None and first_derived_start < source_index:
        errors.append(f"{rel(module_page_path)} must keep the source model link visible before derived views")

    previous_position = source_index if source_index != -1 else complete_end
    for view_name in DERIVED_VIEW_NAMES:
        if view_name not in expected_derived_views:
            continue
        heading = f"### {DERIVED_VIEW_LABELS[view_name]}"
        position = module_page.find(heading)
        if position == -1:
            continue
        if position < previous_position:
            errors.append(f"{rel(module_page_path)} must preserve derived view order after the source model link")
        previous_position = position

    for view_name in DERIVED_VIEW_NAMES:
        if view_name in generated_derived_views:
            continue
        empty_view_file = derived_svg_file_name(Path(source_name), view_name)
        if empty_view_file in module_page:
            errors.append(f"{rel(module_page_path)} must not embed empty {view_name} Derived Whitebox View")

    return errors


def check_active_drift_gate(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    drift_path = case_dir / "input" / "wiki" / "07-drift.md"
    if not drift_path.exists():
        return [f"{rel(case_dir)} active-drift case must include wiki/07-drift.md"]

    drift = read_text(drift_path)
    if "No active drift or coverage gaps." in drift and "###" not in drift:
        errors.append(f"{rel(drift_path)} must show an active Drift Page item")

    if metadata.get("must_stop_before_audit") is not True:
        errors.append(f"{rel(case_dir / 'case.json')} must set must_stop_before_audit")

    if metadata.get("stable_pages_rewritten") is not False:
        errors.append(f"{rel(case_dir / 'case.json')} must not rewrite stable pages")

    return errors


def check_incomplete_skeleton(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing_paths = expect_list(metadata, "missing_fixed_skeleton_paths")
    if not missing_paths:
        errors.append(f"{rel(case_dir / 'case.json')} must list missing skeleton paths")

    for path_name in missing_paths:
        if (case_dir / "input" / path_name).exists():
            errors.append(f"{rel(case_dir / 'input' / path_name)} should be absent in input")

    if "complete_skeleton" not in expect_list(metadata, "actions"):
        errors.append(f"{rel(case_dir / 'case.json')} must expect complete_skeleton")

    if metadata.get("invent_stable_facts") is not False:
        errors.append(f"{rel(case_dir / 'case.json')} must rule out invented stable facts")

    return errors


def check_duplicate_same_concept(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    expected_text = all_markdown_text(case_dir / "expected")
    unique_info = expect_list(metadata, "unique_info_must_survive")

    if not unique_info:
        errors.append(f"{rel(case_dir / 'case.json')} must list unique info to preserve")

    for phrase in unique_info:
        if phrase not in expected_text:
            errors.append(f"{rel(case_dir)} expected output must preserve {phrase!r}")

    actions = set(expect_list(metadata, "actions"))
    if "safe_page_merge" not in actions:
        errors.append(f"{rel(case_dir / 'case.json')} must expect safe_page_merge")
    if "update_canonical_index" not in actions:
        errors.append(f"{rel(case_dir / 'case.json')} must expect update_canonical_index")

    link_updates = metadata.get("expected_link_updates", [])
    if isinstance(link_updates, list):
        for update in link_updates:
            if not isinstance(update, dict):
                errors.append(f"{rel(case_dir / 'case.json')} link updates must be objects")
                continue
            old = update.get("old")
            new = update.get("new")
            if not isinstance(old, str) or not isinstance(new, str):
                errors.append(f"{rel(case_dir / 'case.json')} link updates need old and new")
                continue
            if new not in expected_text:
                errors.append(f"{rel(case_dir)} expected output must contain new link {new!r}")
            if old in expected_text:
                errors.append(f"{rel(case_dir)} expected output still contains old link {old!r}")
    else:
        errors.append(f"{rel(case_dir / 'case.json')} expected_link_updates must be a list")

    return errors


def check_naming_conflict(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    report = read_text(case_dir / "expected" / "report.md")
    if "meaning_loss_risk" not in expect_list(metadata, "classifications"):
        errors.append(f"{rel(case_dir / 'case.json')} must classify meaning_loss_risk")
    if "risk_report_only" not in expect_list(metadata, "actions"):
        errors.append(f"{rel(case_dir / 'case.json')} must expect risk_report_only")
    if "meaning_loss_risk" not in report:
        errors.append(f"{rel(case_dir / 'expected' / 'report.md')} must report meaning_loss_risk")
    if metadata.get("stable_pages_rewritten") is not False:
        errors.append(f"{rel(case_dir / 'case.json')} must not rewrite stable pages")
    return errors


def check_code_wiki_mismatch(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    report = read_text(case_dir / "expected" / "report.md")
    if "drift_or_coverage_suspect" not in expect_list(metadata, "classifications"):
        errors.append(f"{rel(case_dir / 'case.json')} must classify drift_or_coverage_suspect")
    if "recommend_drift_radar" not in expect_list(metadata, "actions"):
        errors.append(f"{rel(case_dir / 'case.json')} must expect recommend_drift_radar")
    if "wiki-drift-radar" not in report:
        errors.append(f"{rel(case_dir / 'expected' / 'report.md')} must recommend wiki-drift-radar")
    if metadata.get("stable_pages_rewritten") is not False:
        errors.append(f"{rel(case_dir / 'case.json')} must not rewrite stable pages")
    return errors


def check_audit_only(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if metadata.get("mode") != "audit-only":
        errors.append(f"{rel(case_dir / 'case.json')} must set mode to audit-only")
    if metadata.get("stable_pages_rewritten") is not False:
        errors.append(f"{rel(case_dir / 'case.json')} must not rewrite stable pages")

    expected_wiki = case_dir / "expected" / "wiki"
    if expected_wiki.exists():
        for expected_path in sorted(expected_wiki.rglob("*.md")):
            relative_path = expected_path.relative_to(expected_wiki)
            input_path = case_dir / "input" / "wiki" / relative_path
            if not input_path.exists():
                errors.append(f"{rel(input_path)} must exist for audit-only no-write comparison")
                continue
            if read_text(input_path) != read_text(expected_path):
                errors.append(f"{rel(expected_path)} must match input for audit-only no-write")

    return errors


def check_old_module_map_safe_whitebox(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    report = read_text(case_dir / "expected" / "report.md")

    if "safe_guidance_rewrite" not in expect_list(metadata, "classifications"):
        errors.append(f"{rel(case_dir / 'case.json')} must classify safe_guidance_rewrite")
    if "add_table_or_diagram" not in expect_list(metadata, "actions"):
        errors.append(f"{rel(case_dir / 'case.json')} must expect add_table_or_diagram")
    if metadata.get("stable_pages_rewritten") is not True:
        errors.append(f"{rel(case_dir / 'case.json')} must rewrite the module page")
    if "Whitebox files refreshed:" not in report:
        errors.append(f"{rel(case_dir / 'expected' / 'report.md')} must report refreshed Whitebox files")

    source_value = metadata.get("whitebox_source")
    svg_value = metadata.get("whitebox_svg")
    derived_value = metadata.get("whitebox_derived_svgs", {})
    module_page_value = metadata.get("module_page")
    derived_paths: dict[str, str] = {}
    if not isinstance(source_value, str) or not source_value.endswith(".whitebox.yaml"):
        errors.append(f"{rel(case_dir / 'case.json')} must set whitebox_source")
        source_path = None
    else:
        source_path = case_dir / "expected" / source_value
        if not source_path.exists():
            errors.append(f"{rel(source_path)} must exist")

    if not isinstance(svg_value, str) or not svg_value.endswith(".whitebox.svg"):
        errors.append(f"{rel(case_dir / 'case.json')} must set whitebox_svg")
        svg_path = None
    else:
        svg_path = case_dir / "expected" / svg_value
        if not svg_path.exists():
            errors.append(f"{rel(svg_path)} must exist")

    if not isinstance(module_page_value, str) or not module_page_value.endswith(".md"):
        errors.append(f"{rel(case_dir / 'case.json')} must set module_page")
        module_page_path = None
    else:
        module_page_path = case_dir / "expected" / module_page_value
        if not module_page_path.exists():
            errors.append(f"{rel(module_page_path)} must exist")

    if not isinstance(derived_value, dict):
        errors.append(f"{rel(case_dir / 'case.json')} whitebox_derived_svgs must be an object")
    else:
        for view_name, path_value in derived_value.items():
            if view_name not in DERIVED_VIEW_NAMES:
                errors.append(f"{rel(case_dir / 'case.json')} has unknown derived view {view_name!r}")
                continue
            if not isinstance(path_value, str) or not path_value.endswith(f".whitebox.{view_name}.svg"):
                errors.append(f"{rel(case_dir / 'case.json')} must set {view_name} derived SVG path")
                continue
            derived_paths[view_name] = path_value

    if module_page_path and source_value and svg_value and module_page_path.exists():
        module_page = read_text(module_page_path)
        source_name = Path(source_value).name
        svg_name = Path(svg_value).name
        errors.extend(
            check_module_page_whitebox_embeds(
                module_page_path,
                module_page,
                source_name,
                svg_name,
                derived_paths,
                set(derived_paths),
            )
        )

    if source_path and source_path.exists():
        source_text = read_text(source_path)
        for phrase in expect_list(metadata, "whitebox_model_must_contain"):
            if phrase not in source_text:
                errors.append(f"{rel(source_path)} must contain {phrase!r}")

        model, load_errors = load_source_model(source_path)
        for error in load_errors:
            errors.append(error)
        if not load_errors:
            validation_errors = validate_source_model(model)
            for error in validation_errors:
                errors.append(error)
            if not validation_errors and svg_path and svg_path.exists() and isinstance(model, dict):
                rendered_svg = render_svg(model, backend=DEFAULT_RENDER_BACKEND)
                expected_svg = read_text(svg_path)
                if rendered_svg != expected_svg:
                    errors.append(f"{rel(svg_path)} must be rendered from {rel(source_path)}")

                derived_models = build_derived_view_models(model)
                generated_views = set(derived_models)
                if generated_views and not derived_paths:
                    errors.append(f"{rel(case_dir / 'case.json')} must list generated Derived Whitebox View SVGs")
                for view_name in sorted(set(derived_paths) - generated_views):
                    errors.append(f"{rel(case_dir / 'case.json')} must not list empty {view_name} Derived Whitebox View")
                for view_name, derived_model in derived_models.items():
                    path_value = derived_paths.get(view_name)
                    if path_value is None:
                        errors.append(f"{rel(case_dir / 'case.json')} must list non-empty {view_name} Derived Whitebox View")
                        continue
                    derived_path = case_dir / "expected" / path_value
                    if not derived_path.exists():
                        errors.append(f"{rel(derived_path)} must exist")
                        continue
                    rendered_derived = render_svg(
                        derived_model,
                        backend=DEFAULT_RENDER_BACKEND,
                        view=whitebox_view(view_name),
                    )
                    if rendered_derived != read_text(derived_path):
                        errors.append(f"{rel(derived_path)} must be rendered from {rel(source_path)}")

                expected_module_page = module_page_path if module_page_path and module_page_path.exists() else None
                if expected_module_page is not None:
                    errors.extend(
                        check_module_page_whitebox_embeds(
                            expected_module_page,
                            read_text(expected_module_page),
                            Path(source_value).name,
                            Path(svg_value).name,
                            derived_paths,
                            generated_views,
                        )
                    )

                for view_name in DERIVED_VIEW_NAMES:
                    if view_name in generated_views:
                        continue
                    empty_view_path = source_path.parent / derived_svg_file_name(source_path, view_name)
                    if empty_view_path.exists():
                        errors.append(f"{rel(empty_view_path)} must be absent because the {view_name} derived view is empty")

    errors.extend(check_expected_text_requirements(case_dir, metadata))
    return errors


def check_old_module_map_meaning_loss(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors = check_naming_conflict(case_dir, metadata)
    errors.extend(check_unchanged_wiki_paths(case_dir, metadata))
    errors.extend(check_expected_text_requirements(case_dir, metadata))
    errors.extend(check_no_expected_whitebox_files(case_dir))
    return errors


def check_old_module_map_drift_radar(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors = check_code_wiki_mismatch(case_dir, metadata)
    errors.extend(check_unchanged_wiki_paths(case_dir, metadata))
    errors.extend(check_expected_text_requirements(case_dir, metadata))
    errors.extend(check_no_expected_whitebox_files(case_dir))
    return errors


def check_boundary_wording() -> list[str]:
    errors: list[str] = []
    docs = [DOC_ROOT / "README.md"]
    docs.extend(sorted(FIXTURE_ROOT.glob("*/expected/*.md")))

    for path in docs:
        if not path.exists():
            continue
        text = read_text(path)
        for pattern in BOUNDARY_WORDING_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{rel(path)} uses mechanical quality wording near {match.group(0)!r}"
                )

    return errors


def main() -> int:
    errors: list[str] = []
    cases: list[tuple[Path, dict[str, object]]] = []

    if not FIXTURE_ROOT.exists():
        print(f"Fixture directory is missing: {rel(FIXTURE_ROOT)}")
        return 1

    for case_dir in sorted(path for path in FIXTURE_ROOT.iterdir() if path.is_dir()):
        metadata, load_errors = load_case(case_dir)
        errors.extend(load_errors)
        if metadata is None:
            continue
        errors.extend(check_basic_contract(case_dir, metadata))
        cases.append((case_dir, metadata))

    seen_behaviors = {
        metadata.get("behavior")
        for _, metadata in cases
        if isinstance(metadata.get("behavior"), str)
    }
    for behavior in sorted(REQUIRED_BEHAVIORS - seen_behaviors):
        errors.append(f"Missing fixture behavior: {behavior}")

    behavior_checks = {
        "active_drift_page_stops_before_audit_or_rewrite": check_active_drift_gate,
        "existing_incomplete_wiki_completes_skeleton_without_new_facts": check_incomplete_skeleton,
        "duplicate_same_concept_pages_preserve_unique_info_and_links": check_duplicate_same_concept,
        "naming_conflicts_report_meaning_loss_risk": check_naming_conflict,
        "suspected_code_wiki_mismatch_recommends_drift_radar": check_code_wiki_mismatch,
        "audit_only_does_not_rewrite_stable_pages": check_audit_only,
        "old_module_map_refreshes_to_whitebox_source_and_svg": check_old_module_map_safe_whitebox,
        "old_module_map_insufficient_evidence_reports_meaning_loss_risk": check_old_module_map_meaning_loss,
        "old_module_map_needing_code_comparison_recommends_drift_radar": check_old_module_map_drift_radar,
    }

    for case_dir, metadata in cases:
        behavior = metadata.get("behavior")
        check = behavior_checks.get(behavior)
        if check:
            errors.extend(check(case_dir, metadata))

    errors.extend(check_boundary_wording())

    if errors:
        print("Boundary check found problems:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Checked {len(cases)} wiki-doctor fixture contracts.")
    print("Covered behaviors:")
    for behavior in sorted(seen_behaviors):
        print(f"- {behavior}")
    print(
        "This only checks fixture coverage and boundary wording; "
        "it does not prove wiki meaning is right."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
