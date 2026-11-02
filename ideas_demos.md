# Ideas de demos interactivas — Módulo 10

Catálogo de demos candidatas para el curso, organizado por bloque. Pensado para un **perfil general de máster de formación permanente**: la demo no enseña la mecánica (fórmulas, álgebra) sino que deja al alumno **tocar algo y ver una consecuencia**.

## Estado actual

Demos ya existentes en `demos/` (Bloque 1, corren en el navegador con Shinylive):

- `bpe.qmd` — Tokenización BPE
- `chunking.qmd` — Estrategias de chunking
- `embeddings.qmd` — Embeddings y similitud (datos precalculados con `scripts/build_demo_data.py`)
- `atencion.qmd` — Atención (1): la idea, ilustrativa, con interruptor «LLM generativo» (pesos diseñados a mano)
- `atencion-modelo-real.qmd` — Atención (2): seis cabezas de BETO reales (datos con `scripts/build_attention_data.py`)

Los Bloques 2, 3 y 4 no tienen demos todavía. La demo de atención (partes 1 y 2) está hecha; el resto de este catálogo está pendiente.

## Principios de diseño

1. **Una idea por demo.** Si hay más de dos controles, sobra uno.
2. **Cada demo termina con «qué has visto».** Dos líneas que fijen el mensaje.
3. **Ejemplos cotidianos y en español**, no vectores abstractos.
4. **Resultado inmediato.** Sin esperar a un modelo: todo precalculado y reproducido.
5. **Detalle numérico opcional**, plegado, para los curiosos.
6. **Un fallo visible.** Lo que más se recuerda es cuándo y por qué falla el sistema.
7. **Sin API key en el navegador.** Datos o respuestas reales grabadas una vez con un script (patrón de `build_demo_data.py`) e inyectadas en el `.qmd`, de forma determinista.
8. **Honestidad sobre los límites.** Si la demo usa un caso real elegido por su claridad, decirlo.

## Prioridad recomendada

| # | Demo | Bloque | Por qué primero |
|---|---|---|---|
| 1 | Atención con palabras clicables | 1 — `01a-transformer` | La más difícil de explicar sin demo y la más lucida con ella |
| 2 | Creatividad / temperatura | 1 — `01b-llms` | Muy barata; explica un parámetro que usarán a diario |
| 3 | Juez LLM con sesgo de posición | 4 — `04a-evaluacion` | Muy memorable; enlaza con el proyecto final |

---

## Bloque 1 — Fundamentos

### Atención con palabras clicables (dos subdemos)
- **Capítulo:** `bloque1/01a-transformer.qmd`
- **Idea:** una frase donde el alumno pulsa una palabra y ve de qué otras palabras «se fija».
- **Se evita:** Q/K/V, softmax, matrices. Casilla opcional «ver los números».
- **Estructura:** dos partes, porque mezclar «idea limpia» y «realidad ruidosa» en una sola demo se estorba. Se pueden publicar por separado.

**Parte 1 — «Qué es la atención» (ilustrativa, una cabeza)**
- Pesos diseñados a mano, declarado abiertamente: etiqueta visible «ilustración» y aviso de que es una simplificación.
- **Ejemplos:** «El banco cerró porque estaba en quiebra» frente a «Me senté en el banco del parque»; un pronombre («La maleta no cabía en el coche porque *era* muy grande» → *era* apunta a *maleta*).
- **Secuencia guiada:** pulsa *banco* en la 1.ª frase → pulsa *banco* en la 2.ª → ¿mismo significado? → caso del pronombre.
- **Mensaje:** el significado de una palabra depende de las que la rodean.
- Sin selector de cabeza, sin tokens partidos. Termina con enlace a la parte 2: «¿Y en un modelo real?».
- Sin dependencias: se puede construir ya.

**Parte 2 — «Qué hace un modelo real» (multi-cabeza)**
- Pesos reales de un modelo **codificador** (BERT), con selector de capa/cabeza y tokens reales (enlaza con la demo de BPE).
- **Mensaje:** en un modelo real hay muchas cabezas y cada una hace algo distinto (token anterior, siguiente, sintaxis, correferencia); algunas no son interpretables. Encaja con la sección de multi-head attention.
- Mostrar solo 2–3 cabezas elegidas con etiqueta descriptiva; el resto en «explorar», para no desanimar.
- **Modelo:** no Qwen3. Es un decodificador con atención causal: cada palabra solo mira a las anteriores, así que *banco* no vería *parque*. Un codificador tiene atención bidireccional y encaja con la intuición.
  - Preferido: `dccuchile/bert-base-spanish-wwm-cased` (BETO, ~110 M, solo español).
  - Alternativas: `google-bert/bert-base-multilingual-cased`, `FacebookAI/xlm-roberta-base`.
