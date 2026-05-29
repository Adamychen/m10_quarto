MÁSTER EN DATA SCIENCE & BIG DATA

**Módulo 10**

**IA Generativa para Data Science**

| **3,0 ECTS**<br><br>Créditos | **A distancia**<br><br>Modalidad | **75 horas**<br><br>Carga total | **Máster técnico**<br><br>Nivel |
| ---------------------------- | -------------------------------- | ------------------------------- | ------------------------------- |

## Distribución de la carga docente

| **Tipo de actividad**          | **Horas** | **% del total** | **Formato**                  |
| ------------------------------ | --------- | --------------- | ---------------------------- |
| Horas Teóricas (HT)            | 18        | 24 %            | Magistral + lectura técnica  |
| Horas Prácticas Docentes (HPD) | 12        | 16 %            | Talleres guiados / notebooks |
| Horas del Alumno (HA)          | 45        | 60 %            | Proyecto + estudio autónomo  |
| **TOTAL**                      | **75**    | **100 %**       |                              |

# 1\. Descripción del módulo

Este módulo introduce al alumno en el ecosistema de la IA Generativa desde una perspectiva de ingeniería aplicada a Data Science. El objetivo es que el alumno adquiera criterio técnico para seleccionar, integrar y desplegar modelos generativos en contextos reales: desde la consulta semántica sobre datos corporativos hasta la automatización de flujos de análisis mediante agentes.

El módulo está diseñado con un enfoque hands-on: cada bloque teórico tiene un correlato práctico directo, y todas las actividades se articulan en torno a un proyecto integrador que el alumno construye de forma incremental a lo largo del módulo.

_Prerrequisitos: haber superado los módulos anteriores del máster, con especial dominio de Python, manipulación de datos con pandas/NumPy y fundamentos de Machine Learning supervisado y no supervisado._

# 2\. Contenidos

## Bloque 1 - Fundamentos: Transformers, LLMs y Representación Vectorial (HT: 6h | HPD: 4h)

_Objetivos de bloque: comprender la arquitectura que subyace a los LLMs modernos y dominar la representación vectorial de texto y datos tabulares._

**Contenidos teóricos:**

- Arquitectura Transformer: mecanismo de atención multi-cabeza, codificación posicional y variantes (encoder-only, decoder-only, encoder-decoder). Lectura complementaria: Vaswani et al. (2017), secciones 3-5.
- Grandes Modelos de Lenguaje (LLMs): preentrenamiento, tokenización (BPE, SentencePiece), ventana de contexto y parámetros relevantes para su uso en producción (temperatura, top-p, top-k).
- Modelos de embeddings: semántica distribucional, modelos de frase (Sentence-BERT, E5, text-embedding-3-small de OpenAI). Embeddings multimodales y para datos tabulares (TabNet, SCARF).
- Bases de datos vectoriales: indexación ANN (HNSW, IVF), métricas de similitud (coseno, producto escalar, L2). Comparativa operacional: Chroma (local/sin servidor), FAISS (librería embebible), Qdrant y Pinecone (cloud-native). Criterios de elección según escala y requisitos de privacidad.

**Actividad práctica (HPD 1 - 4h):**

Pipeline de embeddings end-to-end. El alumno construirá un notebook que: (1) carga un corpus de documentos técnicos en PDF, (2) aplica chunking con solapamiento, (3) genera embeddings con un modelo open-source (e.g., intfloat/e5-small-v2 vía Sentence-Transformers), (4) indexa en Chroma y (5) ejecuta consultas de búsqueda semántica evaluando recall@k.

## Bloque 2 - Orquestación: Prompt Engineering, Frameworks y Agentes (HT: 6h | HPD: 4h)

_Objetivos de bloque: diseñar pipelines de prompting robustos, usar frameworks de orquestación y construir agentes con herramientas externas._

**Contenidos teóricos:**

- Prompt Engineering avanzado aplicado a Data Science: few-shot con ejemplos de código, chain-of-thought (CoT) y tree-of-thought (ToT) para razonamiento analítico, output structuring con JSON Schema, role prompting para análisis de datos.
- LangChain: cadenas (LCEL), memoria conversacional, retrievers, parsers de salida y callbacks. LlamaIndex: índices sobre documentos estructurados y desestructurados, query engines y pipelines de ingesta.
- Model Context Protocol (MCP): especificación del protocolo, recursos, herramientas y prompts. Implementación de servidores MCP locales (stdio) para conectar LLMs a bases de datos, ficheros locales o APIs REST corporativas de forma segura.
- Diseño de Agentes Inteligentes: patrón ReAct (Reasoning + Acting), Tool Calling (function calling nativo de la API), flujos multi-step y gestión del estado. Diferencias entre agentes síncronos y asincrónicos. Introducción a arquitecturas multi-agente (supervisor, swarm).

