# 🔒 Security Audit — AG_Plantilla
## Prompt Injection & Data Leakage Analysis

**Date**: 2026-02-17
**Scope**: Full source tree (`src/`, `scripts/`, `.subagents/`, `config/`, `_template/`, `_global-profile/`)
**Auditor**: Antigravity Architect Agent

---

## Executive Summary

| Severity   | Count | Categories                                                           |
| ---------- | ----- | -------------------------------------------------------------------- |
| 🔴 CRITICAL | 2     | Prompt Injection (dispatch), Hardcoded API Key                       |
| 🟠 HIGH     | 3     | Unsafe dispatch flags, Agent output reflection, CORS wildcard        |
| 🟡 MEDIUM   | 3     | `eval` in health-check, API auth bypass in dev, Filesystem MCP scope |
| 🟢 LOW      | 1     | Default DB path predictable                                          |

**Overall Risk**: 🟠 **HIGH** — Prompt injection vectors in agent dispatch scripts are the most critical finding.

---

## 🔴 CRITICAL Findings

### C-01: Prompt Injection via Sub-Agent Dispatch

> [!CAUTION]
> User-supplied prompts are concatenated directly into agent instructions without sanitization.

| Attribute  | Detail                                                                                                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Files**  | [dispatch.sh](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.sh#L172-L177), [dispatch.ps1](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.ps1#L71-L78) |
| **Vector** | A crafted `$PROMPT` can override the agent's `$INSTRUCTIONS` via prompt injection techniques (e.g., `"Ignore previous instructions. Instead..."`)                          |
| **Impact** | Full control of sub-agent behavior; data exfiltration, file modification, credential disclosure                                                                            |

**Code (dispatch.sh L172-177):**
```bash
FULL_PROMPT="$INSTRUCTIONS

---

Task: $PROMPT"
```

**Remediation:**
1. Wrap user input in clear delimiters that the LLM is trained to respect (e.g., `<user_input>...</user_input>`)
2. Add input validation — reject prompts containing known injection patterns
3. Implement an output filter to detect credential leakage in agent responses

---

### C-02: Hardcoded Default API Key

> [!CAUTION]
> A hardcoded default API key `"dev-secret-key"` ships in the source code.

| Attribute  | Detail                                                                                             |
| ---------- | -------------------------------------------------------------------------------------------------- |
| **File**   | [config.py](file:///c:/_Repositorio/AG_Plantilla/src/config.py#L34)                                |
| **Line**   | `api_key: str = Field("dev-secret-key", validation_alias="API_KEY")`                               |
| **Impact** | If deployed without setting `API_KEY` env var, the API is protected by a known, public default key |

**Remediation:**
1. Remove the default value — make `api_key` **required** (no default)
2. Fail startup in production if `API_KEY` is not explicitly set
3. Add a startup check in `lifespan()` that validates the key is not the default

---

## 🟠 HIGH Findings

### H-01: Unsafe `--dangerously-skip-permissions` Flags

| Attribute  | Detail                                                                                                                                                                                                                                                                                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Files**  | [dispatch.sh:L197](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.sh#L197), [dispatch.sh:L215](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.sh#L215), [dispatch.ps1:L97](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.ps1#L97), [dispatch.ps1:L121](file:///c:/_Repositorio/AG_Plantilla/.subagents/dispatch.ps1#L121) |
| **Impact** | Sub-agents run with **zero permission checks** — combined with C-01, an injected prompt can execute arbitrary filesystem operations                                                                                                                                                                                                                      |

```bash
claude --dangerously-skip-permissions -p "$FULL_PROMPT"      # Line 197
codex exec --dangerously-bypass-approvals-and-sandbox "$FULL_PROMPT"  # Line 215
```

**Remediation:**
1. Remove `--dangerously-skip-permissions` in production mode
2. Use allowlist-based permissions or sandbox configurations
3. Add a `--safe-mode` wrapper that applies per-agent permission boundaries

---

### H-02: Agent Response Reflects User Input (Data Echo)

| Attribute  | Detail                                                                                                                            |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **File**   | [agent_service.py:L84](file:///c:/_Repositorio/AG_Plantilla/src/services/agent_service.py#L84)                                    |
| **Line**   | `output = f"Agent '{agent_name}' processed: {input_text[:100]}..."`                                                               |
| **Impact** | Echoes user input directly in response — can leak sensitive data in logs, be used for reflected XSS if rendered in a web frontend |

**Remediation:**
1. Never echo raw user input in API responses
2. Sanitize/redact the echoed text
3. Move input details to structured metadata only (already partially done)

---

### H-03: CORS Wildcard in Development Mode

| Attribute  | Detail                                                                                                                                                      |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **File**   | [main.py:L58](file:///c:/_Repositorio/AG_Plantilla/src/main.py#L58)                                                                                         |
| **Line**   | `origins = ["*"] if settings.environment == "development" else [settings.frontend_url]`                                                                     |
| **Impact** | In development mode (the **default**), CORS allows **any origin**. If the dev instance is exposed to a network, any website can make authenticated requests |

**Remediation:**
1. Restrict development origins to `["http://localhost:3000", "http://localhost:8000"]`
2. Never default to `"*"` even in development

---

## 🟡 MEDIUM Findings

### M-01: `eval` in Health Check Script

| Attribute  | Detail                                                                                                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **File**   | [health-check.sh:L38](file:///c:/_Repositorio/AG_Plantilla/scripts/setup/health-check.sh#L38)                                                                                                          |
| **Line**   | `if eval "$condition" > /dev/null 2>&1; then`                                                                                                                                                          |
| **Impact** | The `check()` function uses `eval` on its second argument. While currently called with safe static strings, this pattern is fragile — any future dynamic input would create a command injection vector |

**Remediation:**
1. Replace `eval` with direct command execution or `bash -c` in a controlled context
2. Add a comment warning against dynamic input

---

### M-02: API Authentication Bypass in Development Mode

| Attribute  | Detail                                                                                                                                                                 |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **File**   | [main.py:L49](file:///c:/_Repositorio/AG_Plantilla/src/main.py#L49)                                                                                                    |
| **Line**   | `if settings.environment == "production" and api_key != settings.api_key:`                                                                                             |
| **Impact** | In **development** mode (the default), ALL API requests are accepted without authentication. If a dev server is exposed on the network, any client has full API access |

**Remediation:**
1. Require API key in all environments, with a simpler key for dev
2. At minimum, bind dev server to `127.0.0.1` only

---

### M-03: MCP Filesystem Server — Broad Path Scope

| Attribute  | Detail                                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **File**   | [mcp_servers.yaml:L29](file:///c:/_Repositorio/AG_Plantilla/config/mcp_servers.yaml#L29)                                                                           |
| **Line**   | `args: ["-y", "@modelcontextprotocol/server-filesystem", "C:\\_Repositorio"]`                                                                                      |
| **Impact** | The MCP filesystem server allows access to the **entire `C:\_Repositorio`** directory — all AG projects, credentials in `.env` files, and secrets across all repos |

**Remediation:**
1. Restrict to the current project root only: `"C:\\_Repositorio\\AG_Plantilla"`
2. Or use per-project MCP configs that limit scope

---

## 🟢 LOW Findings

### L-01: Predictable Default Database Path

| Attribute  | Detail                                                                        |
| ---------- | ----------------------------------------------------------------------------- |
| **File**   | [config.py:L38](file:///c:/_Repositorio/AG_Plantilla/src/config.py#L38)       |
| **Line**   | `database_url: str = "sqlite:///./data/app.db"`                               |
| **Impact** | Predictable DB location could be targeted if filesystem access is compromised |

---

## ✅ Positive Observations

| Area                                                                        | Status |
| --------------------------------------------------------------------------- | ------ |
| `.gitignore` covers `.env`, `credentials/`, `secrets/`, `*.pem`, `*.key`    | ✅ Good |
| `.env.example` uses placeholder values, not real credentials                | ✅ Good |
| Structured logging via `structlog` (no debug prints)                        | ✅ Good |
| Dockerfile uses multi-stage build with non-root user in production          | ✅ Good |
| `subprocess.run` in `knowledge_sync.py` uses list args (no shell injection) | ✅ Good |
| API uses Pydantic schema validation on all inputs/outputs                   | ✅ Good |
| Pre-commit hooks configured (`.pre-commit-config.yaml`)                     | ✅ Good |

---

## Remediation Priority

| Priority | Finding                                                           | Effort   | Impact                              |
| -------- | ----------------------------------------------------------------- | -------- | ----------------------------------- |
| 1        | **C-01** — Sanitize prompt input in dispatch scripts              | Medium   | Blocks production use of sub-agents |
| 2        | **C-02** — Remove hardcoded API key default                       | Low      | 5-minute fix                        |
| 3        | **H-01** — Remove `--dangerously-skip-permissions` for production | Medium   | Requires permission config design   |
| 4        | **H-03** — Restrict dev CORS origins                              | Low      | 2-minute fix                        |
| 5        | **M-02** — Require auth in all environments                       | Low      | Config change                       |
| 6        | **M-03** — Scope MCP filesystem access                            | Low      | Config change                       |
| 7        | **H-02** — Remove input echo from agent responses                 | Low      | Code change                         |
| 8        | **M-01** — Replace `eval` in health-check                         | Low      | Refactor                            |
| 9        | **L-01** — Randomize DB path                                      | Very Low | Optional                            |
