# Setup Completo — Sistema de Conhecimento + Agentes IA

> **Para qualquer IA:** Leia este arquivo do início ao fim e execute cada passo em ordem.
> Este guia monta um sistema completo de memória persistente + 150+ agentes especializados no Obsidian,
> integrado com Claude Code (ou qualquer LLM) para registrar automaticamente tudo que você faz.

---

## O que este sistema faz

Três camadas trabalhando juntas:

```
┌─────────────────────────────────────────────────────────┐
│  CAMADA 1 — BASE DE CONHECIMENTO (Método Karpathy)      │
│  Wiki em Markdown que cresce sozinha com o uso          │
│  Fontes → Conceitos → Entidades → INDEX → LOG           │
├─────────────────────────────────────────────────────────┤
│  CAMADA 2 — XQUADS SQUADS (150+ Agentes IA)             │
│  13 squads especializados, cada um com um Chief         │
│  META-CHIEF roteia para o squad certo automaticamente   │
├─────────────────────────────────────────────────────────┤
│  CAMADA 3 — REGISTRO AUTOMÁTICO                         │
│  Hook Stop do Claude Code → session-logger.py           │
│  Toda sessão vira uma source na base de conhecimento    │
└─────────────────────────────────────────────────────────┘
```

**Referências originais:**
- Método Karpathy: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Xquads Squads: https://github.com/ohmyjahh/xquads-squads.git

---

## Pré-requisitos

