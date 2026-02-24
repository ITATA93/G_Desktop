# PROMPT DE AUDITORÃA: ValidaciÃ³n del Sistema AgÃ©ntico Multi-Vendor

> **INSTRUCCIÃ“N**: Ejecuta una auditorÃ­a completa del sistema agÃ©ntico configurado en este
> workspace. Verifica CADA punto de las 8 categorÃ­as siguientes. Para cada verificaciÃ³n,
> reporta âœ… (OK), âš ï¸ (parcial/advertencia), o âŒ (falla). Al final genera un reporte
> consolidado con puntuaciÃ³n y acciones correctivas para cada falla encontrada.
> NO corrijas nada automÃ¡ticamente â€” solo diagnostica y reporta.

---

## CATEGORÃA 1: ESTRUCTURA DE ARCHIVOS (Esqueleto del proyecto)

Verifica que TODOS estos archivos y directorios existan. Para cada uno, confirma existencia
y que NO estÃ© vacÃ­o (tamaÃ±o > 0 bytes):

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ“ CATEGORÃA 1: ESTRUCTURA DE ARCHIVOS"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

check_file() {
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        SIZE=$(wc -c < "$1")
        if [ "$SIZE" -gt 10 ]; then
            echo "  âœ… $1 ($SIZE bytes)"
            SCORE=$((SCORE + 1))
        else
            echo "  âš ï¸ $1 (existe pero VACÃO o mÃ­nimo: $SIZE bytes)"
        fi
    else
        echo "  âŒ $1 NO EXISTE"
    fi
}

check_dir() {
    TOTAL=$((TOTAL + 1))
    if [ -d "$1" ]; then
        COUNT=$(ls -1 "$1" 2>/dev/null | wc -l)
        echo "  âœ… $1/ ($COUNT items)"
        SCORE=$((SCORE + 1))
    else
        echo "  âŒ $1/ NO EXISTE"
    fi
}

echo ""
echo "--- RaÃ­z del proyecto ---"
check_file "GEMINI.md"
check_file "CLAUDE.md"
check_file "CHANGELOG.md"
check_file ".gitignore"

echo ""
echo "--- Gemini CLI ---"
check_file ".gemini/settings.json"
check_dir  ".gemini/agents"
check_dir  ".gemini/skills"
check_dir  ".gemini/scripts"
check_dir  ".gemini/rules"
check_dir  ".gemini/brain"

check_file ".gemini/agents/doc-writer.toml"
check_file ".gemini/agents/code-reviewer.toml"
check_file ".gemini/agents/test-writer.toml"
check_file ".gemini/agents/code-analyst.toml"
check_file ".gemini/agents/db-analyst.toml"
check_file ".gemini/agents/deployer.toml"

echo ""
echo "--- Codex CLI ---"
check_file ".codex/config.yaml"
check_dir  ".codex/agents"
check_dir  ".codex/skills"

check_file ".codex/agents/doc-writer.md"
check_file ".codex/agents/code-reviewer.md"
check_file ".codex/agents/test-writer.md"
check_file ".codex/agents/code-analyst.md"
check_file ".codex/agents/db-analyst.md"
check_file ".codex/agents/deployer.md"
check_file ".codex/agents/researcher.md"

echo ""
echo "--- Claude Code ---"
check_dir  ".claude/commands"
check_file ".claude/commands/project-status.md"
check_file ".claude/commands/project-review.md"
check_file ".claude/commands/project-document.md"

echo ""
echo "--- Sub-agentes Multi-vendor ---"
check_file ".subagents/manifest.json"
check_file ".subagents/dispatch.sh"
check_file ".gemini/rules/delegation-protocol.md"

echo ""
echo "--- Skills y Knowledge ---"
check_file ".gemini/skills/project-memory.md"
check_file ".gemini/skills/deep-research.md"

echo ""
echo "--- Biblioteca Central (si existe global-profile) ---"
if [ -d "_global-profile" ]; then
    check_dir  "_global-profile/.antigravity/library"
    check_file "_global-profile/.antigravity/library/catalog.json"
    check_dir  "_global-profile/.antigravity/library/agents"
    check_dir  "_global-profile/.antigravity/library/skills"
    check_dir  "_global-profile/.antigravity/library/scripts"
fi

echo ""
echo "--- DocumentaciÃ³n ---"
check_file "docs/README.md"
check_file "docs/TASKS.md"
check_file "docs/DEVLOG.md"
check_dir  "docs/research"

