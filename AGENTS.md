# AGENTS — Módulo 10: IA Generativa para Data Science

## Estructura del proyecto

```
modulo_10/
├── _quarto.yml                  # Configuración del sitio Quarto
├── *.qmd                        # Páginas de teoría (Quarto, cargadas con jupytext)
├── notebooks/
│   ├── 01-fundamentos.ipynb     # Teoría interactiva (34 celdas)
│   ├── hpd1-embeddings.ipynb    # HPD 1 — Pipeline de embeddings
│   ├── hpd2-agente-tool-calling.ipynb  # HPD 2 — Agente Tool Calling
│   ├── hpd3-servidor-mcp.ipynb  # HPD 3 — Servidor MCP
│   └── hpd4-rag-mixto.ipynb     # HPD 4 — RAG Mixto
├── shiny-apps/
│   ├── app.py                   # App Shiny principal (login + sidebar + notebooks + admin + chat)
│   ├── Dockerfile               # Imagen Docker
│   ├── docker-compose.yml       # Orquestación Docker
│   ├── requirements.txt         # Dependencias Python
│   ├── .env                     # Variables de entorno
│   ├── .env.example             # Template de variables de entorno
│   ├── Makefile                 # Comandos para Docker
│   ├── auth/
│   │   ├── login.py             # Validación de login contra CSV (SHA256), soporta roles
│   │   └── usuarios.csv         # email, pin_hash, nombre, role
│   ├── persistence/
│   │   └── user_state.py        # Guarda/carga progreso por usuario
│   ├── modules/
│   │   ├── base_module.py       # Carga notebooks (.ipynb + .qmd con jupytext), ejecuta código
│   │   └── chat_assistant.py    # Agente LLM con herramientas (búsqueda, navegación, insertar código)
│   ├── solutions/               # Código de solución (botón "Solución")
│   │   ├── hpd1-embeddings.py
│   │   ├── hpd2-agente-tool-calling.py
│   │   ├── hpd3-servidor-mcp.py
│   │   └── hpd4-rag-mixto.py
│   └── scripts/
│       └── generate_users.py    # Genera usuarios.csv con PINs aleatorios, soporta --admin
├── images/                      # Imágenes del sitio
├── styles.css                   # Estilos CSS del sitio Quarto
└── AGENTS.md                    # Este archivo
```

## Cómo ejecutar la app Shiny

### Local (desarrollo)

```bash
cd shiny-apps

# Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# Arrancar servidor (usar --reload para recarga automática)
shiny run app.py --host 0.0.0.0 --port 8000
```

Abrir `http://localhost:8000` en el navegador.

### Solo interfaz (sin ML pesado)

Si solo quieres probar login + navegación (sin torch, chromadb, etc.):

```bash
cd shiny-apps
pip install shiny nbformat jupytext markdown python-dotenv langchain-openai
shiny run app.py --host 0.0.0.0 --port 8000
```

### Docker con Makefile (producción — recomendado)

```bash
cd shiny-apps

# Primera instalación (guía paso a paso)
make install

# Día a día
make deploy    # Construir y arrancar
make logs      # Ver logs en vivo
make stop      # Parar
make restart   # Reiniciar
make update    # git pull + reconstruir
make users     # Generar nuevos alumnos
make status    # Estado de contenedores
make help      # Lista de comandos
```

### Docker manual (alternativa)

```bash
cd shiny-apps

# 1. Crear alumnos
nano emails.txt   # Un email por línea
python scripts/generate_users.py emails.txt

# 2. Configurar API key (solo para chat assistant — opcional)
echo "OPENAI_API_KEY=sk-tu-api-key" >> .env

# 3. Construir y arrancar
docker compose up --build -d
```

## Credenciales demo

- Email: `adam@alum.us.es`
- PIN: `demo123`
- Rol: `admin` (puede gestionar usuarios desde «Administración → Gestión de usuarios»)

## Dependencias principales

| Paquete | Tamaño | Uso |
|---|---|---|
| `shiny` | ~10 MB | Framework web |
| `jupytext` | ~5 MB | Carga .qmd como notebooks |
| `torch` | ~2 GB | Transformers, atención |
| `sentence-transformers` | ~500 MB | Embeddings |
| `transformers` | ~300 MB | Tokenización, LLMs |
| `chromadb` | ~100 MB | Bases de datos vectoriales |
| `faiss-cpu` | ~50 MB | Indexación ANN |
| `langchain` + extras | ~200 MB | Tool calling, chat assistant |
| `mcp` | ~15 MB | Servidor MCP |
| `ragas` + `datasets` | ~100 MB | Evaluación RAG |
| `PyPDF2` | ~5 MB | Procesar PDFs |
| `matplotlib`, `numpy`, `pandas` | ~100 MB | Análisis y gráficos |

## Funcionalidades de la app

- **Login**: Email @alum.us.es + PIN, validado contra CSV con hash SHA256
- **Sidebar**: Misma estructura que el sitio Quarto, con indicador de progreso (●/○)
- **Teoría interactiva**: Páginas .qmd cargadas con jupytext → celdas markdown + código editable
- **Notebooks .ipynb**: Renderizados celda por celda, código editable y ejecutable
- **CodeMirror**: Editor de código con coloreado sintáctico, números de línea, tema Monokai
- **Altura dinámica**: Las celdas de código crecen automáticamente con el contenido
- **Callouts Quarto**: `::: {.callout-note}` → cajas estilizadas con CSS
- **HPDs**: Notebooks con TODOs que los alumnos completan en el navegador
- **Botón "Solución"**: Carga el código completo de la celda seleccionada (vía mensaje custom, sin recargar)
- **Ejecutar todas**: Ejecuta todas las celdas del notebook en secuencia
- **Reiniciar**: Restaura el notebook a su estado original
- **Persistencia**: El progreso se guarda automáticamente y se restaura al hacer login
- **Outputs independientes**: Al ejecutar una celda, solo se actualiza su resultado — sin flash ni recarga
- **Admin**: Gestión de usuarios (añadir, resetear PIN, eliminar)
- **Chat asistente**: Agente LLM con herramientas (buscar en materiales, navegar, insertar código)

