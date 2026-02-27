"""
Tests for scripts/propagate.py
================================

Priority: P1 -- propagate.py writes files to project directories and
can auto-commit via git subprocess, making it high-risk for data loss.

Critical paths tested:
  1. get_all_projects -- scanning for AG_* directories
  2. get_template_content -- placeholder replacement, missing files
  3. compute_drift -- MISSING vs DRIFTED detection
  4. cmd_apply -- file creation, overwrite behavior
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import propagate


# ---------------------------------------------------------------------------
# get_all_projects
# ---------------------------------------------------------------------------


class TestGetAllProjects:
    def test_finds_g_dirs(self, tmp_path):
        domain = tmp_path / "01_DOMAIN"
        (domain / "G_Alpha").mkdir(parents=True)
        (domain / "G_Beta").mkdir(parents=True)
        (domain / "NotG").mkdir(parents=True)

        with patch.object(propagate, "PROJECTS_DIRS", [domain]):
            result = propagate.get_all_projects()
        names = [name for name, _ in result]
        assert "G_Alpha" in names
        assert "G_Beta" in names
        assert "NotG" not in names

    def test_empty_when_dir_missing(self, tmp_path):
        with patch.object(propagate, "PROJECTS_DIRS", [tmp_path / "nope"]):
            result = propagate.get_all_projects()
        assert result == []


# ---------------------------------------------------------------------------
# get_template_content
# ---------------------------------------------------------------------------


class TestGetTemplateContent:
    def test_returns_none_for_missing_template(self, tmp_path):
        with patch.object(propagate, "TEMPLATE_DIR", tmp_path):
            result = propagate.get_template_content("nonexistent.md")
        assert result is None

    def test_reads_plain_file(self, tmp_path):
        (tmp_path / "plain.md").write_text("Hello World", encoding="utf-8")
        with patch.object(propagate, "TEMPLATE_DIR", tmp_path):
            result = propagate.get_template_content("plain.md")
        assert result == "Hello World"

    def test_replaces_placeholder_for_templated_files(self, tmp_path):
        (tmp_path / "GEMINI.md").write_text(
            "Project: {{PROJECT_NAME}}", encoding="utf-8"
        )
        with patch.object(propagate, "TEMPLATE_DIR", tmp_path):
            result = propagate.get_template_content("GEMINI.md", "AG_Hospital")
        assert result == "Project: AG_Hospital"
        assert "{{PROJECT_NAME}}" not in result

    def test_no_replacement_without_project_name(self, tmp_path):
        (tmp_path / "GEMINI.md").write_text(
            "Project: {{PROJECT_NAME}}", encoding="utf-8"
        )
        with patch.object(propagate, "TEMPLATE_DIR", tmp_path):
            result = propagate.get_template_content("GEMINI.md")
        assert "{{PROJECT_NAME}}" in result


# ---------------------------------------------------------------------------
# compute_drift
# ---------------------------------------------------------------------------


class TestComputeDrift:
    def test_missing_file_is_detected(self, tmp_path):
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        (template_dir / "GEMINI.md").write_text("content", encoding="utf-8")

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        # GEMINI.md does not exist in project

        with (
            patch.object(propagate, "TEMPLATE_DIR", template_dir),
            patch.object(propagate, "PROPAGATED_FILES", ["GEMINI.md"]),
        ):
            drifts = propagate.compute_drift("AG_Test", project_dir)
        assert len(drifts) == 1
        assert drifts[0]["status"] == "MISSING"

    def test_identical_files_no_drift(self, tmp_path):
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        (template_dir / ".gitignore").write_text(".env\n__pycache__", encoding="utf-8")

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".gitignore").write_text(".env\n__pycache__", encoding="utf-8")

        with (
            patch.object(propagate, "TEMPLATE_DIR", template_dir),
            patch.object(propagate, "PROPAGATED_FILES", [".gitignore"]),
        ):
            drifts = propagate.compute_drift("AG_Test", project_dir)
        assert drifts == []

    def test_different_content_is_drifted(self, tmp_path):
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        (template_dir / ".gitignore").write_text("v2 content", encoding="utf-8")

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".gitignore").write_text("old content", encoding="utf-8")

        with (
            patch.object(propagate, "TEMPLATE_DIR", template_dir),
            patch.object(propagate, "PROPAGATED_FILES", [".gitignore"]),
        ):
            drifts = propagate.compute_drift("AG_Test", project_dir)
        assert len(drifts) == 1
        assert drifts[0]["status"] == "DRIFTED"
        assert drifts[0]["diff"] is not None


# ---------------------------------------------------------------------------
# cmd_apply (integration-like)
# ---------------------------------------------------------------------------


class TestCmdApply:
    def test_apply_creates_missing_file(self, tmp_path):
        """--apply --all should create files from template."""
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        (template_dir / ".gitignore").write_text(".env\nnode_modules", encoding="utf-8")

        project_dir = tmp_path / "projects" / "AG_Test"
        project_dir.mkdir(parents=True)
        # no .gitignore in project

        with (
            patch.object(propagate, "TEMPLATE_DIR", template_dir),
            patch.object(propagate, "PROPAGATED_FILES", [".gitignore"]),
            patch.object(
                propagate,
                "get_all_projects",
                return_value=[("AG_Test", project_dir)],
            ),
        ):
            import argparse

            args = argparse.Namespace(file=None, all=True)
            propagate.cmd_apply(args)

        created = project_dir / ".gitignore"
        assert created.exists()
        assert ".env" in created.read_text(encoding="utf-8")
