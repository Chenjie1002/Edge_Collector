from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class EffectiveMappingUnavailable(ValueError):
    """The baseline or controlled active mapping cannot be trusted."""


@dataclass(frozen=True)
class EffectiveMappingPath:
    path: Path
    source: str
    used_overlay: bool


@dataclass(frozen=True)
class EffectiveMappingDocument:
    path: Path
    source: str
    used_overlay: bool
    content_sha256: str
    root: dict[str, Any]


def resolve_effective_mapping_path(
    baseline_path: str | Path,
    *,
    deployment_config_dir: str | Path | None = None,
) -> EffectiveMappingPath:
    baseline = _regular_non_symlink(Path(baseline_path), "baseline mapping")
    store = _deployment_config_dir(baseline, deployment_config_dir)
    store_state = _directory_state(store, "deployment-config store")
    if store_state == "absent":
        return EffectiveMappingPath(
            path=baseline,
            source=_source_label(baseline, used_overlay=False),
            used_overlay=False,
        )
    active = store / "active" / "mapping.yaml"
    active_dir_state = _directory_state(active.parent, "active mapping directory")
    if active_dir_state == "absent":
        return EffectiveMappingPath(
            path=baseline,
            source=_source_label(baseline, used_overlay=False),
            used_overlay=False,
        )
    try:
        active_stat = active.lstat()
    except FileNotFoundError:
        return EffectiveMappingPath(
            path=baseline,
            source=_source_label(baseline, used_overlay=False),
            used_overlay=False,
        )
    except OSError as exc:
        raise EffectiveMappingUnavailable("active mapping cannot be inspected") from exc

    if stat.S_ISLNK(active_stat.st_mode):
        raise EffectiveMappingUnavailable("active mapping must not be a symlink")
    if not stat.S_ISREG(active_stat.st_mode):
        raise EffectiveMappingUnavailable("active mapping must be a regular file")
    try:
        active_path = active.resolve(strict=True)
    except OSError as exc:
        raise EffectiveMappingUnavailable("active mapping cannot be resolved") from exc
    return EffectiveMappingPath(
        path=active_path,
        source=_source_label(active, used_overlay=True),
        used_overlay=True,
    )


def read_effective_mapping(
    baseline_path: str | Path,
    *,
    deployment_config_dir: str | Path | None = None,
) -> EffectiveMappingDocument:
    selection = resolve_effective_mapping_path(
        baseline_path,
        deployment_config_dir=deployment_config_dir,
    )
    try:
        raw_bytes = selection.path.read_bytes()
        root = yaml.safe_load(raw_bytes.decode("utf-8"))
    except EffectiveMappingUnavailable:
        raise
    except Exception as exc:
        raise EffectiveMappingUnavailable("effective mapping cannot be parsed") from exc
    if not isinstance(root, dict):
        raise EffectiveMappingUnavailable("effective mapping root must be a mapping")
    return EffectiveMappingDocument(
        path=selection.path,
        source=selection.source,
        used_overlay=selection.used_overlay,
        content_sha256=hashlib.sha256(raw_bytes).hexdigest(),
        root=root,
    )


def _deployment_config_dir(
    baseline: Path,
    configured: str | Path | None,
) -> Path:
    if configured is not None:
        return Path(configured)
    environment_value = os.environ.get("DEPLOYMENT_CONFIG_DIR")
    if environment_value:
        return Path(environment_value)
    return baseline.parent.parent / "data" / "deployment-config"


def _regular_non_symlink(path: Path, label: str) -> Path:
    try:
        path_stat = path.lstat()
    except OSError as exc:
        raise EffectiveMappingUnavailable(f"{label} cannot be inspected") from exc
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISREG(path_stat.st_mode):
        raise EffectiveMappingUnavailable(f"{label} must be a regular file")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise EffectiveMappingUnavailable(f"{label} cannot be resolved") from exc


def _directory_state(path: Path, label: str) -> str:
    try:
        path_stat = path.lstat()
    except FileNotFoundError:
        return "absent"
    except OSError as exc:
        raise EffectiveMappingUnavailable(f"{label} cannot be inspected") from exc
    if stat.S_ISLNK(path_stat.st_mode):
        raise EffectiveMappingUnavailable(f"{label} must not be a symlink")
    if not stat.S_ISDIR(path_stat.st_mode):
        raise EffectiveMappingUnavailable(f"{label} must be a directory")
    return "present"


def _source_label(path: Path, *, used_overlay: bool) -> str:
    if used_overlay:
        return "active/mapping.yaml"
    parts = path.parts
    if len(parts) >= 2 and parts[-2:] == ("config", "mapping.yaml"):
        return "config/mapping.yaml"
    return path.name
