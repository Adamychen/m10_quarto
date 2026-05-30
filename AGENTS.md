# AGENTS — Módulo 10: IA Generativa para Data Science

## Estructura del proyecto

```
m10_quarto/
├── _quarto.yml                  # Configuración del sitio Quarto
├── *.qmd                        # Páginas de teoría con engine jupyter (Python)
├── evaluables/                  # Ejercicios evaluables
│   ├── hpd1-evaluables.qmd      # HPD 1 — Ejercicios evaluables
│   └── hpd1-extension.qmd       # HPD 1 — Extensión avanzada
├── images/                      # Imágenes del sitio
│   ├── multi-head-attention.webp
│   ├── diagrama_transformer_original.webp
│   └── transformer-architecture.png
├── styles.css                   # Estilos CSS
├── requirements.txt             # Dependencias Python
├── generate_notebooks.sh        # Script para generar .ipynb desde .qmd
├── .github/workflows/
│   └── deploy.yml               # GitHub Actions → GitHub Pages
└── AGENTS.md                    # Este archivo
```

## Sidebar del sitio

| Sección | Páginas |
|---|---|
| **Inicio** | `index.qmd` (Presentación), `about.qmd` (Acerca de) |
| **Bloque 1 — Fundamentos** | `01-fundamentos.qmd`, `01a-transformer.qmd`, `01b-llms.qmd`, `01c-embeddings.qmd`, `01d-vectordb.qmd`, `hpd1-embeddings.qmd`, `evaluables/hpd1-evaluables.qmd`, `evaluables/hpd1-extension.qmd` |
| **Bloque 2 — Orquestación** | `02-orquestacion.qmd`, `hpd2-agente-tool-calling.qmd`, `hpd3-servidor-mcp.qmd` |
| **Bloque 3 — Aplicaciones** | `03-aplicaciones.qmd`, `bloque3/03b-rag-avanzado.qmd`, `bloque3/03a-datos-sinteticos.qmd`, `bloque3/03c-fine-tuning.qmd`, `hpd4-rag-mixto.qmd`, `evaluables/hpd4-datos-sinteticos.qmd`, `evaluables/hpd4-datos-sinteticos-extension.qmd` |
| **Bloque 4 — Gobernanza** | `04-gobernanza.qmd` |
| **Evaluación** | `05-evaluacion.qmd` |
| **Recursos** | `06-herramientas.qmd`, `07-bibliografia.qmd` |

## Requisitos

- Python 3.11+
- [Quarto](https://quarto.org/docs/get-started/) 1.6+

## Cómo renderizar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Renderizar sitio (usa QUARTO_PYTHON para usar el venv)
QUARTO_PYTHON=.venv/bin/python3 quarto render

# Ver en local
QUARTO_PYTHON=.venv/bin/python3 quarto preview
```

## Despliegue (CI/CD)

El repositorio usa GitHub Actions (`.github/workflows/deploy.yml`) que:
1. Instala Python y dependencias
2. Ejecuta `quarto render`
3. Publica en GitHub Pages

## Notas importantes

- Los `.qmd` usan `engine: jupyter` y contienen celdas Python ejecutables
- Las celdas con `#| eval: true` se ejecutan durante `quarto render`
- El grid del sitio está configurado en `_quarto.yml` (sidebar 260px, body 850px, margin 0px)
- Footer con créditos en todas las páginas
- Autoría: Adam Leiyi Chen Abolacio, Fernando Sancho Caparrini (Universidad de Sevilla)
