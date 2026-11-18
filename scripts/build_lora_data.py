"""
Precalcula los datos de la demo de LoRA (demos/lora.qmd).

1. Lee el config.json real de cada modelo, cuenta sus parámetros (instanciado en
   el dispositivo «meta», sin descargar pesos) y guarda la forma de cada capa
   lineal de un bloque Transformer (q, k, v, o, gate, up, down).
2. Comprueba que la fórmula de la demo, r · (entrada + salida) · capas, coincide
   con lo que cuenta `peft` para varias configuraciones.
3. Dibuja la palabra «LoRA» en una matriz de 48×48 para la parte 2.

El resultado se inserta como literal Python entre los marcadores
DATA-START / DATA-END de la demo.

Uso (desde la raíz del proyecto):
    .venv/bin/python3 scripts/build_lora_data.py
"""

import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
from peft import LoraConfig, get_peft_model
from transformers import AutoConfig, AutoModelForCausalLM

QMD = Path(__file__).resolve().parent.parent / "demos" / "lora.qmd"
START, END = "# DATA-START", "# DATA-END"

# Modelos sin acceso restringido, para que el alumno pueda comprobarlo él mismo.
MODELS = [
    ("Qwen/Qwen3-0.6B", "0,6B"),
    ("Qwen/Qwen3-8B", "8B"),
    ("Qwen/Qwen3-32B", "32B"),
    ("Qwen/Qwen2.5-72B-Instruct", "72B"),
]
MODULES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
CHECKS = [(8, ["q_proj", "v_proj"]), (16, ["q_proj", "k_proj", "v_proj", "o_proj"]), (64, MODULES)]


def build_model(name):
    cfg = AutoConfig.from_pretrained(name)
    with torch.device("meta"):
        model = AutoModelForCausalLM.from_config(cfg)
    return cfg, model


def shapes(model):
    """(entrada, salida) de cada módulo lineal del primer bloque."""
    layer = model.model.layers[0]
    found = {}
    for mod_name, mod in layer.named_modules():
        short = mod_name.split(".")[-1]
        if short in MODULES:
            found[short] = [mod.in_features, mod.out_features]
    return {m: found[m] for m in MODULES}


def models_data():
    out = []
    for name, label in MODELS:
        cfg, model = build_model(name)
        total = sum(p.numel() for p in model.parameters())
        dims = shapes(model)
        layers = cfg.num_hidden_layers
        for r, targets in CHECKS:
            formula = sum(r * sum(dims[m]) for m in targets) * layers
            _, fresh = build_model(name)
            pm = get_peft_model(fresh, LoraConfig(r=r, target_modules=targets))
            real = sum(p.numel() for p in pm.parameters() if p.requires_grad)
            assert formula == real, (name, r, targets, formula, real)
        print(f"{name}: {total:,} parámetros, {layers} capas, fórmula verificada con peft")
        out.append({"name": name, "label": label, "total": total, "layers": layers, "dims": dims})
    return out


def lora_image(size=48):
    """La palabra «LoRA» ocupando casi todo el ancho, en negro sobre blanco."""
    big = size * 8
    img = Image.new("L", (big, big), 255)
    draw = ImageDraw.Draw(img)
    font_size = big // 2
    while True:
        font = ImageFont.load_default(size=font_size)
        box = draw.textbbox((0, 0), "LoRA", font=font)
        if box[2] - box[0] <= big * 0.9:
            break
        font_size -= 4
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text(((big - w) / 2 - box[0], (big - h) / 2 - box[1]), "LoRA", font=font, fill=0)
    pixels = np.asarray(img.resize((size, size), Image.LANCZOS))
    # 16 niveles de gris, una cadena hexadecimal por fila (0 = negro, f = blanco)
    return ["".join("0123456789abcdef"[v // 16] for v in row) for row in pixels]


def main():
    data = {"models": models_data(), "image": lora_image()}
    literal = "DATA = " + json.dumps(data, ensure_ascii=False, indent=1)
    text = QMD.read_text(encoding="utf-8")
    i, j = text.index(START) + len(START), text.index(END)
    QMD.write_text(text[:i] + "\n" + literal + "\n" + text[j:], encoding="utf-8")
    print(f"Datos escritos en {QMD}")


if __name__ == "__main__":
    main()