echo ""
echo "--- Directorios de cÃ³digo ---"
check_dir "src"
check_dir "tests"

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL archivos/directorios verificados"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 2: INTEGRIDAD DE CONTENIDO (Â¿Los archivos tienen lo correcto?)

Para cada archivo crÃ­tico, verifica que contenga las secciones o claves esperadas:

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ“ CATEGORÃA 2: INTEGRIDAD DE CONTENIDO"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

check_content() {
    # $1 = archivo, $2 = texto a buscar, $3 = descripciÃ³n
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        if grep -q "$2" "$1" 2>/dev/null; then
            echo "  âœ… $1 contiene: $3"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $1 NO contiene: $3"
        fi
    else
        echo "  âŒ $1 no existe (no se puede verificar: $3)"
    fi
}

echo ""
echo "--- GEMINI.md (instrucciones maestras) ---"
check_content "GEMINI.md" "doc-writer" "sub-agente doc-writer documentado"
check_content "GEMINI.md" "code-reviewer" "sub-agente code-reviewer documentado"
check_content "GEMINI.md" "test-writer" "sub-agente test-writer documentado"
check_content "GEMINI.md" "DEVLOG" "protocolo de documentaciÃ³n"

echo ""
echo "--- CLAUDE.md ---"
check_content "CLAUDE.md" "sub-agente\|subagent" "rol como sub-agente definido"

echo ""
echo "--- .gemini/settings.json ---"
check_content ".gemini/settings.json" "subagents\|agents" "sub-agentes habilitados"

echo ""
echo "--- .codex/config.yaml ---"
check_content ".codex/config.yaml" "effort\|model" "configuraciÃ³n de effort levels"

echo ""
echo "--- Sub-agentes Gemini TOML (estructura vÃ¡lida) ---"
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        check_content "$AGENT_FILE" "name" "$AGENT_NAME tiene campo name"
        check_content "$AGENT_FILE" "description" "$AGENT_NAME tiene description"
        check_content "$AGENT_FILE" "system_prompt" "$AGENT_NAME tiene system_prompt"
    fi
done