- **Datos:** extraídos con `output_attentions=True` (`attn_implementation="eager"`) en un script offline y precalculados; el navegador no necesita el modelo.
- **Aclarar siempre que es un BERT, no un LLM autorregresivo.** Riesgo: que el alumno asuma que los LLM (ChatGPT, Qwen, Llama…) miran en ambos sentidos como esta demo.
  - Etiqueta fija y visible en la demo: «Modelo: BERT (codificador). Mira antes **y** después. Los LLM generativos son decodificadores y solo miran hacia atrás».
  - Interruptor «Ver como un LLM generativo» que aplica la máscara causal: al pulsar *banco* en «Me senté en el banco del parque», *parque* queda tachada porque aún no existe. Es un ejemplo directo de por qué un LLM no puede usar el contexto posterior al generar.
  - Enlazar con el apartado de encoder vs decoder de `01a-transformer.qmd`.
  - La máscara se aplica sobre los pesos del propio BERT; se avisa de que es una ilustración (un decodificador real se entrena así, no se enmascara a posteriori). También puede hacerse en la parte 1.
- **Resultado de la prueba de viabilidad** (BETO, 5 frases, `scripts/probe_attention.py`):
  - Se ven con claridad cabezas posicionales (token anterior: L00H10, L03H08; token siguiente: L05H07, L01H08; `[CLS]`/`[SEP]`: L10H05/H07/H08/H09).
  - **No** aparece una cabeza que desambigüe «banco» ni que resuelva pronombres (*era* → *maleta*): el efecto no es visible en los pesos crudos. Por eso la parte 1 es ilustrativa y la parte 2 promete solo «tipos de cabezas».
  - Segunda prueba (frases sintácticas, pares no adyacentes): L6H10 (sujeto→verbo) y L1H3 (objeto→verbo) aparecen en las dos pruebas con criterios distintos, pero con 3–4 casos y frases con las que se eligieron (circular). En la demo se presentan como «tendencia», y ~50 % de su atención va a `[CLS]`/`[SEP]`.
  - Ampliación pendiente (opcional): validar con ~30–40 frases por relación de un treebank (p. ej. UD Spanish-GSD).
- **Cautelas:**
  - BERT concentra mucha atención en `[CLS]`, `[SEP]` y puntuación (Clark et al., 2019, *What Does BERT Look At?*): ocultarlos/atenuarlos o explicarlos.
  - No está garantizado que una cabeza desambigüe «banco»; la correferencia y los patrones sintácticos son más probables. Decidir frases y cabezas finales tras la prueba de viabilidad (`scripts/probe_attention.py`).
  - Considerar añadir Clark et al. (2019) a `references.bib`.

### Creatividad / temperatura
- **Capítulo:** `bloque1/01b-llms.qmd`
- **Idea:** botón «continuar la frase» que escribe la siguiente palabra; un slider de «creatividad» de «predecible» a «caótico». El alumno genera 10 veces y compara.
- **Mensaje:** el modelo no «decide», saca una palabra de un abanico de probabilidades. A 0 siempre sale lo mismo; a valores altos aparece lo absurdo.
- **Extensión:** top-k y top-p como «recortar el abanico» (barras que se acortan).
- **Datos:** distribuciones de siguiente token precalculadas para 3–4 frases.

### Ventana de contexto: la mochila
- **Capítulo:** `bloque1/01b-llms.qmd`
- **Idea:** el alumno arrastra documentos a una «mochila» con capacidad limitada y ve qué cabe y qué se queda fuera.
- **Mensaje:** el contexto es finito y lo del medio se pierde con más facilidad («lost in the middle»).
- **Extensión:** barra de coste y latencia según longitud (tokens → euros). Tamaño del KV-cache como dato plegado.

