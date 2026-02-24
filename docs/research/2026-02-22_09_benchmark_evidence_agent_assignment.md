---
depends_on:
  - .subagents/manifest.json
  - docs/research/2026-02-22_02_cli_agentic_stack.md
impacts:
  - .subagents/manifest.json
  - docs/library/agents.md
---

# R-09: Benchmark Evidence for Agent-Vendor Assignment

> **Date:** 2026-02-22 (updated with Gemini 3.1 Pro data, released Feb 19 2026)
> **Sources:** Independent third-party benchmarks (no vendor self-reporting unless noted)
> **Purpose:** Justify every vendor assignment in `.subagents/manifest.json` v3.2

---

## 1. User Subscription Context

The user holds the **highest personal tier** for each vendor CLI:

| Vendor | Plan | Cost/mo | Models Available | Key Exclusive Features |
|--------|------|---------|-----------------|----------------------|
| Anthropic | Claude Max 20x | $200 | Opus 4.6, Sonnet 4.6, Haiku 4.5 | 1M context (beta), 128K output, Agent Teams, Compaction API, ~900 msg/5h |
| Google | AI Ultra | $249.99* | Gemini 3.1 Pro, 3 Flash | Deep Think Mini (exclusive), 25K API credits, Jules 20x, 30TB storage, YouTube Premium |
| OpenAI | Pro | $200 | GPT-5.3-Codex, GPT-5.2, Spark | Spark model (exclusive, >1000 tok/s), 2x Codex rate limits, Deep Research enhanced |
| GitHub | Copilot Pro+ | $39 | Multi-vendor marketplace | 1500 premium requests/mo, agent mode, code reviews |
| **Total** | | **~$689** | | |

*Google AI Ultra: introductory $124.99/mo for first 3 months, then $249.99/mo.

---

## 2. Context Window & Output Comparison

| Model | Context Window | Max Output | 1M Beta | Long-Context Quality (MRCR v2) |
|-------|---------------|------------|---------|-------------------------------|
| **Claude Opus 4.6** | 200K (1M beta) | **128K** | Yes | 76% at 1M, 93% at 256K |
| **Claude Sonnet 4.6** | 200K (1M beta) | 64K | Yes | -- |
| **Gemini 3.1 Pro** | **1M** (native) | 64K | Native | 84.9% at 128K, 26.3% at 1M |
| **GPT-5.2** | 400K | 128K | No | -- |
| **GPT-5.3-Codex** | 400K | 128K | No | -- |
| **GPT-5.3-Codex-Spark** | 128K | ~128K | No | >1000 tok/s (Cerebras WSE-3) |
| Claude Haiku 4.5 | 200K | 64K | No | -- |
| Gemini 3 Flash | 1M | 64K | Native | -- |

**Key insight:** Claude Opus 4.6 has the largest output (128K) and best long-context reliability (93% at 256K, 76% at 1M). Gemini 3.1 Pro has native 1M but degrades more aggressively (26.3% at 1M). GPT family capped at 400K input.

---

## 3. Independent Benchmark Sources

| Source | Type | Reference |
|--------|------|-----------|
| LMSYS Chatbot Arena | Crowd-sourced ELO (163K+ coding votes) | arena.ai / lmarena.ai |
| SWE-bench Verified | Real GitHub issue resolution (500 tasks) | swebench.com / marc0.dev |
| SWE-Bench Pro (SEAL) | Harder variant, public + private codebases | scale.com/leaderboard |
| Aider Polyglot | Diff-based code editing (225 Exercism exercises) | aider.chat/leaderboards |
| LiveCodeBench Pro | Contamination-free competitive coding (ELO) | livecodebench.github.io |
| MMLU / MMMLU | Academic reasoning (multilingual variant) | -- |
| GPQA Diamond | PhD-level science QA (198 questions) | -- |
| Terminal-Bench 2.0 | Real terminal task completion (89 tasks) | tbench.ai |
| OSWorld | Desktop GUI automation (369 tasks) | os-world.github.io |
| ARC-AGI-2 | Abstract reasoning / novel patterns | -- |
| Humanity's Last Exam | 2,500 frontier-knowledge questions | scale.com/leaderboard |
| MCP Atlas | Tool use across 36 MCP servers (1000 tasks) | scale.com/leaderboard |
| BrowseComp | Agentic web browsing | -- |
| GDPVal-AA | Expert preference ELO for generation quality | -- |
| tau2-bench | Dual-control conversational agent evaluation | -- |

