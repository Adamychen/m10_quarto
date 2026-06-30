# AGENTS — Módulo 10: IA Generativa para Data Science

## Estructura del proyecto

```
m10_quarto/
├── _quarto.yml                  # Configuración del sitio (sidebar, grid, tema)
├── index.qmd                    # Presentación
├── about.qmd                    # Acerca de
├── mod10.md                     # Guía docente pública del módulo
├── bloque1/                     # Fundamentos: Transformers, LLMs, embeddings, vector DB
│   ├── 01-fundamentos.qmd       # Índice del bloque
│   ├── 01a-transformer.qmd      # Arquitectura Transformer
│   ├── 01b-llms.qmd             # LLMs e inferencia
│   ├── 01c-embeddings.qmd       # Modelos de embeddings
│   └── 01d-vectordb.qmd         # Bases de datos vectoriales
├── bloque2/                     # Orquestación: prompt, frameworks, MCP, agentes
│   ├── 02-orquestacion.qmd      # Índice del bloque
│   ├── 02a-prompt-engineering.qmd
│   ├── 02b-langchain.qmd
│   ├── 02c-llamaindex.qmd
│   ├── 02d-mcp.qmd
│   ├── 02e-agentes.qmd
│   ├── hpd2-agente-tool-calling.qmd   # HPD 2
│   └── hpd3-servidor-mcp.qmd         # HPD 3
├── bloque3/                     # Aplicaciones: RAG, datos sintéticos, fine-tuning
│   ├── 03-aplicaciones.qmd      # Índice del bloque
│   ├── 03a-datos-sinteticos.qmd
│   ├── 03b-rag-avanzado.qmd
│   └── 03c-fine-tuning.qmd
├── bloque4/                     # Despliegue y gobernanza (CE-6)
│   └── 04-gobernanza.qmd
├── evaluables/                  # Ejercicios evaluables (10 ficheros)
│   ├── hpd1-embeddings.qmd           # Taller presencial HPD 1
│   ├── hpd1-evaluables.qmd          # HPD 1 — entrega
│   ├── hpd1-extension.qmd           # HPD 1 — extensión avanzada
│   ├── hpd2-evaluables.qmd          # HPD 2 — entrega
│   ├── hpd2-extension.qmd           # HPD 2 — extensión avanzada
│   ├── hpd3-evaluables.qmd          # HPD 3 — entrega
│   ├── hpd3-extension.qmd           # HPD 3 — extensión avanzada
│   ├── hpd4-rag-mixto.qmd           # HPD 4 — RAG mixto
│   ├── hpd4-datos-sinteticos.qmd    # HPD 4 — datos sintéticos
│   └── hpd4-datos-sinteticos-extension.qmd
├── 05-evaluacion.qmd            # Evaluación y proyecto integrador
├── 06-herramientas.qmd          # Herramientas y stack recomendado
├── 07-bibliografia.qmd          # Bibliografía y recursos
├── images/                      # Imágenes del sitio
│   ├── diagrama_transformer_original.webp
│   ├── logo_cfp.png
│   ├── multi-head-attention.webp
│   └── sbert_figure_2.png
├── includes/footer.html         # Pie de página
├── styles.css                   # Estilos CSS personalizados
├── requirements.txt             # Dependencias Python fijadas
├── generate_notebooks.sh        # Genera .ipynb desde .qmd
└── AGENTS.md                    # Este archivo
```

## Sidebar del sitio

