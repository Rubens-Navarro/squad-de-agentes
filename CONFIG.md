# Configuração — Xquads Squads

> **NOVO USUÁRIO:** Edite apenas os valores na seção "Caminhos Ativos" abaixo.

---

## Caminhos Ativos

<!-- O parser lê APENAS esta seção. Edite os valores para o seu sistema. -->

OBSIDIAN_ROOT=/Users/seunome/obsidian
KNOWLEDGE_BASE=/Users/seunome/obsidian/Base de Conhecimento
XQUADS_PATH=/Users/seunome/obsidian/squad-de-agentes
DESIGN_TEMPLATES_PATH=/Users/seunome/obsidian/design-system-templates
DESIGN_TEMPLATES_REPO=https://github.com/Rubens-Navarro/system-design-templates.git

<!-- FIM DOS CAMINHOS -->

---

## Como descobrir seus caminhos

**Mac:** Arraste a pasta do Obsidian no Terminal — o caminho aparece.
**Linux:** `echo ~/obsidian` ou `find ~ -name "*.md" -path "*/xquads-squads/*" -maxdepth 6 | head -1`
**Windows:** Clique direito na pasta → Propriedades → Localização.

---

## Para a IA

Leia os valores entre `<!-- O parser lê APENAS esta seção -->` e `<!-- FIM DOS CAMINHOS -->`.
Use KNOWLEDGE_BASE e XQUADS_PATH como base para todos os outros caminhos.