---

## 4. Benchmark Results by Category

### 4.1 Code Review & Editing

**Primary benchmarks:** Chatbot Arena Coding ELO, SWE-bench Verified, SWE-Bench Pro

| Model | Arena Coding ELO | SWE-bench Verified | SWE-Bench Pro (Public) |
|-------|-----------------|-------------------|----------------------|
| **Claude Opus 4.6** | **1561** | **80.8%** | ~46% |
| Claude Sonnet 4.6 | 1524 | 79.6% | -- |
| Claude Opus 4.5 | 1469 | 80.9% | 45.9% |
| GPT-5.2 (high) | 1471 | 80.0% | **55.6%** |
| GPT-5.3-Codex | -- | -- | 56.8% |
| Gemini 3.1 Pro | 1461 | 80.6% | 54.2% |
| Gemini 3 Pro | 1444 | 76.2% | 43.3% |

**Winner: Claude Opus 4.6** — Arena Coding ELO 1561 leads by +90 over GPT-5.2 and +100 over Gemini 3.1 Pro. SWE-bench Verified essentially tied top-3 (80.8/80.6/80.0). On harder SWE-Bench Pro, GPT-5.3-Codex leads (56.8%).

### 4.2 Research & Reasoning

**Primary benchmarks:** GPQA Diamond, MMMLU, HLE, ARC-AGI-2

| Model | GPQA Diamond | MMMLU | HLE (no tools) | HLE (with tools) | ARC-AGI-2 |
|-------|-------------|-------|----------------|-------------------|-----------|
| **Gemini 3.1 Pro** | **94.3%** | **92.6%** | **44.4%** | 51.4% | **77.1%** |
| Claude Opus 4.6 | 91.3% | 91.1% | 40.0% | **53.1%** | 68.8% |
| GPT-5.2 | 92.4% | 89.6% | 27.8% | 50.0% | 54.2% |
| Claude Opus 4.5 | 87.0% | 90.8% | 25.2% | -- | 37.6% |
| Gemini 3 Pro | 91.9% | ~90% | 37.5% | -- | 31.1% |

**Winner: Gemini 3.1 Pro** — Leads GPQA (94.3%), MMMLU (92.6%), HLE no tools (44.4%), ARC-AGI-2 (77.1%, 2x over Gemini 3 Pro). Claude leads HLE with tools (53.1%). Deep Think Mini mode (3-tier: low/medium/high) exclusive to AI Ultra.

### 4.3 Algorithmic Code Generation

**Primary benchmark:** LiveCodeBench Pro (ELO, contamination-free competitive programming)

| Model | LiveCodeBench Pro ELO |
|-------|-----------------------|
| **Gemini 3.1 Pro** | **2887** |
| GPT-5.2-Codex | 2439 |
| Gemini 3 Pro | ~2439 |
| GPT-5.2 | 2393 |
| Claude Opus 4.5 | ~2200 (pass rate 87%) |

**Winner: Gemini 3.1 Pro** — Massive 448 ELO lead over second place. Competitive/algorithmic coding is its strongest category.

### 4.4 Terminal & Deployment Automation

**Primary benchmarks:** Terminal-Bench 2.0, OSWorld

| Model | Terminal-Bench 2.0 | Terminal-Bench Hard | OSWorld |
|-------|--------------------|--------------------|---------
| GPT-5.3-Codex | **75.1%** | -- | 64.7% |
| **Claude Opus 4.6** | 74.7% | 48.5% | **72.7%** |
| Claude Sonnet 4.6 | -- | 53.0% | 72.5% |
| Gemini 3.1 Pro | 67.4-68.5% | **53.8%** | -- |
| GPT-5.2-Codex | 66.5% | -- | -- |
| Claude Opus 4.5 | 63.1% | -- | 66.3% |
| Gemini 3 Pro | 64.7% | -- | -- |

**Winner: Claude Opus 4.6** — Terminal-Bench essentially tied with GPT-5.3-Codex (74.7% vs 75.1%), but OSWorld lead is massive (72.7% vs 64.7%). Human baseline on OSWorld is ~72%, so Opus 4.6 matches human performance. Gemini 3.1 Pro leads Terminal-Bench Hard subset (53.8%).

### 4.5 Web Browsing & Search

| Model | BrowseComp |
|-------|-----------|
| **Gemini 3.1 Pro** | **85.9%** |
| Claude Opus 4.6 | 84.0% |
| Claude Opus 4.5 | 67.8% |

