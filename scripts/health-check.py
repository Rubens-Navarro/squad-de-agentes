#!/usr/bin/env python3
"""
health-check.py — Verifica se todo o sistema Xquads está funcionando.
Execute: python3 /Users/rubens/obsidian/xquads-squads/scripts/health-check.py
"""
import sys, json, subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from _config import load_config

cfg = load_config()
ok  = True

def check(label, condition, fix=''):
    global ok
    status = '✓' if condition else '✗'
    if not condition:
        ok = False
        print(f"  {status} {label}")
        if fix:
            print(f"      → {fix}")
    else:
        print(f"  {status} {label}")

print("\n=== Xquads Health Check ===\n")

# ── Caminhos ────────────────────────────────────────────────────────────────
print("[ Caminhos ]")
check("XQUADS_PATH existe",           cfg['XQUADS_PATH'].exists())
check("KNOWLEDGE_BASE existe",        cfg['KNOWLEDGE_BASE'].exists(),
      f"mkdir -p '{cfg['KNOWLEDGE_BASE']}'")
check("DESIGN_TEMPLATES_PATH existe", cfg['DESIGN_TEMPLATES_PATH'].exists(),
      f"git clone {cfg['DESIGN_TEMPLATES_REPO']} '{cfg['DESIGN_TEMPLATES_PATH']}'")

# ── Base de Conhecimento ─────────────────────────────────────────────────────
print("\n[ Base de Conhecimento ]")
wiki = cfg['KNOWLEDGE_BASE'] / 'wiki'
check("wiki/ existe",                 wiki.exists())
check("wiki/sources/ existe",         (wiki / 'sources').exists())
check("wiki/INDEX.md existe",         (wiki / 'INDEX.md').exists())
check("wiki/LOG.md existe",           (wiki / 'LOG.md').exists())

# ── Design Templates ─────────────────────────────────────────────────────────
print("\n[ Design Templates ]")
dt = cfg['DESIGN_TEMPLATES_PATH']
if dt.exists():
    brands = [d.name for d in dt.iterdir() if d.is_dir() and not d.name.startswith('.')]
    check(f"{len(brands)} marcas disponíveis", len(brands) > 0)
    sample = [b for b in brands if (dt / b / 'DESIGN.md').exists()]
    check(f"{len(sample)} marcas com DESIGN.md", len(sample) > 0)
else:
    check("Repo clonado", False,
          f"git clone {cfg['DESIGN_TEMPLATES_REPO']} '{dt}'")

# ── Hooks ────────────────────────────────────────────────────────────────────
print("\n[ Hooks Claude Code ]")
settings = Path.home() / '.claude' / 'settings.json'
if settings.exists():
    try:
        s = json.loads(settings.read_text())
        hooks = s.get('hooks', {})
        has_stop = bool(hooks.get('Stop'))
        has_pre  = bool(hooks.get('PreToolUse'))
        check("Stop hook configurado (session-logger)", has_stop,
              "Adicione Stop hook em ~/.claude/settings.json")
        check("PreToolUse hook configurado (startup-check)", has_pre,
              "Adicione PreToolUse hook em ~/.claude/settings.json")
    except Exception as e:
        check("settings.json válido", False, f"Erro: {e}")
else:
    check("~/.claude/settings.json existe", False,
          "Crie ~/.claude/settings.json com os hooks")

# ── Scripts ──────────────────────────────────────────────────────────────────
print("\n[ Scripts ]")
scripts = cfg['XQUADS_PATH'] / 'scripts'
for s in ['startup-check.py', 'session-logger.py', 'log-session.py', '_config.py']:
    check(f"scripts/{s}", (scripts / s).exists())

# ── Session Logger — último registro ─────────────────────────────────────────
print("\n[ Último Registro de Sessão ]")
sources = wiki / 'sources'
if sources.exists():
    files = sorted(sources.glob('Sessao Claude *.md'), key=lambda f: f.stat().st_mtime, reverse=True)
    if files:
        last = files[0]
        mtime = datetime.fromtimestamp(last.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        check(f"Último: {last.name} ({mtime})", True)
    else:
        check("Nenhuma sessão registrada ainda", True)

# ── Error log ────────────────────────────────────────────────────────────────
err_log = Path.home() / '.claude' / 'xquads-logger-errors.log'
if err_log.exists() and err_log.stat().st_size > 0:
    lines = err_log.read_text().strip().splitlines()
    print(f"\n[ ⚠ Erros Recentes ({len(lines)} linhas em xquads-logger-errors.log) ]")
    for l in lines[-5:]:
        print(f"  {l}")

# ── Resultado ────────────────────────────────────────────────────────────────
print(f"\n{'✅ Sistema OK' if ok else '❌ Problemas encontrados — corrija os itens acima'}\n")
sys.exit(0 if ok else 1)
