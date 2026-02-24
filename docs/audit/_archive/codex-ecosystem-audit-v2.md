`$FinalPrompt` is defined in two places in this repo.

`script`s/run-consensus.ps1:

```powershell
$FinalPrompt = "You are the Master Orchestrator. Review the entire expert panel discussion. Synthesize a final, unified, and highly polished Implementation Plan (Markdown format). Incorporate the best parts of the proposal, address all critiques, and use the technical solutions provided by Codex. Output ONLY the final document.`n`nDISCUSSION:`nInitial Req: $InitialContext`n`nArchitecture: $GeminiOutput`n`nCritique: $ClaudeOutput`n`nImplementation: $CodexOutput"
```

`scripts/temp/run_consensus_last_step.ps1` has a multiline version:

```powershell
You are the Master Orchestrator. Review the expert panel discussion regarding the recent AG Ecosystem Audit.
The user's core requirement is: "We need a master architecture proposal to fix the entire ecosystem. Incorporate my idea: AG_Orquesta_Desk MUST become the pure Master Orchestrator, completely detached from the AG_Plantilla codebase setup."

Synthesize a final, unified, and highly polished Implementation Plan (Markdown format). Incorporate the best parts of the audits, and give a highly critical proposal.
Output ONLY the final document.
...
```
