#!/bin/bash
# generate_notebooks.sh
# Genera notebooks .ipynb para Colab desde los .qmd con engine: jupyter
# Descubrimiento automático: escanea bloque1/..4, evaluables/

set -e

echo "==> Generando notebooks para Colab..."
mkdir -p notebooks

grep -rl "engine: jupyter" \
  bloque1/ bloque2/ bloque3/ bloque4/ evaluables/ \
  --include="*.qmd" \
| sort \
| while read -r f; do
  name=$(basename "${f%.qmd}")
  echo "  → $name.ipynb ..."
  quarto render "$f" --to ipynb --output-dir notebooks/
done

echo ""
echo "✅ Notebooks generados en notebooks/:"
ls -lh notebooks/
echo ""
echo "==> No olvides commitear: git add notebooks/ && git commit -m 'Update notebooks' && git push"
echo ""
echo "==> No olvides commitear: git add notebooks/ && git commit -m 'Update notebooks' && git push"
