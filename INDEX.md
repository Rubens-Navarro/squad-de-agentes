# Xquads Squads — Índice de Navegação

**13 squads | 150+ agentes especializados | Compatível com qualquer IA**

---

## Ponto de Entrada

- [[META-CHIEF]] — **Comece aqui.** Orquestrador mestre que roteia para o squad certo.

---

## Os 13 Squads

### Estratégia & Liderança

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[advisory-board/README\|Advisory Board]] | [[advisory-board/agents/board-chair\|Board Chair]] | 11 | Decisões difíceis, estratégia, mentoria com Ray Dalio, Munger, Naval... |
| [[c-level-squad/README\|C-Level Squad]] | [[c-level-squad/agents/vision-chief\|Vision Chief]] | 6 | Estratégia executiva, CEO/COO/CMO/CTO/CIO/CAIO |

### Negócios & Crescimento

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[hormozi-squad/README\|Hormozi Squad]] | [[hormozi-squad/agents/hormozi-chief\|Hormozi Chief]] | 16 | Ofertas, vendas, precificação, escala (framework Hormozi) |
| [[data-squad/README\|Data Squad]] | [[data-squad/agents/data-chief\|Data Chief]] | 7 | Analytics, growth, retenção, comunidade, Sean Ellis, Avinash... |

### Marca & Comunicação

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[brand-squad/README\|Brand Squad]] | [[brand-squad/agents/brand-chief\|Brand Chief]] | 15 | Branding, posicionamento, naming, identidade, arquétipos |
| [[storytelling/README\|Storytelling]] | [[storytelling/agents/story-chief\|Story Chief]] | 12 | Pitch, narrativa, apresentações, roteiro, Joseph Campbell, Oren Klaff... |
| [[movement/README\|Movement]] | [[movement/agents/movement-chief\|Movement Chief]] | 7 | Construção de movimento, manifesto, comunidade, identidade coletiva |

### Copy & Conversão

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[copy-squad/README\|Copy Squad]] | [[copy-squad/agents/copy-chief\|Copy Chief]] | 23 | Copy rápido: emails, landing pages, funis, headlines, VSL |
| [[copy-master/README\|Copy Master]] | [[copy-master/agents/copy-master-chief\|Copy Master Chief]] | 33 | Copy de elite: campanhas completas, Gary Halbert, Eugene Schwartz... |

### Tráfego & Design

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[traffic-masters/README\|Traffic Masters]] | [[traffic-masters/agents/traffic-chief\|Traffic Chief]] | 16 | Meta Ads, Google Ads, YouTube, TikTok, Pedro Sobral, Kasim Aslam... |
| [[design-squad/README\|Design Squad]] | [[design-squad/agents/design-chief\|Design Chief]] | 8 | UX/UI, design systems, componentes, Brad Frost, Dan Mall... |

### Tecnologia & Segurança

| Squad | Chief | Agentes | Quando usar |
|-------|-------|---------|-------------|
| [[claude-code-mastery/README\|Claude Code Mastery]] | [[claude-code-mastery/agents/claude-mastery-chief\|Claude Mastery Chief]] | 8 | Claude Code, desenvolvimento com IA, AIOS, automação |
| [[cybersecurity/README\|Cybersecurity]] | [[cybersecurity/agents/cyber-chief\|Cyber Chief]] | 15 | Pentest, segurança defensiva, CTF, OWASP, red team |

---

## Atalhos por Situação

| Situação | Squad | Arquivo do Chief |
|----------|-------|-----------------|
| Não sei por onde começar | Advisory Board | `advisory-board/agents/board-chair.md` |
| Quero construir uma marca forte | Brand Squad | `brand-squad/agents/brand-chief.md` |
| Preciso definir a estratégia da empresa | C-Level Squad | `c-level-squad/agents/vision-chief.md` |
| Quero escrever copy que vende | Copy Squad | `copy-squad/agents/copy-chief.md` |
| Quero copy de nível elite | Copy Master | `copy-master/agents/copy-master-chief.md` |
| Preciso de segurança ou pentest | Cybersecurity | `cybersecurity/agents/cyber-chief.md` |
| Quero entender meus dados e crescer | Data Squad | `data-squad/agents/data-chief.md` |
| Preciso de design e UX | Design Squad | `design-squad/agents/design-chief.md` |
| Quero criar oferta irresistível e escalar | Hormozi Squad | `hormozi-squad/agents/hormozi-chief.md` |
| Quero construir um movimento | Movement | `movement/agents/movement-chief.md` |
| Preciso contar uma história que prende | Storytelling | `storytelling/agents/story-chief.md` |
| Quero rodar anúncios pagos | Traffic Masters | `traffic-masters/agents/traffic-chief.md` |
| Desenvolvimento com Claude/AIOS | Claude Code Mastery | `claude-code-mastery/agents/claude-mastery-chief.md` |

---

## Estrutura de Cada Squad

```
squad-name/
├── squad.yaml          → Manifesto (agentes, tasks, workflows)
├── agents/             → Definições dos agentes (persona, role, frameworks)
├── tasks/              → Tasks executáveis com inputs/outputs definidos
├── workflows/          → Workflows multi-agente automatizados
├── checklists/         → Checklists de qualidade
├── config/             → Configurações
└── data/               → Frameworks e catálogos de referência
```

---

## Como Usar com Qualquer IA

```
1. Abra o arquivo do agente/chief desejado neste Obsidian
2. Copie o conteúdo completo do arquivo .md
3. Cole no início da sua conversa com a IA (Claude, ChatGPT, Gemini, etc.)
4. Diga: "Aja como este agente e me ajude com: [sua tarefa]"

OU simplesmente:
1. Cole o conteúdo do META-CHIEF.md
2. Descreva sua necessidade em linguagem natural
3. O META-CHIEF roteia para o squad e chief corretos
```

---

## Base de Conhecimento Automática

Toda sessão do Claude Code é registrada automaticamente em:

- **[[../conhecimento-claude/_INDEX|Índice da Base de Conhecimento]]** — lista de todas as sessões
- **`/Users/rubens/obsidian/conhecimento-claude/`** — notas organizadas por projeto

Cada nota registra:
- O que foi pedido (pedido do usuário)
- Quais agentes Xquads foram ativados
- Arquivos criados e modificados
- Comandos executados
- Resumo do que foi feito

O registro acontece automaticamente ao final de toda sessão, em qualquer pasta de trabalho.

Script: `xquads-squads/scripts/session-logger.py`

---

*Base instalada em: `/Users/rubens/obsidian/xquads-squads/`*
