"""
Precalcula los datos de la demo de temperatura (demos/temperatura.qmd).

La demo corre en el navegador (Shinylive), así que no puede cargar un LLM. Este
script mide una vez, con Qwen3-0.6B, la probabilidad de que cada palabra
candidata continúe una frase, y la inserta como literal Python entre los
marcadores DATA-START / DATA-END de la demo.

Las candidatas se eligen a mano (incluidas algunas poco plausibles, para que se
vea la cola del abanico). Como muchas palabras en español ocupan varios tokens,
la puntuación de una palabra es el producto de las probabilidades de sus tokens;
después se renormaliza entre las candidatas.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/build_temperature_data.py
"""

import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen3-0.6B"
QMD = Path(__file__).resolve().parent.parent / "demos" / "temperatura.qmd"
START, END = "# DATA-START", "# DATA-END"

# (frase, candidatas). Las palabras poco plausibles del final se quedan con
# probabilidad casi nula: es lo que la temperatura alta hace aflorar.
PROMPTS = [
    ("El gato se subió al",
     "coche sofá árbol suelo camión muro techo balcón cielo armario tejado ordenador"),
    ("Los fines de semana suelo ir al",
     "mar mercado centro trabajo campo cine bosque parque museo hospital teatro tribunal"),
    ("Mi comida favorita es la",
     "pizza ensalada sopa pasta carne paella hamburguesa fruta tortilla lasaña electricidad democracia"),
    ("Para el desayuno me gusta tomar un café con",
     "leche chocolate azúcar hielo mantequilla aceite nata sal tostadas canela miel pimienta"),
]


def word_logprob(model, tok, prompt: str, word: str) -> float:
    prefix = tok.encode(prompt)
    full = tok.encode(f"{prompt} {word}")
    assert full[: len(prefix)] == prefix, f"tokenización inestable en {word!r}"
    with torch.no_grad():
        logp = torch.log_softmax(model(torch.tensor([full])).logits[0], dim=-1)
    return sum(logp[i - 1, full[i]].item() for i in range(len(prefix), len(full)))


def main() -> None:
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32).eval()

    items = []
    for prompt, words in PROMPTS:
        words = words.split()
        scores = torch.tensor([word_logprob(model, tok, prompt, w) for w in words])
        probs = torch.softmax(scores, dim=0)
        order = torch.argsort(-probs)
        items.append({
            "prompt": prompt,
            "words": [words[i] for i in order],
            "probs": [round(probs[i].item(), 5) for i in order],
        })
        print(prompt, "→", ", ".join(f"{items[-1]['words'][k]} {items[-1]['probs'][k]:.1%}" for k in range(4)))

    literal = "DATA = " + json.dumps({"model": MODEL, "prompts": items}, ensure_ascii=False, indent=1)
    text = QMD.read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    QMD.write_text(f"{head}{START}\n{literal}\n{END}{tail}", encoding="utf-8")
    print(f"Datos insertados en {QMD} ({len(items)} frases)")


if __name__ == "__main__":
    main()
