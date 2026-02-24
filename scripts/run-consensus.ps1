<#
.SYNOPSIS
    Run Consensus Panel (Mixture of Experts)
.DESCRIPTION
    Executes a turn-based discussion workflow using Gemini, Claude, and Codex to arrive at a highly refined, peer-reviewed technical solution.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,

    [string]$OutputDir = "docs\temp"
)

$ErrorActionPreference = "Stop"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$OutputFile = "consensus-$Timestamp.md"

$WorkspaceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$OutPath = Join-Path $WorkspaceRoot $OutputDir
if (!(Test-Path $OutPath)) {
    New-Item -ItemType Directory -Path $OutPath -Force | Out-Null
}
$FullOutPath = Join-Path $OutPath $OutputFile

# Dispatch scripts usually assume being run from the repo root
Set-Location $WorkspaceRoot
$DispatchScript = Join-Path $WorkspaceRoot ".subagents\dispatch.ps1"

Write-Host "🧠 Initiating Mixture of Experts (MoE) Consensus Panel..." -ForegroundColor Cyan
Write-Host "Topic: $Topic" -ForegroundColor White
Write-Host "Log: $FullOutPath`n" -ForegroundColor DarkGray

# Initialize file
"# Consensus Panel: $Topic`n`n" | Set-Content -Path $FullOutPath -Encoding UTF8

# Initial Context
Write-Host "Gathering Initial Requirement..." -ForegroundColor Magenta
$ContextPrompt = "You are the Requirements Analyst. Elaborate the following request into a detailed, structured technical requirement document so the experts can evaluate it. Request: $Topic"
$InitialContext = & $DispatchScript "doc-writer" $ContextPrompt "gemini"
if (-not $InitialContext) { $InitialContext = "(Error or no response from Gemini/Analyst)" }

"## 1. Elaborated Requirement`n`n$InitialContext`n`n" | Add-Content -Path $FullOutPath -Encoding UTF8

# Turn 1: Gemini (The Architect)
Write-Host "[1/3] Gemini is designing the architecture..." -ForegroundColor Yellow
$GeminiPrompt = "You are the Lead Architect. Propose a high-level architectural design and strategic approach for the following requirement: $InitialContext"
$GeminiOutput = & $DispatchScript "doc-writer" $GeminiPrompt "gemini"
if (-not $GeminiOutput) { $GeminiOutput = "(Error or no response from Gemini)" }

"## 2. Architecture Proposal (Gemini)`n`n$GeminiOutput`n`n" | Add-Content -Path $FullOutPath -Encoding UTF8

# Turn 2: Claude (The Critic)
Write-Host "[2/3] Claude Opus is critiquing the proposal..." -ForegroundColor Yellow
$ClaudePrompt = "You are the Security & System Critic. Read the requirement and Gemini's architectural proposal. Critique the proposal. Find flaws, vulnerabilities, scalability issues, edge cases, and suggest improvements.`n`nREQUIREMENT:`n$InitialContext`n`nPROPOSAL:`n$GeminiOutput"
$ClaudeOutput = & $DispatchScript "code-reviewer" $ClaudePrompt "claude"
if (-not $ClaudeOutput) { $ClaudeOutput = "(Error or no response from Claude)" }

"## 3. Vulnerability Analysis & Critique (Claude)`n`n$ClaudeOutput`n`n" | Add-Content -Path $FullOutPath -Encoding UTF8

# Turn 3: Codex (The Implementer)
Write-Host "[3/3] Codex is implementing and auditing the code/tech..." -ForegroundColor DarkGreen
$CodexPrompt = "You are the Technical Implementer & Code Auditor. Read the requirement, the architecture proposal, and the critique. Provide the technical validation, code structure, directory trees, or exact library configurations needed to execute the architecture perfectly while avoiding the flaws mentioned in the critique.`n`nREQUIREMENT:`n$InitialContext`n`nPROPOSAL:`n$GeminiOutput`n`nCRITIQUE:`n$ClaudeOutput"
$CodexOutput = & $DispatchScript "code-analyst" $CodexPrompt "codex"
if (-not $CodexOutput) { $CodexOutput = "(Error or no response from Codex)" }

"## 4. Technical Validation & Implementation (Codex)`n`n$CodexOutput`n`n" | Add-Content -Path $FullOutPath -Encoding UTF8

# Turn 4: Consolidation (The Judge)
Write-Host "[Consolidation] Gemini is writing the final consensus document..." -ForegroundColor Cyan
$FinalPrompt = "You are the Master Orchestrator. Review the entire expert panel discussion. Synthesize a final, unified, and highly polished Implementation Plan (Markdown format). Incorporate the best parts of the proposal, address all critiques, and use the technical solutions provided by Codex. Output ONLY the final document.`n`nDISCUSSION:`nInitial Req: $InitialContext`n`nArchitecture: $GeminiOutput`n`nCritique: $ClaudeOutput`n`nImplementation: $CodexOutput"
$FinalOutput = & $DispatchScript "doc-writer" $FinalPrompt "gemini"

"## 5. Final Consolidated Architecture`n`n$FinalOutput`n" | Add-Content -Path $FullOutPath -Encoding UTF8

Write-Host "`n✅ Consensus reached! Read the full discussion here:" -ForegroundColor Green
Write-Host $FullOutPath -ForegroundColor Yellow
