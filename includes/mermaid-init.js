// Tema Mermaid para el Módulo 10 — IA Generativa para Data Science.
// Paleta Python + extensiones semánticas (ver AGENTS.md).
//
// Esta inicialización se ejecuta antes de que Mermaid renderice cualquier
// diagrama del sitio. Los `classDef` y `style X fill:#...` explícitos de
// cada diagrama siguen teniendo precedencia sobre estos valores.

mermaid.initialize({
  startOnLoad: true,
  theme: "base",
  themeVariables: {
    // Colores primarios (azul Python)
    primaryColor:        "#4B8BBE",
    primaryBorderColor:  "#1e3a5f",
    primaryTextColor:    "#ffffff",

    // Colores secundarios (azul Python oscuro)
    secondaryColor:      "#306998",

    // Color terciario (amarillo Python)
    tertiaryColor:       "#FFD43B",

    // Fondos
    background:          "#ffffff",
    mainBkg:             "#ffffff",
    secondBkg:           "#f5f5f5",
    tertiaryBkg:         "#fff8e1",

    // Líneas
    lineColor:           "#1e3a5f",

    // Subgraphs
    clusterBkg:          "#f5f5f5",
    clusterBorder:       "#1e3a5f",

    // Tipografía
    fontFamily:          'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
    fontSize:            "14px",
  },
  flowchart: {
    curve:           "basis",
    htmlLabels:      true,
    nodeSpacing:     50,
    rankSpacing:     60,
    padding:         10,
  },
});
