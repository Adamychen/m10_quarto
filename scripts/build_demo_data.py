"""
Precalcula los datos de la demo de embeddings (demos/embeddings.qmd).

La demo corre en el navegador (Shinylive), así que no puede cargar un modelo
de embeddings. Este script calcula una vez la matriz de similitud coseno y una
proyección 2D (PCA) de un corpus de frases, y los inserta como literal Python
entre los marcadores DATA-START / DATA-END de demos/embeddings.qmd.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/build_demo_data.py
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
QMD = Path(__file__).resolve().parent.parent / "demos" / "embeddings.qmd"
START, END = "# DATA-START", "# DATA-END"

CORPUS = {
    "ia": [
        "El modelo de lenguaje genera texto coherente a partir de una instrucción.",
        "Las redes neuronales aprenden representaciones a partir de grandes cantidades de datos.",
        "El sistema responde preguntas consultando documentos almacenados.",
        "Entrenar un algoritmo requiere datos etiquetados de buena calidad.",
        "La inteligencia artificial ya escribe código y resume informes.",
        "Los transformers procesan secuencias prestando atención a todas sus partes.",
        "Un chatbot puede mantener una conversación sobre temas técnicos.",
        "El ordenador aprendió a reconocer rostros en las fotografías.",
    ],
    "cocina": [
        "Hay que dejar reposar la masa del pan durante una hora.",
        "Añade una pizca de sal y remueve la salsa a fuego lento.",
        "Este bizcocho queda esponjoso si montas bien las claras.",
        "La paella se hace mejor con arroz bomba y caldo casero.",
        "Asar las verduras con aceite de oliva realza su sabor.",
        "Para una tortilla jugosa, cocina los huevos a fuego suave.",
    ],
    "finanzas": [
        "La inflación reduce el poder adquisitivo de los salarios.",
        "El banco central subió los tipos de interés para frenar los precios.",
        "Diversificar la cartera disminuye el riesgo de perder dinero.",
        "Las acciones de la empresa cayeron tras presentar pérdidas trimestrales.",
        "Ahorrar una parte fija del sueldo cada mes es una buena costumbre.",
        "El préstamo hipotecario se paga en cuotas durante veinte años.",
    ],
    "deporte": [
        "El delantero marcó dos goles en la segunda parte.",
        "El equipo necesita ganar el partido del domingo para clasificarse.",
        "Correr cinco kilómetros cada mañana mejora la resistencia.",
        "El portero detuvo el penalti en el último minuto.",
        "La selección entrenó bajo la lluvia antes del torneo.",
        "Nadar es un ejercicio completo que cuida las articulaciones.",
    ],
}


def pca_2d(x: np.ndarray) -> np.ndarray:
    """Proyección PCA a 2 dimensiones con SVD (sin depender de sklearn)."""
    centered = x - x.mean(axis=0)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    return centered @ vt[:2].T


def main() -> None:
    sentences, topics = [], []
    for topic, items in CORPUS.items():
        sentences.extend(items)
        topics.extend([topic] * len(items))

    model = SentenceTransformer(MODEL)
    vectors = model.encode(sentences, normalize_embeddings=True)

    cosine = vectors @ vectors.T
    xy = pca_2d(vectors)
    xy = (xy - xy.min(axis=0)) / (xy.max(axis=0) - xy.min(axis=0))

    payload = {
        "model": MODEL,
        "dim": int(vectors.shape[1]),
        "sentences": sentences,
        "topics": topics,
        "xy": np.round(xy, 4).tolist(),
        "cosine": np.round(cosine, 4).tolist(),
    }
    literal = "DATA = " + json.dumps(payload, ensure_ascii=False, indent=1)
    text = QMD.read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    QMD.write_text(f"{head}{START}\n{literal}\n{END}{tail}", encoding="utf-8")
    print(f"Datos insertados en {QMD} ({len(sentences)} frases, dim={payload['dim']})")


if __name__ == "__main__":
    main()
