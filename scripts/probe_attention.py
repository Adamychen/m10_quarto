"""
Prueba de viabilidad de la demo de atención (parte 2: modelo real).

Extrae los pesos de atención de un codificador tipo BERT para unas frases y
resume, por cabeza, qué hace: atención al token anterior/siguiente, a
[CLS]/[SEP], y a qué se fija la palabra objetivo. Sirve para decidir qué
frases y cabezas merece la pena mostrar. No modifica ningún fichero.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/probe_attention.py
    .venv/bin/python3 scripts/probe_attention.py --model google-bert/bert-base-multilingual-cased
"""

import argparse

import torch
from transformers import AutoModel, AutoTokenizer

DEFAULT_MODEL = "dccuchile/bert-base-spanish-wwm-cased"

# (frase, palabra objetivo). La palabra se busca como subcadena de un token.
CASES = [
    ("Me senté en el banco del parque.", "banco"),
    ("El banco cerró porque estaba en quiebra.", "banco"),
    ("La maleta no cabía en el coche porque era muy grande.", "era"),
    ("El perro persiguió al gato porque tenía hambre.", "tenía"),
    ("Los alumnos que estudiaron mucho aprobaron el examen.", "aprobaron"),
]
SPECIAL = {"[CLS]", "[SEP]", "<s>", "</s>"}


def clean(tok: str) -> str:
    return tok.replace("##", "").replace("▁", "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--top", type=int, default=8, help="cabezas a listar por frase")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModel.from_pretrained(args.model, attn_implementation="eager")
    model.eval()
    print(f"Modelo: {args.model}\n")

    for sentence, target in CASES:
        enc = tok(sentence, return_tensors="pt")
        tokens = tok.convert_ids_to_tokens(enc["input_ids"][0])
        n = len(tokens)
        idx = [i for i, t in enumerate(tokens) if target in clean(t).lower()]
        if not idx:
            print(f"## {sentence}\n   (objetivo «{target}» no encontrado en {tokens})\n")
            continue
        t = idx[0]
        with torch.no_grad():
            att = model(**enc, output_attentions=True).attentions  # L x [1,H,n,n]
        att = torch.stack([a[0] for a in att])  # [L, H, n, n]
        keep = torch.tensor([x not in SPECIAL for x in tokens])

        # Atención de la palabra objetivo, renormalizada sin tokens especiales.
        row = att[:, :, t, :] * keep
        row = row / row.sum(-1, keepdim=True).clamp_min(1e-9)
        # Qué tan concentrada es (1 = toda en un token) y a quién apunta.
        peak, arg = row.max(-1)
        special_mass = att[:, :, t, :][..., ~keep].sum(-1)

        print(f"## {sentence}")
        print(f"   tokens: {tokens}")
        print(f"   objetivo: «{tokens[t]}» (pos {t})")

        # Candidatas: pico alto fuera de sí mismo y poca masa en especiales.
        scores = []
        for l in range(att.shape[0]):
            for h in range(att.shape[1]):
                r = row[l, h].clone()
                r[t] = 0
                r = r / r.sum().clamp_min(1e-9)
                p, a = r.max(0)
                scores.append((float(p) * (1 - float(special_mass[l, h])), l, h, int(a)))
        scores.sort(reverse=True)
        for s, l, h, a in scores[: args.top]:
            tops = row[l, h].clone()
            tops[t] = 0
            top3 = tops.topk(min(3, n)).indices.tolist()
            desc = ", ".join(f"{tokens[i]} {tops[i]:.0%}" for i in top3)
            print(f"   L{l:02d} H{h:02d}  score={s:.2f}  → {desc}")
        print()

    # Perfil global de cabezas: qué hace cada una de media sobre todas las frases.
    print("## Perfil medio de cabezas (todas las frases)")
    prev = torch.zeros(12, 12)
    nxt = torch.zeros(12, 12)
    spec = torch.zeros(12, 12)
    cnt = 0
    for sentence, _ in CASES:
        enc = tok(sentence, return_tensors="pt")
        tokens = tok.convert_ids_to_tokens(enc["input_ids"][0])
        n = len(tokens)
        with torch.no_grad():
            att = model(**enc, output_attentions=True).attentions
        att = torch.stack([a[0] for a in att])
        ar = torch.arange(1, n)
        prev += att[:, :, ar, ar - 1].mean(-1)
        nxt += att[:, :, ar[:-1] - 1, ar[:-1]].mean(-1)
        sp = torch.tensor([x in SPECIAL for x in tokens])
        spec += att[..., sp].sum(-1).mean(-1)
        cnt += 1
    for name, m in (("token anterior", prev), ("token siguiente", nxt), ("[CLS]/[SEP]", spec)):
        m = m / cnt
        top = [(float(m[l, h]), l, h) for l in range(m.shape[0]) for h in range(m.shape[1])]
        top.sort(reverse=True)
        print(f"   {name}: " + ", ".join(f"L{l:02d}H{h:02d}={v:.2f}" for v, l, h in top[:6]))


if __name__ == "__main__":
    main()
