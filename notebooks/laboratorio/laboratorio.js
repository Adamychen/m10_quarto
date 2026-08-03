(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const svgText = (value) => escapeHtml(value);

  // Tabs
  $$(".tab-button").forEach((button) => {
    button.addEventListener("click", () => {
      const panelName = button.dataset.panel;
      $$(".tab-button").forEach((item) => item.classList.toggle("is-active", item === button));
      $$(".lab-panel").forEach((panel) => {
        const active = panel.dataset.panelContent === panelName;
        panel.hidden = !active;
        panel.classList.toggle("is-active", active);
      });
    });
  });

  // 01. Toy BPE tokenizer
  const tokenInput = $("#token-input");
  const tokenOutput = $("#token-output");
  const tokenIds = $("#token-ids");
  const tokenSteps = $("#token-steps");
  const tokenCount = $("#token-count");

  const mergeRules = [
    ["t", "h"], ["h", "e"], ["i", "n"], ["e", "r"], ["r", "e"],
    ["a", "t"], ["i", "o"], ["o", "n"], ["u", "n"], ["e", "m"],
    ["e", "d"], ["d", "d"], ["d", "i"], ["i", "n"], ["g", "s"],
    ["h", "a"], ["h", "a", "p", "p", "i"], ["h", "a", "p", "p"],
    ["h", "a", "p"], ["h", "a"], ["n", "e", "s", "s"], ["i", "n", "g"],
    ["t", "i", "o", "n"], ["e", "m", "b", "e", "d", "d", "i", "n", "g", "s"],
    ["t", "r", "a", "n", "s", "f", "o", "r", "m", "e", "r"],
    ["r", "e", "t", "r", "i", "e", "v", "a", "l"]
  ];

  const preferredTokenizations = {
    unhappiness: ["un", "happi", "ness"],
    transformer: ["transform", "er"],
    embeddings: ["embedding", "s"],
    retrieval: ["retriev", "al"],
    attention: ["attention"]
  };

  const segmentWord = (word) => {
    const normalized = word.toLowerCase().replace(/[^a-záéíóúüñ0-9]/gi, "");
    let units = Array.from(normalized);
    const steps = [{ units: [...units], rule: "vocabulario inicial" }];

    const preferred = preferredTokenizations[normalized];
    if (preferred) {
      preferred.forEach((target) => {
        for (let index = 0; index < units.length; index += 1) {
          let collected = "";
          let end = index;
          while (end < units.length && collected.length < target.length) {
            collected += units[end];
            end += 1;
          }
          if (collected === target) {
            units.splice(index, end - index, target);
            steps.push({ units: [...units], rule: `merge ${target}` });
            break;
          }
        }
      });
      return { units: units.length ? units : ["∅"], steps };
    }

    mergeRules.forEach((rule) => {
      for (let index = 0; index <= units.length - rule.length; index += 1) {
        if (rule.every((part, offset) => units[index + offset] === part)) {
          units.splice(index, rule.length, rule.join(""));
          steps.push({ units: [...units], rule: rule.join(" + ") });
          break;
        }
      }
    });

    return { units: units.length ? units : ["∅"], steps };
  };

  const renderTokens = () => {
    const { units, steps } = segmentWord(tokenInput.value);
    tokenOutput.innerHTML = units.map((unit, index) => {
      const merged = unit.length > 1;
      return `<span class="token-chip${merged ? " is-merged" : ""}" title="Token ${index + 1}">${escapeHtml(unit)}</span>`;
    }).join("");
    tokenIds.innerHTML = units.map((unit, index) => `<span class="token-id">${String((unit.charCodeAt(0) * 17 + index * 31) % 997).padStart(3, "0")}</span>`).join("");
    tokenCount.textContent = `${units.length} token${units.length === 1 ? "" : "s"}`;
    tokenSteps.innerHTML = steps.map((step, index) => {
      const renderedUnits = step.units.map((unit) => escapeHtml(unit)).join("  |  ");
      const rule = index === 0 ? step.rule : `<strong>${escapeHtml(step.rule)}</strong>`;
      return `<div class="merge-step"><span class="merge-step-number">${String(index).padStart(2, "0")}</span><span class="merge-step-code">${rule} <span class="step-arrow">→</span> ${renderedUnits}</span></div>`;
    }).join("");
  };

  $("#token-run").addEventListener("click", renderTokens);
  tokenInput.addEventListener("input", renderTokens);
  $$('[data-token-example]').forEach((button) => {
    button.addEventListener("click", () => {
      tokenInput.value = button.dataset.tokenExample;
      renderTokens();
    });
  });
  renderTokens();

  // 02. Attention matrix
  const attentionData = {
    cat: {
      tokens: ["El", "gato", "duerme", "en", "la", "alfombra"],
      relations: { duerme: ["gato", "alfombra"], gato: ["El", "duerme"], alfombra: ["en", "la"] }
    },
    model: {
      tokens: ["Los", "modelos", "aprenden", "representaciones"],
      relations: { aprenden: ["modelos", "representaciones"], modelos: ["Los", "aprenden"], representaciones: ["aprenden"] }
    }
  };
  const attentionSelect = $("#attention-sentence");
  const attentionFocus = $("#attention-focus");
  const attentionFocusLabel = $("#attention-focus-label");
  const attentionGrid = $("#attention-grid");
  const attentionStrip = $("#attention-token-strip");
  const attentionExplain = $("#attention-explain");

  const attentionWeights = (tokens, focusIndex, key) => {
    const focus = tokens[focusIndex];
    const related = attentionData[key].relations[focus] || [];
    const raw = tokens.map((token, index) => {
      if (index === focusIndex) return 0.68;
      if (related.includes(token)) return 0.92;
      return 0.11 + ((index * 13 + focusIndex * 7) % 9) / 100;
    });
    const total = raw.reduce((sum, value) => sum + value, 0);
    return raw.map((value) => value / total);
  };

  const renderAttention = () => {
    const data = attentionData[attentionSelect.value];
    attentionFocus.max = String(data.tokens.length - 1);
    attentionFocus.value = String(clamp(Number(attentionFocus.value), 0, data.tokens.length - 1));
    const focusIndex = Number(attentionFocus.value);
    const focusToken = data.tokens[focusIndex];
    const weights = attentionWeights(data.tokens, focusIndex, attentionSelect.value);
    attentionFocusLabel.textContent = focusToken;

    const cell = 50;
    const left = 98;
    const top = 40;
    const width = left + data.tokens.length * cell + 12;
    const height = top + data.tokens.length * cell + 25;
    let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Matriz de atención para ${svgText(focusToken)}">`;
    svg += `<text x="${left - 10}" y="18" text-anchor="end" fill="#86939b" font-size="8" font-family="monospace">QUERY ↓ / KEY →</text>`;
    data.tokens.forEach((token, index) => {
      const x = left + index * cell + cell / 2;
      svg += `<text x="${x}" y="${top - 10}" text-anchor="middle" fill="${index === focusIndex ? "#e65100" : "#66747d"}" font-size="9" font-family="monospace" font-weight="${index === focusIndex ? "700" : "400"}">${svgText(token)}</text>`;
      const y = top + index * cell + cell / 2 + 3;
      svg += `<text x="${left - 10}" y="${y}" text-anchor="end" fill="${index === focusIndex ? "#e65100" : "#66747d"}" font-size="9" font-family="monospace" font-weight="${index === focusIndex ? "700" : "400"}">${svgText(token)}</text>`;
    });
    data.tokens.forEach((rowToken, row) => {
      const rowWeights = row === focusIndex ? weights : attentionWeights(data.tokens, row, attentionSelect.value);
      rowWeights.forEach((weight, column) => {
        const x = left + column * cell + 3;
        const y = top + row * cell + 3;
        const opacity = 0.08 + weight * 0.92;
        const active = row === focusIndex;
        svg += `<rect x="${x}" y="${y}" width="${cell - 6}" height="${cell - 6}" fill="#4b8bbe" fill-opacity="${opacity.toFixed(3)}" stroke="${active ? "#e65100" : "#dfe7ea"}" stroke-width="${active ? "1.8" : "0.8"}" rx="2"><title>${svgText(rowToken)} consulta a ${svgText(data.tokens[column])}: ${(weight * 100).toFixed(1)}%</title></rect>`;
        if (active) {
          svg += `<text x="${x + (cell - 6) / 2}" y="${y + 26}" text-anchor="middle" fill="${weight > 0.18 ? "#fff" : "#24415a"}" font-size="8" font-family="monospace">${(weight * 100).toFixed(0)}%</text>`;
        }
      });
    });
    svg += "</svg>";
    attentionGrid.innerHTML = svg;
    attentionStrip.innerHTML = data.tokens.map((token, index) => `<button class="attention-token${index === focusIndex ? " is-focus" : ""}" type="button" data-attention-index="${index}">${escapeHtml(token)}</button>`).join("");
    $$('[data-attention-index]').forEach((button) => button.addEventListener("click", () => {
      attentionFocus.value = button.dataset.attentionIndex;
      renderAttention();
    }));
    const important = data.tokens.map((token, index) => ({ token, weight: weights[index] })).sort((a, b) => b.weight - a.weight).slice(0, 3);
    attentionExplain.innerHTML = `<strong>${escapeHtml(focusToken)}</strong> distribuye su atención principalmente entre ${important.map((item) => `<b>${escapeHtml(item.token)}</b> (${(item.weight * 100).toFixed(0)}%)`).join(", ")}. En un Transformer real, estos pesos se calculan por cabeza y por capa.`;
  };

  attentionSelect.addEventListener("change", renderAttention);
  attentionFocus.addEventListener("input", renderAttention);
  renderAttention();

  // 03. Embedding map
  const embeddingItems = [
    { label: "gato", group: "animales", x: 2.5, y: 7.8, note: "animal doméstico" },
    { label: "felino", group: "animales", x: 3.3, y: 8.5, note: "sinónimo aproximado" },
    { label: "gatito", group: "animales", x: 2.1, y: 8.8, note: "animal doméstico" },
    { label: "perro", group: "animales", x: 3.9, y: 7.4, note: "animal doméstico" },
    { label: "transformer", group: "modelos", x: 7.3, y: 7.5, note: "arquitectura" },
    { label: "atención", group: "modelos", x: 8.1, y: 8.5, note: "mecanismo" },
    { label: "embeddings", group: "modelos", x: 8.8, y: 7.2, note: "representación" },
    { label: "vector DB", group: "modelos", x: 7.7, y: 6.5, note: "recuperación" },
    { label: "mercado", group: "finanzas", x: 7.7, y: 2.6, note: "economía" },
    { label: "acciones", group: "finanzas", x: 8.8, y: 3.6, note: "mercado" },
    { label: "bolsa", group: "finanzas", x: 7.0, y: 3.5, note: "mercado" },
    { label: "inflación", group: "finanzas", x: 8.4, y: 2.1, note: "economía" }
  ];
  const embeddingQuery = $("#embedding-query");
  const embeddingPlot = $("#embedding-plot");
  const embeddingRanking = $("#embedding-ranking");
  const embeddingMetrics = $("#embedding-metrics");
  const embeddingRankingLabel = $("#embedding-ranking-label");
  const groupColors = { animales: "#4b8bbe", modelos: "#e65100", finanzas: "#2e7d32" };

  const queryPosition = (query) => {
    const text = query.toLowerCase();
    if (/gato|felino|animal|perro|mascota/.test(text)) return { x: 3.0, y: 8.0, group: "animales" };
    if (/transform|atención|atencion|embedding|vector|modelo/.test(text)) return { x: 7.9, y: 7.5, group: "modelos" };
    if (/mercado|acción|accion|bolsa|inflación|inflacion|finanz/.test(text)) return { x: 8.0, y: 3.0, group: "finanzas" };
    const seed = [...text].reduce((sum, char) => sum + char.charCodeAt(0), 0);
    return { x: 4 + (seed % 20) / 10, y: 4 + ((seed * 7) % 20) / 10, group: "consulta" };
  };

  const cosineSimilarity = (a, b) => {
    const dot = a[0] * b[0] + a[1] * b[1];
    const normaA = Math.hypot(a[0], a[1]);
    const normaB = Math.hypot(b[0], b[1]);
    return normaA && normaB ? dot / (normaA * normaB) : 0;
  };

  const renderEmbeddings = () => {
    const query = embeddingQuery.value.trim() || "consulta";
    const target = queryPosition(query);
    const queryVector = [target.x - 5, target.y - 5];
    const ranked = embeddingItems.map((item) => {
      const vector = [item.x - 5, item.y - 5];
      const distance = Math.hypot(target.x - item.x, target.y - item.y);
      const cosine = cosineSimilarity(queryVector, vector);
      const localScore = clamp(1 - distance / 7, 0, 1);
      return { ...item, distance, cosine, localScore };
    }).sort((a, b) => b.localScore - a.localScore);

    const width = 680;
    const height = 360;
    const pad = { left: 38, right: 18, top: 20, bottom: 36 };
    const px = (x) => pad.left + (x / 10) * (width - pad.left - pad.right);
    const py = (y) => height - pad.bottom - (y / 10) * (height - pad.top - pad.bottom);
    let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Espacio de embeddings con consulta ${svgText(query)}">`;
    for (let tick = 0; tick <= 10; tick += 1) {
      svg += `<line x1="${px(tick)}" y1="${py(0)}" x2="${px(tick)}" y2="${py(10)}" stroke="#e9edef" stroke-width="1"/>`;
      svg += `<line x1="${px(0)}" y1="${py(tick)}" x2="${px(10)}" y2="${py(tick)}" stroke="#e9edef" stroke-width="1"/>`;
    }
    svg += `<line x1="${px(0)}" y1="${py(0)}" x2="${px(10)}" y2="${py(0)}" stroke="#9eabb1"/><line x1="${px(0)}" y1="${py(0)}" x2="${px(0)}" y2="${py(10)}" stroke="#9eabb1"/>`;
    svg += `<text x="${px(10)}" y="${height - 8}" text-anchor="end" fill="#8a989f" font-size="9" font-family="monospace">dimensión 1</text>`;
    svg += `<text x="12" y="${py(10)}" fill="#8a989f" font-size="9" font-family="monospace" transform="rotate(-90 12 ${py(10)})">dimensión 2</text>`;

    ["animales", "modelos", "finanzas"].forEach((group) => {
      const items = embeddingItems.filter((item) => item.group === group);
      const center = items.reduce((acc, item) => ({ x: acc.x + item.x / items.length, y: acc.y + item.y / items.length }), { x: 0, y: 0 });
      svg += `<ellipse cx="${px(center.x)}" cy="${py(center.y)}" rx="${group === "animales" ? 78 : 84}" ry="${group === "animales" ? 38 : 40}" fill="${groupColors[group]}" fill-opacity="0.06" stroke="${groupColors[group]}" stroke-opacity="0.28" stroke-dasharray="4 4"/>`;
    });

    ranked.forEach((item) => {
      const color = groupColors[item.group] || "#8b969b";
      const isTop = item === ranked[0];
      svg += `<circle cx="${px(item.x)}" cy="${py(item.y)}" r="${isTop ? 7 : 5}" fill="${color}" stroke="#fff" stroke-width="2"><title>${svgText(item.label)} · proximidad ${(item.localScore * 100).toFixed(0)}%</title></circle>`;
      svg += `<text x="${px(item.x) + 9}" y="${py(item.y) + 3}" fill="#34434c" font-size="9" font-family="monospace">${svgText(item.label)}</text>`;
    });
    svg += `<line x1="${px(target.x) - 9}" y1="${py(target.y)}" x2="${px(target.x) + 9}" y2="${py(target.y)}" stroke="#c62828" stroke-width="2"/><line x1="${px(target.x)}" y1="${py(target.y) - 9}" x2="${px(target.x)}" y2="${py(target.y) + 9}" stroke="#c62828" stroke-width="2"/><circle cx="${px(target.x)}" cy="${py(target.y)}" r="12" fill="none" stroke="#c62828" stroke-dasharray="3 3"/><text x="${px(target.x) + 13}" y="${py(target.y) - 12}" fill="#c62828" font-size="9" font-family="monospace">consulta</text>`;
    svg += "</svg>";
    embeddingPlot.innerHTML = svg;

    embeddingRankingLabel.textContent = query;
    embeddingRanking.innerHTML = ranked.slice(0, 3).map((item, index) => `<div class="ranking-item"><span class="ranking-number">0${index + 1}</span><span><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.group)} · ${escapeHtml(item.note)}</small></span><span class="ranking-score">${(item.localScore * 100).toFixed(0)}%</span></div>`).join("");
    embeddingMetrics.innerHTML = [
      ["grupo detectado", target.group],
      ["dimensión visual", "2D"],
      ["vecinos mostrados", "3 / 12"],
      ["métrica", "proximidad local"]
    ].map(([label, value]) => `<div class="metric-row"><span class="metric-label">${label}</span><span class="metric-value">${escapeHtml(value)}</span></div>`).join("");
  };

  $("#embedding-run").addEventListener("click", renderEmbeddings);
  embeddingQuery.addEventListener("keydown", (event) => {
    if (event.key === "Enter") renderEmbeddings();
  });
  $$('[data-embedding-example]').forEach((button) => {
    button.addEventListener("click", () => {
      embeddingQuery.value = button.dataset.embeddingExample;
      renderEmbeddings();
    });
  });
  renderEmbeddings();

  // 04. RAG demo
  const ragDocuments = [
    { id: "DOC-01", title: "Atención y contexto", tags: ["atención", "contexto", "transformer", "secuencia"], text: "La atención permite que cada posición combine información de otras posiciones mediante consultas, claves y valores." },
    { id: "DOC-02", title: "Embeddings de frases", tags: ["embedding", "embeddings", "frases", "vector", "semántica"], text: "Un embedding de frase resume una consulta en un vector para poder compararla con documentos semánticamente cercanos." },
    { id: "DOC-03", title: "Búsqueda vectorial", tags: ["vector", "índice", "hnsw", "búsqueda", "vecinos"], text: "Las bases de datos vectoriales utilizan índices aproximados para recuperar vecinos cercanos sin comparar todos los vectores." },
    { id: "DOC-04", title: "RAG y contexto externo", tags: ["rag", "recuperación", "contexto", "documentos", "respuesta"], text: "RAG recupera documentos relevantes y los incorpora al contexto del modelo antes de generar una respuesta." },
    { id: "DOC-05", title: "Tokenización BPE", tags: ["token", "tokenización", "bpe", "vocabulario", "subpalabra"], text: "BPE construye un vocabulario fusionando pares frecuentes y permite representar palabras raras mediante subpalabras." },
    { id: "DOC-06", title: "Evaluar un RAG", tags: ["evaluación", "recall", "faithfulness", "ragas", "métrica"], text: "Un sistema RAG debe evaluar tanto la recuperación de contexto como la fidelidad de la respuesta generada." }
  ];
  const ragQuery = $("#rag-query");
  const ragResults = $("#rag-results");
  const ragAnswer = $("#rag-answer");
  const ragSources = $("#rag-sources");
  const ragScoreLabel = $("#rag-score-label");
  const ragTrace = $("#rag-trace");
  let ragTimers = [];

  const scoreDocument = (document, query) => {
    const queryTerms = query.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").split(/\W+/).filter((term) => term.length > 3);
    const haystack = `${document.title} ${document.tags.join(" ")} ${document.text}`.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const matches = queryTerms.filter((term) => haystack.includes(term));
    return { ...document, matches, score: matches.length / Math.max(1, Math.min(queryTerms.length, 4)) };
  };

  const setRagNode = (name) => {
    const order = ["query", "embed", "search", "prompt", "answer"];
    const current = order.indexOf(name);
    $$("[data-rag-node]").forEach((node) => {
      const index = order.indexOf(node.dataset.ragNode);
      node.classList.toggle("is-active", index === current);
      node.classList.toggle("is-done", index < current);
    });
  };

  const finishRag = (query, ranked) => {
    const top = ranked.slice(0, 3);
    ragResults.innerHTML = top.map((document, index) => `<article class="rag-result"><span class="rag-result-rank">0${index + 1}</span><span><strong>${escapeHtml(document.title)}</strong><p>${escapeHtml(document.text)}</p></span><span class="rag-result-score">${Math.round((document.score || 0.2) * 100)}%</span></article>`).join("");
    ragScoreLabel.textContent = `${top.length} documentos / top-k`;
    const sourceNames = top.map((document) => document.id).join(", ");
    ragAnswer.innerHTML = `La atención permite que cada posición de una secuencia consulte otras posiciones mediante representaciones de <strong>query</strong>, <strong>key</strong> y <strong>value</strong>. Esto permite incorporar contexto sin procesar la secuencia únicamente paso a paso. En un sistema RAG, esta explicación se obtiene a partir de los documentos recuperados antes de generar la respuesta.`;
    ragSources.textContent = `Fuentes utilizadas: ${sourceNames} · Consulta: “${query}”`;
    ragTrace.innerHTML = `<strong>RECORRIDO COMPLETO</strong> · embedding calculado · ${top.length} documentos recuperados · contexto preparado · respuesta simulada con fuentes.`;
    setRagNode("answer");
  };

  const runRag = () => {
    ragTimers.forEach((timer) => clearTimeout(timer));
    ragTimers = [];
    const query = ragQuery.value.trim() || "consulta vacía";
    const ranked = ragDocuments.map((document) => scoreDocument(document, query)).sort((a, b) => b.score - a.score);
    setRagNode("query");
    ragTrace.innerHTML = `<strong>INICIO</strong> · recibiendo consulta del usuario...`;
    ["embed", "search", "prompt"].forEach((node, index) => {
      ragTimers.push(setTimeout(() => {
        setRagNode(node);
        const messages = {
          embed: "vector de consulta calculado...",
          search: "comparando con el índice vectorial...",
          prompt: "seleccionando contexto para el modelo..."
        };
        ragTrace.innerHTML = `<strong>${node.toUpperCase()}</strong> · ${messages[node]}`;
      }, (index + 1) * 430));
    });
    ragTimers.push(setTimeout(() => finishRag(query, ranked), 1800));
  };

  $("#rag-run").addEventListener("click", runRag);
  ragQuery.addEventListener("keydown", (event) => {
    if (event.key === "Enter") runRag();
  });
  runRag();
})();
