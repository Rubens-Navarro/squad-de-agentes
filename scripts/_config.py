"""
_config.py — Lê CONFIG.md e retorna os caminhos do sistema.
Importado por session-logger.py e log-session.py.
"""
import re, os
from pathlib import Path

def load_config():
    """
    Localiza CONFIG.md subindo a partir deste arquivo (scripts/ → xquads-squads/)
    e retorna um dict com OBSIDIAN_ROOT, KNOWLEDGE_BASE, XQUADS_PATH.
    Fallback: tenta ~/obsidian se CONFIG.md não for encontrado.
    """
    # Sobe de scripts/ para xquads-squads/
    config_file = Path(__file__).parent.parent / 'CONFIG.md'

    cfg = {}
    if config_file.exists():
        text = config_file.read_text(encoding='utf-8')
        # Lê apenas entre os marcadores de seção ativa
        in_active = False
        for line in text.splitlines():
            if 'O parser lê APENAS esta seção' in line:
                in_active = True
                continue
            if 'FIM DOS CAMINHOS' in line:
                break
            if in_active:
                m = re.match(r'^([A-Z_]+)=(.+)$', line.strip())
                if m:
                    cfg[m.group(1)] = m.group(2).strip()

    # Fallbacks razoáveis se CONFIG.md não tiver os valores
    home = Path.home()
    xquads = Path(__file__).parent.parent

    cfg.setdefault('XQUADS_PATH',            str(xquads))
    cfg.setdefault('OBSIDIAN_ROOT',          str(xquads.parent))
    cfg.setdefault('KNOWLEDGE_BASE',         str(xquads.parent / 'tudo' / 'Base de Conhecimento'))
    cfg.setdefault('DESIGN_TEMPLATES_PATH',  str(xquads.parent / 'design-system-templates'))
    cfg.setdefault('DESIGN_TEMPLATES_REPO',  'https://github.com/Rubens-Navarro/system-design-templates.git')

    # DESIGN_TEMPLATES_REPO é string pura — não converte para Path
    repo = cfg.pop('DESIGN_TEMPLATES_REPO')
    result = {k: Path(v) for k, v in cfg.items()}
    result['DESIGN_TEMPLATES_REPO'] = repo
    return result
