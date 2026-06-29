# Módulo 10 — IA Generativa para Data Science

Sitio web del módulo 10 del **Máster en Data Science & Big Data** de la Universidad de Sevilla.

**IA Generativa para Data Science** — 3,0 ECTS | 75 horas

## Para alumnos

### Ver el sitio online

El sitio está publicado en GitHub Pages. Accede desde la URL que se muestra en el repositorio (pestaña **Settings → Pages**).

### Abrir notebooks en Colab

Cada página tiene un badge **Open in Colab** en la parte superior. Si es la primera vez:
1. Abre [colab.research.google.com](https://colab.research.google.com)
2. Ve a **Settings → GitHub → Connect to GitHub** y autoriza la app
3. Vuelve a la página y haz clic en el badge

Como alternativa: **File → Open Notebook → GitHub**, busca `Adamychen/m10_quarto` y selecciona el notebook de la carpeta `notebooks/`.

### Ejercicios evaluables

Hay 4 HPDs con sus ejercicios evaluables (entrega básica) y una extensión avanzada por cada uno. Todos se entregan como notebook `.ipynb` ejecutado con todas las celdas completas.

| HPD | Ejercicios evaluables | Extensión avanzada |
|---|---|---|
| HPD 1 — Embeddings | `evaluables/hpd1-evaluables.qmd` | `evaluables/hpd1-extension.qmd` |
| HPD 2 — Agente Tool Calling | `evaluables/hpd2-evaluables.qmd` | `evaluables/hpd2-extension.qmd` |
| HPD 3 — Servidor MCP | `evaluables/hpd3-evaluables.qmd` | `evaluables/hpd3-extension.qmd` |
| HPD 4 — RAG mixto + Datos sintéticos | `evaluables/hpd4-rag-mixto.qmd` y `evaluables/hpd4-datos-sinteticos.qmd` | `evaluables/hpd4-datos-sinteticos-extension.qmd` |

Los talleres presenciales (con código parcialmente completado por el alumno) están en `bloque1/`, `bloque2/`, `bloque3/` y `bloque4/`.

---

## Para profesores

### Requisitos

- Python 3.11+
- [Quarto](https://quarto.org/docs/get-started/) 1.6+

### Clonar y preparar

```bash
git clone https://github.com/Adamychen/m10_quarto.git
cd m10_quarto
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Renderizar en local

```bash
QUARTO_PYTHON=.venv/bin/python3 quarto render
```

Para verlo en el navegador con recarga automática:

```bash
QUARTO_PYTHON=.venv/bin/python3 quarto preview
```

### Estructura del proyecto

```
m10_quarto/
├── _quarto.yml                  # Configuración del sitio (sidebar, grid, tema)
├── index.qmd                    # Presentación
├── about.qmd                    # Acerca de
├── mod10.md                     # Guía docente pública
├── bloque1/                     # Fundamentos: Transformers, LLMs, embeddings, vector DB
│   ├── 01-fundamentos.qmd
│   ├── 01a-transformer.qmd
│   ├── 01b-llms.qmd
│   ├── 01c-embeddings.qmd
│   └── 01d-vectordb.qmd
├── bloque2/                     # Orquestación: prompt, frameworks, MCP, agentes
│   ├── 02-orquestacion.qmd
│   ├── 02a-prompt-engineering.qmd
│   ├── 02b-langchain.qmd
│   ├── 02c-llamaindex.qmd
│   ├── 02d-mcp.qmd
│   ├── 02e-agentes.qmd
│   ├── hpd2-agente-tool-calling.qmd
│   └── hpd3-servidor-mcp.qmd
├── bloque3/                     # Aplicaciones: RAG avanzado, datos sintéticos, fine-tuning
│   ├── 03-aplicaciones.qmd
│   ├── 03a-datos-sinteticos.qmd
│   ├── 03b-rag-avanzado.qmd
│   └── 03c-fine-tuning.qmd
├── bloque4/                     # Despliegue y gobernanza
│   └── 04-gobernanza.qmd
├── evaluables/                  # Ejercicios evaluables (10 ficheros)
│   ├── hpd1-embeddings.qmd
│   ├── hpd1-evaluables.qmd
│   ├── hpd1-extension.qmd
│   ├── hpd2-evaluables.qmd
│   ├── hpd2-extension.qmd
│   ├── hpd3-evaluables.qmd
│   ├── hpd3-extension.qmd
│   ├── hpd4-rag-mixto.qmd
│   ├── hpd4-datos-sinteticos.qmd
│   └── hpd4-datos-sinteticos-extension.qmd
├── 05-evaluacion.qmd            # Evaluación y proyecto
├── 06-herramientas.qmd          # Herramientas y stack recomendado
├── 07-bibliografia.qmd          # Bibliografía y recursos
├── images/                      # Imágenes del sitio
├── includes/footer.html         # Pie de página
├── styles.css                   # Estilos CSS personalizados
├── requirements.txt             # Dependencias Python fijadas
├── generate_notebooks.sh        # Genera .ipynb desde .qmd
├── .github/workflows/
│   └── deploy.yml               # CI/CD a GitHub Pages
└── AGENTS.md                    # Instrucciones para asistentes IA
```

### Añadir o modificar contenido

1. Las páginas están en `.qmd` con `engine: jupyter`
2. Las celdas con `#| eval: true` se ejecutan durante `quarto render`
3. Edita `_quarto.yml` para cambiar el sidebar, el grid o el tema
4. Edita `styles.css` para estilos personalizados

### Despliegue

El sitio se despliega automáticamente a GitHub Pages mediante GitHub Actions (`.github/workflows/deploy.yml`) al hacer push a `main`. También puedes lanzarlo manualmente desde la pestaña **Actions** del repositorio.

### Generar notebooks .ipynb

```bash
./generate_notebooks.sh
```

### Personalizar el grid

En `_quarto.yml`:

```yaml
format:
  html:
    grid:
      sidebar-width: 260px
      body-width: 850px
      margin-width: 0px
      gutter-width: 1.5rem
```

---

## Autoría

**Departamento de Ciencias de la Computación e Inteligencia Artificial** — Universidad de Sevilla

- Adam Leiyi Chen Abolacio — `achen@us.es`
- Fernando Sancho Caparrini — `fsancho@us.es`
