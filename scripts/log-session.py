#!/usr/bin/env python3
"""
log-session.py — Qualquer IA chama este script ao fim de uma sessão de trabalho.
Não precisa de transcript. A IA passa os dados diretamente via argumentos.

Uso:
  python3 log-session.py \
    --tool "cursor" \
    --cwd "/path/to/project" \
    --summary "O que foi feito nesta sessão" \
    --files "arquivo1.py,arquivo2.ts" \
    --agents "Hormozi Squad,Copy Chief"
"""
import argparse, sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _config import load_config

_cfg  = load_config()
KB    = _cfg['KNOWLEDGE_BASE']
WIKI  = KB / 'wiki'
SRC   = WIKI / 'sources'
INDEX = WIKI / 'INDEX.md'
LOG   = WIKI / 'LOG.md'

parser = argparse.ArgumentParser()
parser.add_argument('--tool',    default='ai',      help='Nome da IA (cursor, codex, windsurf...)')
parser.add_argument('--cwd',     default='',        help='Pasta de trabalho')
parser.add_argument('--summary', default='',        help='Resumo do que foi feito')
parser.add_argument('--files',   default='',        help='Arquivos modificados, separados por vírgula')
parser.add_argument('--agents',  default='',        help='Agentes Xquads usados, separados por vírgula')
args = parser.parse_args()

cwd          = args.cwd or str(Path.cwd())
project_name = Path(cwd).name
now          = datetime.now()
date_str     = now.strftime('%Y-%m-%d')
time_str     = now.strftime('%H:%M')
tool         = args.tool.lower()
files        = [f.strip() for f in args.files.split(',') if f.strip()]
agents       = [a.strip() for a in args.agents.split(',') if a.strip()]
summary      = args.summary.strip()

source_title = f"Sessao {tool.title()} {project_name} {date_str}"
source_file  = SRC / f"{source_title}.md"
is_update    = source_file.exists()

tags = ['source', f'{tool}-session', project_name.lower().replace(' ','-').replace('_','-')]
if agents:
    tags.append('xquads')

lines = [
    "---", "type: source", "status: ingested",
    f'title: "Sessão {tool.title()} — {project_name} — {date_str}"',
    f'captured_at: "{date_str}"',
    f'project_path: "{cwd}"',
    f'updated_at: "{time_str}"',
    f'tool: "{tool}"',
    "tags:",
] + [f"  - {t}" for t in tags] + [
    "---", "",
    f"# Sessão {tool.title()} — {project_name} — {date_str}",
    f"_Última atualização: {time_str}_", "",
    f"Ferramenta: **{tool}** | Pasta: `{cwd}`", "",
]

if summary:
    lines += ["## O que foi feito", "", summary, ""]

if agents:
    lines += ["## Agentes Xquads Ativados", ""]
    for a in agents:
        lines.append(f"- [[Xquads Squads]] → **{a}**")
    lines.append("")

if files:
    lines += ["## Arquivos Modificados", ""]
    for f in files:
        lines.append(f"- `{f}`")
    lines.append("")

source_file.write_text('\n'.join(lines), encoding='utf-8')

# Atualiza INDEX
wiki_name   = source_title
index_text  = INDEX.read_text(encoding='utf-8') if INDEX.exists() else ''
index_entry = f"- [[{wiki_name}]]"
if index_entry not in index_text and '## Sources' in index_text:
    index_text = index_text.replace('## Sources\n', f'## Sources\n{index_entry}\n', 1)
    INDEX.write_text(index_text, encoding='utf-8')

# Atualiza LOG
log_text    = LOG.read_text(encoding='utf-8') if LOG.exists() else '# Log\n'
date_header = f"## {date_str}"
if is_update:
    update_line = f"- [[{wiki_name}]] atualizada ({tool})."
    if update_line not in log_text and date_header in log_text:
        log_text = log_text.replace(date_header + '\n', date_header + '\n' + update_line + '\n', 1)
        LOG.write_text(log_text, encoding='utf-8')
else:
    entries = [f"- Sessão {tool} em `{project_name}` registrada como [[{wiki_name}]]."]
    if agents:
        entries.append(f"- Agentes Xquads: {', '.join(f'[[{a}]]' for a in agents)}.")
    if files:
        entries.append(f"- {len(files)} arquivo(s): {', '.join(f'`{f}`' for f in files[:5])}{'...' if len(files)>5 else ''}.")
    block = '\n'.join(entries)
    if date_header in log_text:
        log_text = log_text.replace(date_header + '\n', date_header + '\n' + block + '\n', 1)
    else:
        log_text = log_text.replace('# Log\n', f'# Log\n\n{date_header}\n{block}\n', 1)
    LOG.write_text(log_text, encoding='utf-8')

print(f"✓ Registrado: {source_title}")
