"""
Precalcula los datos de la demo de atención con un modelo real
(demos/atencion-modelo-real.qmd).

La demo corre en el navegador (Shinylive), así que no puede cargar BERT. Este
script extrae una vez los pesos de atención de BETO (BERT en español) para unas
frases y unas cabezas elegidas, y los inserta como literal Python entre los
marcadores DATA-START / DATA-END de la demo. Antes imprime, para cada cabeza,
cuánto de lo que se dice de ella en la demo se cumple en estas frases.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/build_attention_data.py
"""

import json
from pathlib import Path

import torch
from transformers import AutoModel, AutoTokenizer

MODEL = "dccuchile/bert-base-spanish-wwm-cased"
QMD = Path(__file__).resolve().parent.parent / "demos" / "atencion-modelo-real.qmd"
START, END = "# DATA-START", "# DATA-END"

# Frase (palabras separadas por espacios, con el punto final) e índice de palabra
# (base 0) que se selecciona por defecto: el sujeto.
SENTENCES = [
    ("El perro grande persiguió al gato negro .", 1),
    ("La profesora explicó la lección difícil a los alumnos .", 1),
    ("Los alumnos que estudiaron mucho aprobaron el examen final .", 1),
    ("Mi hermana pequeña compró unos libros viejos en la librería .", 1),
]

# (capa, cabeza, etiqueta corta, descripción). Elegidas con scripts/probe_attention*.py.
HEADS = [
    (3, 8, "Mira a la palabra anterior",
     "Cada token atiende casi del todo al token que tiene justo a la izquierda."),
    (5, 7, "Mira a la palabra siguiente",
     "Cada token atiende casi del todo al token que tiene justo a la derecha."),
    (10, 5, "Se ancla al inicio y al final",
     "Casi toda la atención va a [CLS] y [SEP], los marcadores de inicio y fin: una cabeza que 'descansa'."),
    (6, 10, "Tiende a unir sujeto y verbo",
     "En estas frases el sujeto atiende al verbo de su oración, aunque haya palabras entre medias. Una parte grande de su atención va, además, a [CLS]/[SEP]."),
    (1, 3, "Tiende a unir objeto y verbo",
     "En estas frases el objeto atiende al verbo que lo rige, aunque haya palabras entre medias. Una parte grande de su atención va, además, a [CLS]/[SEP]."),
    (6, 8, "Reparte sin un patrón claro",
     "La atención se reparte entre muchos tokens sin un patrón fácil de describir."),
]


def main() -> None:
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModel.from_pretrained(MODEL, attn_implementation="eager").eval()

    sentences = []
    stats = {(l, h): {"prev": [], "next": [], "sink": [], "ent": []} for l, h, *_ in HEADS}
    for text, default_word in SENTENCES:
        words = text.split()
        enc = tok(words, is_split_into_words=True, return_tensors="pt")
        tokens = tok.convert_ids_to_tokens(enc["input_ids"][0])
        word_ids = enc.word_ids(0)
        n = len(tokens)
        with torch.no_grad():
            att = torch.stack([a[0] for a in model(**enc, output_attentions=True).attentions])
        ar = torch.arange(1, n)
        heads = {}
        for l, h, *_ in HEADS:
            a = att[l, h]
            heads[f"L{l}H{h}"] = [[round(float(v), 3) for v in row] for row in a]
            s = stats[(l, h)]
            s["prev"].append(float(a[ar, ar - 1].mean()))
            idx = torch.arange(n - 1)
            s["next"].append(float(a[idx, idx + 1].mean()))
            s["sink"].append(float(a[:, [0, n - 1]].sum(-1).mean()))
            s["ent"].append(float(-(a * a.clamp_min(1e-9).log()).sum(-1).mean()))
        # Token por defecto: primer trozo de la palabra elegida.
        default = word_ids.index(default_word)
        sentences.append({"text": text, "tokens": tokens, "default": default, "att": heads})

    print("Comprobación de las etiquetas (media sobre las frases de la demo):")
    for l, h, label, _ in HEADS:
        s = stats[(l, h)]
        m = {k: sum(v) / len(v) for k, v in s.items()}
        print(f"  L{l:02d} H{h:02d}  anterior={m['prev']:.2f}  siguiente={m['next']:.2f}  "
              f"[CLS]/[SEP]={m['sink']:.2f}  entropía={m['ent']:.2f}  → {label}")

    payload = {
        "model": MODEL,
        "heads": [{"id": f"L{l}H{h}", "layer": l, "head": h, "label": lab, "desc": desc}
                  for l, h, lab, desc in HEADS],
        "sentences": sentences,
    }
    literal = "DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    text = QMD.read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    QMD.write_text(f"{head}{START}\n{literal}\n{END}{tail}", encoding="utf-8")
    print(f"Datos insertados en {QMD} ({len(sentences)} frases, {len(HEADS)} cabezas)")


if __name__ == "__main__":
    main()
