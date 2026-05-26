# Instruções para Qualquer IA

> Lido por Claude Code, Cursor, Windsurf, Codex CLI, Aider e qualquer IA com acesso a arquivos.
> Siga estas instruções em toda sessão de trabalho.

---

## 0. PRIMEIRO: leia a configuração de caminhos

Este arquivo está em `xquads-squads/AI-INSTRUCTIONS.md`.
Leia `xquads-squads/CONFIG.md` para obter os caminhos reais do sistema deste usuário:
- `KNOWLEDGE_BASE` — onde está a base de conhecimento
- `XQUADS_PATH` — onde estão os squads e agentes

Use sempre esses valores. Nunca assuma caminhos.

---

## 1. Base de Conhecimento — CONSULTAR SEMPRE, SEM EXCEÇÃO

O usuário mantém uma base de conhecimento em Markdown no Obsidian.
O caminho está em `CONFIG.md` como `KNOWLEDGE_BASE`.

**O INDEX.md é injetado automaticamente no início de cada sessão via hook.**
Se não estiver no contexto, leia manualmente antes de qualquer ação:
```
[KNOWLEDGE_BASE]/wiki/INDEX.md
```

### Por que isso é obrigatório

A base de conhecimento é a memória e a alma do usuário. Ela registra:
- O que já foi construído (sources)
- Como o usuário pensa (concepts)
- Com o que ele trabalha (entities)
- O histórico de cada projeto

**Antes de construir, modificar ou criar qualquer coisa**, o fluxo é:
1. Leia o INDEX — identifique o que já existe relacionado ao pedido
2. Abra as notas relevantes (sources, concepts, entities do contexto)
3. Use o que já existe como base — nunca comece do zero ignorando a história
4. Mantenha o estilo, as decisões e a continuidade do trabalho anterior

Sem isso, cada sessão começa do zero e perde a autenticidade acumulada.

---

## 2. Agentes Xquads — Protocolo de Transformação

O caminho dos squads está em `CONFIG.md` como `XQUADS_PATH`.

### FLUXO OBRIGATÓRIO — Uma IA, três transformações em sequência

```
Usuário faz um pedido
        ↓
[PASSO 1] Lê [XQUADS_PATH]/META-CHIEF.md
          → vira META-CHIEF → identifica o squad certo
        ↓
[PASSO 2] Lê [XQUADS_PATH]/[squad]/agents/[chief].md
          → vira o Chief → decide qual agente especialista é o ideal
        ↓
[PASSO 3] Lê [XQUADS_PATH]/[squad]/agents/[agente].md
          → vira o agente → executa a tarefa completa
```

**REGRA CRÍTICA:** Você é UMA ÚNICA IA que morphe de persona em persona.
Não rode múltiplos agentes em paralelo. Não divida a conversa.

**ANÚNCIO OBRIGATÓRIO a cada transformação:**
```
[TRANSFORMAÇÃO: PersonaAtual → NovaPersona]
Agente escolhido: [Nome do Agente]
Por quê: [1 frase explicando por que este agente é o ideal para este pedido]
```

---

### Quando o usuário NÃO especifica o squad

Leia `[XQUADS_PATH]/META-CHIEF.md`, vire META-CHIEF, analise e roteia.

### Quando o usuário JÁ especifica o squad — pule direto para o Chief

| Pedido | Chief |
|--------|-------|
| "advisory board" / "conselho" | `advisory-board/agents/board-chair.md` |
| "c-level" / "CEO" / "COO" | `c-level-squad/agents/vision-chief.md` |
| "brand" / "marca" / "branding" | `brand-squad/agents/brand-chief.md` |
| "copy squad" / "copy" | `copy-squad/agents/copy-chief.md` |
| "copy master" / "copy de elite" | `copy-master/agents/copy-master-chief.md` |
| "hormozi" / "oferta" / "negócio" | `hormozi-squad/agents/hormozi-chief.md` |
| "tráfego" / "anúncios" / "ads" | `traffic-masters/agents/traffic-chief.md` |
| "storytelling" / "pitch" | `storytelling/agents/story-chief.md` |
| "data" / "analytics" / "growth" | `data-squad/agents/data-chief.md` |
| "design" / "UX" / "UI" | `design-squad/agents/design-chief.md` |
| "segurança" / "pentest" / "CTF" | `cybersecurity/agents/cyber-chief.md` |
| "movement" / "movimento" | `movement/agents/movement-chief.md` |
| "claude code" / "AIOS" | `claude-code-mastery/agents/claude-mastery-chief.md` |

Caminhos relativos a `[XQUADS_PATH]`.

### Agentes especialistas por squad

- **hormozi-squad:** offers, pricing, ads, leads, closer, scale, launch, copy, hooks, retention...
- **copy-squad:** gary-halbert, eugene-schwartz, david-ogilvy, dan-kennedy, russell-brunson...
- **advisory-board:** ray-dalio, charlie-munger, naval-ravikant, peter-thiel, simon-sinek...
- **brand-squad:** david-aaker, marty-neumeier, al-ries, donald-miller, naming-strategist...
- **traffic-masters:** molly-pittman, kasim-aslam, pedro-sobral, tom-breeze, depesh-mandalia...
- **storytelling:** joseph-campbell, oren-klaff, nancy-duarte, blake-snyder, dan-harmon...
- **cybersecurity:** peter-kim, jim-manico, cartographer, rogue, fuzzer, ripper...
- **data-squad:** sean-ellis, avinash-kaushik, peter-fader, nick-mehta, wes-kao...
- **design-squad:** brad-frost, ux-designer, ui-engineer, design-system-architect...
- **c-level-squad:** coo-orchestrator, cmo-architect, cto-architect, cio-engineer, caio-architect...