| Sección | Páginas |
|---|---|
| **Inicio** | `index.qmd` (Presentación), `about.qmd` (Acerca de), `mod10.md` (Guía docente) |
| **Bloque 1 — Fundamentos** | `bloque1/01-fundamentos.qmd`, `01a-transformer.qmd`, `01b-llms.qmd`, `01c-embeddings.qmd`, `01d-vectordb.qmd`, `evaluables/hpd1-embeddings.qmd`, `evaluables/hpd1-evaluables.qmd`, `evaluables/hpd1-extension.qmd` |
| **Bloque 2 — Orquestación** | `bloque2/02-orquestacion.qmd`, `02a-prompt-engineering.qmd`, `02b-langchain.qmd`, `02c-llamaindex.qmd`, `02d-mcp.qmd`, `02e-agentes.qmd`, `hpd2-agente-tool-calling.qmd`, `evaluables/hpd2-evaluables.qmd`, `evaluables/hpd2-extension.qmd`, `hpd3-servidor-mcp.qmd`, `evaluables/hpd3-evaluables.qmd`, `evaluables/hpd3-extension.qmd` |
| **Bloque 3 — Aplicaciones** | `bloque3/03-aplicaciones.qmd`, `03b-rag-avanzado.qmd`, `03a-datos-sinteticos.qmd`, `03c-fine-tuning.qmd`, `evaluables/hpd4-rag-mixto.qmd`, `evaluables/hpd4-datos-sinteticos.qmd`, `evaluables/hpd4-datos-sinteticos-extension.qmd` |
| **Bloque 4 — Gobernanza** | `bloque4/04-gobernanza.qmd` |
| **Evaluación** | `05-evaluacion.qmd` |
| **Recursos** | `06-herramientas.qmd`, `07-bibliografia.qmd` |

> La fuente de verdad del sidebar es `_quarto.yml` (líneas 12-99). Si este fichero y `_quarto.yml` divergen, prioriza `_quarto.yml`.

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

## Generar notebooks para Colab

Los `.ipynb` que se enlazan desde los badges "Open in Colab" se generan desde los `.qmd` con `engine: jupyter`:

```bash
./generate_notebooks.sh
```

Esto descubre automáticamente todos los `.qmd` con `engine: jupyter` en `bloque1/..4/` y `evaluables/`, y produce los `.ipynb` correspondientes en `notebooks/` (preservando la estructura de carpetas).

## Despliegue (publicación manual con `quarto publish`)

**No hay CI/CD en este repositorio.** Los `push` a `main` no despliegan nada. La publicación se hace en local, desde la máquina del mantenedor, con la CLI de Quarto.

### Procedimiento

```bash
# 1. Renderizar (opcional, para previsualizar antes de publicar)
QUARTO_PYTHON=.venv/bin/python3 quarto preview

# 2. Publicar a GitHub Pages
quarto publish gh-pages
```

`quarto publish gh-pages`:
1. Ejecuta `quarto render` y genera `_site/`.
2. Crea (si no existe) o actualiza la rama `gh-pages` con el contenido de `_site/`.
3. Hace `git push` de esa rama al remoto.

### Configuración requerida en GitHub (una sola vez)

En **Settings → Pages** del repositorio:
- **Source:** `Deploy from a branch`
- **Branch:** `gh-pages` / `(root)`

A partir de ahí, cada `quarto publish gh-pages` actualiza la rama `gh-pages` y GitHub Pages la sirve automáticamente (sin Actions).

### Requisitos en la máquina del mantenedor

- Quarto CLI 1.6+ instalado localmente.
- `git` con permisos de push al repo (escritura sobre la rama `gh-pages`).
- No se necesita `LLM_API_KEY` en local: las celdas con `#| eval: false` se omiten en `quarto render`.

### Limpieza recomendada tras la migración

- En **Settings → Environments**, eliminar el environment `github-pages` (ya no se usa).
- Si existían ejecuciones previas de Actions, quedan en el historial pero dejan de generarse runs nuevos.

## Notas importantes

- Los `.qmd` usan `engine: jupyter` y contienen celdas Python ejecutables.
- Las celdas con `#| eval: true` se ejecutan durante `quarto render`.
- Las celdas con `#| eval: false` (típicamente las que llaman al LLM) NO se ejecutan en render; los notebooks Colab son el vehículo de ejecución real.
- El grid del sitio está configurado en `_quarto.yml` (sidebar 260px, body 850px, margin 0px).
- Footer con créditos en todas las páginas.
- `scripts/`, `solutions/` y `guias/` están en `.gitignore` y excluidos del render. Los scripts de corrección (`scripts/corregir_hpdN.py`) referenciados en los `.qmd` evaluables se desarrollarán en una iteración futura.
- `mod10.md` (raíz) es la guía docente pública del módulo: se renderiza (`*.md` en `_quarto.yml`) y aparece en el sidebar bajo "Inicio".
- Autoría: Adam Leiyi Chen Abolacio, Fernando Sancho Caparrini (Universidad de Sevilla).