**Actividades prácticas (HPD 2 y 3 - 4h):**

HPD 2 (2h): Construcción de un agente analítico con LangChain + Tool Calling. El agente recibirá preguntas en lenguaje natural sobre un dataset y usará herramientas (ejecutar pandas, llamar a una API de visualización) para responderlas de forma autónoma.

HPD 3 (3h): Configuración de un servidor MCP local con Python. El alumno expondrá como herramienta MCP el acceso a una base de datos SQLite corporativa ficticia, y comprobará la conexión desde un cliente LLM, evaluando los riesgos de inyección de prompts y fuga de datos.

## Bloque 3 - Aplicaciones: RAG, Datos Sintéticos y Fine-tuning (HT: 6h | HPD: 4h)

_Objetivos de bloque: implementar sistemas RAG de calidad producción, generar datos sintéticos útiles y aplicar técnicas de ajuste fino eficientes._

**Contenidos teóricos:**

- RAG avanzado: arquitectura naive vs. avanzada (re-ranking, query expansion, HyDE, RAG-Fusion). RAG sobre datos estructurados: Text-to-SQL con validación, RAG sobre DataFrames. Evaluación de pipelines RAG: Ragas framework (faithfulness, answer relevancy, context precision).
- Generación de datos sintéticos: usos en DS (oversampling de clases minoritarias, anonimización, aumento de dataset de entrenamiento). Técnicas: prompting guiado con esquemas, Evol-Instruct, SDV (Synthetic Data Vault) para datos tabulares. Validación estadística de datos sintéticos (fidelidad, utilidad, privacidad).
- Fine-tuning eficiente (PEFT): LoRA y QLoRA - intuición matemática del rango bajo, hiperparámetros clave (r, alpha, target_modules). Cuándo hacer fine-tuning vs. RAG vs. prompting. Infraestructura mínima: fine-tuning de un modelo de 7B parámetros en GPU de consumidor con Hugging Face TRL y bitsandbytes.

**Actividad práctica (HPD 4 - 4h):**

Implementación de un sistema RAG sobre datos mixtos. El alumno construirá un pipeline RAG que procesa tanto documentos PDF no estructurados como una tabla SQL, implementará un re-ranker con cross-encoder (e.g., ms-marco-MiniLM) y evaluará la calidad con Ragas sobre un conjunto de preguntas anotadas manualmente.

## Bloque 4 - Despliegue y Gobernanza (HT: 0h conceptual - integrado en proyecto | HPD: 0h - evaluado en proyecto final)

_Este bloque no tiene sesiones teóricas independientes: sus contenidos se imparten de forma integrada en los bloques anteriores y se evalúan exclusivamente a través del proyecto final._

**Contenidos:**

- Evaluación de LLMs: métricas automáticas (ROUGE, BERTScore), LLM-as-a-judge (prompt de evaluación, sesgos del juez, calibración). Frameworks: DeepEval, RAGAS, LangSmith.
- Ética y gobernanza: alucinaciones - taxonomía (factual, faithfulness, extrinsic) y técnicas de mitigación (grounding, citation, RLHF). Privacidad de datos corporativos: PII detection, data masking antes del envío a APIs externas, on-premise vs. cloud. Sesgo en LLMs: tipos, herramientas de auditoría, estrategias de documentación (Model Card, System Card).
- Patrones de despliegue: API gateway sobre modelos open-source con vLLM/Ollama, control de costes (caching semántico con GPTCache), observabilidad (LangSmith, Langfuse, Prometheus).

# 3\. Competencias específicas

| **Cód.** | **Competencia**                                   | **Descriptor de logro**                                                                                                                                                                               |
| -------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CE-1** | **Representación vectorial y búsqueda semántica** | Diseñar pipelines de embeddings adecuados a la naturaleza del dato (texto, tabular, código) y seleccionar la base de datos vectorial más apropiada según requisitos de escala, latencia y privacidad. |
| **CE-2** | **Orquestación de modelos y agentes**             | Construir flujos complejos con LangChain/LlamaIndex y diseñar agentes autónomos con Tool Calling que integran herramientas externas de forma robusta y trazable.                                      |
| **CE-3** | **Integración segura con entornos locales**       | Implementar servidores MCP que expongan fuentes de datos corporativas a LLMs, aplicando controles de acceso y evaluando superficies de ataque (prompt injection, data leakage).                       |
| **CE-4** | **Sistemas RAG orientados a negocio**             | Implementar y evaluar arquitecturas RAG sobre datos estructurados y desestructurados, midiendo su calidad con frameworks estándar (RAGAS) e iterando sobre componentes individuales.                  |
| **CE-5** | **Ajuste fino y datos sintéticos**                | Aplicar técnicas PEFT (LoRA/QLoRA) para adaptar modelos open-source a dominios específicos y generar datos sintéticos validados estadísticamente para aumentar o anonimizar datasets.                 |
| **CE-6** | **Gobernanza y despliegue responsable**           | Evaluar modelos con métricas LLM-as-a-judge, detectar y mitigar alucinaciones y sesgos, y documentar sistemas generativos siguiendo estándares de transparencia algorítmica.                          |

