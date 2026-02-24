"""
Meta-tests for scripts/audit_ecosystem.py
=========================================

These tests validate that core audit controls are sensitive to intentional
mutations. They reduce "false green" risk by proving checks fail when control
logic is removed or weakened.
"""

import hashlib
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_ecosystem


def _create_required_files(project_dir: Path) -> None:
    """Create all required files/dirs with minimal non-secret content."""
    for rel_path in audit_ecosystem.REQUIRED_FILES:
        target = project_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("ok\n", encoding="utf-8")
    for rel_dir in audit_ecosystem.REQUIRED_DIRS:
        (project_dir / rel_dir).mkdir(parents=True, exist_ok=True)


class TestAuditMetaSecurityControls:
    def test_known_hash_registry_control_is_effective(self, tmp_path, monkeypatch):
        secret = "MetaKnown_Secret_2026"
        monkeypatch.setattr(
            audit_ecosystem,
            "KNOWN_CREDENTIAL_HASHES",
            {
                hashlib.sha256(secret.encode("utf-8")).hexdigest(): {
                    "label": "meta-known",
                    "severity": "critical",
                }
            },
        )
        monkeypatch.setattr(audit_ecosystem, "GENERIC_PATTERNS", [])

        file_path = tmp_path / "settings.py"
        file_path.write_text(f'API_TOKEN = "{secret}"\n', encoding="utf-8")

        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) == 1
        assert findings[0]["type"] == "known"

        # Mutation: remove registry control, detection should disappear.
        monkeypatch.setattr(audit_ecosystem, "KNOWN_CREDENTIAL_HASHES", {})
        findings_without_registry = audit_ecosystem.scan_security(tmp_path)
        assert findings_without_registry == []

    def test_generic_password_control_is_effective(self, tmp_path, monkeypatch):
        file_path = tmp_path / "config.json"
        file_path.write_text('{"password":"UltraSecret_4455"}\n', encoding="utf-8")

        findings = audit_ecosystem.scan_security(tmp_path)
        assert any(f["type"] == "generic" for f in findings)

        # Mutation: remove generic patterns and known registry to isolate control.
        monkeypatch.setattr(audit_ecosystem, "GENERIC_PATTERNS", [])
        monkeypatch.setattr(audit_ecosystem, "KNOWN_CREDENTIAL_HASHES", {})
        findings_without_generic = audit_ecosystem.scan_security(tmp_path)
        assert findings_without_generic == []

    def test_safe_context_guard_control_is_effective(self, tmp_path, monkeypatch):
        secret = "MetaSafeContext_7788"
        monkeypatch.setattr(
            audit_ecosystem,
            "KNOWN_CREDENTIAL_HASHES",
            {
                hashlib.sha256(secret.encode("utf-8")).hexdigest(): {
                    "label": "meta-safe-context",
                    "severity": "high",
                }
            },
        )
        file_path = tmp_path / "validator.py"
        file_path.write_text(f'forbidden = {{"{secret}"}}\n', encoding="utf-8")

        findings = audit_ecosystem.scan_security(tmp_path)
        assert findings == []

        # Mutation: disable safe-context patterns, same line should now trigger.
        monkeypatch.setattr(audit_ecosystem, "SAFE_LINE_PATTERNS", [])
        findings_without_guard = audit_ecosystem.scan_security(tmp_path)
        assert len(findings_without_guard) == 1
        assert findings_without_guard[0]["type"] == "known"

    def test_dotenv_files_are_scanned(self, tmp_path):
        env_file = tmp_path / ".env.local"
        env_file.write_text('password = "MetaEnvSecret_1122"\n', encoding="utf-8")

        findings = audit_ecosystem.scan_security(tmp_path)
        assert len(findings) >= 1
        assert any(f["type"] == "generic" for f in findings)


class TestAuditMetaStructuralControls:
    def test_check_project_required_control_is_effective(self, tmp_path):
        project = tmp_path / "AG_Meta"
        project.mkdir()

        empty_result = audit_ecosystem.check_project(project)
        assert empty_result["required_ok"] < empty_result["required_total"]

        _create_required_files(project)
        full_result = audit_ecosystem.check_project(project)
        assert full_result["required_ok"] == full_result["required_total"]

    def test_grade_regresses_to_f_when_high_severity_present(self, tmp_path, monkeypatch):
        project = tmp_path / "AG_MetaGrade"
        project.mkdir()
        _create_required_files(project)

        clean_result = audit_ecosystem.check_project(project)
        assert audit_ecosystem.grade_project(clean_result) == "A"

        secret = "MetaGradeSecret_9911"
        monkeypatch.setattr(
            audit_ecosystem,
            "KNOWN_CREDENTIAL_HASHES",
            {
                hashlib.sha256(secret.encode("utf-8")).hexdigest(): {
                    "label": "grade-regression-secret",
                    "severity": "critical",
                }
            },
        )
        (project / "config.py").write_text(f'PASSWORD = "{secret}"\n', encoding="utf-8")

        compromised_result = audit_ecosystem.check_project(project)
        assert audit_ecosystem.grade_project(compromised_result) == "F"


class TestAuditMetaAutofixControls:
    def test_autofix_uses_template_and_replaces_project_name(self, tmp_path, monkeypatch):
        project = tmp_path / "AG_MetaFix"
        project.mkdir()
        template_dir = tmp_path / "template-workspace"

        for file_path, template_rel in audit_ecosystem.TEMPLATE_MAP.items():
            template_src = template_dir / template_rel
            template_src.parent.mkdir(parents=True, exist_ok=True)
            template_src.write_text(
                f"TEMPLATE::{template_rel}::{{{{PROJECT_NAME}}}}\n",
                encoding="utf-8",
            )

        monkeypatch.setattr(audit_ecosystem, "TEMPLATE_DIR", template_dir)

        fixed = audit_ecosystem.fix_missing_files(project)

        assert "README.md" in fixed
        readme = (project / "README.md").read_text(encoding="utf-8")
        assert "AG_MetaFix" in readme
        assert "TEMPLATE::README.md::" in readme
