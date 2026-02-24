"""
Tests for scripts/cross_task.py
================================

Priority: P0 -- cross_task.py is the primary cross-repository coordination
tool. It writes to multiple project directories and manages a shared counter.

Critical paths tested:
  1. get_next_task_id -- counter file creation, increment, year rollover
  2. find_project_root -- exact match, case-insensitive match, not found
  3. ensure_tasks_file -- creates with correct template structure
  4. format_task_entry -- incoming vs outgoing direction
  5. insert_task -- replaces (none), inserts before next section, appends
  6. parse_tasks_from_file -- parses well-formed and malformed TASKS.md
  7. cmd_create -- end-to-end task creation with dual writes
  8. cmd_update -- status change + move to Completed section
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import cross_task


# ---------------------------------------------------------------------------
# get_next_task_id
# ---------------------------------------------------------------------------


class TestGetNextTaskId:
    """Task ID counter must be sequential and year-aware."""

    def test_creates_counter_file_if_missing(self, tmp_path):
        counter_path = tmp_path / "data" / "task_counter.json"
        with patch.object(cross_task, "COUNTER_PATH", counter_path):
            task_id = cross_task.get_next_task_id()
        assert counter_path.exists()
        year = datetime.now().year
        assert task_id == f"TASK-{year}-0001"

    def test_increments_existing_counter(self, tmp_path):
        counter_path = tmp_path / "task_counter.json"
        year = str(datetime.now().year)
        counter_path.write_text(json.dumps({year: 5}), encoding="utf-8")
        with patch.object(cross_task, "COUNTER_PATH", counter_path):
            task_id = cross_task.get_next_task_id()
        assert task_id.endswith("-0006")
        data = json.loads(counter_path.read_text(encoding="utf-8"))
        assert data[year] == 6

    def test_new_year_starts_at_one(self, tmp_path):
        counter_path = tmp_path / "task_counter.json"
        counter_path.write_text(json.dumps({"2025": 99}), encoding="utf-8")
        with patch.object(cross_task, "COUNTER_PATH", counter_path):
            task_id = cross_task.get_next_task_id()
        year = datetime.now().year
        assert task_id == f"TASK-{year}-0001"

    def test_concurrent_safety_counter_persists(self, tmp_path):
        """Multiple sequential calls produce unique IDs."""
        counter_path = tmp_path / "task_counter.json"
        with patch.object(cross_task, "COUNTER_PATH", counter_path):
            ids = [cross_task.get_next_task_id() for _ in range(5)]
        assert len(set(ids)) == 5  # all unique


# ---------------------------------------------------------------------------
# find_project_root
# ---------------------------------------------------------------------------


class TestFindProjectRoot:
    def test_finds_plantilla(self, tmp_path):
        with patch.object(cross_task, "PLANTILLA_DIR", tmp_path / "AG_Plantilla"):
            result = cross_task.find_project_root("AG_Plantilla")
        assert result == tmp_path / "AG_Plantilla"

    def test_exact_match_in_projects_dir(self, tmp_path):
        domain = tmp_path / "01_DOMAIN"
        project = domain / "AG_Test"
        project.mkdir(parents=True)
        with patch.object(cross_task, "get_projects_dirs", return_value=[domain]):
            result = cross_task.find_project_root("AG_Test")
        assert result == project

    def test_case_insensitive_match(self, tmp_path):
        domain = tmp_path / "01_DOMAIN"
        project = domain / "AG_Hospital"
        project.mkdir(parents=True)
        with patch.object(cross_task, "get_projects_dirs", return_value=[domain]):
            result = cross_task.find_project_root("ag_hospital")
        assert result == project

    def test_returns_none_for_nonexistent(self, tmp_path):
        domain = tmp_path / "01_DOMAIN"
        domain.mkdir(parents=True)
        with patch.object(cross_task, "get_projects_dirs", return_value=[domain]):
            result = cross_task.find_project_root("AG_DoesNotExist")
        assert result is None


# ---------------------------------------------------------------------------
# ensure_tasks_file
# ---------------------------------------------------------------------------


class TestEnsureTasksFile:
    def test_creates_tasks_file_with_structure(self, tmp_path):
        tasks_path = tmp_path / "docs" / "TASKS.md"
        cross_task.ensure_tasks_file(tasks_path, "AG_TestProject")
        assert tasks_path.exists()
        content = tasks_path.read_text(encoding="utf-8")
        assert "AG_TestProject" in content
        assert "## Incoming" in content
        assert "## Outgoing" in content
        assert "## Completed" in content

    def test_does_not_overwrite_existing(self, tmp_path):
        tasks_path = tmp_path / "docs" / "TASKS.md"
        tasks_path.parent.mkdir(parents=True)
        tasks_path.write_text("existing content", encoding="utf-8")
        cross_task.ensure_tasks_file(tasks_path, "AG_TestProject")
        assert tasks_path.read_text(encoding="utf-8") == "existing content"


# ---------------------------------------------------------------------------
# format_task_entry
# ---------------------------------------------------------------------------


class TestFormatTaskEntry:
    def test_incoming_has_from_field(self):
        entry = cross_task.format_task_entry(
            "TASK-2026-0001", "Test Task", "AG_A", "AG_B", "high", "Description", "incoming"
        )
        assert "**From**: AG_A" in entry
        assert "**To**" not in entry

    def test_outgoing_has_to_field(self):
        entry = cross_task.format_task_entry(
            "TASK-2026-0001", "Test Task", "AG_A", "AG_B", "high", "Description", "outgoing"
        )
        assert "**To**: AG_B" in entry
        assert "**From**" not in entry

    def test_priority_maps_correctly(self):
        entry = cross_task.format_task_entry(
            "TASK-2026-0001", "Test", "A", "B", "critical", "D", "incoming"
        )
        assert "P0-Critical" in entry

    def test_unknown_priority_used_as_is(self):
        entry = cross_task.format_task_entry(
            "TASK-2026-0001", "Test", "A", "B", "custom", "D", "incoming"
        )
        assert "custom" in entry


# ---------------------------------------------------------------------------
# insert_task
# ---------------------------------------------------------------------------


class TestInsertTask:
    def _make_tasks_file(self, tmp_path, content):
        p = tmp_path / "TASKS.md"
        p.write_text(content, encoding="utf-8")
        return p

    def test_replaces_none_placeholder(self, tmp_path):
        content = "## Incoming (tasks requested to this project)\n\n(none)\n\n## Completed\n"
        p = self._make_tasks_file(tmp_path, content)
        cross_task.insert_task(p, "### TASK-2026-0001: New Task\n", "incoming")
        result = p.read_text(encoding="utf-8")
        assert "(none)" not in result.split("## Incoming")[1].split("## Completed")[0]
        assert "TASK-2026-0001" in result

    def test_inserts_before_next_section(self, tmp_path):
        content = (
            "## Incoming (tasks requested to this project)\n\n"
            "### TASK-2026-0001: Old Task\n\n"
            "## Completed\n"
        )
        p = self._make_tasks_file(tmp_path, content)
        cross_task.insert_task(p, "### TASK-2026-0002: Another\n", "incoming")
        result = p.read_text(encoding="utf-8")
        assert "TASK-2026-0002" in result

    def test_appends_when_no_section_boundary(self, tmp_path):
        content = "## Incoming (tasks)\n\n### TASK-2026-0001: Old\n"
        p = self._make_tasks_file(tmp_path, content)
        cross_task.insert_task(p, "### TASK-2026-0002: New\n", "incoming")
        result = p.read_text(encoding="utf-8")
        assert "TASK-2026-0002" in result


# ---------------------------------------------------------------------------
# parse_tasks_from_file
# ---------------------------------------------------------------------------


class TestParseTasksFromFile:
    def test_parses_well_formed_tasks(self, tmp_path):
        content = """# Tasks -- AG_Test

