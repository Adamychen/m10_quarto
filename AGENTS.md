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
│   ├── 04-gobernanza.qmd        # Índice del bloque
│   ├── 04a-evaluacion.qmd       # Métricas + LLM-as-judge + frameworks
│   ├── 04b-alucinaciones.qmd    # Taxonomía + grounding + citation
│   ├── 04c-privacidad.qmd       # PII + datos sintéticos + DP
│   ├── 04d-sesgo.qmd            # Tipos + auditoría de sesgo
│   ├── 04e-documentacion.qmd    # Model Card + System Card
│   └── 04f-despliegue.qmd       # On-prem + observabilidad + caching
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
├── includes/
│   ├── footer.html              # Pie de página
│   ├── mermaid-init.js          # Tema Mermaid del sitio (paleta Python + semánticos)
│   └── setup_keys.py            # Fuente única de la lógica de carga de LLM_API_KEY
├── styles.css                   # Estilos CSS personalizados
├── requirements.txt             # Dependencias Python fijadas
├── generate_notebooks.sh        # Genera .ipynb desde .qmd
├── scripts/
│   └── sync_setup_keys.py       # Pre-render: inyecta setup_keys.py en los .qmd
└── AGENTS.md                    # Este archivo
```

## Sidebar del sitio

| Sección | Páginas |
|---|---|
| **Inicio** | `index.qmd` (Presentación), `about.qmd` (Acerca de), `mod10.md` (Guía docente) |
| **Bloque 1 — Fundamentos** | `bloque1/01-fundamentos.qmd`, `01a-transformer.qmd`, `01b-llms.qmd`, `01c-embeddings.qmd`, `01d-vectordb.qmd`, `evaluables/hpd1-embeddings.qmd`, `evaluables/hpd1-evaluables.qmd`, `evaluables/hpd1-extension.qmd` |
| **Bloque 2 — Orquestación** | `bloque2/02-orquestacion.qmd`, `02a-prompt-engineering.qmd`, `02b-langchain.qmd`, `02c-llamaindex.qmd`, `02d-mcp.qmd`, `02e-agentes.qmd`, `hpd2-agente-tool-calling.qmd`, `evaluables/hpd2-evaluables.qmd`, `evaluables/hpd2-extension.qmd`, `hpd3-servidor-mcp.qmd`, `evaluables/hpd3-evaluables.qmd`, `evaluables/hpd3-extension.qmd` |
| **Bloque 3 — Aplicaciones** | `bloque3/03-aplicaciones.qmd`, `03b-rag-avanzado.qmd`, `03a-datos-sinteticos.qmd`, `03c-fine-tuning.qmd`, `evaluables/hpd4-rag-mixto.qmd`, `evaluables/hpd4-datos-sinteticos.qmd`, `evaluables/hpd4-datos-sinteticos-extension.qmd` |
| **Bloque 4 — Gobernanza** | `bloque4/04-gobernanza.qmd`, `04a-evaluacion.qmd`, `04b-alucinaciones.qmd`, `04c-privacidad.qmd`, `04d-sesgo.qmd`, `04e-documentacion.qmd`, `04f-despliegue.qmd` |
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

## API key centralizada (Llamus)

Todos los notebooks que usan Llamus comparten una única lógica de carga de la API key, centralizada en `includes/setup_keys.py`. La fuente de verdad es **un solo archivo**; los `.qmd` consumen un marcador y un pre-render lo expande.

### Orden de resolución de `LLM_API_KEY`

1. `.env` local (cargado con `python-dotenv`).
2. `os.environ` ya configurado externamente.
3. **Google Colab userdata:** secret `LLAMUS_API_KEY` (preferente) o `LLM_API_KEY`.

### Cómo se inyecta en los `.qmd`

1. El `.qmd` contiene el marcador `"""
Setup compartido para la API key de Llamus en todos los notebooks.
Inyectado en cada .qmd/.ipynb vía scripts/sync_setup_keys.py (pre-render).

Orden de resolución:
  1. .env local (python-dotenv)
  2. os.environ ya configurado externamente
  3. Google Colab userdata: secret "LLAMUS_API_KEY" (preferente) o "LLM_API_KEY"

Las celdas posteriores pueden leer la key con os.environ.get("LLM_API_KEY").
"""

import os


def _load_llm_api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    if not os.getenv("LLM_API_KEY"):
        try:
            from google.colab import userdata
            for name in ("LLAMUS_API_KEY", "LLM_API_KEY"):
                try:
                    value = userdata.get(name)
                    if value:
                        os.environ["LLM_API_KEY"] = value
                        break
                except Exception:
                    continue
        except ImportError:
            pass


_load_llm_api_key()

if os.getenv("LLM_API_KEY"):
    print("✓ LLM_API_KEY cargada.")
