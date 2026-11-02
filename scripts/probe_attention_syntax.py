"""
Segunda prueba de viabilidad de la demo de atención: relaciones sintácticas.

Para frases con relaciones etiquetadas a mano (determinante→nombre,
adjetivo→nombre, sujeto→verbo, objeto→verbo, preposición→complemento),
mide qué cabezas de un codificador tipo BERT atienden a la palabra relacionada
(en cualquiera de los dos sentidos) y cuánto por encima del azar. No modifica
ningún fichero.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/probe_attention_syntax.py
"""

import argparse
from collections import defaultdict

import torch
from transformers import AutoModel, AutoTokenizer

DEFAULT_MODEL = "dccuchile/bert-base-spanish-wwm-cased"

# Frase como lista de palabras (sin puntuación) y relaciones (dependiente, núcleo)
# como índices de palabra. Etiquetadas a mano.
CASES = [
    (["El", "perro", "grande", "persiguió", "al", "gato", "negro"],
     {"det-nombre": [(0, 1), (4, 5)], "adj-nombre": [(2, 1), (6, 5)],
      "sujeto-verbo": [(1, 3)], "objeto-verbo": [(5, 3)]}),
    (["La", "profesora", "explicó", "la", "lección", "difícil", "a", "los", "alumnos"],
     {"det-nombre": [(0, 1), (3, 4), (7, 8)], "adj-nombre": [(5, 4)],
      "sujeto-verbo": [(1, 2)], "objeto-verbo": [(4, 2)]}),
    (["Mi", "hermana", "pequeña", "compró", "unos", "libros", "viejos", "en", "la", "librería"],
     {"det-nombre": [(0, 1), (4, 5), (8, 9)], "adj-nombre": [(2, 1), (6, 5)],
      "sujeto-verbo": [(1, 3)], "objeto-verbo": [(5, 3)], "prep-complemento": [(7, 9)]}),
    (["Los", "alumnos", "que", "estudiaron", "mucho", "aprobaron", "el", "examen", "final"],
     {"det-nombre": [(0, 1), (6, 7)], "adj-nombre": [(8, 7)],
      "sujeto-verbo": [(1, 5)], "objeto-verbo": [(7, 5)]}),
    (["El", "equipo", "de", "la", "ciudad", "ganó", "el", "partido", "importante"],
     {"det-nombre": [(0, 1), (3, 4), (6, 7)], "adj-nombre": [(8, 7)],
      "sujeto-verbo": [(1, 5)], "objeto-verbo": [(7, 5)], "prep-complemento": [(2, 4)]}),
    (["Una", "mujer", "joven", "abrió", "la", "puerta", "de", "madera"],
     {"det-nombre": [(0, 1), (4, 5)], "adj-nombre": [(2, 1)],
      "sujeto-verbo": [(1, 3)], "objeto-verbo": [(5, 3)], "prep-complemento": [(6, 7)]}),
]


def word_attention(att: torch.Tensor, word_ids: list, n_words: int) -> torch.Tensor:
    """[L,H,n,n] sobre tokens → [L,H,w,w] sobre palabras (suma al destino, media al origen)."""
    L, H, _, _ = att.shape
    out = torch.zeros(L, H, n_words, n_words)
    for dst in range(n_words):
        dst_tok = [i for i, w in enumerate(word_ids) if w == dst]
        for src in range(n_words):
            src_tok = [i for i, w in enumerate(word_ids) if w == src]
            out[:, :, src, dst] = att[:, :, src_tok][:, :, :, dst_tok].sum(-1).mean(-1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--top", type=int, default=3, help="cabezas a listar por relación")
    ap.add_argument("--min-dist", type=int, default=1,
                    help="distancia mínima entre palabras del par (2 = excluir adyacentes)")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModel.from_pretrained(args.model, attn_implementation="eager")
    model.eval()
    print(f"Modelo: {args.model}\n")

    # Por relación: atención dependiente→núcleo y núcleo→dependiente, y la
    # atención media a cualquier otra palabra (referencia de azar).
    fwd = defaultdict(list)
    bwd = defaultdict(list)
    base = []
    for words, rels in CASES:
        enc = tok(words, is_split_into_words=True, return_tensors="pt")
        wids = enc.word_ids(0)
        n_words = len(words)
        with torch.no_grad():
            att = torch.stack([a[0] for a in model(**enc, output_attentions=True).attentions])
        wa = word_attention(att, wids, n_words)
        # Renormalizar sobre palabras (sin especiales) para comparar con 1/(w-1).
        wa = wa / wa.sum(-1, keepdim=True).clamp_min(1e-9)
        eye = torch.eye(n_words, dtype=torch.bool)
        base.append(wa.masked_fill(eye, 0).sum(-1).div(n_words - 1).mean(-1))
        for rel, pairs in rels.items():
            for dep, head in pairs:
                if abs(dep - head) < args.min_dist:
                    continue
                fwd[rel].append(wa[:, :, dep, head])
                bwd[rel].append(wa[:, :, head, dep])
    baseline = torch.stack(base).mean(0)  # [L,H], atención media por palabra

    for rel in fwd:
        if not fwd[rel]:
            continue
        f = torch.stack(fwd[rel]).mean(0)
        b = torch.stack(bwd[rel]).mean(0)
        best = torch.maximum(f, b)
        print(f"## {rel}  ({len(fwd[rel])} casos)")
        flat = [(float(best[l, h]), l, h) for l in range(12) for h in range(12)]
        flat.sort(reverse=True)
        for v, l, h in flat[: args.top]:
            way = "dep→núcleo" if f[l, h] >= b[l, h] else "núcleo→dep"
            lift = v / float(baseline[l, h].clamp_min(1e-9))
            print(f"   L{l:02d} H{h:02d}  atención={v:.0%}  {way}  ×{lift:.1f} sobre la media")
        print()


if __name__ == "__main__":
    main()
