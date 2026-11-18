"""
Precalcula los datos de la demo de búsqueda híbrida (demos/hibrida.qmd).

La demo corre en el navegador (Shinylive), así que no puede cargar un modelo de
embeddings. Este script calcula una vez la similitud coseno entre cada consulta
de la demo y cada documento del FAQ, y la inserta como literal Python entre los
marcadores DATA-START / DATA-END de la demo. BM25 se calcula en el navegador.

El FAQ, el modelo y el BM25 son los mismos que en bloque1/01e-recuperacion.qmd,
de modo que la demo reproduce lo que el alumno obtiene en el notebook.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/build_hybrid_data.py
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
QMD = Path(__file__).resolve().parent.parent / "demos" / "hibrida.qmd"
START, END = "# DATA-START", "# DATA-END"

# (texto, etiqueta corta para la demo). Mismo orden que el FAQ de 01e.
FAQ = [
    ("Puedes pagar con tarjeta de crédito o débito en cualquier comercio adherido.", "Pagar con tarjeta"),
    ("No se admite el pago con tarjeta en operaciones superiores a 3.000 euros; usa transferencia.", "Límite de pago con tarjeta"),
    ("Para pedir un reembolso, solicita la devolución en la app en un plazo de 14 días.", "Reembolsos"),
    ("La comisión por transferencia SEPA es de 0,50 euros por operación.", "Comisión SEPA"),
    ("Las transferencias internacionales tienen una comisión del 2 % del importe.", "Transf. internacionales"),
    ("Si pierdes tu tarjeta, bloquéala desde la app o llama al teléfono de atención 24 horas.", "Tarjeta perdida"),
    ("El IBAN es el código que identifica tu cuenta bancaria en transferencias nacionales e internacionales.", "Qué es el IBAN"),
    ("Para cambiar tu contraseña, entra en Ajustes > Seguridad y pulsa «Restablecer».", "Cambiar contraseña"),
    ("El límite diario de retirada en cajeros es de 600 euros.", "Límite en cajeros"),
    ("Abrir una cuenta nueva es gratis y se completa en cinco minutos con tu DNI.", "Abrir una cuenta"),
    ("Los préstamos personales se conceden en 24 horas si tienes la nómina domiciliada.", "Préstamos personales"),
    ("La hipoteca a tipo variable se revisa cada seis meses según el Euríbor.", "Hipoteca y Euríbor"),
    ("Error E-4021: la operación fue rechazada por saldo insuficiente.", "Error E-4021"),
    ("Error E-4012: la tarjeta ha caducado y debe renovarse.", "Error E-4012"),
]

# (consulta, índice del documento correcto, lección que ilustra)
QUERIES = [
    ("Euríbor", 11,
     "Nombre propio: BM25 lo encuentra al instante; los embeddings lo dejan en el puesto 5. "
     "La fusión lo rescata, porque basta con que un método lo ponga arriba."),
    ("he olvidado mi clave de acceso", 7,
     "«Clave de acceso» no comparte ninguna palabra con «contraseña»: BM25 no encuentra nada, el significado sí. "
     "La fusión acierta aunque uno de los dos métodos no aporte nada."),
    ("¿qué significa el error E-4012?", 13,
     "BM25 pone E-4012 primero y E-4021 segundo; los embeddings, al revés. Los dos suman exactamente lo mismo: "
     "empate. Cuando los métodos se contradicen así, la fusión no sabe decidir."),
    ("límite para pagar con tarjeta", 1,
     "«Pagar» y «tarjeta» salen en muchos documentos y BM25 entierra la respuesta en el puesto 5. "
     "La fusión no la pone primera, pero la mantiene entre las tres que leería el LLM."),
]


def main() -> None:
    model = SentenceTransformer(MODEL)
    docs = model.encode([t for t, _ in FAQ], normalize_embeddings=True)
    qs = model.encode([q for q, _, _ in QUERIES], normalize_embeddings=True)
    cos = (qs @ docs.T).round(4).tolist()

    data = {
        "model": MODEL,
        "docs": [t for t, _ in FAQ],
        "labels": [l for _, l in FAQ],
        "queries": [
            {"q": q, "gold": g, "lesson": lesson, "cos": c}
            for (q, g, lesson), c in zip(QUERIES, cos)
        ],
    }
    literal = "DATA = " + json.dumps(data, ensure_ascii=False, indent=1)

    text = QMD.read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    QMD.write_text(f"{head}{START}\n{literal}\n{END}{tail}", encoding="utf-8")
    print(f"Datos escritos en {QMD.relative_to(QMD.parent.parent)}")
    for qd in data["queries"]:
        order = sorted(range(len(FAQ)), key=lambda j: -qd["cos"][j])
        print(f"  {qd['q']!r}: correcto en el puesto {order.index(qd['gold']) + 1} por embeddings")


if __name__ == "__main__":
    main()