### Búsqueda vectorial en un mapa
- **Capítulo:** `bloque1/01d-vectordb.qmd` (amplía `demos/embeddings.qmd`)
- **Idea:** mapa 2D de puntos; el alumno escribe una consulta, aparece como un punto y se iluminan sus vecinos.
- **Mensaje:** buscar por significado es buscar «lo más cercano».
- **Extensión:** exacta vs aproximada (HNSW/IVF) con un control «más rápido ↔ más exacto» que muestre qué vecinos se pierden. Recall frente a latencia como dato plegado.

### Taller HPD 1 (apoyo)
- **Capítulo:** `bloque1/hpd1-embeddings.qmd`
- **Idea:** reutilizar la demo de mapa de búsqueda como paso previo al taller, para que el alumno llegue con la intuición antes de escribir el pipeline.

---

## Bloque 2 — Orquestación

### Anatomía del tool calling
- **Capítulo:** `bloque2/02e-agentes.qmd`, base de `hpd2-agente-tool-calling.qmd` y `hpd4-servidor-mcp.qmd` (evaluables)
- **Idea:** mostrar paso a paso el esquema de la herramienta, la petición del modelo, la ejecución y la respuesta, con un LLM simulado. El alumno edita la **descripción** de la herramienta y ve cuándo falla la selección.
- **Mensaje:** el modelo decide qué herramienta usar leyendo su descripción; una descripción ambigua produce llamadas equivocadas.
- **Por qué importa:** el error típico de los alumnos en HPD2/HPD4 está justo aquí.

### Prompt lab
- **Capítulo:** `bloque2/02a-prompt-engineering.qmd`
- **Idea:** el mismo problema resuelto con zero-shot, few-shot, CoT y salida estructurada. Respuestas reales pregrabadas; el alumno puntúa y compara.
- **Mensaje:** pequeñas diferencias en el prompt cambian mucho el resultado, y cada técnica tiene su caso de uso.

### Traza de un agente
- **Capítulo:** `bloque2/02e-agentes.qmd`, `02f-patrones-agentes.qmd`
- **Idea:** reproducir una conversación paso a paso: pensando → usa herramienta → resultado → respuesta, con botón «siguiente».
- **Fallos incorporados:** bucle infinito, herramienta equivocada, error de parseo, alucinación de una herramienta inexistente.
- **Mensaje:** un agente es un bucle, y los bucles pueden fallar de formas muy concretas.

### Inspector de MCP
- **Capítulo:** `bloque2/02d-mcp.qmd`, `hpd4-servidor-mcp.qmd`
- **Idea:** simulador del handshake y de `tools/list` entre cliente y servidor (JSON-RPC), mostrando qué se dicen y en qué orden.
- **Mensaje:** MCP es un protocolo estándar de descubrimiento y uso de herramientas, no magia.

### Grafo de LangGraph interactivo
- **Capítulo:** `bloque2/hpd3-workflows-langgraph.qmd` (no evaluable), `02f-patrones-agentes.qmd`
- **Idea:** editar nodos y aristas condicionales y ver cómo evoluciona el estado al ejecutar.
- **Mensaje:** un workflow es un grafo con estado; las decisiones están en las aristas.

---

## Bloque 3 — Aplicaciones

### Pipeline RAG con palancas
- **Capítulo:** `bloque3/03b-rag-avanzado.qmd`, `evaluables/hpd5-rag-mixto.qmd`
- **Idea:** el alumno mueve tamaño de fragmento, top-k, reranker y umbral, y ve cómo cambian el contexto recuperado y la respuesta.
- **Fallo visible:** el fragmento correcto no entra en el top-k y la respuesta falla.
- **Mensaje:** la calidad de un RAG depende más de la recuperación que del modelo.
- **Conexión:** reutiliza el chunking de `demos/chunking.qmd`.

### Comparador híbrido (BM25 + densa + RRF)
- **Capítulo:** `bloque3/03b-rag-avanzado.qmd`
- **Idea:** la misma consulta con búsqueda por palabras y por significado; rankings distintos; la fusión de rankings en directo.
- **Mensaje:** cada método acierta donde el otro falla (nombres propios y códigos frente a paráfrasis).

### Fine-tuning y LoRA
- **Capítulo:** `bloque3/03c-fine-tuning.qmd`
- **Idea:** un modelo gigante «congelado» con una pequeña pieza acoplada, que es lo único que se entrena. Slider del tamaño de esa pieza, con porcentaje de parámetros entrenados y memoria como barras.
- **Extensión:** comparación full fine-tuning vs LoRA vs QLoRA.
- **Mensaje:** se puede adaptar un modelo enorme entrenando una fracción mínima.

