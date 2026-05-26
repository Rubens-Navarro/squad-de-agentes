#!/usr/bin/env python3
"""
morph-reminder.py — Hook PreToolUse leve.
Reinjeta o protocolo de transformação a cada N tool uses.
Sem IO pesado — só o lembrete. Roda em < 5ms.
"""
import os
import sys
from pathlib import Path

# Injeta a cada 8 tool uses — frequente o suficiente pra manter vivo,
# espaçado o suficiente pra não poluir o contexto
N = 8

session_id = os.environ.get('CLAUDE_SESSION_ID', '') or str(os.getppid())
counter_file = Path(f'/tmp/.xquads-morph-{session_id[:32]}')

try:
    count = int(counter_file.read_text().strip()) if counter_file.exists() else 0
except Exception:
    count = 0

count += 1
try:
    counter_file.write_text(str(count))
except Exception:
    pass

if count % N != 0:
    sys.exit(0)

print(
    "━━━ PROTOCOLO DE TRANSFORMAÇÃO — LEMBRETE ━━━\n"
    "A cada nova solicitação que mude de domínio ou tipo de tarefa:\n"
    "OBRIGATÓRIO: vire META-CHIEF → identifique squad → vire Chief → vire Agente → execute.\n"
    "NÃO continue como o agente anterior só porque foi usado antes.\n"
    "Cada nova tarefa = nova análise = nova transformação completa.\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
)