### 4.6 Tool Use & MCP

| Model | MCP Atlas | tau2-bench Retail | tau2-bench Telecom |
|-------|-----------|-------------------|-------------------|
| Claude Opus 4.5 | **62.3%** | -- | -- |
| GPT-5.2 | 60.6% | -- | -- |
| Gemini 3.1 Pro | 69.2% (vendor) | -- | -- |
| Gemini 3 Flash | 57.4% | -- | -- |
| Claude Opus 4.6 | 59.5% | **91.9%** | **99.3%** |

**Note:** MCP Atlas shows mixed results — Gemini 3.1 Pro vendor-reported 69.2%, but SEAL independent shows Claude Opus 4.5 at 62.3%. Claude Opus 4.6 dominates tau2-bench conversational agent tasks.

### 4.7 Expert Preference Quality

| Model | GDPVal-AA ELO |
|-------|--------------|
| **Claude Opus 4.6** | **1606** |
| GPT-5.2 | 1462 |
| Claude Opus 4.5 | 1416 |
| Gemini 3 Pro | 1195 |

**Winner: Claude Opus 4.6** — 144 ELO gap over GPT-5.2 in expert preference for generation quality.

### 4.8 Database & SQL Analysis

No dedicated SQL benchmark. Proxy evidence:
- **SWE-bench** includes DB migration tasks → Claude Opus 4.6 leads (80.8%)
- **GPQA Diamond** includes data science reasoning → Gemini 3.1 Pro leads (94.3%)
- **tau2-bench** tests stateful data operations → Claude Opus 4.6 leads (99.3% telecom)
- Claude Opus 4.6 has purpose-built security analysis (safe for DROP/DELETE)

**Winner: Claude** — Best for safety-critical DB work (tau2-bench + security tooling).

### 4.9 Security Analysis

| Model | Security Features | BigLaw Bench |
|-------|-------------------|-------------|
| **Claude Opus 4.6** | Claude Code Security (purpose-built vulnerability detection) | **90.2%** |
| GPT-5.2 | General code review | -- |
| Gemini 3.1 Pro | General analysis | -- |

**Winner: Claude Opus 4.6** — Only model with dedicated security tooling + leads legal reasoning.

---

## 5. Head-to-Head Summary Matrix

| Benchmark | Claude Opus 4.6 | Gemini 3.1 Pro | GPT-5.2 / 5.3-Codex | Leader |
|-----------|-----------------|----------------|---------------------|--------|
| Arena Coding ELO | **1561** | 1461 | 1471 | Claude |
| SWE-bench Verified | **80.8%** | 80.6% | 80.0% | Claude (tied) |
| SWE-Bench Pro | ~46% | 54.2% | **56.8%** | Codex |
| LiveCodeBench Pro ELO | ~2200 | **2887** | 2439 | Gemini |
| GPQA Diamond | 91.3% | **94.3%** | 92.4% | Gemini |
| MMMLU | 91.1% | **92.6%** | 89.6% | Gemini |
| HLE (no tools) | 40.0% | **44.4%** | 27.8% | Gemini |
| HLE (with tools) | **53.1%** | 51.4% | 50.0% | Claude |
| ARC-AGI-2 | 68.8% | **77.1%** | 54.2% | Gemini |
| Terminal-Bench 2.0 | 74.7% | 68.5% | **75.1%** | Codex (barely) |
| OSWorld | **72.7%** | -- | 64.7% | Claude |
| BrowseComp | 84.0% | **85.9%** | -- | Gemini |
| MCP Atlas | 59.5% | **69.2%*** | 60.6% | Gemini* |
| GDPVal-AA ELO | **1606** | 1317 | 1462 | Claude |
| tau2-bench Telecom | **99.3%** | -- | -- | Claude |
| BigLaw Bench | **90.2%** | -- | -- | Claude |
| Context Window | 1M (beta) | **1M (native)** | 400K | Gemini |
| Max Output | **128K** | 64K | 128K | Claude/GPT |

*MCP Atlas: Gemini score is vendor-reported; independent SEAL shows Claude Opus 4.5 at 62.3%.

### Score by domain (who leads):
- **Gemini 3.1 Pro leads:** GPQA, MMMLU, HLE, ARC-AGI-2, LiveCodeBench Pro, BrowseComp (6 benchmarks)
- **Claude Opus 4.6 leads:** Arena Coding, SWE-bench, OSWorld, GDPVal, tau2-bench, BigLaw, HLE with tools (7 benchmarks)
- **GPT-5.3-Codex leads:** SWE-Bench Pro, Terminal-Bench 2.0 (2 benchmarks)