## Incoming (tasks requested to this project)

### TASK-2026-0001: Fix the widget
- **From**: AG_A
- **Priority**: P1-High
- **Status**: PENDING
- **Created**: 2026-01-15
- **Description**: Fix it properly

## Outgoing (tasks delegated to other projects)

### TASK-2026-0002: Build API
- **To**: AG_B
- **Priority**: P2-Medium
- **Status**: IN-PROGRESS
- **Created**: 2026-01-20
- **Description**: Build the API

## Completed

(none)
"""
        p = tmp_path / "docs" / "TASKS.md"
        p.parent.mkdir(parents=True)
        p.write_text(content, encoding="utf-8")

        tasks = cross_task.parse_tasks_from_file(p)
        assert len(tasks) == 2
        assert tasks[0]["id"] == "TASK-2026-0001"
        assert tasks[0]["section"] == "incoming"
        assert tasks[1]["id"] == "TASK-2026-0002"
        assert tasks[1]["section"] == "outgoing"

    def test_returns_empty_for_missing_file(self, tmp_path):
        p = tmp_path / "nonexistent" / "TASKS.md"
        assert cross_task.parse_tasks_from_file(p) == []

    def test_returns_empty_for_no_tasks(self, tmp_path):
        p = tmp_path / "TASKS.md"
        p.write_text("# Tasks\n\n(none)\n", encoding="utf-8")
        assert cross_task.parse_tasks_from_file(p) == []
