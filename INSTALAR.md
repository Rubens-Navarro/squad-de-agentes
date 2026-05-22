# Instalador — Squad de Agentes + Base de Conhecimento

> **INSTRUÇÃO PARA A IA:** Você é o instalador deste sistema.
> Leia este arquivo do início ao fim e execute cada passo em ordem.
> Não pule etapas. Os caminhos são calculados automaticamente — não pergunte sobre eles.

---

## PASSO 0 — Detectar o ambiente e perguntar apenas o necessário

### 0a. Calcular caminhos automaticamente (sem perguntar ao usuário)

Execute para descobrir o home do usuário:

```bash
python3 -c "from pathlib import Path; print(Path.home())"
```

A partir do resultado (`HOME`), derive todos os caminhos:

| Variável | Valor |
|----------|-------|
| `HOME` | resultado do comando acima |
| `VAULT` | `HOME/obsidian` |
| `KB` | `HOME/obsidian/Base de Conhecimento` |
| `XQUADS` | `HOME/obsidian/squad-de-agentes` |
| `DESIGN_TEMPLATES` | `HOME/obsidian/design-system-templates` |
| `DESIGN_REPO` | `https://github.com/Rubens-Navarro/system-design-templates.git` |

Exemplos reais:
- Mac/Linux: `HOME=/Users/maria` → `VAULT=/Users/maria/obsidian`
- Windows: `HOME=C:\Users\Maria` → `VAULT=C:\Users\Maria\obsidian`

**Não pergunte sobre caminhos. Crie tudo nessa estrutura.**

### 0b. Perguntar apenas isto

**Pergunta única:**
> "Qual ferramenta de IA você usa para programar?
> Opções: Claude Code, Cursor, Windsurf, Codex CLI, Aider, GitHub Copilot, Outra"

Salve o valor como `TOOL`.

Aguarde a resposta antes de continuar.

---

## PASSO 1 — Verificar pré-requisitos

Execute e verifique:

```bash
git --version
python3 --version
```

Se algum não estiver instalado, informe o usuário:
- Git: https://git-scm.com
- Python: https://python.org

---

## PASSO 2 — Instalar o Squad de Agentes

```bash
git clone https://github.com/Rubens-Navarro/squad-de-agentes.git "[XQUADS]"
```

Se a pasta já existir, execute:
```bash
cd "[XQUADS]" && git pull
```

---

## PASSO 2b — Instalar os Design System Templates

```bash
git clone [DESIGN_REPO] "[DESIGN_TEMPLATES]"
```

Se a pasta já existir, execute:
```bash
cd "[DESIGN_TEMPLATES]" && git pull
```

Este repositório contém DESIGN.md files de marcas reais (Airbnb, Apple, Stripe, Notion, Cursor, etc.)
e será usado pela IA como base para criar layouts autênticos em qualquer projeto frontend.

---

## PASSO 3 — Criar a estrutura da base de conhecimento

```bash
mkdir -p "[KB]/wiki/sources"
mkdir -p "[KB]/wiki/concepts"
mkdir -p "[KB]/wiki/entities"
mkdir -p "[KB]/wiki/queries"
mkdir -p "[KB]/wiki/topics"
mkdir -p "[KB]/raw/youtube"
mkdir -p "[KB]/raw/papers"
mkdir -p "[KB]/raw/web"
mkdir -p "[KB]/scripts"
mkdir -p "[KB]/templates"
mkdir -p "[KB]/prompts"
```

Crie `[KB]/wiki/INDEX.md`:
```markdown
# Index

Este indice resume o que existe na base de conhecimento.

## Sources

## Concepts

## Entities

## Topics

## Queries

_Nenhuma query registrada ainda._
```

Crie `[KB]/wiki/LOG.md`:
```markdown
# Log
```

---

## PASSO 4 — Configurar os caminhos no CONFIG.md

Edite o arquivo `[XQUADS]/CONFIG.md` para refletir os caminhos do usuário.

Substitua a seção entre os marcadores pelo seguinte:

```
OBSIDIAN_ROOT=[VAULT]
KNOWLEDGE_BASE=[KB]
XQUADS_PATH=[XQUADS]
DESIGN_TEMPLATES_PATH=[DESIGN_TEMPLATES]
DESIGN_TEMPLATES_REPO=[DESIGN_REPO]
```

Onde `[VAULT]`, `[KB]` e `[XQUADS]` são os valores coletados no Passo 0.

---

## PASSO 5 — Configurar a ferramenta de IA do usuário

### Se for Claude Code

**5a. Criar `~/.claude/CLAUDE.md`** (ou adicionar ao existente):

```markdown
# Instruções Globais

## Sistema Squad de Agentes + Base de Conhecimento

Leia `[XQUADS]/AI-INSTRUCTIONS.md` para instruções completas.
Leia `[XQUADS]/CONFIG.md` para os caminhos do sistema.

### Protocolo de Transformação

Pedido do usuário
      ↓
[1] Lê META-CHIEF.md → vira META-CHIEF → identifica o squad
      ↓
[2] Lê o Chief do squad → vira o Chief → decide o agente ideal
      ↓
[3] Lê o agente → vira o agente → executa a tarefa completa

REGRA: Uma única IA que morphe em sequência. Nunca múltiplos agentes em paralelo.
Anuncie: [TRANSFORMAÇÃO: PersonaAtual → NovaPersona]
```

**5b. Configurar hook de registro automático em `~/.claude/settings.json`:**

