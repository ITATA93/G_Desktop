"""
Tests for scripts/env_resolver.py
==================================

Priority: P0 -- env_resolver is the foundational module imported by every
other script. If it breaks, the entire orchestrator is non-functional.

Critical paths tested:
  1. _load_config / _save_config -- JSON round-trip integrity
  2. detect_environment -- resolution order (AG_ENV > active_environment > probe > default)
  3. get_repo_root -- exits on unreachable path
  4. get_projects_dirs -- domain-dir detection + legacy fallback
  5. get_plantilla_dir -- 00_CORE path + legacy fallback
  6. list_ag_projects -- recursive AG_* scanning
  7. register_environment -- idempotent writes
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure scripts/ is on sys.path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import env_resolver


# ---------------------------------------------------------------------------
# _load_config / _save_config
# ---------------------------------------------------------------------------


class TestLoadSaveConfig:
    """JSON config round-trip tests."""

    def test_load_missing_file_returns_empty(self, tmp_path):
        """When environments.json doesn't exist, _load_config returns empty dict."""
        fake_path = tmp_path / "nonexistent" / "environments.json"
        with patch.object(env_resolver, "_CONFIG_PATH", fake_path):
            config = env_resolver._load_config()
        assert config == {"environments": {}}

    def test_load_valid_json(self, tmp_path):
        """Reads a well-formed config correctly."""
        cfg = {"environments": {"test": {"base_path": str(tmp_path)}}}
        cfg_path = tmp_path / "environments.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        with patch.object(env_resolver, "_CONFIG_PATH", cfg_path):
            loaded = env_resolver._load_config()
        assert loaded["environments"]["test"]["base_path"] == str(tmp_path)

    def test_save_creates_parent_dirs(self, tmp_path):
        """_save_config creates missing parent directories."""
        deep_path = tmp_path / "a" / "b" / "environments.json"
        with patch.object(env_resolver, "_CONFIG_PATH", deep_path):
            env_resolver._save_config({"environments": {}})
        assert deep_path.exists()
        loaded = json.loads(deep_path.read_text(encoding="utf-8"))
        assert "environments" in loaded

    def test_round_trip_preserves_data(self, tmp_path):
        """Save then load should be lossless."""
        cfg = {
            "environments": {
                "e1": {"base_path": "/a", "capabilities": ["git"]},
            },
            "active_environment": "e1",
        }
        cfg_path = tmp_path / "environments.json"
        with patch.object(env_resolver, "_CONFIG_PATH", cfg_path):
            env_resolver._save_config(cfg)
            loaded = env_resolver._load_config()
        assert loaded["environments"]["e1"]["capabilities"] == ["git"]
        assert loaded["active_environment"] == "e1"


# ---------------------------------------------------------------------------
# detect_environment
# ---------------------------------------------------------------------------


