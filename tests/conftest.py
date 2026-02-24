"""
Shared pytest fixtures for AG_Orquesta_Desk test suite.

Provides isolated temporary directories, mock configurations, and
fake project structures so tests never touch real filesystem state.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure scripts/ is importable
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# Fixtures: Temporary filesystem structures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_ecosystem(tmp_path):
    """Create a minimal fake Antigravity ecosystem directory tree.

    Layout:
        tmp_path/
            00_CORE/
                AG_Plantilla/
                    _template/workspace/
                    config/
                    docs/
                    data/
            01_HOSPITAL_PRIVADO/
                AG_Hospital/
                    docs/
                    .git/   (empty marker)
            02_HOSPITAL_PUBLICO/
                AG_NB_Apps/
                    docs/
    """
    core = tmp_path / "00_CORE"
    plantilla = core / "AG_Plantilla"
    template_ws = plantilla / "_template" / "workspace"
    template_ws.mkdir(parents=True)
    (plantilla / "config").mkdir(parents=True)
    (plantilla / "docs").mkdir(parents=True)
    (plantilla / "data").mkdir(parents=True)

    hosp_priv = tmp_path / "01_HOSPITAL_PRIVADO"
    hospital = hosp_priv / "AG_Hospital"
    (hospital / "docs").mkdir(parents=True)
    (hospital / ".git").mkdir(parents=True)

    hosp_pub = tmp_path / "02_HOSPITAL_PUBLICO"
    nb_apps = hosp_pub / "AG_NB_Apps"
    (nb_apps / "docs").mkdir(parents=True)

    return {
        "root": tmp_path,
        "plantilla": plantilla,
        "template_ws": template_ws,
        "hospital": hospital,
        "nb_apps": nb_apps,
    }


@pytest.fixture
def environments_json(tmp_ecosystem):
    """Write a minimal environments.json and return its path."""
    config = {
        "schema_version": "1.0",
        "environments": {
            "test": {
                "base_path": str(tmp_ecosystem["root"]),
                "projects_dirs": [
                    "01_HOSPITAL_PRIVADO",
                    "02_HOSPITAL_PUBLICO",
                ],
                "plantilla_dir": "00_CORE\\AG_Plantilla",
                "capabilities": ["git", "python"],
                "is_default": True,
            }
        },
        "active_environment": "test",
        "env_var_override": "AG_ENV",
    }
    config_path = tmp_ecosystem["plantilla"] / "config" / "environments.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return config_path


@pytest.fixture
def project_registry_json(tmp_ecosystem):
    """Write a minimal project_registry.json and return its path."""
    registry = {
        "registry_version": "1.0",
        "categories": {
            "hospital-personal": {"icon": "H", "description": "Hospital privado"},
        },
        "projects": [
            {
                "id": "ag-hospital",
                "name": "AG_Hospital",
                "category": "hospital-personal",
                "type": "python-app",
                "path_relative": "01_HOSPITAL_PRIVADO/AG_Hospital",
            },
            {
                "id": "ag-nb-apps",
                "name": "AG_NB_Apps",
                "category": "hospital-personal",
                "type": "nocobase",
                "path_relative": "02_HOSPITAL_PUBLICO/AG_NB_Apps",
            },
        ],
    }
    config_path = tmp_ecosystem["plantilla"] / "config" / "project_registry.json"
    config_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return config_path


@pytest.fixture
def mock_env_resolver(tmp_ecosystem):
    """Patch env_resolver functions to use the tmp_ecosystem paths.

    Usage in tests:
        def test_something(mock_env_resolver):
            # Now all env_resolver.get_* functions return tmp paths
            ...
    """
    eco = tmp_ecosystem

    def _get_repo_root():
        return eco["root"]

    def _get_projects_dirs():
        dirs = []
        for d in sorted(eco["root"].iterdir()):
            if d.is_dir() and d.name[:2].isdigit():
                dirs.append(d)
        return dirs

    def _get_plantilla_dir():
        return eco["plantilla"]

    def _get_template_dir():
        return eco["plantilla"] / "_template" / "workspace"

    def _list_ag_projects():
        projects = []
        for domain_dir in _get_projects_dirs():
            if domain_dir.exists():
                projects.extend(
                    d
                    for d in domain_dir.iterdir()
                    if d.is_dir() and d.name.startswith("AG_")
                )
        return sorted(projects)

    patches = {
        "env_resolver.get_repo_root": patch(
            "env_resolver.get_repo_root", side_effect=_get_repo_root
        ),
        "env_resolver.get_projects_dirs": patch(
            "env_resolver.get_projects_dirs", side_effect=_get_projects_dirs
        ),
        "env_resolver.get_plantilla_dir": patch(
            "env_resolver.get_plantilla_dir", side_effect=_get_plantilla_dir
        ),
        "env_resolver.get_template_dir": patch(
            "env_resolver.get_template_dir", side_effect=_get_template_dir
        ),
        "env_resolver.list_ag_projects": patch(
            "env_resolver.list_ag_projects", side_effect=_list_ag_projects
        ),
    }
    started = {}
    for name, p in patches.items():
        try:
            started[name] = p.start()
        except Exception:
            pass

    yield eco

    for p in patches.values():
        try:
            p.stop()
        except Exception:
            pass
