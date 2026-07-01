#!/usr/bin/env python3
"""
scripts/sync_setup_keys.py
Pre-render: reemplaza el marcador {{ SETUP_KEYS }} en todos los .qmd/.md
por el contenido de includes/setup_keys.py.

Idempotente: solo procesa archivos que aún contienen el marcador.
Si el archivo ya fue inyectado previamente, se omite.

Uso:
  python3 scripts/sync_setup_keys.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETUP_FILE = ROOT / "includes" / "setup_keys.py"
MARKER = "{{ SETUP_KEYS }}"

if not SETUP_FILE.exists():
    print(f"ERROR: no se encuentra {SETUP_FILE}", file=sys.stderr)
    sys.exit(1)

setup_content = SETUP_FILE.read_text()

count = 0
for ext in ("*.qmd", "*.md"):
    for f in ROOT.rglob(ext):
        # Excluir directorios de control
        if any(part in f.parts for part in (".venv", "node_modules", "_site", "site_libs", "notebooks")):
            continue
        try:
            content = f.read_text()
        except Exception:
            continue
        if MARKER in content:
            new_content = content.replace(MARKER, setup_content)
            f.write_text(new_content)
            count += 1
            print(f"  ✓ {f.relative_to(ROOT)}")

if count == 0:
    print("  (sin marcadores que sincronizar)")
else:
    print(f"  {count} archivo(s) sincronizado(s).")