---

## 6. Evidence-Based Agent Assignment (manifest v3.2)

### Final Assignment Table

| Agent | Role | Vendor | Primary Evidence | Confidence |
|-------|------|--------|-----------------|------------|
| **code-reviewer** | Code review, security, audit | **claude** | Arena Coding #1 (1561 ELO, +90 gap), SWE-bench #1 (80.8%), BigLaw 90.2%, security tooling | Very High |
| **researcher** | Deep research, APIs, docs | **gemini** | GPQA #1 (94.3%), MMMLU #1 (92.6%), HLE #1 (44.4%), ARC-AGI-2 #1 (77.1%), BrowseComp #1 (85.9%), Deep Think Mini | Very High |
| **code-analyst** | Architecture analysis | **gemini** | GPQA #1, ARC-AGI-2 #1, LiveCodeBench Pro #1 (2887 ELO), Deep Think for complex reasoning | Very High |
| **doc-writer** | Documentation maintenance | **claude** | GDPVal-AA #1 (1606 ELO, expert preference), 1M context + 128K output for full-doc work | High |
| **test-writer** | Test creation, coverage | **codex** | SWE-Bench Pro #1 (56.8%), Terminal-Bench #1 (75.1%), GPT-5.3-Codex-Spark for fast iteration | High |
| **db-analyst** | SQL, schema, migrations | **claude** | tau2-bench #1 (99.3%), SWE-bench #1, dedicated security for safe DB operations | High |
| **deployer** | Docker, CI/CD, infra | **claude** | OSWorld #1 (72.7%, human-level), Terminal-Bench ~tied #1 (74.7%), desktop automation dominance | High |

### Changes from v3.1 to v3.2

| Change | Detail |
|--------|--------|
| Benchmark data refresh | All scores updated with Gemini 3.1 Pro (Feb 19), independent Terminal-Bench, SEAL data |
| Terminal-Bench correction | Opus 4.6 = 74.7% (not 65.4% from earlier data), GPT-5.3-Codex = 75.1% |
| Gemini 3.1 Pro replaces Gemini 3 Pro | Massive improvements: GPQA +2.4%, ARC-AGI-2 2x, LiveCodeBench +448 ELO |
| 12 new benchmarks added | HLE, ARC-AGI-2, BrowseComp, MCP Atlas, GDPVal-AA, tau2-bench, BigLaw, etc. |
| Context window data added | Full comparison including long-context quality (MRCR v2) |
| **No vendor assignment changes** | v3.1 assignments confirmed correct with updated evidence |

### Vendor Distribution (v3.2, unchanged from v3.1)

| Vendor | Count | Agents |
|--------|-------|--------|
| Claude (Opus 4.6) | 4 | code-reviewer, doc-writer, db-analyst, deployer |
| Gemini (3.1 Pro) | 2 | researcher, code-analyst |
| Codex (GPT-5.3) | 1 | test-writer |

### Fallback Priority Per Agent

| Agent | Primary | Fallback 1 | Fallback 2 | Reasoning |
|-------|---------|------------|------------|-----------|
| code-reviewer | claude | codex | gemini | GPT-5.2 Arena Coding #2 (1471) |
| researcher | gemini | claude | codex | Claude HLE with tools #1 (53.1%) |
| code-analyst | gemini | claude | codex | Claude Arena Coding strong |
| doc-writer | claude | gemini | codex | Gemini strong language/reasoning |
| test-writer | codex | claude | gemini | Claude SWE-bench #1 |
| db-analyst | claude | gemini | codex | Gemini GPQA for data reasoning |
| deployer | claude | codex | gemini | GPT-5.3-Codex Terminal-Bench #1 |

---

## 7. Subscription Feature Utilization

