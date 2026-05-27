#!/bin/bash
# generate_notebooks.sh
# Genera notebooks .ipynb para Colab desde los .qmd
# Ejecutar tras modificar cualquier .qmd que tenga badge Colab

set -e

FILES=(
  01-fundamentos.qmd
  01a-transformer.qmd
  01b-llms.qmd
  01c-embeddings.qmd
  01d-vectordb.qmd
  hpd1-embeddings.qmd
  hpd2-agente-tool-calling.qmd
  hpd3-servidor-mcp.qmd
  hpd4-rag-mixto.qmd
)

echo "==> Generando notebooks para Colab..."
mkdir -p notebooks

for f in "${FILES[@]}"; do
  name=$(basename "${f%.qmd}")
  echo "  → $name.ipynb ..."
  quarto render "$f" --to ipynb --output-dir notebooks/
done

echo ""
echo "✅ Notebooks generados en notebooks/:"
ls -lh notebooks/
echo ""
echo "==> No olvides commitear: git add notebooks/ && git commit -m 'Update notebooks' && git push"