- [Obsidian](https://obsidian.md) instalado
- [Claude Code](https://claude.ai/code) instalado (`npm install -g @anthropic-ai/claude-code`)
- Python 3.8+ (`python3 --version`)
- Git (`git --version`)

---

## PASSO 1 — Criar a estrutura do Obsidian

Escolha onde ficará seu cofre Obsidian. Neste guia usamos `~/obsidian/tudo/`.
Ajuste todos os caminhos para o seu.

```bash
# Cria a estrutura completa da base de conhecimento
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/wiki/sources
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/wiki/concepts
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/wiki/entities
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/wiki/queries
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/wiki/topics
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/raw/youtube
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/raw/papers
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/raw/web
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/scripts
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/templates
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/prompts
```

### 1.1 — Criar INDEX.md

Crie o arquivo `~/obsidian/tudo/Base de Conhecimento/wiki/INDEX.md`:

```markdown
# Index

Este indice resume o que existe na base `Base de Conhecimento`.

## Sources

## Concepts

## Entities

## Topics

## Queries

_Nenhuma query registrada ainda._
```

### 1.2 — Criar LOG.md

Crie o arquivo `~/obsidian/tudo/Base de Conhecimento/wiki/LOG.md`:

```markdown
# Log
```

### 1.3 — Como a base funciona (Método Karpathy)

A base tem três camadas imutáveis/mutáveis:

| Camada | Pasta | O que é |
|--------|-------|---------|
| **Raw** | `raw/` | Material bruto — nunca editado pela IA |
| **Wiki** | `wiki/` | Conhecimento processado — mantido pela IA |
| **Schema** | `CLAUDE.md` | Regras de comportamento da IA |

Quando você pede para "ingerir" algo, a IA:
1. Salva o bruto em `raw/`
2. Cria/atualiza uma **source** em `wiki/sources/`
3. Extrai **conceitos** para `wiki/concepts/`
4. Extrai **entidades** para `wiki/entities/`
5. Conecta tudo com `[[wikilinks]]`
6. Atualiza `wiki/INDEX.md` e `wiki/LOG.md`

**Formato de uma source:**
```markdown
---
type: source
status: ingested
title: "Título da fonte"
captured_at: "YYYY-MM-DD"
tags:
  - source
  - [tag-do-projeto]
---

# Título

Resumo do que foi capturado.

## Seção 1
...
```

**Formato de um conceito:**
```markdown
---
type: concept
---

# Nome do Conceito

Definição clara e concisa.

## Como se aplica
...

## Relacionado a
- [[Outro Conceito]]
- [[Entidade Relevante]]
```

---

## PASSO 2 — Instalar os Xquads Squads

```bash
# Clona o repositório
git clone https://github.com/ohmyjahh/xquads-squads.git /tmp/xquads-squads

# Copia para dentro do Obsidian (ajuste o caminho)
rsync -av --exclude=".DS_Store" --exclude=".next" /tmp/xquads-squads/ ~/obsidian/xquads-squads/

# Limpa o temporário
rm -rf /tmp/xquads-squads
```

### 2.1 — Criar o META-CHIEF

Crie `~/obsidian/xquads-squads/META-CHIEF.md` com o conteúdo abaixo.
**Este é o arquivo mais importante** — é o ponto de entrada para qualquer IA.

```markdown
# META-CHIEF — Orquestrador Mestre dos Xquads

> ACTIVATION-NOTICE: Você é o META-CHIEF. Diagnostique o que o usuário precisa
> e ative o Chief do squad mais adequado. Não execute tarefas diretamente.

## Squads e Chiefs disponíveis

| Squad | Chief | Especialidade |
|-------|-------|---------------|
| advisory-board | board-chair | Estratégia, mentores mundiais (Dalio, Munger, Naval...) |
| brand-squad | brand-chief | Branding, posicionamento, naming |
| c-level-squad | vision-chief | CEO/COO/CMO/CTO/CIO/CAIO virtual |
| claude-code-mastery | claude-mastery-chief | Claude Code, AIOS, desenvolvimento com IA |
| copy-master | copy-master-chief | Copy de elite — 33 agentes (Halbert, Schwartz...) |
| copy-squad | copy-chief | Copy funcional — 23 agentes |
| cybersecurity | cyber-chief | Pentest, segurança defensiva, CTF |
| data-squad | data-chief | Analytics, growth, retenção, comunidade |
| design-squad | design-chief | UX/UI, design systems |
| hormozi-squad | hormozi-chief | Ofertas, vendas, escala (framework Hormozi) |
| movement | movement-chief | Movimento, manifesto, comunidade |
| storytelling | story-chief | Pitch, narrativa, storytelling |
| traffic-masters | traffic-chief | Meta/Google/YouTube/TikTok Ads |

## Lógica de roteamento

- Estratégia / decisão difícil → advisory-board
- Marca / identidade → brand-squad
- Empresa / executivo → c-level-squad
- Escrever copy / texto → copy-squad ou copy-master
- Negócio / oferta / venda → hormozi-squad
- Tráfego / anúncios → traffic-masters
- Pitch / narrativa → storytelling
- Dados / métricas → data-squad
- Design / UX → design-squad
- Segurança → cybersecurity
- Movimento / causa → movement
- Claude Code / IA / código → claude-code-mastery

## Como ativar um Chief

Leia o arquivo .md do Chief, assuma a persona e inicie com o greeting do agente.

Exemplo: para ativar o Hormozi Chief, leia:
`xquads-squads/hormozi-squad/agents/hormozi-chief.md`
```

### 2.2 — Criar a pasta de scripts

```bash
mkdir -p ~/obsidian/xquads-squads/scripts
```

---

## PASSO 3 — Criar o session-logger.py

Crie `~/obsidian/xquads-squads/scripts/session-logger.py`:

```python
#!/usr/bin/env python3
"""
Session Logger — ingere sessões do Claude Code na base de conhecimento.
Hook: Stop do Claude Code. Roda automaticamente após cada resposta.
AJUSTE: Mude KB_PATH para o caminho da sua base de conhecimento.
"""
import json, sys, os, re
from datetime import datetime
from pathlib import Path

# ── AJUSTE ESTES CAMINHOS ─────────────────────────────────────────────────────
KB    = Path.home() / 'obsidian/tudo/Base de Conhecimento'
# ─────────────────────────────────────────────────────────────────────────────

WIKI  = KB / 'wiki'
SRC   = WIKI / 'sources'
INDEX = WIKI / 'INDEX.md'
LOG   = WIKI / 'LOG.md'

CHIEF_LABELS = {
    'board-chair': 'Advisory Board', 'vision-chief': 'C-Level Squad',
    'brand-chief': 'Brand Squad', 'copy-chief': 'Copy Squad',
    'copy-master-chief': 'Copy Master', 'hormozi-chief': 'Hormozi Squad',
    'traffic-chief': 'Traffic Masters', 'story-chief': 'Storytelling',
    'data-chief': 'Data Squad', 'design-chief': 'Design Squad',
    'cyber-chief': 'Cybersecurity', 'movement-chief': 'Movement',
    'claude-mastery-chief': 'Claude Code Mastery', 'meta-chief': 'META-CHIEF',
}

try:
    data = json.loads(sys.stdin.read())
except Exception:
    sys.exit(0)

transcript_path = data.get('transcript_path', '')
cwd             = data.get('cwd', os.getcwd())
project_name    = Path(cwd).name

files_created, files_modified, bash_commands = [], [], []
user_messages, assistant_first = [], ''
agents_used = []

if transcript_path and os.path.exists(transcript_path):
    with open(transcript_path, encoding='utf-8') as f:
        for line in f:
            try:
                turn = json.loads(line.strip())
            except Exception:
                continue
            role    = turn.get('type', '')
            msg     = turn.get('message', {})
            if not isinstance(msg, dict):
                continue
            content = msg.get('content', [])
            if isinstance(content, str):
                if role == 'user' and len(content) > 5:
                    user_messages.append(content[:400])
                    for kw, label in CHIEF_LABELS.items():
                        if kw in content.lower() and label not in agents_used:
                            agents_used.append(label)
                continue
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if role == 'user' and block.get('type') == 'text':
                    txt = block['text'].strip()
                    if txt and len(txt) > 5:
                        user_messages.append(txt[:400])
                    for kw, label in CHIEF_LABELS.items():
                        if kw in txt.lower() and label not in agents_used:
                            agents_used.append(label)
                if role == 'assistant' and block.get('type') == 'text' and not assistant_first:
                    t = block.get('text', '').strip()
                    if len(t) > 30 and not t.startswith('```'):
                        assistant_first = t[:600]
                if role == 'assistant' and block.get('type') == 'tool_use':
                    name = block.get('name', '')
                    inp  = block.get('input', {})
                    if name == 'Write':
                        fp = inp.get('file_path', '')
                        if fp and fp not in files_created:
                            files_created.append(fp)
                    elif name == 'Edit':
                        fp = inp.get('file_path', '')
                        if fp and fp not in files_modified:
                            files_modified.append(fp)
                    elif name == 'Bash':
                        cmd = inp.get('command', '').strip()
                        if cmd and len(bash_commands) < 20:
                            bash_commands.append(cmd[:150])

all_changed = files_created + files_modified
if not user_messages and not all_changed:
    sys.exit(0)

now      = datetime.now()
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H:%M')

source_title = f"Sessao Claude {project_name} {date_str}"
source_file  = SRC / f"{source_title}.md"
is_update    = source_file.exists()

tags = ['source', 'claude-session', project_name.lower().replace(' ','-').replace('_','-')]
if agents_used:
    tags.append('xquads')

meaningful_cmds = [
    c for c in bash_commands
    if not any(s in c for s in ['ls ','echo ','cat ','pwd','which ','head ','tail '])
]

lines = [
    "---", "type: source", "status: ingested",
    f'title: "Sessão Claude — {project_name} — {date_str}"',
    f'captured_at: "{date_str}"', f'project_path: "{cwd}"',
    f'updated_at: "{time_str}"', "tags:",
] + [f"  - {t}" for t in tags] + [
    "---", "",
    f"# Sessão Claude — {project_name} — {date_str}",
    f"_Última atualização: {time_str}_", "",
    f"Sessão de trabalho em `{cwd}`.", "",
]

if user_messages:
    lines += ["## O que foi pedido", ""]
    for msg in user_messages[:5]:
        lines.append(f"> {msg}"); lines.append(">")
    lines.append("")

if agents_used:
    lines += ["## Agentes Xquads Ativados", ""]
    for a in agents_used:
        lines.append(f"- [[Xquads Squads]] → **{a}**")
    lines.append("")

if files_created:
    lines += ["## Arquivos Criados", ""]
    for fp in files_created:
        short = fp.replace(cwd + '/', '').replace(str(Path.home()), '~')
        lines.append(f"- `{short}`")
    lines.append("")

if files_modified:
    lines += ["## Arquivos Modificados", ""]
    for fp in files_modified:
        short = fp.replace(cwd + '/', '').replace(str(Path.home()), '~')
        lines.append(f"- `{short}`")
    lines.append("")

if meaningful_cmds:
    lines += ["## Comandos Executados", ""]
    for cmd in meaningful_cmds[:10]:
        lines.append(f"- `{cmd}`")
    lines.append("")

if assistant_first:
    lines += ["## Resumo", "", assistant_first, ""]

source_file.write_text('\n'.join(lines), encoding='utf-8')

wiki_name  = source_title
index_text = INDEX.read_text(encoding='utf-8') if INDEX.exists() else ''
index_entry = f"- [[{wiki_name}]]"
if index_entry not in index_text and '## Sources' in index_text:
    index_text = index_text.replace('## Sources\n', f'## Sources\n{index_entry}\n', 1)
    INDEX.write_text(index_text, encoding='utf-8')

log_text    = LOG.read_text(encoding='utf-8') if LOG.exists() else '# Log\n'
date_header = f"## {date_str}"

if is_update:
    if all_changed and wiki_name in log_text:
        n = len(all_changed)
        nomes = ', '.join(f'`{Path(f).name}`' for f in all_changed[:5])
        update_line = f"- [[{wiki_name}]] atualizada: {n} arquivo(s) — {nomes}{'...' if n > 5 else ''}."
        if update_line not in log_text:
            log_text = log_text.replace(date_header + '\n', date_header + '\n' + update_line + '\n', 1)
            LOG.write_text(log_text, encoding='utf-8')
else:
    log_entries = [f"- Ingerida sessão Claude em `{project_name}` como [[{wiki_name}]]."]
    if agents_used:
        log_entries.append(f"- Agentes Xquads: {', '.join(f'[[{a}]]' for a in agents_used)}.")
    if all_changed:
        n = len(all_changed)
        nomes = ', '.join(f'`{Path(f).name}`' for f in all_changed[:5])
        log_entries.append(f"- {n} arquivo(s): {nomes}{'...' if n > 5 else ''}.")
    log_block = '\n'.join(log_entries)
    if date_header in log_text:
        log_text = log_text.replace(date_header + '\n', date_header + '\n' + log_block + '\n', 1)
    else:
        log_text = log_text.replace('# Log\n', f'# Log\n\n{date_header}\n{log_block}\n', 1)
    LOG.write_text(log_text, encoding='utf-8')

if agents_used:
    entity_path = WIKI / 'entities' / 'Xquads Squads.md'
    if not entity_path.exists() and (WIKI / 'entities').exists():
        entity_path.write_text(
            "---\ntype: entity\n---\n\n# Xquads Squads\n\n"
            "Sistema de 13 squads com 150+ agentes IA especializados.\n"
            "Repo: https://github.com/ohmyjahh/xquads-squads\n",
            encoding='utf-8'
        )
```

```bash
# Torna executável
chmod +x ~/obsidian/xquads-squads/scripts/session-logger.py
```

---

## PASSO 4 — Configurar o Claude Code

### 4.1 — CLAUDE.md global (carrega em qualquer pasta)

Crie `~/.claude/CLAUDE.md`. **Ajuste os caminhos para os seus.**

```markdown
# Instruções Globais

## Base de Conhecimento

Cofre do Obsidian com base de conhecimento em Markdown.

Base principal:
~/obsidian/tudo/Base de Conhecimento

Ao responder perguntas sobre memória, comece por:
~/obsidian/tudo/Base de Conhecimento/wiki/INDEX.md

Abra apenas as notas relevantes linkadas no índice.

## Ingestão

Quando o usuário pedir "ingerir", "processar", "salvar na memória", "adicionar à base":

1. Preserve material bruto em `Base de Conhecimento/raw/`
2. Crie/atualize uma source em `Base de Conhecimento/wiki/sources/`
3. Extraia conceitos para `Base de Conhecimento/wiki/concepts/`
4. Extraia entidades para `Base de Conhecimento/wiki/entities/`
5. Conecte tudo com backlinks `[[Nome da Nota]]`
6. Atualize `wiki/INDEX.md` e `wiki/LOG.md`

## Regras

- Nunca salve senhas, tokens, chaves, .pem ou secrets
- Não invente fatos — marque inferências como inferências
- Prefira notas pequenas e reutilizáveis
- Antes de criar nota nova, verifique se já existe

## Sistema de Agentes Xquads

13 squads com 150+ agentes em: ~/obsidian/xquads-squads/

Quando o usuário pedir um agente/squad, leia o arquivo do Chief e assuma a persona.

| Quando disser... | Leia este arquivo |
|------------------|-------------------|
| "advisory board" / "board chair" | xquads-squads/advisory-board/agents/board-chair.md |
| "c-level" / "vision chief" | xquads-squads/c-level-squad/agents/vision-chief.md |
| "brand" / "brand chief" | xquads-squads/brand-squad/agents/brand-chief.md |
| "copy squad" / "copy chief" | xquads-squads/copy-squad/agents/copy-chief.md |
| "copy master" | xquads-squads/copy-master/agents/copy-master-chief.md |
| "hormozi" | xquads-squads/hormozi-squad/agents/hormozi-chief.md |
| "tráfego" / "traffic" | xquads-squads/traffic-masters/agents/traffic-chief.md |
| "storytelling" / "pitch" | xquads-squads/storytelling/agents/story-chief.md |
| "data squad" / "analytics" | xquads-squads/data-squad/agents/data-chief.md |
| "design squad" | xquads-squads/design-squad/agents/design-chief.md |
| "cybersecurity" / "pentest" | xquads-squads/cybersecurity/agents/cyber-chief.md |
| "movement" | xquads-squads/movement/agents/movement-chief.md |
| "claude code mastery" | xquads-squads/claude-code-mastery/agents/claude-mastery-chief.md |
| "meta-chief" / não sabe qual | xquads-squads/META-CHIEF.md |
```

### 4.2 — Hook de registro automático

Crie/edite `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/obsidian/xquads-squads/scripts/session-logger.py"
          }
        ]
      }
    ]
  }
}
```

> **O que faz:** Após cada resposta do Claude Code, o script roda automaticamente,
> lê o transcript da sessão e registra o que foi feito na base de conhecimento.
> Você não precisa fazer nada — é 100% automático.

---

## PASSO 5 — Testar

### Teste 1: Script de logging

```bash
echo '{"session_id":"test","transcript_path":"","cwd":"'"$HOME"'"}' | \
  python3 ~/obsidian/xquads-squads/scripts/session-logger.py && echo "OK"
