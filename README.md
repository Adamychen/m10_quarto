# Módulo 10 — IA Generativa para Data Science

Sitio web del módulo 10 del **Máster en Data Science & Big Data** de la Universidad de Sevilla.

**IA Generativa para Data Science** — 3,0 ECTS | 75 horas

## 👨‍🎓 Para alumnos

### Ver el sitio online

El sitio está publicado en GitHub Pages. Accede desde la URL que se muestra en el repositorio (pestaña **Settings → Pages**).

### Abrir notebooks en Colab

Cada página tiene un badge 🟢 **Open in Colab** en la parte superior. Si es la primera vez:
1. Abre [colab.research.google.com](https://colab.research.google.com)
2. Ve a ⚙️ Settings → GitHub → **Connect to GitHub** y autoriza la app
3. Vuelve a la página y haz clic en el badge

Como alternativa: **File → Open Notebook → GitHub**, busca `Adamychen/m10_quarto` y selecciona el notebook de la carpeta `notebooks/`.

### Ejercicios evaluables

Los ejercicios evaluables están en `evaluables/hpd1-evaluables.qmd` y la extensión avanzada en `evaluables/hpd1-extension.qmd`. Se entregan como notebook `.ipynb` ejecutado con todas las celdas completas.

---

## 👨‍🏫 Para profesores

### Requisitos

- Python 3.10+
- [Quarto](https://quarto.org/docs/get-started/) 1.6+

### Clonar y preparar

```bash
git clone https://github.com/Adamychen/m10_quarto.git
cd m10_quarto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Renderizar en local

```bash
quarto render
```

Para verlo en el navegador con recarga automática:

```bash
quarto preview
```

### Estructura del proyecto

```
m10_quarto/
├── _quarto.yml                  # Configuración del sitio (sidebar, grid, tema)
├── *.qmd                        # Páginas con engine jupyter (Python)
├── evaluables/                  # Ejercicios evaluables
│   ├── hpd1-evaluables.qmd
│   └── hpd1-extension.qmd
├── images/                      # Imágenes del sitio
├── styles.css                   # Estilos CSS personalizados
├── requirements.txt             # Dependencias Python
├── generate_notebooks.sh        # Genera .ipynb desde .qmd
├── .github/workflows/
│   └── deploy.yml               # CI/CD a GitHub Pages
└── AGENTS.md                    # Instrucciones para asistentes IA
```

### Añadir o modificar contenido

1. Las páginas están en `.qmd` con `engine: jupyter`
2. Las celdas con `#| eval: true` se ejecutan durante `quarto render`
3. Edita `_quarto.yml` para cambiar el sidebar, el grid o el tema
4. Edita `styles.css` para estilos personalizados

### Despliegue

El sitio se despliega automáticamente a GitHub Pages mediante GitHub Actions (`.github/workflows/deploy.yml`) al hacer push a `main`. También puedes lanzarlo manualmente desde la pestaña **Actions** del repositorio.

### Generar notebooks .ipynb

```bash
./generate_notebooks.sh
```

### Personalizar el grid

En `_quarto.yml`:

```yaml
format:
  html:
    grid:
      sidebar-width: 260px
      body-width: 850px
      margin-width: 0px
      gutter-width: 1.5rem
```

---

## Autoría

**Departamento de Ciencias de la Computación e Inteligencia Artificial** — Universidad de Sevilla

- Adam Leiyi Chen Abolacio — `achen@us.es`
- Fernando Sancho Caparrini — `fsancho@us.es`
