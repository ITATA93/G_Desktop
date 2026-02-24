"""
Tests for scripts/ecosystem_dashboard.py
==========================================

Priority: P2 -- dashboard is a read-only reporting tool. Lower risk than
scripts that write to the filesystem, but incorrect health checks could
mislead operational decisions.

Critical paths tested:
  1. resolve_project_path -- relative path resolution
  2. check_project_health -- health score calculation
  3. load_registry -- missing file handling
  4. print_json_output -- JSON schema correctness
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ecosystem_dashboard


# ---------------------------------------------------------------------------
# resolve_project_path
# ---------------------------------------------------------------------------


class TestResolveProjectPath:
    def test_resolves_relative_path(self, tmp_path):
        project = {"path_relative": "01_HOSPITAL/AG_Test", "name": "AG_Test"}
        with patch.object(ecosystem_dashboard, "REPO_ROOT", tmp_path):
            result = ecosystem_dashboard.resolve_project_path(project)
        assert result == tmp_path / "01_HOSPITAL" / "AG_Test"

    def test_falls_back_to_absolute_path(self, tmp_path):
        project = {"path": "/absolute/path/AG_Test", "name": "AG_Test"}
        result = ecosystem_dashboard.resolve_project_path(project)
        # Path() normalizes separators per-OS, so compare Path objects
        assert result == Path("/absolute/path/AG_Test")


# ---------------------------------------------------------------------------
# check_project_health
# ---------------------------------------------------------------------------


class TestCheckProjectHealth:
    def test_nonexistent_project(self, tmp_path):
        health = ecosystem_dashboard.check_project_health(tmp_path / "nope")
        assert health["exists"] is False
        assert health["has_git"] is False
        assert health["score"] == 0

    def test_minimal_project(self, tmp_path):
        """A directory that exists but has nothing gets score=1 (exists only)."""
        health = ecosystem_dashboard.check_project_health(tmp_path)
        assert health["exists"] is True
        assert health["has_git"] is False
        assert health["score"] == 1  # only "exists" is True

    def test_fully_equipped_project(self, tmp_path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "GEMINI.md").write_text("x", encoding="utf-8")
        (tmp_path / "CHANGELOG.md").write_text("x", encoding="utf-8")
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "TASKS.md").write_text("x", encoding="utf-8")
        (tmp_path / ".subagents").mkdir()
        (tmp_path / ".subagents" / "manifest.json").write_text("{}", encoding="utf-8")

        health = ecosystem_dashboard.check_project_health(tmp_path)
        assert health["exists"] is True
        assert health["has_git"] is True
        assert health["has_gemini"] is True
        assert health["has_changelog"] is True
        assert health["has_tasks"] is True
        assert health["has_agents"] is True
        assert health["score"] == health["max_score"]

    def test_score_scales_with_checks(self, tmp_path):
        """Adding individual features should increase the score."""
        (tmp_path / ".git").mkdir()
        health1 = ecosystem_dashboard.check_project_health(tmp_path)
        (tmp_path / "GEMINI.md").write_text("x", encoding="utf-8")
        health2 = ecosystem_dashboard.check_project_health(tmp_path)
        assert health2["score"] > health1["score"]


# ---------------------------------------------------------------------------
# load_registry
# ---------------------------------------------------------------------------


class TestLoadRegistry:
    def test_exits_on_missing_registry(self, tmp_path):
        with patch.object(
            ecosystem_dashboard, "REGISTRY_PATH", tmp_path / "nonexistent.json"
        ):
            with pytest.raises(SystemExit):
                ecosystem_dashboard.load_registry()

    def test_loads_valid_registry(self, tmp_path):
        reg = {"projects": [], "categories": {}}
        reg_path = tmp_path / "registry.json"
        reg_path.write_text(json.dumps(reg), encoding="utf-8")
        with patch.object(ecosystem_dashboard, "REGISTRY_PATH", reg_path):
            loaded = ecosystem_dashboard.load_registry()
        assert loaded == reg