```

### Teste 2: Claude Code lendo um Chief

Abra o Claude Code em qualquer pasta e diga:
```
chama o hormozi chief
```
O Claude deve ler `xquads-squads/hormozi-squad/agents/hormozi-chief.md` e assumir a persona.

### Teste 3: Ingestão manual

No Claude Code, diga:
```
ingere isso na base de conhecimento: [cole qualquer texto aqui]
```
Verifique se uma source foi criada em `wiki/sources/` e se INDEX e LOG foram atualizados.

---

## Estrutura final esperada

```
~/obsidian/
├── tudo/
│   ├── CLAUDE.md                          ← regras da base para IA
│   └── Base de Conhecimento/
│       ├── wiki/
│       │   ├── INDEX.md                   ← índice mestre
│       │   ├── LOG.md                     ← log cronológico
│       │   ├── sources/                   ← fontes ingeridas
│       │   ├── concepts/                  ← conceitos extraídos
│       │   ├── entities/                  ← entidades (pessoas, projetos...)
│       │   ├── queries/                   ← perguntas respondidas
│       │   └── topics/                    ← tópicos agrupados
│       ├── raw/                           ← material bruto (não editado)
│       │   ├── youtube/
│       │   ├── papers/
│       │   └── web/
│       ├── scripts/
│       └── templates/
└── xquads-squads/                         ← 13 squads, 150+ agentes
    ├── META-CHIEF.md                      ← ponto de entrada universal
    ├── INDEX.md                           ← índice dos squads
    ├── SETUP-COMPLETO.md                  ← este arquivo
    ├── scripts/
    │   └── session-logger.py              ← hook de registro automático
    ├── advisory-board/
    ├── brand-squad/
    ├── c-level-squad/
    ├── claude-code-mastery/
    ├── copy-master/
    ├── copy-squad/
    ├── cybersecurity/
    ├── data-squad/
    ├── design-squad/
    ├── hormozi-squad/
    ├── movement/
    ├── storytelling/
    └── traffic-masters/