# 4\. Actividades formativas

## 4.1 Clases magistrales

Cada bloque dispone de presentaciones organizadas en píldoras temáticas que incluyen demostraciones de código y se acompañan de notebooks ejecutables en Google Colab / Kaggle. Se recomienda el seguimiento en directo con la ejecución de los notebooks posteriormente para replicar los ejemplos y mejorar la comprensión de los fundamentos. Además, para cada bloque se proponen un conjunto de lecturas complementarias.

**Lecturas técnicas complementarias obligatorias por bloque:**

- Bloque 1: Vaswani et al. (2017) «Attention is All You Need» (secciones 3-5); ficha técnica del modelo de embeddings utilizado en la práctica.
- Bloque 2: documentación oficial de LangChain LCEL; especificación MCP v1.0 (secciones Resources y Tools).
- Bloque 3: Es et al. (2023) «RAGAS: Automated Evaluation of Retrieval Augmented Generation»; Hu et al. (2022) «LoRA: Low-Rank Adaptation of Large Language Models» (secciones 1-4).
- Bloque 4: Anthropic Model Card (Claude 3); artículo de blog de Langfuse sobre trazabilidad en producción.

## 4.2 Talleres prácticos guiados (HPD)

Los talleres prácticos siguen el hilo conductor del proyecto integrador que supone el porcentaje mayor de la evaluación. Cada taller entrega un componente que el alumno incorporará a su proyecto final:

| **HPD** | **Título**                                     | **Duración** | **Entregable parcial**                            |
| ------- | ---------------------------------------------- | ------------ | ------------------------------------------------- |
| **1**   | Pipeline de embeddings y búsqueda semántica    | 4 h          | Notebook con índice vectorial y métricas recall@k |
| **2**   | Agente analítico con Tool Calling              | 4 h          | Script del agente con al menos 2 herramientas     |
| **3**   | Servidor MCP y conexión segura a datos locales | 4 h          | Servidor MCP funcional + análisis de riesgos      |
| **4**   | Sistema RAG sobre datos mixtos con evaluación  | 6 h          | Pipeline RAG evaluado con RAGAS (score > 0,6)     |

## 4.3 Foro de evolución del ecosistema

Actividad asíncrona quincenal. Se publicará una lectura corta (post técnico, paper, anuncio de modelo) y el alumno deberá aportar un comentario argumentado (mínimo 150 palabras) conectando el contenido con algún bloque del módulo. Se valora la capacidad crítica sobre limitaciones y el impacto en flujos de trabajo reales de Data Science.

# 5\. Evaluación

## 5.1 Estructura de la evaluación

| **Instrumento**                        | **Peso** | **Nota mínima**              | **Vinculación**            |
| -------------------------------------- | -------- | ---------------------------- | -------------------------- |
| Entregas prácticas parciales (HPD 1-4) | 30 %     | 5,0 / 10                     | CE-1, CE-2, CE-3, CE-4     |
| Participación en foros (mínimo 3 de 4) | 10 %     | Participado / No participado | CE-6 (pensamiento crítico) |
| Proyecto integrador final              | 60 %     | 5,0 / 10                     | CE-1 a CE-6                |

## 5.2 Proyecto integrador final

El proyecto consiste en el diseño e implementación de un sistema de Inteligencia de Negocio conversacional orientado a datos corporativos. El alumno debe integrar todos los componentes construidos durante el módulo:

- Un pipeline de embeddings sobre un corpus propio (mínimo 50 documentos o 10.000 filas tabulares).
- Un sistema RAG avanzado con al menos una técnica de mejora (re-ranking, query expansion o HyDE).
- Un agente con al menos dos herramientas (e.g., búsqueda semántica + ejecución de consultas SQL o código Python).
- Opcionalmente: conexión segura mediante servidor MCP o fine-tuning ligero de un componente del pipeline.
- Un informe de evaluación con métricas RAGAS y análisis de al menos un riesgo ético / de gobernanza.

