from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_collector_build_context_includes_shared_common_package() -> None:
    compose = yaml.safe_load(
        (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    )

    collector_build = compose["services"]["collector"]["build"]

    assert collector_build == {
        "context": ".",
        "dockerfile": "collector/Dockerfile",
    }


def test_collector_dockerfile_materializes_runtime_import_closure() -> None:
    dockerfile_lines = {
        line.strip()
        for line in (ROOT / "collector" / "Dockerfile")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    assert "COPY collector/requirements.txt ./requirements.txt" in dockerfile_lines
    assert "COPY collector/app ./app" in dockerfile_lines
    assert "COPY common ./common" in dockerfile_lines
