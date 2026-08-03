"""Test: mlx-community/Qwen3.6-35B-A3B-8bit + agent con create_agent."""
import os, io, pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import warnings; warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()
LLM_KEY = os.getenv("LLM_API_KEY")
if not LLM_KEY:
    print("❌ Configura LLM_API_KEY en .env"); exit(1)

llm = ChatOpenAI(
    model="mlx-community/Qwen3.6-35B-A3B-8bit", base_url="https://llamus.cs.us.es/api/v1",
    api_key=LLM_KEY, temperature=0,
)

df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

@tool
def consulta_pandas(expresion: str) -> str:
    """Ejecuta una expresión pandas sobre df (Titanic)."""
    try:
        return str(eval(expresion, {"df": df, "pd": pd}, {}))
    except Exception as e:
        return f"Error: {e}"

@tool
def histograma(columna: str, titulo: str = "") -> str:
    """Genera un histograma de una columna numérica del Titanic (Age, Fare...)."""
    df[columna].hist()
    plt.title(titulo or f"Histograma de {columna}")
    plt.savefig("grafico.png"); plt.close()
    return f"Histograma de {columna} generado"

@tool
def barras(columna: str, agrupar_por: str = "") -> str:
    """Genera un gráfico de barras. agrupar_por opcional (Sex, Pclass...)."""
    if agrupar_por:
        df.groupby(agrupar_por)[columna].mean().plot.bar()
    else:
        df[columna].value_counts().plot.bar()
    plt.title(f"Barras de {columna}")
    plt.savefig("grafico.png"); plt.close()
    return f"Barras de {columna} generado"

@tool
def boxplot(columna: str, agrupar_por: str = "") -> str:
    """Genera un boxplot. agrupar_por opcional."""
    if agrupar_por:
        df.boxplot(columna, by=agrupar_por)
    else:
        df.boxplot(columna)
    plt.savefig("grafico.png"); plt.close()
    return f"Boxplot de {columna} generado"

@tool
def codigo_libre(codigo: str) -> str:
    """
    Ejecuta código matplotlib libre sobre df (Titanic).
    REGLAS: usa plt.<funcion>(), NUNCA df.plot().
    NO uses plt.show() (se elimina automáticamente).
    NO leas archivos (df ya cargado).
    Variables: df, plt, pd, np.
    """
    codigo = codigo.replace("plt.show()", "")
    try:
        plt.figure()
        exec(codigo, {"plt": plt, "pd": pd, "df": df, "np": np})
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight"); plt.close()
        return f"Gráfico generado ({len(buf.getvalue())} bytes)"
    except Exception as e:
        plt.close()
        return f"Error: {e}. Reintenta con plt.<funcion>() en vez de df.plot()"

tools = [consulta_pandas, histograma, barras, boxplot, codigo_libre]

agente = create_agent(
    model=llm,
    tools=tools,
    system_prompt="Eres un analista del Titanic. Usa las herramientas disponibles. Responde en español.",
)

preguntas = [
    # → consulta_pandas
    "¿Cuál es la edad media de los pasajeros?",
    # → histograma
    "Genera un histograma de la distribución de edades",
    # → barras con agrupar_por
    "Haz un gráfico de barras de la tarifa media por clase",
    # → boxplot
    "Genera un boxplot de la edad comparando entre hombres y mujeres",
    # → codigo_libre
    "Haz un scatter plot de edad vs tarifa, coloreando por supervivencia",
]

for i, p in enumerate(preguntas, 1):
    print(f"\n{'='*60}")
    print(f"PREGUNTA {i}: {p}")
    print('='*60)
    try:
        result = agente.invoke({"messages": [{"role": "user", "content": p}]})
        print(f"RESPUESTA: {result['messages'][-1].content}")
    except Exception as e:
        print(f"ERROR: {e}")
