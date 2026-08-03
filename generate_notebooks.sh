#!/bin/bash
# generate_notebooks.sh
# Genera notebooks .ipynb para Colab desde los .qmd con engine: jupyter
# Descubrimiento automático: escanea bloque1/..4, evaluables/

set -euo pipefail

cleanup_quarto_intermediates() {
  local source_path="$1"
  local base="${source_path%.qmd}.quarto_ipynb"

  # Quarto appends _1, _2, ... when an intermediate file already exists.
  rm -f "$base" "${base}"_*
}

echo "==> Generando notebooks para Colab..."
mkdir -p notebooks

grep -rl "engine: jupyter" \
  bloque1/ bloque2/ bloque3/ bloque4/ evaluables/ \
  --include="*.qmd" \
| sort \
| while read -r f; do
  name=$(basename "${f%.qmd}")
  cleanup_quarto_intermediates "$f"
  echo "  → $name.ipynb ..."
  if ! quarto render "$f" --to ipynb --output-dir notebooks/; then
    cleanup_quarto_intermediates "$f"
    exit 1
  fi
  cleanup_quarto_intermediates "$f"
done

echo ""
echo "✅ Notebooks generados en notebooks/:"
ls -lh notebooks/
echo ""
echo "==> No olvides commitear: git add notebooks/ && git commit -m 'Update notebooks' && git push"
echo ""
echo "==> No olvides commitear: git add notebooks/ && git commit -m 'Update notebooks' && git push"
