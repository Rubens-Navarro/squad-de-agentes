# Tabela de Descrição — Xquads Squads

**353 arquivos | 13 squads | 150+ agentes especializados | Compatível com qualquer IA**

---

## O que foi criado além dos squads originais

| Arquivo | Função |
|---------|--------|
| `META-CHIEF.md` | Orquestrador mestre — ponto de entrada único. Roteia para o Chief certo com base na sua necessidade em linguagem natural. |
| `INDEX.md` | Mapa de navegação completo no Obsidian com links para todos os squads, Chiefs e atalhos por situação. |
| `tabela-de-descricao.md` | Este arquivo — resumo do sistema instalado. |

---

## Como usar com qualquer IA

**Via META-CHIEF** — Cole o conteúdo de `META-CHIEF.md` na conversa com qualquer IA (Claude, ChatGPT, Gemini, etc.) e descreva o que precisa. Ele roteia.

**Direto no Chief** — Se já sabe qual squad quer, abra o arquivo do Chief (ex: `hormozi-squad/agents/hormozi-chief.md`), cole no chat e a IA assume aquela persona.

---

## Os 13 Squads e Quando Usar

| Squad | Chief | Use quando... |
|-------|-------|--------------|
| `advisory-board` | Board Chair | Precisar de estratégia ou decisão difícil (Ray Dalio, Munger, Naval...) |
| `c-level-squad` | Vision Chief | Precisar de CEO/COO/CMO/CTO virtual |
| `hormozi-squad` | Hormozi Chief | Quiser criar oferta irresistível ou escalar negócio |
| `copy-squad` | Copy Chief | Precisar escrever copy que vende (emails, landing pages, VSL) |
| `copy-master` | Copy Master Chief | Copy de elite com 33 agentes — Gary Halbert, Eugene Schwartz... |
| `brand-squad` | Brand Chief | Quiser construir ou reformular uma marca |
| `traffic-masters` | Traffic Chief | Precisar de anúncios pagos (Meta, Google, YouTube, TikTok) |
| `storytelling` | Story Chief | Quiser criar pitch ou narrativa (Joseph Campbell, Oren Klaff...) |
| `data-squad` | Data Chief | Precisar de analytics, growth ou retenção |
| `design-squad` | Design Chief | Precisar de UX/UI ou design system |
| `movement` | Movement Chief | Quiser construir um movimento ou comunidade |
| `cybersecurity` | Cyber Chief | Precisar de segurança, pentest ou CTF |
| `claude-code-mastery` | Claude Mastery Chief | Precisar desenvolver com Claude/IA |

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

*Base instalada em: `/Users/rubens/obsidian/xquads-squads/`*