echo ""
echo "--- Sub-agentes Codex MD (estructura vÃ¡lida) ---"
for AGENT_FILE in .codex/agents/*.md; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .md)
        check_content "$AGENT_FILE" "Role\|Purpose\|##" "$AGENT_NAME tiene estructura markdown"
    fi
done

echo ""
echo "--- Manifest de sub-agentes (multi-vendor) ---"
check_content ".subagents/manifest.json" "doc-writer" "doc-writer registrado"
check_content ".subagents/manifest.json" "code-reviewer" "code-reviewer registrado"
check_content ".subagents/manifest.json" "test-writer" "test-writer registrado"
check_content ".subagents/manifest.json" "researcher" "researcher registrado"
check_content ".subagents/manifest.json" "vendor" "vendor definido"
check_content ".subagents/manifest.json" "supported_vendors" "multi-vendor configurado"
check_content ".subagents/manifest.json" "codex" "Codex como vendor"
check_content ".subagents/manifest.json" "gemini" "Gemini como vendor"
check_content ".subagents/manifest.json" "claude" "Claude como vendor"

echo ""
echo "--- DocumentaciÃ³n (no tiene placeholders sin reemplazar) ---"
for DOC_FILE in docs/*.md CHANGELOG.md; do
    if [ -f "$DOC_FILE" ]; then
        TOTAL=$((TOTAL + 1))
        if grep -q "FECHA_HOY\|TODO_REPLACE\|PLACEHOLDER" "$DOC_FILE" 2>/dev/null; then
            echo "  âŒ $DOC_FILE tiene placeholders sin reemplazar"
        else
            echo "  âœ… $DOC_FILE sin placeholders pendientes"
            SCORE=$((SCORE + 1))
        fi
    fi
done

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL verificaciones de contenido"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 3: HERRAMIENTAS DEL ENTORNO (Â¿EstÃ¡n instaladas y accesibles?)

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ”§ CATEGORÃA 3: HERRAMIENTAS DEL ENTORNO"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

check_tool() {
    # $1 = comando, $2 = nombre descriptivo, $3 = criticidad (CRITICAL/OPTIONAL)
    TOTAL=$((TOTAL + 1))
    if command -v "$1" &>/dev/null; then
        VERSION=$($1 --version 2>&1 | head -1)
        echo "  âœ… $2: $VERSION"
        SCORE=$((SCORE + 1))
    else
        if [ "$3" = "CRITICAL" ]; then
            echo "  âŒ $2: NO INSTALADO (CRÃTICO)"
        else
            echo "  âš ï¸ $2: no instalado (opcional)"
            SCORE=$((SCORE + 1))  # No penalizar opcionales
        fi
    fi
}

echo ""
echo "--- Herramientas crÃ­ticas ---"
check_tool "node" "Node.js" "CRITICAL"
check_tool "npm" "npm" "CRITICAL"
check_tool "git" "Git" "CRITICAL"

echo ""
echo "--- Agentes AI (Multi-vendor) ---"
check_tool "gemini" "Gemini CLI" "CRITICAL"
check_tool "claude" "Claude Code CLI" "CRITICAL"
check_tool "codex" "Codex CLI" "CRITICAL"

echo ""
echo "--- Herramientas auxiliares ---"
check_tool "jq" "jq (JSON processor)" "OPTIONAL"
check_tool "curl" "curl" "CRITICAL"
check_tool "docker" "Docker" "OPTIONAL"

echo ""
echo "--- Versiones mÃ­nimas recomendadas ---"
TOTAL=$((TOTAL + 1))
NODE_MAJOR=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
if [ -n "$NODE_MAJOR" ] && [ "$NODE_MAJOR" -ge 18 ]; then
    echo "  âœ… Node.js >= 18 (tienes v$NODE_MAJOR)"
    SCORE=$((SCORE + 1))
elif [ -n "$NODE_MAJOR" ]; then
    echo "  âš ï¸ Node.js $NODE_MAJOR (recomendado >= 18)"
else
    echo "  âŒ No se pudo verificar versiÃ³n de Node.js"
fi

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL herramientas verificadas"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 4: PERMISOS Y EJECUTABILIDAD

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ” CATEGORÃA 4: PERMISOS Y EJECUTABILIDAD"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

check_executable() {
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        if [ -x "$1" ]; then
            echo "  âœ… $1 es ejecutable"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $1 existe pero NO es ejecutable (falta chmod +x)"
        fi
    else
        echo "  âŒ $1 no existe"
    fi
}

echo ""
echo "--- Scripts deben ser ejecutables ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        check_executable "$SCRIPT"
    fi
done

echo ""
echo "--- Verificar shebang correcto ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        TOTAL=$((TOTAL + 1))
        FIRST_LINE=$(head -1 "$SCRIPT")
        if echo "$FIRST_LINE" | grep -q "^#!/bin/bash\|^#!/usr/bin/env bash"; then
            echo "  âœ… $SCRIPT tiene shebang correcto"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $SCRIPT shebang incorrecto: $FIRST_LINE"
        fi
    fi
done

echo ""
echo "--- Biblioteca central scripts (si existe) ---"
if [ -d "_global-profile/.antigravity/library/scripts" ]; then
    for SCRIPT in _global-profile/.antigravity/library/scripts/*.sh; do
        if [ -f "$SCRIPT" ]; then
            check_executable "$SCRIPT"
        fi
    done
fi

echo ""
echo "--- Directorios escribibles (para logs y outputs) ---"
for DIR in .gemini/agents/logs docs/research .gemini/brain; do
    TOTAL=$((TOTAL + 1))
    mkdir -p "$DIR" 2>/dev/null
    if [ -w "$DIR" ]; then
        echo "  âœ… $DIR es escribible"
        SCORE=$((SCORE + 1))
    else
        echo "  âŒ $DIR NO es escribible"
    fi
done

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL permisos verificados"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 5: VALIDACIÃ“N DE SINTAXIS (Â¿Los archivos de configuraciÃ³n son vÃ¡lidos?)

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "âœï¸  CATEGORÃA 5: VALIDACIÃ“N DE SINTAXIS"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

echo ""
echo "--- JSON vÃ¡lido ---"
for JSON_FILE in .gemini/settings.json .subagents/manifest.json; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$JSON_FILE" ]; then
        if jq empty "$JSON_FILE" 2>/dev/null; then
            echo "  âœ… $JSON_FILE es JSON vÃ¡lido"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $JSON_FILE tiene JSON INVÃLIDO"
            jq empty "$JSON_FILE" 2>&1 | head -3 | sed 's/^/     /'
        fi
    else
        echo "  âŒ $JSON_FILE no existe"
    fi
done

echo ""
echo "--- Biblioteca central catalog.json ---"
if [ -f "_global-profile/.antigravity/library/catalog.json" ]; then
    TOTAL=$((TOTAL + 1))
    if jq empty "_global-profile/.antigravity/library/catalog.json" 2>/dev/null; then
        echo "  âœ… catalog.json es JSON vÃ¡lido"
        SCORE=$((SCORE + 1))
    else
        echo "  âŒ catalog.json tiene JSON INVÃLIDO"
    fi
fi

echo ""
echo "--- YAML vÃ¡lido (.codex/config.yaml) ---"
TOTAL=$((TOTAL + 1))
if [ -f ".codex/config.yaml" ]; then
    # VerificaciÃ³n bÃ¡sica de YAML
    if grep -q "^[a-zA-Z]" ".codex/config.yaml" 2>/dev/null; then
        echo "  âœ… .codex/config.yaml tiene estructura YAML"
        SCORE=$((SCORE + 1))
    else
        echo "  âš ï¸ .codex/config.yaml puede tener problemas de formato"
    fi
else
    echo "  âŒ .codex/config.yaml no existe"
fi

echo ""
echo "--- TOML bÃ¡sico (sub-agentes Gemini) ---"
for TOML_FILE in .gemini/agents/*.toml; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$TOML_FILE" ]; then
        HAS_NAME=$(grep -c "^name" "$TOML_FILE" 2>/dev/null)
        HAS_DESC=$(grep -c "^description" "$TOML_FILE" 2>/dev/null)
        HAS_PROMPT=$(grep -c "system_prompt" "$TOML_FILE" 2>/dev/null)

        if [ "$HAS_NAME" -gt 0 ] && [ "$HAS_DESC" -gt 0 ] && [ "$HAS_PROMPT" -gt 0 ]; then
            echo "  âœ… $TOML_FILE estructura TOML correcta"
            SCORE=$((SCORE + 1))
        else
            echo "  âš ï¸ $TOML_FILE faltan campos (name:$HAS_NAME desc:$HAS_DESC prompt:$HAS_PROMPT)"
        fi
    fi
done

echo ""
echo "--- Bash syntax check ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        TOTAL=$((TOTAL + 1))
        if bash -n "$SCRIPT" 2>/dev/null; then
            echo "  âœ… $SCRIPT sintaxis bash vÃ¡lida"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $SCRIPT tiene errores de sintaxis:"
            bash -n "$SCRIPT" 2>&1 | head -3 | sed 's/^/     /'
        fi
    fi
done

echo ""
echo "--- Markdown (sin caracteres rotos) ---"
for MD_FILE in GEMINI.md CLAUDE.md CHANGELOG.md docs/README.md docs/DEVLOG.md; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$MD_FILE" ]; then
        if file "$MD_FILE" | grep -q "text"; then
            echo "  âœ… $MD_FILE es texto vÃ¡lido"
            SCORE=$((SCORE + 1))
        else
            echo "  âš ï¸ $MD_FILE encoding sospechoso: $(file "$MD_FILE")"
        fi
    else
        echo "  âŒ $MD_FILE no existe"
    fi
done

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL validaciones de sintaxis"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 6: CONECTIVIDAD Y AUTENTICACIÃ“N

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸŒ CATEGORÃA 6: CONECTIVIDAD Y AUTENTICACIÃ“N"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

echo ""
echo "--- Gemini CLI autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v gemini &>/dev/null; then
    GEMINI_AUTH=$(timeout 30 gemini -p "Responde solo: OK" --non-interactive 2>&1 | head -5)
    if echo "$GEMINI_AUTH" | grep -qi "ok\|OK\|gemini"; then
        echo "  âœ… Gemini CLI responde (autenticado)"
        SCORE=$((SCORE + 1))
    elif echo "$GEMINI_AUTH" | grep -qi "auth\|login\|credential\|error"; then
        echo "  âŒ Gemini CLI: problema de autenticaciÃ³n"
        echo "     $GEMINI_AUTH" | head -2 | sed 's/^/     /'
    else
        echo "  âš ï¸ Gemini CLI: respuesta inesperada"
    fi
else
    echo "  âŒ Gemini CLI no instalado"
fi

echo ""
echo "--- Claude Code autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v claude &>/dev/null; then
    CLAUDE_AUTH=$(timeout 30 claude -p "Responde solo: OK" --no-input 2>&1 | head -5)
    if echo "$CLAUDE_AUTH" | grep -qi "ok\|OK\|claude"; then
        echo "  âœ… Claude Code responde (autenticado)"
        SCORE=$((SCORE + 1))
    elif echo "$CLAUDE_AUTH" | grep -qi "auth\|login\|key\|error"; then
        echo "  âŒ Claude Code: problema de autenticaciÃ³n"
        echo "     $CLAUDE_AUTH" | head -2 | sed 's/^/     /'
    else
        echo "  âš ï¸ Claude Code: respuesta inesperada"
    fi
else
    echo "  âŒ Claude Code CLI no instalado"
fi

echo ""
echo "--- Codex CLI autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v codex &>/dev/null; then
    # Codex puede verificarse con un comando simple
    CODEX_AUTH=$(timeout 30 codex --version 2>&1 | head -3)
    if echo "$CODEX_AUTH" | grep -qi "codex\|version\|[0-9]"; then
        echo "  âœ… Codex CLI disponible: $CODEX_AUTH"
        SCORE=$((SCORE + 1))
    else
        echo "  âš ï¸ Codex CLI: respuesta inesperada"
    fi
else
    echo "  âŒ Codex CLI no instalado"
fi

echo ""
echo "--- Git configurado ---"
TOTAL=$((TOTAL + 1))
if git rev-parse --is-inside-work-tree &>/dev/null; then
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    BRANCH=$(git branch --show-current 2>/dev/null || echo "desconocida")
    echo "  âœ… Git repo activo (rama: $BRANCH, commits: $COMMIT_COUNT)"
    SCORE=$((SCORE + 1))
else
    echo "  âš ï¸ No es un repositorio Git"
fi

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL verificaciones de conectividad"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 7: TEST FUNCIONAL DE SUB-AGENTES

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ¤– CATEGORÃA 7: TEST FUNCIONAL DE SUB-AGENTES"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "âš ï¸  Estos tests invocan agentes reales (consumen cuota)."
echo "    Ejecutar solo si CategorÃ­as 1-6 pasaron bien."
echo ""

SCORE=0
TOTAL=0
```

Para esta categorÃ­a, ejecuta cada test UNO POR UNO y reporta el resultado.
No ejecutes todos de golpe. Espera que cada uno termine.

### Test 7.1: Sub-agente doc-writer (Gemini CLI)

```bash
echo ""
echo "--- Test 7.1: doc-writer via Gemini CLI ---"
TOTAL=$((TOTAL + 1))

RESULT=$(timeout 120 gemini -p "Eres doc-writer. Genera una entrada de DEVLOG para hoy que diga: 'Se completÃ³ la auditorÃ­a del sistema agÃ©ntico'. Formato Keep a Changelog, en espaÃ±ol. Solo responde con el texto markdown." --yolo 2>&1 | tail -20)

if echo "$RESULT" | grep -qi "auditorÃ­a\|agÃ©ntico\|DEVLOG\|##"; then
    echo "  âœ… doc-writer respondiÃ³ correctamente"
    SCORE=$((SCORE + 1))
else
    echo "  âŒ doc-writer no respondiÃ³ como esperado"
    echo "     Output: $(echo "$RESULT" | tail -3)"
fi
```

### Test 7.2: Claude Code como sub-agente

```bash
echo ""
echo "--- Test 7.2: Claude Code CLI ---"
TOTAL=$((TOTAL + 1))

if command -v claude &>/dev/null; then
    RESULT=$(timeout 120 claude -p "Responde brevemente: Â¿QuÃ© archivo deberÃ­as leer primero al trabajar en este proyecto? (pista: CLAUDE.md)" --no-input 2>&1 | tail -10)

    if echo "$RESULT" | grep -qi "CLAUDE\|claude\|proyecto\|documentaciÃ³n"; then
        echo "  âœ… Claude Code respondiÃ³ correctamente"
        SCORE=$((SCORE + 1))
    else
        echo "  âš ï¸ Claude Code respondiÃ³ pero sin contexto del proyecto"
        echo "     Output: $(echo "$RESULT" | tail -3)"
    fi
else
    echo "  âŒ Claude Code no disponible (no instalado)"
fi
```

### Test 7.3: Codex CLI (researcher agent)

```bash
echo ""
echo "--- Test 7.3: Codex CLI ---"
TOTAL=$((TOTAL + 1))

if command -v codex &>/dev/null; then
    # Test bÃ¡sico de Codex
    RESULT=$(timeout 120 codex exec "Responde solo: OK" 2>&1 | tail -10)

    if echo "$RESULT" | grep -qi "ok\|OK"; then
        echo "  âœ… Codex CLI respondiÃ³ correctamente"
        SCORE=$((SCORE + 1))
    else
        echo "  âš ï¸ Codex CLI: respuesta inesperada"
        echo "     Output: $(echo "$RESULT" | tail -3)"
    fi
else
    echo "  âŒ Codex CLI no disponible"
fi
```

### Test 7.4: Dispatcher multi-vendor

```bash
echo ""
echo "--- Test 7.4: VerificaciÃ³n de dispatcher multi-vendor ---"
TOTAL=$((TOTAL + 1))

if [ -x ".subagents/dispatch.sh" ]; then
    echo "  âœ… dispatch.sh existe y es ejecutable"
    SCORE=$((SCORE + 1))

    # Verificar que soporte los 3 vendors
    TOTAL=$((TOTAL + 1))
    if grep -q "gemini\|claude\|codex" .subagents/dispatch.sh 2>/dev/null; then
        echo "  âœ… dispatch.sh soporta mÃºltiples vendors"
        SCORE=$((SCORE + 1))
    else
        echo "  âš ï¸ dispatch.sh puede no soportar todos los vendors"
    fi
else
    echo "  âŒ dispatch.sh no existe o no es ejecutable"
fi
```

### Test 7.5: Biblioteca central scripts

```bash
echo ""
echo "--- Test 7.5: Biblioteca central (si existe) ---"
if [ -d "_global-profile/.antigravity/library/scripts" ]; then
    for SCRIPT in enable.sh disable.sh list.sh; do
        TOTAL=$((TOTAL + 1))
        if [ -x "_global-profile/.antigravity/library/scripts/$SCRIPT" ]; then
            echo "  âœ… $SCRIPT existe y es ejecutable"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ $SCRIPT no existe o no es ejecutable"
        fi
    done
else
    echo "  âš ï¸ Biblioteca central no configurada (opcional)"
fi
```

```bash
echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL tests funcionales"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## CATEGORÃA 8: COHERENCIA Y CROSS-REFERENCES

Verifica que los archivos se referencien correctamente entre sÃ­:

```bash
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo "ðŸ”— CATEGORÃA 8: COHERENCIA Y CROSS-REFERENCES"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"

SCORE=0
TOTAL=0

echo ""
echo "--- GEMINI.md referencia todos los sub-agentes Gemini ---"
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" GEMINI.md 2>/dev/null; then
            echo "  âœ… GEMINI.md menciona $AGENT_NAME"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ GEMINI.md NO menciona $AGENT_NAME"
        fi
    fi
done

echo ""
echo "--- manifest.json referencia todos los sub-agentes ---"
# Verificar agentes Gemini
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" .subagents/manifest.json 2>/dev/null; then
            echo "  âœ… manifest.json registra $AGENT_NAME"
            SCORE=$((SCORE + 1))
        else
            echo "  âŒ manifest.json NO registra $AGENT_NAME"
        fi
    fi
done

# Verificar researcher (Codex)
TOTAL=$((TOTAL + 1))
if grep -q "researcher" .subagents/manifest.json 2>/dev/null; then
    echo "  âœ… manifest.json registra researcher"
    SCORE=$((SCORE + 1))
else
    echo "  âŒ manifest.json NO registra researcher"
fi

echo ""
echo "--- Agentes Codex tienen equivalente en manifest ---"
for AGENT_FILE in .codex/agents/*.md; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .md)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" .subagents/manifest.json 2>/dev/null; then
            echo "  âœ… Codex agent $AGENT_NAME estÃ¡ en manifest"
            SCORE=$((SCORE + 1))
        else
            echo "  âš ï¸ Codex agent $AGENT_NAME no estÃ¡ explÃ­cito en manifest"
        fi
    fi
done

echo ""
echo "--- Multi-vendor configurado correctamente ---"
TOTAL=$((TOTAL + 1))
VENDORS_COUNT=$(grep -o "supported_vendors" .subagents/manifest.json 2>/dev/null | wc -l)
if [ "$VENDORS_COUNT" -gt 3 ]; then
    echo "  âœ… Multi-vendor configurado ($VENDORS_COUNT agentes)"
    SCORE=$((SCORE + 1))
else
    echo "  âš ï¸ Solo $VENDORS_COUNT agentes tienen supported_vendors"
fi

echo ""
echo "--- Docs referenciados existen ---"
for DOC in "docs/DEVLOG.md" "docs/TASKS.md" "docs/README.md" "docs/research" "CHANGELOG.md"; do
    TOTAL=$((TOTAL + 1))
    if [ -e "$DOC" ]; then
        echo "  âœ… $DOC existe"
        SCORE=$((SCORE + 1))
    else
        echo "  âŒ $DOC NO existe"
    fi
done

echo ""
echo "--- .gitignore cubre archivos sensibles ---"
TOTAL=$((TOTAL + 1))
IGNORE_CHECKS=0
grep -q ".env" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
grep -q "node_modules" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
grep -q "__pycache__" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
if [ "$IGNORE_CHECKS" -ge 2 ]; then
    echo "  âœ… .gitignore cubre archivos sensibles ($IGNORE_CHECKS/3 patterns)"
    SCORE=$((SCORE + 1))
else
    echo "  âš ï¸ .gitignore incompleto ($IGNORE_CHECKS/3 patterns)"
fi

echo ""
echo "ðŸ“Š Resultado: $SCORE/$TOTAL verificaciones de coherencia"
echo "â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

---

## REPORTE FINAL CONSOLIDADO

Al terminar TODAS las categorÃ­as, genera este reporte:

```bash
echo ""
echo ""
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘      REPORTE DE AUDITORÃA â€” SISTEMA AGÃ‰NTICO MULTI-VENDOR   â•‘"
echo "â•‘                $(date +%Y-%m-%d\ %H:%M)                            â•‘"
echo "â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£"
echo "â•‘                                                              â•‘"
echo "â•‘  Cat. 1: Estructura de archivos    â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 2: Integridad de contenido   â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 3: Herramientas del entorno  â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 4: Permisos y ejecutabilidad â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 5: ValidaciÃ³n de sintaxis    â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 6: Conectividad y auth       â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 7: Tests funcionales         â†’ __/__ (___%)            â•‘"
echo "â•‘  Cat. 8: Coherencia y cross-refs   â†’ __/__ (___%)            â•‘"
echo "â•‘                                                              â•‘"
echo "â•‘  TOTAL GENERAL:  ___/___ (___%)                              â•‘"
echo "â•‘                                                              â•‘"
echo "â•‘  VENDORS VERIFICADOS:                                        â•‘"
echo "â•‘    â€¢ Gemini CLI:  [OK/FAIL]                                  â•‘"
echo "â•‘    â€¢ Claude Code: [OK/FAIL]                                  â•‘"
echo "â•‘    â€¢ Codex CLI:   [OK/FAIL]                                  â•‘"
echo "â•‘                                                              â•‘"
echo "â•‘  VEREDICTO:                                                  â•‘"
echo "â•‘    >= 90%  â†’ âœ… SISTEMA LISTO PARA PRODUCCIÃ“N                â•‘"
echo "â•‘    70-89%  â†’ âš ï¸  FUNCIONAL CON ADVERTENCIAS                  â•‘"
echo "â•‘    < 70%   â†’ âŒ REQUIERE CORRECCIONES                        â•‘"
echo "â•‘                                                              â•‘"
echo "â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£"
echo "â•‘  ACCIONES CORRECTIVAS REQUERIDAS:                            â•‘"
echo "â•‘                                                              â•‘"
echo "â•‘  (Lista aquÃ­ cada âŒ encontrada con su fix)                  â•‘"
echo "â•‘                                                              â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
```

**INSTRUCCIONES PARA EL REPORTE FINAL:**

1. Reemplaza los `__` con los nÃºmeros reales de cada categorÃ­a
2. Calcula porcentajes reales
3. Para CADA âŒ encontrada, escribe:
   - QuÃ© fallÃ³
   - Comando exacto para corregirlo
   - Prioridad (CRÃTICO / MEDIO / BAJO)
4. Para CADA âš ï¸, indica si requiere acciÃ³n o es aceptable
5. Da un veredicto final honesto
6. Si el score es < 90%, pregunta al usuario si quiere que corrijas las fallas automÃ¡ticamente

---

**FIN DEL PROMPT DE AUDITORÃA MULTI-VENDOR. Ejecuta categorÃ­a por categorÃ­a y genera el reporte final consolidado.**