| Feature | Used By | Justification |
|---------|---------|---------------|
| Claude 1M context (beta) | code-reviewer, doc-writer, db-analyst | Ingest entire codebases/docs; 93% MRCR at 256K |
| Claude 128K output | doc-writer, deployer | Generate complete documents/configs in one pass |
| Claude Agent Teams | deep-audit, full-review teams | Parallel multi-agent orchestration (Opus 4.6 exclusive) |
| Claude Compaction API | All Claude agents (long sessions) | Automatic context management for extended tasks |
| Claude Adaptive Thinking | All Claude agents | Dynamic effort allocation per-request complexity |
| Gemini Deep Think Mini | researcher, code-analyst | 3-tier reasoning (low/medium/high), exclusive to AI Ultra |
| Gemini 1M native context | researcher | Full documentation ingestion without beta flags |
| Gemini 25K API credits | MCP integrations (future) | Programmatic access for n8n/Dify workflows |
| Codex GPT-5.3-Codex-Spark | test-writer | >1000 tok/s real-time generation, exclusive to Pro |
| Codex 2x rate limits | test-writer | Double agent rate limits vs Plus tier |
| Codex Deep Research | researcher (fallback) | Alternative research with full citations |
| Copilot Pro+ marketplace | IDE integration | VS Code inline across all vendors, 1500 premium req/mo |

---

## 8. Confidence Assessment

| Assignment | Confidence | Evidence Strength |
|------------|------------|-------------------|
| code-reviewer → claude | **Very High** | +90 ELO gap in Arena Coding; leads SWE-bench; dedicated security tooling |
| researcher → gemini | **Very High** | Leads 6/15 benchmarks; GPQA 94.3%; Deep Think Mini exclusive |
| code-analyst → gemini | **Very High** | LiveCodeBench Pro 2887 ELO (massive lead); ARC-AGI-2 77.1% |
| deployer → claude | **High** | OSWorld 72.7% (human-level); Terminal-Bench 74.7% (~tied with Codex 75.1%) |
| doc-writer → claude | **High** | GDPVal 1606 ELO (expert quality); 128K output ideal for long docs |
| test-writer → codex | **High** | SWE-Bench Pro 56.8% (#1); Terminal-Bench 75.1% (#1); Spark for speed |
| db-analyst → claude | **High** | tau2-bench 99.3% (stateful ops); security awareness for DB safety |

---

## 9. Critical Caveats

1. **Aider Polyglot**: Latest models (Opus 4.6, Gemini 3.1, GPT-5.2) NOT yet tested on official Aider leaderboard. Latest entry is Claude Opus 4.5 (89.4%).
2. **Vendor-reported vs independent**: Gemini 3.1 Pro MCP Atlas (69.2%) and Terminal-Bench (68.5%) are vendor-reported. Independent Terminal-Bench shows 67.4%. SmartScope notes Google selectively publishes favorable benchmarks.
3. **Gemini 3.1 Pro is 3 days old** (Feb 19 2026). Independent evaluations are still ongoing. Scores may shift.
4. **MMLU-Pro saturation**: Top models within 3% of each other. Industry shifting to HLE and harder benchmarks.
5. **LiveCodeBench tests algorithmic competition coding**, not production software engineering. SWE-bench is better proxy for real work.

---

## 10. Re-Evaluation Schedule

- **Weekly**: Check Chatbot Arena ELO for Gemini 3.1 Pro stabilization
- **Monthly**: Full SEAL/Terminal-Bench/OSWorld refresh
- **On model release**: Any vendor releasing new model or point release
- **On subscription change**: If tier features or pricing change

> Last evaluated: 2026-02-22
> Next scheduled: 2026-03-01 (accelerated due to Gemini 3.1 Pro being < 1 week old)

---

## Sources

### Independent Benchmark Platforms
- LMSYS Chatbot Arena: arena.ai, lmarena.ai
- SWE-bench: swebench.com, marc0.dev/leaderboard
- SEAL (Scale AI): scale.com/leaderboard
- Aider: aider.chat/docs/leaderboards
- LiveCodeBench: livecodebench.github.io
- Terminal-Bench: tbench.ai
- OSWorld: os-world.github.io
- LiveBench: livebench.ai
- Artificial Analysis: artificialanalysis.ai

### Analysis & Reviews
- Vellum: vellum.ai/blog/claude-opus-4-6-benchmarks
- SmartScope: smartscope.blog/en/generative-ai/google-gemini/gemini-3-1-pro-benchmark-analysis-2026
- NxCode: nxcode.io/resources/news/gemini-3-1-pro-vs-claude-opus-4-6-vs-gpt-5-comparison-2026
- DataCamp: datacamp.com/blog/gemini-3-1

### Vendor Announcements (used only for feature/pricing data, NOT benchmark claims)
- Anthropic: anthropic.com/news/claude-opus-4-6
- Google: blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro
- OpenAI: openai.com/index/introducing-gpt-5-3-codex