**Rúbrica de evaluación del proyecto:**

| **Dimensión**             | **Insuficiente (< 5)**                               | **Suficiente (5-6,9)**                 | **Notable (7-8,9)**                         | **Sobresaliente (9-10)**                      |
| ------------------------- | ---------------------------------------------------- | -------------------------------------- | ------------------------------------------- | --------------------------------------------- |
| **Funcionalidad técnica** | El sistema no ejecuta o falla en el flujo principal. | Flujo básico RAG + agente funcionando. | Integración robusta con manejo de errores.  | Pipeline óptimo, modular y reproducible.      |
| **Calidad del RAG**       | Sin evaluación cuantitativa.                         | RAGAS ejecutado, score > 0,5.          | Score > 0,65 con análisis de componentes.   | Score > 0,75, iteración documentada.          |
| **Gobernanza y ética**    | No se aborda.                                        | Se identifica un riesgo.               | Riesgo identificado y mitigación propuesta. | Análisis de múltiples riesgos con evidencias. |
| **Documentación**         | Código sin comentarios, sin README.                  | README básico y código legible.        | Docstrings, diagrama de arquitectura.       | Documentación completa tipo producción.       |

# 6\. Herramientas y entorno tecnológico recomendado

El módulo está diseñado para ser completado íntegramente con herramientas gratuitas o de tier libre. El siguiente stack solo muestra algunas opciones, aunque el alumno puede sustituir componentes equivalentes justificando la elección:

| **Categoría**      | **Herramienta recomendada**                  | **Alternativas / Notas**                                                              |
| ------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------- |
| **LLM API**        | OpenAI GPT-4o-mini                           | Anthropic Claude Haiku, Google Gemini Flash - tier gratuito suficiente para el módulo |
| **LLM local**      | Ollama + Llama 3.1 8B                        | LM Studio; recomendado para HPD 3 (privacidad de datos)                               |
| **Embeddings**     | Sentence-Transformers (intfloat/e5-small-v2) | OpenAI text-embedding-3-small (API); all-MiniLM-L6-v2 para prototipado rápido         |
| **Vector DB**      | Chroma (local)                               | FAISS (embebible, sin servidor); Qdrant para producción                               |
| **Orquestación**   | LangChain >= 0.3 (LCEL)                      | LlamaIndex para indexación documental avanzada                                        |
| **Fine-tuning**    | Hugging Face TRL + bitsandbytes (QLoRA)      | Google Colab Pro o Kaggle (GPU T4 gratuita)                                           |
| **Evaluación RAG** | RAGAS >= 0.1                                 | DeepEval; LangSmith (trazabilidad)                                                    |
| **MCP**            | Python MCP SDK (Anthropic)                   | Servidor stdio local; no requiere infraestructura cloud                               |
| **Entorno**        | VS Code + Python 3.11, Jupyter               | Google Colab para talleres que requieren GPU                                          |

# 7\. Bibliografía y recursos de referencia

## Artículos técnicos fundamentales

- Vaswani, A. et al. (2017). Attention is All You Need. NeurIPS. \[arXiv:1706.03762\]
- Hu, E. et al. (2022). LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022. \[arXiv:2106.09685\]
- Es, S. et al. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. \[arXiv:2309.15217\]
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. \[arXiv:2005.11401\]
- Dettmers, T. et al. (2023). QLoRA: Efficient Finetuning of Quantized LLMs. NeurIPS 2023. \[arXiv:2305.14314\]

## Documentación técnica (versiones estables al inicio del curso)

- LangChain Expression Language (LCEL) - <https://python.langchain.com/docs/expression_language>
- LlamaIndex - <https://docs.llamaindex.ai>
- Model Context Protocol Specification - <https://spec.modelcontextprotocol.io>
- RAGAS Documentation - <https://docs.ragas.io>
- Hugging Face TRL - <https://huggingface.co/docs/trl>

## Lecturas de contexto (recomendadas, no obligatorias)

- Anthropic (2023). Model Card: Claude 3 - análisis de riesgos y mitigaciones en un LLM de producción.
- Gao, Y. et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. \[arXiv:2312.10997\] - visión panorámica del estado del arte en RAG.
- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. Stanford CRFM. \[arXiv:2108.07258\]

_Nota: el ecosistema de IA Generativa evoluciona con rapidez. Las herramientas y versiones indicadas son las estables en el momento de redacción de este documento. El profesorado actualizará los notebooks y referencias al inicio de cada edición del módulo._