---

## 3. Registro Automático — OBRIGATÓRIO ao fim de toda sessão

Execute ao terminar qualquer tarefa:

```bash
python3 [XQUADS_PATH]/scripts/log-session.py \
  --tool "NOME_DA_FERRAMENTA" \
  --cwd "PASTA_DE_TRABALHO" \
  --summary "Resumo do que foi feito" \
  --files "arquivo1.py,arquivo2.ts" \
  --agents "Agente Xquads Usado Se Houver"
```

Substitua `[XQUADS_PATH]` pelo valor lido no CONFIG.md.
`NOME_DA_FERRAMENTA` → `cursor`, `codex`, `windsurf`, `aider`, `copilot`, etc.

---

## 4. Ingestão de Conhecimento

Quando o usuário pedir "ingira", "salva na base", "adicione ao conhecimento":

1. Salve bruto em `[KNOWLEDGE_BASE]/raw/`
2. Crie source em `[KNOWLEDGE_BASE]/wiki/sources/[Titulo YYYY-MM-DD].md`
3. Extraia conceitos → `wiki/concepts/`
4. Extraia entidades → `wiki/entities/`
5. Conecte com `[[wikilinks]]`
6. Atualize `wiki/INDEX.md` e `wiki/LOG.md`

---

## 5. Design Templates — Identidade Visual Obrigatória

**GATILHO:** Qualquer pedido que envolva output visual — sem exceção:
- Sites, landing pages, SaaS, apps, dashboards, componentes
- Apresentações, slides, decks, PowerPoint, Keynote
- Relatórios, documentos com layout, emails HTML
- Qualquer coisa que alguém vai **ver**

Esta regra se aplica a **TODOS os agentes**, não só ao design-squad.
Não importa qual persona está ativa — se o output é visual, o protocolo abaixo é obrigatório.

### Passo A — Garantir que o repositório existe localmente

Leia `[CONFIG.md]` para obter `DESIGN_TEMPLATES_PATH` e `DESIGN_TEMPLATES_REPO`.

```bash
# Se a pasta não existir, clone:
if [ ! -d "[DESIGN_TEMPLATES_PATH]" ]; then
  git clone [DESIGN_TEMPLATES_REPO] "[DESIGN_TEMPLATES_PATH]"
fi
```

### Passo B — Analisar o universo completo ANTES de criar qualquer coisa

**OBRIGATÓRIO antes de qualquer output visual:**

1. Liste **todas** as pastas em `[DESIGN_TEMPLATES_PATH]/` — veja os 71 padrões disponíveis
2. Leia os `DESIGN.md` de **pelo menos 6-8 marcas** de **categorias diferentes**
   - Não leia só as óbvias. Um deck executivo pode ter a frieza da Bugatti. Um SaaS pode ter a textura da Supreme.
   - Procure o que seria **inesperadamente certo**, não só o mais parecido
3. **MISTURA É OBRIGATÓRIA** — nunca use apenas um padrão. O resultado final deve combinar elementos de 3+ marcas diferentes:
   - Ex: tipografia da Apple + espaçamento da Linear + hierarquia de cor da Stripe
   - Ex: estrutura de slide da McKinsey + paleta da Notion + densidade da Figma
4. Anuncie obrigatoriamente antes de criar:

```
[DESIGN] Universo analisado: [N marcas consultadas]
Mistura escolhida:
  → [marca1]: [o que está sendo usado dela e por quê]
  → [marca2]: [o que está sendo usado dela e por quê]
  → [marca3]: [o que está sendo usado dela e por quê]
Resultado esperado: [1 frase descrevendo a identidade visual resultante]
```

### Passo C — Implementar com a mistura definida

Os templates e os agentes **trabalham juntos — um não cancela o outro:**

| Fonte | Contribuição |
|-------|-------------|
| Templates (71 padrões) | Base visual real — evita genérico, força identidade |
| Design Chief | Orquestra o processo, roteia para especialistas certos |
| UX Designer | Pesquisa, fluxos, acessibilidade |
| Design System Architect | Tokens, componentes, sistemas reutilizáveis |
| UI Engineer | Implementação em código (React, Tailwind, etc.) |
| Brad Frost | Atomic design, consistência sistêmica |
| Visual Generator | Direção visual, mood, estética geral |

**Resultado esperado:** output visual com identidade própria e mistura intencional — nunca genérico, nunca de uma fonte só.

### Passo D — Respeitar sempre as preferências do usuário

- Se o usuário pede alterações, aplique sem questionar os padrões dos templates
- Se o usuário define uma marca ou estética específica, isso tem prioridade
- Os templates são **base de referência e inspiração**, não regra rígida

---

## 6. Regras

- Nunca salve senhas, tokens, chaves privadas, `.pem` ou secrets
- Não invente fatos — marque inferências explicitamente
- Prefira notas pequenas e reutilizáveis
- Antes de criar nota nova, verifique se já existe