Se o arquivo não existir, crie-o. Se existir, adicione a chave `hooks` sem remover o que já está:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 [XQUADS]/scripts/startup-check.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 [XQUADS]/scripts/session-logger.py"
          }
        ]
      }
    ]
  }
}
```

`[XQUADS]` deve ser substituído pelo caminho real informado no Passo 0.
Exemplo: se `XQUADS` = `/Users/maria/obsidian/squad-de-agentes`, o comando fica:
`python3 /Users/maria/obsidian/squad-de-agentes/scripts/startup-check.py`

---

### Se for Cursor

Crie `~/.cursorrules` (regra global) ou `.cursorrules` na raiz de cada projeto:

```
Leia [XQUADS]/AI-INSTRUCTIONS.md para instruções completas.
Leia [XQUADS]/CONFIG.md para os caminhos do sistema.
Antes de trabalhar: leia [KB]/wiki/INDEX.md
Ao fim de toda sessão: execute python3 [XQUADS]/scripts/log-session.py --tool "cursor" --cwd "PASTA" --summary "RESUMO" --files "ARQUIVOS"
```

---

### Se for Windsurf

Crie `~/.windsurfrules`:

```
Leia [XQUADS]/AI-INSTRUCTIONS.md para instruções completas.
Leia [XQUADS]/CONFIG.md para os caminhos do sistema.
Antes de trabalhar: leia [KB]/wiki/INDEX.md
Ao fim de toda sessão: execute python3 [XQUADS]/scripts/log-session.py --tool "windsurf" --cwd "PASTA" --summary "RESUMO" --files "ARQUIVOS"
```

---

### Se for Codex CLI (OpenAI)

Crie `~/AGENTS.md`:

```markdown
# AGENTS.md

Leia [XQUADS]/AI-INSTRUCTIONS.md para instruções completas.
Leia [XQUADS]/CONFIG.md para os caminhos do sistema.
Antes de trabalhar: leia [KB]/wiki/INDEX.md
Ao fim de toda sessão: execute python3 [XQUADS]/scripts/log-session.py --tool "codex" --cwd "PASTA" --summary "RESUMO" --files "ARQUIVOS"
```

---

### Se for GitHub Copilot

Crie `.github/copilot-instructions.md` na raiz de cada projeto:

```markdown
Leia [XQUADS]/AI-INSTRUCTIONS.md para instruções completas.
Ao fim de toda sessão: execute python3 [XQUADS]/scripts/log-session.py --tool "copilot" --cwd "PASTA" --summary "RESUMO" --files "ARQUIVOS"
```

---

### Se for Aider

Adicione ao `~/.aider.conf.yml`:

```yaml
system-prompt: |
  Leia [XQUADS]/AI-INSTRUCTIONS.md para instruções completas.
  Leia [XQUADS]/CONFIG.md para os caminhos do sistema.
  Ao fim de toda sessão: execute python3 [XQUADS]/scripts/log-session.py --tool "aider" ...
```

---

## PASSO 6 — Criar entidade Squad de Agentes na base de conhecimento

Crie `[KB]/wiki/entities/Squad de Agentes.md`:

```markdown
---
type: entity
---

# Squad de Agentes

Sistema de 13 squads com 150+ agentes IA especializados.
Instalado em: [XQUADS]
Repositório: https://github.com/Rubens-Navarro/squad-de-agentes
Referência do método: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
```

Adicione ao `[KB]/wiki/INDEX.md` na seção `## Entities`:
```
- [[Squad de Agentes]]
```

Adicione ao `[KB]/wiki/LOG.md`:
```
## [DATA DE HOJE]
- Instalado Squad de Agentes em [[Squad de Agentes]].
- Base de conhecimento criada em `[KB]`.
- Ferramenta configurada: [TOOL].
```

---

## PASSO 7 — Verificar instalação

Execute o health check do sistema:

```bash
python3 "[XQUADS]/scripts/health-check.py"
```

Todos os itens devem mostrar `✓`. Se algum mostrar `✗`, o health check indica o comando para corrigir.

Em seguida, registre a instalação na base de conhecimento:

```bash
python3 "[XQUADS]/scripts/log-session.py" \
  --tool "[TOOL]" \
  --cwd "[VAULT]" \
  --summary "Instalação do Squad de Agentes e base de conhecimento" \
  --files "CONFIG.md,AI-INSTRUCTIONS.md,META-CHIEF.md"
```

---

## PASSO 8 — Confirmar para o usuário

Informe o usuário:

> ✅ **Sistema instalado com sucesso!**
>
> **O que foi criado em `[HOME]/obsidian/`:**
> - `xquads-squads/` — 13 squads com 150+ agentes IA
> - `Base de Conhecimento/` — sua base de conhecimento pessoal
> - `design-system-templates/` — referência visual de 71 marcas reais
>
> **Próximo passo obrigatório — abrir o Obsidian:**
> 1. Abra o Obsidian (baixe em https://obsidian.md se ainda não tiver)
> 2. Clique em "Abrir pasta como cofre"
> 3. Selecione `[VAULT]`
> 4. Pronto — sua base de conhecimento aparece organizada no Obsidian
>
> **Como usar com a IA:**
> - Diga "quero criar uma oferta" → a IA roteia para o agente certo automaticamente
> - Diga "cria o frontend do app" → a IA lê os templates de design e entrega layout autêntico
> - Diga "salva na base" → a IA ingere na base de conhecimento
> - O registro de sessões acontece automaticamente em segundo plano
>
> **Para começar agora:** diga o que você quer fazer.

---

## Referências

| Recurso | Link |
|---------|------|
| Squad de Agentes | https://github.com/Rubens-Navarro/squad-de-agentes |
| Método Karpathy (base de conhecimento) | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| Obsidian | https://obsidian.md |
| Claude Code | https://claude.ai/code |