### Calidad de datos sintéticos
- **Capítulo:** `bloque3/03a-datos-sinteticos.qmd`
- **Idea:** inspeccionar un lote generado y detectar duplicados, colapso de diversidad y sesgos (diversidad léxica, distribución de etiquetas).
- **Mensaje:** generar muchos datos no es generar buenos datos.

---

## Bloque 4 — Gobernanza (CE-6)

### Juez LLM con sesgo de posición
- **Capítulo:** `bloque4/04a-evaluacion.qmd`, `evaluables/proyecto-final.qmd`
- **Idea:** el alumno ve dos respuestas y elige la mejor; luego se intercambia el orden y el «juez» cambia de opinión.
- **Otros sesgos:** de longitud (la respuesta más larga gana) y de autopreferencia.
- **Mensaje:** un LLM-as-judge no es neutral; hay que controlarlo (intercambiar orden, rúbricas, calibrar con humanos).
- **Datos:** veredictos reales grabados.

### Detector de alucinaciones por grounding
- **Capítulo:** `bloque4/04b-alucinaciones.qmd`
- **Idea:** una respuesta con afirmaciones marcadas como soportadas o no por el contexto, con las citas resaltadas.
- **Mensaje:** una respuesta fluida no es una respuesta verdadera; el grounding permite comprobarla.

### Anonimización de PII
- **Capítulo:** `bloque4/04c-privacidad.qmd`
- **Idea:** pegar un texto y ver qué detectan reglas (regex) y NER, con falsos positivos y falsos negativos visibles.
- **Extensión:** compromiso privacidad-utilidad con ruido de privacidad diferencial (ε), como slider.
- **Mensaje:** anonimizar bien es difícil y siempre hay lo que se escapa.

### Auditoría de sesgo
- **Capítulo:** `bloque4/04d-sesgo.qmd`
- **Idea:** plantillas de prompt con atributos intercambiados (género, origen) y comparación lado a lado de las salidas, con una métrica sencilla de disparidad.
- **Mensaje:** el sesgo se detecta comparando, no leyendo una sola respuesta.

### Calculadora de despliegue
- **Capítulo:** `bloque4/04f-despliegue.qmd`
- **Idea:** coste por petición, tasa de aciertos de caché y comparación API vs on-premise (VRAM necesaria según cuantización).
- **Mensaje:** el coste y la viabilidad dependen de decisiones de despliegue concretas.

### Model Card (apoyo)
- **Capítulo:** `bloque4/04e-documentacion.qmd`
- **Idea (por explorar):** rellenar una Model Card guiada con un caso de uso y ver qué riesgos quedan sin documentar.

---

## Resumen por capítulo

| Capítulo | Demo(s) |
|---|---|
| `01a-transformer` | Atención con palabras clicables |
| `01b-llms` | Creatividad/temperatura; mochila de contexto |
| `01d-vectordb` | Búsqueda vectorial en un mapa |
| `02a-prompt-engineering` | Prompt lab |
| `02d-mcp` / `hpd4` | Inspector de MCP |
| `02e-agentes` / `hpd2` | Anatomía del tool calling; traza de un agente |
| `02f-patrones-agentes` / `hpd3` | Traza de un agente; grafo de LangGraph |
| `03a-datos-sinteticos` | Calidad de datos sintéticos |
| `03b-rag-avanzado` / `hpd5` | RAG con palancas; comparador híbrido |
| `03c-fine-tuning` | LoRA |
| `04a-evaluacion` | Juez LLM con sesgo de posición |
| `04b-alucinaciones` | Detector por grounding |
| `04c-privacidad` | Anonimización de PII |
| `04d-sesgo` | Auditoría de sesgo |
| `04e-documentacion` | Model Card guiada (por explorar) |
| `04f-despliegue` | Calculadora de despliegue |

## Notas técnicas

- Las demos van en `demos/` como `.qmd` con Shinylive; los datos precalculados se generan con scripts en `scripts/` (ver `build_demo_data.py`) y se insertan entre marcadores `DATA-START` / `DATA-END`.
- Hay que añadir cada demo al sidebar en `_quarto.yml` y enlazarla desde el capítulo correspondiente.
- Las demos que dependen de un LLM usan respuestas grabadas una sola vez, para que sean deterministas y no requieran `LLM_API_KEY`.
