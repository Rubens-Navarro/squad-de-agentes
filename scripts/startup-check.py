#!/usr/bin/env python3
"""
startup-check.py — Hook PreToolUse do Claude Code.
Roda uma vez por sessão. Garante estrutura, atualiza repos automaticamente (1x/dia)
e injeta a lista de marcas no contexto da IA.
"""
import os, sys, subprocess
from pathlib import Path
from datetime import date

# ── Flag de sessão: roda apenas uma vez por processo Claude ──────────────────
session_id = os.environ.get('CLAUDE_SESSION_ID', '') or str(os.getppid())
flag = Path(f'/tmp/.xquads-startup-{session_id[:32]}')
if flag.exists():
    sys.exit(0)
flag.touch()

# ── Carrega config ────────────────────────────────────────────────────────────
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from _config import load_config
    cfg = load_config()
except Exception as e:
    print(f"[XQUADS STARTUP] ERRO ao carregar config: {e}", file=sys.stderr)
    sys.exit(0)

errors  = []
updates = []
today   = str(date.today())


def git_pull(path, label):
    """Faz git pull silencioso. Retorna True se havia novidades."""
    try:
        r = subprocess.run(
            ['git', '-C', str(path), 'pull', '--ff-only', '--quiet'],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0 and 'Already up to date' not in r.stdout + r.stderr:
            updates.append(f"{label} atualizado")
            return True
    except Exception as e:
        errors.append(f"git pull {label}: {e}")
    return False


def should_update_today(marker_file):
    """Retorna True se ainda não atualizou hoje."""
    if not marker_file.exists():
        return True
    return marker_file.read_text().strip() != today


def mark_updated(marker_file):
    marker_file.write_text(today)


# ── 1. Garante KB estrutura ───────────────────────────────────────────────────
kb = cfg['KNOWLEDGE_BASE']
for d in [
    kb / 'wiki' / 'sources', kb / 'wiki' / 'concepts',
    kb / 'wiki' / 'entities', kb / 'wiki' / 'queries',
    kb / 'wiki' / 'topics',   kb / 'raw' / 'youtube',
    kb / 'raw' / 'papers',    kb / 'raw' / 'web',
    kb / 'scripts',            kb / 'templates', kb / 'prompts',
]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        errors.append(f"mkdir {d.name}: {e}")

for fpath, content in [
    (kb / 'wiki' / 'INDEX.md',
     "# Index\n\n## Sources\n\n## Concepts\n\n## Entities\n\n## Topics\n\n## Queries\n\n_Nenhuma query registrada ainda._\n"),
    (kb / 'wiki' / 'LOG.md', "# Log\n"),
]:
    if not fpath.exists():
        try:
            fpath.write_text(content, encoding='utf-8')
        except Exception as e:
            errors.append(f"Criar {fpath.name}: {e}")

# ── 2. Xquads Squads — auto-update 1x por dia ────────────────────────────────
xquads       = cfg['XQUADS_PATH']
xquads_flag  = Path(f'/tmp/.xquads-pull-xquads-{today}')
if xquads.exists() and should_update_today(xquads_flag):
    git_pull(xquads, 'xquads-squads')
    mark_updated(xquads_flag)

# ── 3. Design Templates — clone se não existe, pull 1x por dia ───────────────
templates    = cfg['DESIGN_TEMPLATES_PATH']
repo         = str(cfg['DESIGN_TEMPLATES_REPO'])
dt_flag      = Path(f'/tmp/.xquads-pull-design-{today}')
cloned       = False

if not templates.exists():
    try:
        r = subprocess.run(
            ['git', 'clone', repo, str(templates)],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0:
            cloned = True
            mark_updated(dt_flag)
        else:
            errors.append(f"git clone design templates: {r.stderr.strip()[:200]}")
    except Exception as e:
        errors.append(f"git clone design templates: {e}")
elif should_update_today(dt_flag):
    git_pull(templates, 'design-system-templates')
    mark_updated(dt_flag)

# ── 4. Lê INDEX.md da base de conhecimento ───────────────────────────────────
index_content = ''
index_path = kb / 'wiki' / 'INDEX.md'
try:
    if index_path.exists():
        raw = index_path.read_text(encoding='utf-8').strip()
        # Verifica se tem conteúdo real além dos cabeçalhos vazios
        non_empty_lines = [l for l in raw.splitlines()
                           if l.strip() and not l.strip().startswith('#')
                           and l.strip() != '_Nenhuma query registrada ainda._']
        if non_empty_lines:
            index_content = raw
except Exception as e:
    errors.append(f"Leitura do INDEX.md: {e}")

# ── 5. Lista marcas disponíveis → injeta no contexto ─────────────────────────
brands = []
if templates.exists():
    try:
        brands = sorted([
            d.name for d in templates.iterdir()
            if d.is_dir() and not d.name.startswith('.') and (d / 'DESIGN.md').exists()
        ])
    except Exception:
        pass

# ── 6. Saída para o contexto da IA ───────────────────────────────────────────
lines = []

if errors:
    lines.append(f"[XQUADS] AVISOS: {' | '.join(errors)}")

if updates:
    lines.append(f"[XQUADS] Atualizado hoje: {', '.join(updates)}")

# Injeta a base de conhecimento — SEMPRE, antes de qualquer coisa
if index_content:
    lines.append(
        f"━━━ BASE DE CONHECIMENTO DO USUÁRIO ━━━\n"
        f"INSTRUÇÃO OBRIGATÓRIA: Antes de construir, modificar ou criar qualquer coisa,\n"
        f"consulte este índice. Use o que já existe para manter continuidade, autenticidade\n"
        f"e coerência com a história e a alma do trabalho do usuário.\n"
        f"Abra as notas relevantes ao pedido antes de agir.\n\n"
        f"{index_content}\n"
        f"━━━ FIM DO ÍNDICE ━━━"
    )
else:
    lines.append(
        f"[BASE DE CONHECIMENTO] Ainda vazia em {index_path}. "
        f"À medida que o usuário trabalhar, ela será preenchida automaticamente."
    )

if brands:
    status = "Clonado agora" if cloned else "Disponível"
    lines.append(
        f"\n[DESIGN TEMPLATES {status} — {len(brands)} marcas]\n"
        f"{', '.join(brands)}\n"
        f"Para qualquer trabalho de frontend/layout/UI: leia DESIGN.md das marcas mais\n"
        f"inspiradoras (explore livremente — qualquer categoria). Combine com os agentes do design-squad."
    )

if lines:
    print('\n'.join(lines))