~/.claude/
├── CLAUDE.md                              ← instruções globais (qualquer pasta)
└── settings.json                          ← hook Stop configurado
```

---

## Como usar com outras IAs (não Claude Code)

O sistema funciona com **qualquer LLM**. Para GPT-4, Gemini, Llama, etc.:

**Opção A — Ativar um Chief diretamente:**
1. Abra o arquivo `.md` do Chief desejado no Obsidian
2. Copie o conteúdo completo
3. Cole no início da conversa com a IA
4. Diga: "Aja como este agente e me ajude com: [sua tarefa]"

**Opção B — Usar o META-CHIEF como roteador:**
1. Abra `xquads-squads/META-CHIEF.md`
2. Copie o conteúdo
3. Cole na IA e descreva sua necessidade em linguagem natural
4. O META-CHIEF vai identificar o squad certo e você ativa o Chief

**Opção C — Ingestão manual na base:**
Se não usar Claude Code, copie o prompt de ingestão abaixo e use com qualquer IA:

```
Você é um assistente de gestão de conhecimento.
Tenho uma base de conhecimento em Markdown estruturada assim:
- wiki/sources/ → fontes processadas
- wiki/concepts/ → conceitos extraídos
- wiki/entities/ → entidades (pessoas, projetos, ferramentas)
- wiki/INDEX.md → índice mestre com seções Sources, Concepts, Entities, Topics
- wiki/LOG.md → log cronológico com headers ## YYYY-MM-DD