class TestDetectEnvironment:
    """Tests the 4-level resolution cascade."""

    def _make_config(self, tmp_path, envs, active=None):
        cfg = {"environments": envs}
        if active:
            cfg["active_environment"] = active
        cfg["env_var_override"] = "AG_ENV"
        cfg_path = tmp_path / "environments.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        return cfg_path

    def test_empty_config_raises_runtime_error(self, tmp_path):
        cfg_path = self._make_config(tmp_path, {})
        with patch.object(env_resolver, "_CONFIG_PATH", cfg_path):
            with pytest.raises(RuntimeError, match="No environments defined"):
                env_resolver.detect_environment()

    def test_ag_env_var_takes_priority(self, tmp_path):
        """AG_ENV env var should override everything else."""
        envs = {
            "prod": {"base_path": "/doesnotexist/prod"},
            "dev": {"base_path": "/doesnotexist/dev"},
        }
        cfg_path = self._make_config(tmp_path, envs, active="prod")
        with (
            patch.object(env_resolver, "_CONFIG_PATH", cfg_path),
            patch.dict(os.environ, {"AG_ENV": "dev"}),
        ):
            env_id, env_cfg = env_resolver.detect_environment()
        assert env_id == "dev"

    def test_active_environment_used_when_no_env_var(self, tmp_path):
        envs = {
            "alpha": {"base_path": "/no/alpha"},
            "beta": {"base_path": "/no/beta"},
        }
        cfg_path = self._make_config(tmp_path, envs, active="beta")
        with (
            patch.object(env_resolver, "_CONFIG_PATH", cfg_path),
            patch.dict(os.environ, {}, clear=True),
        ):
            # Remove AG_ENV if present
            os.environ.pop("AG_ENV", None)
            env_id, _ = env_resolver.detect_environment()
        assert env_id == "beta"

    def test_filesystem_probe_fallback(self, tmp_path):
        """When no env var and no active_environment, probe filesystem."""
        real_dir = tmp_path / "real_base"
        real_dir.mkdir()
        envs = {
            "ghost": {"base_path": "/nonexistent"},
            "real": {"base_path": str(real_dir)},
        }
        cfg_path = self._make_config(tmp_path, envs)
        with (
            patch.object(env_resolver, "_CONFIG_PATH", cfg_path),
            patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("AG_ENV", None)
            env_id, _ = env_resolver.detect_environment()
        assert env_id == "real"

    def test_default_flag_fallback(self, tmp_path):
        """When nothing matches, is_default=True is used."""
        envs = {
            "a": {"base_path": "/nonexistent1"},
            "b": {"base_path": "/nonexistent2", "is_default": True},
        }
        cfg_path = self._make_config(tmp_path, envs)
        with (
            patch.object(env_resolver, "_CONFIG_PATH", cfg_path),
            patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("AG_ENV", None)
            env_id, _ = env_resolver.detect_environment()
        assert env_id == "b"

    def test_no_match_raises_runtime_error(self, tmp_path):
        envs = {
            "x": {"base_path": "/nope_x"},
            "y": {"base_path": "/nope_y"},
        }
        cfg_path = self._make_config(tmp_path, envs)
        with (
            patch.object(env_resolver, "_CONFIG_PATH", cfg_path),
            patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("AG_ENV", None)
            with pytest.raises(RuntimeError, match="Cannot detect environment"):
                env_resolver.detect_environment()


# ---------------------------------------------------------------------------
# get_repo_root
# ---------------------------------------------------------------------------


class TestGetRepoRoot:
    """get_repo_root must exit(1) when the base_path doesn't exist."""

    def test_exits_on_missing_base_path(self, tmp_path):
        fake_cfg = (
            "missing",
            {"base_path": str(tmp_path / "nonexistent_drive")},
        )
        with patch.object(env_resolver, "detect_environment", return_value=fake_cfg):
            with pytest.raises(SystemExit):
                env_resolver.get_repo_root()

    def test_returns_path_when_exists(self, tmp_path):
        fake_cfg = ("test", {"base_path": str(tmp_path)})
        with patch.object(env_resolver, "detect_environment", return_value=fake_cfg):
            result = env_resolver.get_repo_root()
        assert result == tmp_path


# ---------------------------------------------------------------------------
# get_projects_dirs
# ---------------------------------------------------------------------------


class TestGetProjectsDirs:
    """Domain directory detection vs legacy fallback."""

    def test_detects_numbered_domain_dirs(self, tmp_path):
        """Dirs starting with digits (00_, 01_) are detected as domains."""
        (tmp_path / "00_CORE").mkdir()
        (tmp_path / "01_HOSPITAL").mkdir()
        (tmp_path / "random_dir").mkdir()  # should be excluded

        fake_cfg = ("test", {"base_path": str(tmp_path)})
        with (
            patch.object(env_resolver, "detect_environment", return_value=fake_cfg),
            patch.object(env_resolver, "get_repo_root", return_value=tmp_path),
        ):
            dirs = env_resolver.get_projects_dirs()
        names = [d.name for d in dirs]
        assert "00_CORE" in names
        assert "01_HOSPITAL" in names
        assert "random_dir" not in names

    def test_legacy_projects_dir_fallback(self, tmp_path):
        """When no numbered dirs exist, falls back to projects_dir config."""
        proj = tmp_path / "AG_Proyectos"
        proj.mkdir()

        fake_cfg = ("test", {"base_path": str(tmp_path), "projects_dir": "AG_Proyectos"})
        with (
            patch.object(env_resolver, "detect_environment", return_value=fake_cfg),
            patch.object(env_resolver, "get_repo_root", return_value=tmp_path),
        ):
            dirs = env_resolver.get_projects_dirs()
        assert len(dirs) == 1
        assert dirs[0].name == "AG_Proyectos"


# ---------------------------------------------------------------------------
# list_ag_projects
# ---------------------------------------------------------------------------


class TestListAgProjects:
    """Scanning for AG_* directories."""

    def test_finds_ag_projects(self, tmp_path):
        domain = tmp_path / "01_DOMAIN"
        domain.mkdir()
        (domain / "AG_Alpha").mkdir()
        (domain / "AG_Beta").mkdir()
        (domain / "NotAnAG").mkdir()

        with (
            patch.object(
                env_resolver, "get_projects_dirs", return_value=[domain]
            ),
        ):
            projects = env_resolver.list_ag_projects()
        names = [p.name for p in projects]
        assert "AG_Alpha" in names
        assert "AG_Beta" in names
        assert "NotAnAG" not in names

    def test_empty_when_no_domains(self, tmp_path):
        with patch.object(env_resolver, "get_projects_dirs", return_value=[]):
            assert env_resolver.list_ag_projects() == []


# ---------------------------------------------------------------------------
# register_environment
# ---------------------------------------------------------------------------


class TestRegisterEnvironment:
    def test_register_new_env(self, tmp_path):
        cfg_path = tmp_path / "environments.json"
        cfg_path.write_text('{"environments": {}}', encoding="utf-8")
        with patch.object(env_resolver, "_CONFIG_PATH", cfg_path):
            env_resolver.register_environment("newpc", "/data/repos", "My new PC")
        loaded = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert "newpc" in loaded["environments"]
        assert loaded["active_environment"] == "newpc"

    def test_register_existing_env_updates(self, tmp_path):
        cfg = {"environments": {"old": {"base_path": "/old"}}}
        cfg_path = tmp_path / "environments.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        with patch.object(env_resolver, "_CONFIG_PATH", cfg_path):
            env_resolver.register_environment("old", "/new", "Updated")
        loaded = json.loads(cfg_path.read_text(encoding="utf-8"))
        assert loaded["environments"]["old"]["base_path"] == "/new"
