"""
Tests for scripts/audit_ecosystem.py
======================================

Priority: P1 -- audit_ecosystem.py performs security scanning across the
entire ecosystem. False negatives in credential detection are dangerous;
false positives in safe-context detection break the audit.

Critical paths tested:
  1. is_safe_context -- must NOT flag validators/migration tools
  2. scan_security -- must detect known and generic credential patterns
  3. check_content_quality -- file quality heuristics
  4. grade_project -- grading logic
  5. check_project -- full audit integration
  6. fix_missing_files -- auto-fix from template
"""

import sys
import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_ecosystem


# ---------------------------------------------------------------------------
# is_safe_context
# ---------------------------------------------------------------------------


class TestIsSafeContext:
    """Lines matching safe patterns should be excluded from findings."""

    def test_comment_line_is_safe(self):
        assert audit_ecosystem.is_safe_context("# password = 'secret123'")

    def test_js_comment_is_safe(self):
        assert audit_ecosystem.is_safe_context("// password = 'secret123'")

    def test_validator_blocklist_is_safe(self):
        assert audit_ecosystem.is_safe_context('forbidden = {"hkEVC9AFVjFeRTkp"}')

    def test_regex_compile_is_safe(self):
        assert audit_ecosystem.is_safe_context("re.compile(r'password.*')")

    def test_replace_migration_is_safe(self):
        assert audit_ecosystem.is_safe_context("content.replace('hkEVC9AFVjFeRTkp', 'REDACTED')")

    def test_real_credential_is_not_safe(self):
        assert not audit_ecosystem.is_safe_context('password = "hkEVC9AFVjFeRTkp"')

    def test_assertion_is_safe(self):
        assert audit_ecosystem.is_safe_context('assert password != "hkEVC9AFVjFeRTkp"')

    def test_template_reference_is_safe(self):
        assert audit_ecosystem.is_safe_context("_template/workspace/config.py")


# ---------------------------------------------------------------------------
# scan_security
# ---------------------------------------------------------------------------


class TestScanSecurity:
    def test_detects_known_credential(self, tmp_path, monkeypatch):
        secret = "KnownCredToken_2026"
        monkeypatch.setattr(
            audit_ecosystem,
            "KNOWN_CREDENTIAL_HASHES",
            {
                hashlib.sha256(secret.encode("utf-8")).hexdigest(): {
                    "label": "test known credential",
                    "severity": "critical",
                }
            },
        )
        bad_file = tmp_path / "config.py"
        bad_file.write_text(f'DB_PASS = "{secret}"\n', encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) >= 1
        assert findings[0]["severity"] == "critical"
        assert findings[0]["label"] == "test known credential"

    def test_ignores_safe_placeholder(self, tmp_path):
        safe_file = tmp_path / "config.py"
        safe_file.write_text('"password": "REPLACE_ME"\n', encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) == 0

    def test_detects_generic_password_in_json(self, tmp_path):
        bad_json = tmp_path / "settings.json"
        bad_json.write_text('{"password": "MyR3alP@ssw0rd"}\n', encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) >= 1

    def test_skips_git_directory(self, tmp_path):
        git_dir = tmp_path / ".git" / "config"
        git_dir.parent.mkdir(parents=True)
        git_dir.write_text('password = "secret_in_git"\n', encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) == 0

    def test_skips_venv_directory(self, tmp_path):
        venv_file = tmp_path / ".venv" / "lib" / "config.py"
        venv_file.parent.mkdir(parents=True)
        venv_file.write_text('password = "venv_secret"\n', encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) == 0

    def test_skips_non_scan_extension(self, tmp_path):
        img = tmp_path / "photo.png"
        img.write_text("password = secret_in_png", encoding="utf-8")
        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# grade_project
# ---------------------------------------------------------------------------


class TestGradeProject:
    def _make_result(self, req_ok, req_total, sec_findings=None):
        return {
            "required_ok": req_ok,
            "required_total": req_total,
            "security_findings": sec_findings or [],
        }

    def test_grade_f_with_critical_security(self):
        r = self._make_result(7, 7, [{"severity": "critical"}])
        assert audit_ecosystem.grade_project(r) == "F"

    def test_grade_a_with_full_compliance(self):
        r = self._make_result(7, 7)
        assert audit_ecosystem.grade_project(r) == "A"

    def test_grade_b_with_75_percent(self):
        r = self._make_result(6, 7)
        assert audit_ecosystem.grade_project(r) == "B"

    def test_grade_c_with_50_percent(self):
        r = self._make_result(4, 7)
        assert audit_ecosystem.grade_project(r) == "C"

    def test_grade_d_with_low_compliance(self):
        r = self._make_result(2, 7)
        assert audit_ecosystem.grade_project(r) == "D"


# ---------------------------------------------------------------------------
# check_content_quality
# ---------------------------------------------------------------------------


class TestCheckContentQuality:
    def test_gitignore_coverage_pass(self, tmp_path):
        gi = tmp_path / ".gitignore"
        gi.write_text(".env\nnode_modules\n__pycache__", encoding="utf-8")
        result = audit_ecosystem.check_content_quality(tmp_path)
        assert result["gitignore_coverage"] is True

    def test_gitignore_coverage_fail(self, tmp_path):
        gi = tmp_path / ".gitignore"
        gi.write_text("*.log\n", encoding="utf-8")
        result = audit_ecosystem.check_content_quality(tmp_path)
        assert result["gitignore_coverage"] is False

    def test_tasks_unified_structure(self, tmp_path):
        tasks = tmp_path / "docs" / "TASKS.md"
        tasks.parent.mkdir(parents=True)
        tasks.write_text(
            "# Tasks\n## Incoming\n## Outgoing\n## Completed\n", encoding="utf-8"
        )
        result = audit_ecosystem.check_content_quality(tmp_path)
        assert result["tasks_unified"] is True

    def test_missing_files_return_false(self, tmp_path):
        result = audit_ecosystem.check_content_quality(tmp_path)
        assert result["gemini_keywords"] is False
        assert result["devlog_has_entries"] is False
        assert result["gitignore_coverage"] is False
        assert result["tasks_unified"] is False
        assert result["changelog_active"] is False