else:
    print("⚠️  LLM_API_KEY no encontrada.")
    print("    • Local: crea un archivo .env con LLM_API_KEY=tu_clave")
    print("    • Colab: añade un Secret 🔑 con nombre 'LLAMUS_API_KEY'")
` en la celda de setup.
2. `_quarto.yml` declara `pre-render: scripts/sync_setup_keys.py`.
3. Antes de cada `quarto render`, el script reemplaza el marcador por el contenido de `includes/setup_keys.py` (in-place, idempotente).
4. Los `.ipynb` generados ya llevan el código inlinado y funcionan en Colab sin necesidad de clonar el repositorio.

### Configurar la API key en Colab

1. Abrir el icono 🔑 (Secrets) en la barra lateral izquierda.
2. "Add new secret" → nombre: `LLAMUS_API_KEY` (preferente) o `LLM_API_KEY`.
3. Pegar la clave como valor → activar "Notebook access".
4. Re-ejecutar la celda de setup.

### Configurar la API key en local

Crear un archivo `.env` en la raíz del proyecto:

```
LLM_API_KEY=tu_clave_aquí
```

### Actualizar la lógica centralizada

Si cambia el orden de resolución o el formato de los secrets:

1. Editar `includes/setup_keys.py`.
2. Re-añadir el marcador `"""
Setup compartido para la API key de Llamus en todos los notebooks.
Inyectado en cada .qmd/.ipynb vía scripts/sync_setup_keys.py (pre-render).

Orden de resolución:
  1. .env local (python-dotenv)
  2. os.environ ya configurado externamente
  3. Google Colab userdata: secret "LLAMUS_API_KEY" (preferente) o "LLM_API_KEY"

Las celdas posteriores pueden leer la key con os.environ.get("LLM_API_KEY").
"""

import os


def _load_llm_api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    if not os.getenv("LLM_API_KEY"):
        try:
            from google.colab import userdata
            for name in ("LLAMUS_API_KEY", "LLM_API_KEY"):
                try:
                    value = userdata.get(name)
                    if value:
                        os.environ["LLM_API_KEY"] = value
                        break
                except Exception:
                    continue
        except ImportError:
            pass


_load_llm_api_key()

if os.getenv("LLM_API_KEY"):
    print("✓ LLM_API_KEY cargada.")
else:
    print("⚠️  LLM_API_KEY no encontrada.")
    print("    • Local: crea un archivo .env con LLM_API_KEY=tu_clave")
    print("    • Colab: añade un Secret 🔑 con nombre 'LLAMUS_API_KEY'")