## Chat asistente (IA)

La app incluye un chat flotante (💬 abajo a la derecha) con un agente LLM que puede:

- Responder preguntas sobre el temario
- Buscar contenido en todos los `.qmd` y `.ipynb` del curso
- Navegar a una página específica
- Insertar código directamente en una celda

### Configuración del LLM

Las variables de entorno controlan el modelo:

| Variable | Default | Descripción |
|---|---|---|
| `LLM_MODEL` | `qwen3.5:35b-a3b` | Modelo a usar |
| `LLM_BASE_URL` | `https://llamus.cs.us.es/api/v1` | URL de la API (OpenAI-compatible) |
| `LLM_API_KEY` | `not-needed` | API key (si el endpoint lo requiere) |

### Arquitectura del agente

```
chat_assistant.py:
  - process_message(history, msg, context) → acción estructurada
  - Herramientas (tool-calling de OpenAI):
      search_content(query): busca en .qmd y .ipynb
      get_page_content(page_id): lee página completa
  - Acciones de respuesta:
      respond: texto normal
      navigate: lleva al alumno a otra página
      insert_code: escribe código en una celda
```

## Generar usuarios

```bash
cd shiny-apps
# Crear archivo con emails (uno por línea)
echo -e "adam@alum.us.es\nana@alum.us.es" > emails.txt
python scripts/generate_users.py emails.txt

# Con admin:
python scripts/generate_users.py emails.txt --admin profesor@alum.us.es
```

Esto genera:
- `auth/usuarios.csv` — hashes SHA256 de los PINs, con columna `role` (student | admin)
- `auth/pins_generated.txt` — PINs en texto plano (para imprimir/compartir)

## Arquitectura técnica

### Flujo de autenticación

```
Login (email + PIN) → validar contra usuarios.csv (hash SHA256, con role)
→ crear token de sesión → guardar en sessions.json → cookie session_token (7 días)
→ cargar progreso de disco → restaurar estado
```

### Flujo de ejecución de celdas

```
Usuario edita código (CodeMirror) → click "Ejecutar"
→ JS flushes CodeMirror → Shiny.setInputValue('run_cell_idx', idx)
→ Server: exec(code, user_ns) → captura stdout + figuras
→ Solo output de esa celda se actualiza (output independiente cr_{page}_{idx})
→ Guarda progreso a disco
```

### Carga de páginas

```
.ipynb → load_notebook() → nbformat.read()
.qmd   → load_qmd_notebook() → jupytext.reads(fmt="Rmd") → NotebookNode
Ambos → notebook_ui() → renderiza celdas markdown + código editable
```

### Persistencia

- Cada usuario tiene su progreso en `users/{hash_email_16chars}/{page_id}.json`
- Se guarda al ejecutar una celda o al cambiar de página
- Se restaura al hacer login

### Mapa de notebooks a secciones

| Sidebar ID | Fuente | Anchor cell |
|---|---|---|
| `01-fundamentos` | `01-fundamentos.ipynb` | 0 |
| `01a-transformer` | `01-fundamentos.ipynb` | 5 |
| `01b-llms` | `01-fundamentos.ipynb` | 17 |
| `01c-embeddings` | `01-fundamentos.ipynb` | 25 |
| `01d-vectordb` | `01-fundamentos.ipynb` | 27 |
| `hpd1-embeddings` | `hpd1-embeddings.ipynb` | 0 |
| `hpd2-agente-tool-calling` | `hpd2-agente-tool-calling.ipynb` | 0 |
| `hpd3-servidor-mcp` | `hpd3-servidor-mcp.ipynb` | 0 |
| `hpd4-rag-mixto` | `hpd4-rag-mixto.ipynb` | 0 |
| `inicio` | `index.qmd` (jupytext) | 0 |
| `02-orquestacion` | `02-orquestacion.qmd` (jupytext) | 0 |
| `03-aplicaciones` | `03-aplicaciones.qmd` (jupytext) | 0 |
| `04-gobernanza` | `04-gobernanza.qmd` (jupytext) | 0 |
| `05-evaluacion` | `05-evaluacion.qmd` (jupytext) | 0 |
| `06-herramientas` | `06-herramientas.qmd` (jupytext) | 0 |
| `07-bibliografia` | `07-bibliografia.qmd` (jupytext) | 0 |

## Despliegue con nginx (Quarto + Shiny bajo mismo dominio)

```nginx
server {
    listen 80;
    server_name modulo10.miuniversidad.es;

    # Sitio Quarto (estático)
    location / {
        root /var/www/modulo10/_site;
    }

    # App Shiny (vivo)
    location /lab/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Los enlaces en Quarto apuntan a `/lab/`. Shiny maneja login y ejecución.

## Notas importantes

- Los notebooks `.ipynb` originales **no se modifican** — Shiny solo los lee
- Los `.qmd` se cargan con jupytext (formato Rmd) — **no requiere Quarto CLI**
- Las celdas no-Python (mermaid, bash) se muestran como HTML read-only
- La imagen Docker pesa ~5-6 GB por las dependencias de ML
- El chat asistente requiere conexión al endpoint LLM configurado
- Cada alumno tiene su propia sesión aislada (estado en RAM + persistencia a disco)
- Para rebuild completo de Docker: `docker compose up --build -d`