Ingira o conteúdo abaixo seguindo este processo:
1. Crie uma source em wiki/sources/[Titulo YYYY-MM-DD].md
2. Extraia 3-7 conceitos reutilizáveis para wiki/concepts/
3. Identifique entidades para wiki/entities/
4. Atualize INDEX.md (seção Sources e Concepts)
5. Atualize LOG.md (seção da data de hoje)
6. Use [[wikilinks]] para conectar tudo

Conteúdo a ingerir:
[COLE O CONTEÚDO AQUI]
```

---

## Referências

| Recurso | Link |
|---------|------|
| Método Karpathy (LLM Wiki) | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| Xquads Squads (repositório) | https://github.com/ohmyjahh/xquads-squads.git |
| Obsidian | https://obsidian.md |
| Claude Code | https://claude.ai/code |
| Dashboard dos agentes | https://xquads.vercel.app/xquads |

---

## Resumo em 5 comandos

```bash
# 1. Estrutura da base de conhecimento
mkdir -p ~/obsidian/tudo/Base\ de\ Conhecimento/{wiki/{sources,concepts,entities,queries,topics},raw/{youtube,papers,web},scripts,templates}

# 2. Instalar os squads
git clone https://github.com/ohmyjahh/xquads-squads.git /tmp/xq && rsync -av --exclude=".DS_Store" --exclude=".next" /tmp/xq/ ~/obsidian/xquads-squads/ && rm -rf /tmp/xq

# 3. Criar CLAUDE.md global (edite os caminhos)
# → Veja conteúdo no Passo 4.1 acima

# 4. Configurar hook de registro automático
# → Veja settings.json no Passo 4.2 acima

# 5. Criar session-logger.py
# → Veja código no Passo 3 acima (ajuste KB_PATH)
```

---

*Criado em 2026-05-22 | Base: `/Users/rubens/obsidian/xquads-squads/`*
