#!/usr/bin/env python3
"""
Knowledge Base Logger — ingere sessões do Claude Code na base de conhecimento real.
Segue o padrão: source em wiki/sources/, atualiza wiki/INDEX.md e wiki/LOG.md.
Hook: Stop do Claude Code.
"""
import json, sys, os, re, traceback
from datetime import datetime
from pathlib import Path

_ERROR_LOG = Path.home() / '.claude' / 'xquads-logger-errors.log'

def _log_error(msg):
    """Grava erros em arquivo — nunca falha silenciosamente."""
    try:
        with open(_ERROR_LOG, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass  # se nem isso funcionar, não há o que fazer

try:
    sys.path.insert(0, str(Path(__file__).parent))
    from _config import load_config
    _cfg = load_config()
except Exception as e:
    _log_error(f"Falha ao carregar _config: {e}\n{traceback.format_exc()}")
    sys.exit(0)

KB    = _cfg['KNOWLEDGE_BASE']
WIKI  = KB / 'wiki'
SRC   = WIKI / 'sources'
INDEX = WIKI / 'INDEX.md'
LOG   = WIKI / 'LOG.md'

# Garante estrutura mínima — nunca falha se KB não existir
for _d in [SRC, WIKI / 'concepts', WIKI / 'entities']:
    try:
        _d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

CHIEF_LABELS = {
    'board-chair': 'Advisory Board', 'vision-chief': 'C-Level Squad',
    'brand-chief': 'Brand Squad', 'copy-chief': 'Copy Squad',
    'copy-master-chief': 'Copy Master', 'hormozi-chief': 'Hormozi Squad',
    'traffic-chief': 'Traffic Masters', 'story-chief': 'Storytelling',
    'data-chief': 'Data Squad', 'design-chief': 'Design Squad',
    'cyber-chief': 'Cybersecurity', 'movement-chief': 'Movement',
    'claude-mastery-chief': 'Claude Code Mastery', 'meta-chief': 'META-CHIEF',
}

# ── Lê contexto do hook ──────────────────────────────────────────────────────
try:
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
except Exception as e:
    _log_error(f"Falha ao ler stdin: {e} | raw={repr(raw[:200]) if 'raw' in dir() else 'N/A'}")
    sys.exit(0)

transcript_path = data.get('transcript_path', '')
cwd             = data.get('cwd', os.getcwd())
project_name    = Path(cwd).name

# ── Parse do transcript ──────────────────────────────────────────────────────
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

            # Formato real: type no topo, conteúdo em message.content
            role = turn.get('type', '')
            msg  = turn.get('message', {})
            if not isinstance(msg, dict):
                continue
            content = msg.get('content', [])

            # content pode ser string simples
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

                # Texto do usuário
                if role == 'user' and block.get('type') == 'text':
                    txt = block['text'].strip()
                    if txt and len(txt) > 5:
                        user_messages.append(txt[:400])
                    for kw, label in CHIEF_LABELS.items():
                        if kw in txt.lower() and label not in agents_used:
                            agents_used.append(label)

                # Primeiro parágrafo útil do assistente
                if role == 'assistant' and block.get('type') == 'text' and not assistant_first:
                    t = block.get('text', '').strip()
                    if len(t) > 30 and not t.startswith('```'):
                        assistant_first = t[:600]

                # Tool use
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

# Sem conteúdo relevante → não registra
all_changed = files_created + files_modified
if not user_messages and not all_changed:
    sys.exit(0)

# ── Prepara metadados ────────────────────────────────────────────────────────
now      = datetime.now()
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H:%M')

first_request = user_messages[0] if user_messages else 'Sessão Claude'
# Título limpo para nome de arquivo (sem acentos problemáticos)
def slugify(s):
    s = re.sub(r'[^\w\s\-]', '', s)
    return ' '.join(s.split())[:50]

title_slug   = slugify(first_request)
source_title = f"Sessao Claude {project_name} {date_str}"
source_file  = SRC / f"{source_title}.md"
is_update    = source_file.exists()   # já existe nota do dia → atualiza, não duplica

# Tags
tags = ['source', 'claude-session', project_name.lower().replace(' ', '-').replace('_', '-')]
if agents_used:
    tags.append('xquads')

# ── Monta a source note (sempre reescreve com dados completos do transcript) ─
meaningful_cmds = [
    c for c in bash_commands
    if not any(s in c for s in ['ls ', 'echo ', 'cat ', 'pwd', 'which ', 'head ', 'tail '])
]

lines = [
    "---",
    "type: source",
    "status: ingested",
    f'title: "Sessão Claude — {project_name} — {date_str}"',
    f'captured_at: "{date_str}"',
    f'project_path: "{cwd}"',
    f'updated_at: "{time_str}"',
    "tags:",
] + [f"  - {t}" for t in tags] + [
    "---",
    "",
    f"# Sessão Claude — {project_name} — {date_str}",
    f"_Última atualização: {time_str}_",
    "",
    f"Sessão de trabalho em `{cwd}`.",
    "",
]

if user_messages:
    lines += ["## O que foi pedido", ""]
    for msg in user_messages[:5]:
        lines.append(f"> {msg}")
        lines.append(">")
    lines.append("")

if agents_used:
    lines += ["## Agentes Xquads Ativados", ""]
    for a in agents_used:
        lines.append(f"- [[Squad de Agentes]] → **{a}**")
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

# Reescreve o arquivo (atualiza se já existia, cria se é novo)
try:
    SRC.mkdir(parents=True, exist_ok=True)
    source_file.write_text('\n'.join(lines), encoding='utf-8')
except Exception as e:
    _log_error(f"Falha ao escrever source note {source_file}: {e}\n{traceback.format_exc()}")
    sys.exit(0)

# ── Atualiza INDEX.md (só insere se ainda não existe o link) ─────────────────
try:
    wiki_name   = source_title
    index_text  = INDEX.read_text(encoding='utf-8') if INDEX.exists() else '# Index\n\n## Sources\n\n## Concepts\n\n## Entities\n\n## Topics\n\n## Queries\n'
    index_entry = f"- [[{wiki_name}]]"

    if index_entry not in index_text and '## Sources' in index_text:
        index_text = index_text.replace('## Sources\n', f'## Sources\n{index_entry}\n', 1)
        INDEX.write_text(index_text, encoding='utf-8')
except Exception as e:
    _log_error(f"Falha ao atualizar INDEX.md: {e}")

# ── Atualiza LOG.md ──────────────────────────────────────────────────────────
try:
    log_text    = LOG.read_text(encoding='utf-8') if LOG.exists() else '# Log\n'
    date_header = f"## {date_str}"

    if is_update:
        if all_changed and wiki_name in log_text:
            n       = len(all_changed)
            nomes   = ', '.join(f'`{Path(f).name}`' for f in all_changed[:5])
            suffix  = '...' if n > 5 else ''
            update_line = f"- Sessao [[{wiki_name}]] atualizada: {n} arquivo(s) — {nomes}{suffix}."
            if update_line not in log_text:
                log_text = log_text.replace(
                    date_header + '\n',
                    date_header + '\n' + update_line + '\n',
                    1
                )
                LOG.write_text(log_text, encoding='utf-8')
    else:
        log_entries = [f"- Ingerida sessão Claude em `{project_name}` como [[{wiki_name}]]."]
        if agents_used:
            log_entries.append(f"- Agentes Xquads: {', '.join(f'[[{a}]]' for a in agents_used)}.")
        if all_changed:
            n     = len(all_changed)
            nomes = ', '.join(f'`{Path(f).name}`' for f in all_changed[:5])
            log_entries.append(f"- {n} arquivo(s): {nomes}{'...' if n > 5 else ''}.")
        log_block = '\n'.join(log_entries)
        if date_header in log_text:
            log_text = log_text.replace(date_header + '\n', date_header + '\n' + log_block + '\n', 1)
        else:
            log_text = log_text.replace('# Log\n', f'# Log\n\n{date_header}\n{log_block}\n', 1)
        LOG.write_text(log_text, encoding='utf-8')
except Exception as e:
    _log_error(f"Falha ao atualizar LOG.md: {e}\n{traceback.format_exc()}")

# ── Garante entidade Squad de Agentes se ainda não existe ──────────────────────
try:
    if agents_used:
        entity_path = WIKI / 'entities' / 'Squad de Agentes.md'
        if not entity_path.exists() and (WIKI / 'entities').exists():
            entity_path.write_text(
                "---\ntype: entity\n---\n\n# Squad de Agentes\n\n"
                "Sistema de 13 squads com 150+ agentes IA especializados.\n"
                f"Instalado em `{_cfg['XQUADS_PATH']}`.\n"
                "Ponto de entrada: [[META-CHIEF]].\n",
                encoding='utf-8'
            )
except Exception as e:
    _log_error(f"Falha ao criar entidade Squad de Agentes: {e}")