` en los `.qmd` que lo necesiten (queda oculto tras la primera inyección; buscar con `grep -L "from dotenv" bloque*/evaluables/*.qmd`).
3. Re-ejecutar `./generate_notebooks.sh` o `quarto render`.

### Diagnóstico rápido

Si una celda con LLM devuelve 401, ejecutar en una celda aparte:

```python
import os
print("LLM_API_KEY set:", bool(os.getenv("LLM_API_KEY")))
print("Source:", "env" if "LLM_API_KEY" in os.environ else "missing")
```

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
- La lógica de carga de `LLM_API_KEY` está centralizada en `includes/setup_keys.py` y se inyecta vía el marcador `"""
Setup compartido para la API key de Llamus en todos los notebooks.
Inyectado en cada .qmd/.ipynb vía scripts/sync_setup_keys.py (pre-render).

Orden de resolución:
  1. .env local (python-dotenv)
  2. os.environ ya configurado externamente
  3. Google Colab userdata: secret "LLAMUS_API_KEY" (preferente) o "LLM_API_KEY"

Las celdas posteriores pueden leer la key con os.environ.get("LLM_API_KEY").
"""

import os


def _load_llm_api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    if not os.getenv("LLM_API_KEY"):
        try:
            from google.colab import userdata
            for name in ("LLAMUS_API_KEY", "LLM_API_KEY"):
                try:
                    value = userdata.get(name)
                    if value:
                        os.environ["LLM_API_KEY"] = value
                        break
                except Exception:
                    continue
        except ImportError:
            pass


_load_llm_api_key()

if os.getenv("LLM_API_KEY"):
    print("✓ LLM_API_KEY cargada.")
else:
    print("⚠️  LLM_API_KEY no encontrada.")
    print("    • Local: crea un archivo .env con LLM_API_KEY=tu_clave")
    print("    • Colab: añade un Secret 🔑 con nombre 'LLAMUS_API_KEY'")
` (pre-render automático, ver sección "API key centralizada").
- El grid del sitio está configurado en `_quarto.yml` (sidebar 260px, body 850px, margin 0px).
- Footer con créditos en todas las páginas.
- `scripts/`, `solutions/` y `guias/` están en `.gitignore` y excluidos del render. Los scripts de corrección (`scripts/corregir_hpdN.py`) referenciados en los `.qmd` evaluables se desarrollarán en una iteración futura.
- `mod10.md` (raíz) es la guía docente pública del módulo: se renderiza (`*.md` en `_quarto.yml`) y aparece en el sidebar bajo "Inicio".
- Autoría: Adam Leiyi Chen Abolacio, Fernando Sancho Caparrini (Universidad de Sevilla).

## Paleta de colores Mermaid

El sitio usa una paleta de 6 colores con significado semántico fijo. El tema base está definido en `includes/mermaid-init.js` (carga vía `mermaid: init` en `_quarto.yml`) y aplica los azules y amarillo de Python como colores por defecto. El resto se aplica por diagrama con `classDef`.

| Significado              | Hex       | classDef sugerido  | Notas                          |
|--------------------------|-----------|--------------------|--------------------------------|
| Input / fuente           | `#4B8BBE` | `metric` / `input` | Azul Python claro              |
| Proceso / orquestación   | `#306998` | `proc`             | Azul Python oscuro             |
| Resultado intermedio     | `#FFD43B` | `doc`              | Amarillo Python (texto negro)  |
| Aviso / herramienta      | `#e65100` | `obs`              | Naranja                        |
| Éxito / meta final       | `#2e7d32` | `out` / `ready`    | Verde                          |
| Riesgo / error           | `#c62828` | `risk`             | Rojo                           |

Texto blanco (`color:#fff`) sobre los oscuros, negro (`color:#000`) sobre amarillo. Bordes con un tono más oscuro del mismo color (p. ej. `#1e3a5f` para los azules).

**Cómo usar `classDef`** en un diagrama:

```
flowchart LR
    classDef input fill:#4B8BBE,stroke:#1e3a5f,color:#fff,stroke-width:1.5px
    classDef out   fill:#2e7d32,stroke:#0d3010,color:#fff,stroke-width:2px

    A[Pregunta del usuario]:::input
    B[LLM]:::input
    C[Respuesta validada]:::out

    A --> B --> C
```

## Convención de cross-refs nativa de Quarto

Todos los `.qmd` usan cross-references nativas de Quarto en lugar de texto plano ("sección X", "tabla Y") o slugs auto-generados. Esto evita que las referencias se rompan al renombrar un heading.

| Tipo | Prefijo | Cómo añadir el label | Cómo referenciarlo |
|---|---|---|---|
| Sección (heading) | `sec-` | `## 1.4 Embeddings e indexación {#sec-embeddings-chroma}` | `@sec-embeddings-chroma` |
| Tabla | `tbl-` | Insertar `: Caption {#tbl-nombre}` **antes** de la tabla | `@tbl-nombre` |
| Figura (imagen o Mermaid) | `fig-` | `![Caption](img.png){#fig-nombre}` o `::: {#fig-nombre} \`\`\`{mermaid}…\`\`\` :::` | `@fig-nombre` |

**Reglas de naming (kebab-case, español, sin tildes):**

- `## 1.4 Embeddings e indexación` → `{#sec-embeddings-chroma}` (NO `{#sec-1-4-embeddings}`)
- `### ¿Qué es un prompt?` → `{#sec-que-es-prompt}` (sin tildes, sin signos de puntuación)
- `## De JSON Schema a datos sintéticos` → `{#sec-json-schema-datos-sint}` (sin acentos, sin `:`)

**Rangos de secciones** (cuando se quiere referenciar "sección X a Y"):

```markdown
@sec-inicio--@sec-fin
```

Genera automáticamente "Sección 1 — Sección 3".

**Anclas inter-página:** en sitios Quarto (no libros), las cross-refs entre páginas distintas siguen siendo enlaces Markdown, no `@sec-…`. Usar **siempre labels estables** en lugar de slugs auto-generados:

```markdown
# ❌ Frágil (slug auto-generado)
[Evaluación](../index.qmd#competencias-específicas)

# ✅ Estable (label manual)
[Evaluación](../index.qmd#sec-competencias-especificas)
```

**Mermaid en div etiquetado:** los bloques Mermaid necesitan envoltorio explícito para tener label:

```markdown
::: {#fig-flujo-evaluacion}
```{mermaid}
flowchart LR
    A --> B
```
:::
```

(El `:::` alrededor es necesario porque los bloques de código no aceptan `#fig-…` en los cell options de Quarto.)

**Excepciones a la convención:**

- Los comentarios Python en celdas pueden seguir diciendo "sección 1.4" como orientación al alumno; no son markdown y no rompen nada.
- Las referencias a secciones de papers externos (Vaswani 2017, LoRA 2022, etc.) se mantienen como texto plano: "Leer Vaswani et al. (2017) secciones 3-5" es una cita bibliográfica, no una cross-ref.
