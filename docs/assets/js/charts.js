// Gráficos interativos (Chart.js) -- lê as cores diretamente das custom
// properties do CSS, então segue automaticamente o tema claro/escuro do
// navegador sem duplicar a paleta aqui.
window.SiteCharts = (function () {
  var CRIME_ORDER = [
    "Ameaça",
    "Estupro",
    "Feminicídio Consumado",
    "Feminicídio Tentado",
    "Lesão Corporal",
  ];
  var CRIME_VAR = {
    "Ameaça": "--crime-ameaca",
    "Estupro": "--crime-estupro",
    "Feminicídio Consumado": "--crime-fem-consumado",
    "Feminicídio Tentado": "--crime-fem-tentado",
    "Lesão Corporal": "--crime-lesao",
  };

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function crimeColor(tipo) {
    return cssVar(CRIME_VAR[tipo] || "--muted");
  }
  function ink(name) {
    return cssVar(name);
  }

  function fmtInt(n) {
    return Number(n).toLocaleString("pt-BR");
  }

  function baseGridColor() {
    return cssVar("--grid");
  }
  function baseTickColor() {
    return cssVar("--ink-secondary");
  }

  // Renderiza a legenda em HTML (fora do canvas) para os tipos presentes --
  // Chart.js já tem legenda própria, mas manter uma versão HTML garante que
  // o rótulo nunca dependa só de cor (checklist de acessibilidade).
  function renderLegend(container, tipos) {
    container.innerHTML = "";
    container.className = "legend";
    tipos.forEach(function (tipo) {
      var item = document.createElement("span");
      item.className = "item";
      var sw = document.createElement("span");
      sw.className = "swatch";
      sw.style.background = crimeColor(tipo);
      item.appendChild(sw);
      item.appendChild(document.createTextNode(tipo));
      container.appendChild(item);
    });
  }

  /**
   * Série anual por tipo de crime (linha, escala log) -- réplica interativa
   * da Seção 2 de analise_exploratoria.ipynb.
   * dados: [{ano, tipo_crime, casos_total}]
   */
  function renderTrendChart(canvas, dados, opts) {
    opts = opts || {};
    var anos = Array.from(new Set(dados.map(function (d) { return d.ano; }))).sort();
    var datasets = CRIME_ORDER.filter(function (tipo) {
      return dados.some(function (d) { return d.tipo_crime === tipo; });
    }).map(function (tipo) {
      var porAno = {};
      dados.filter(function (d) { return d.tipo_crime === tipo; }).forEach(function (d) {
        porAno[d.ano] = d.casos_total;
      });
      return {
        label: tipo,
        data: anos.map(function (ano) { return porAno[ano] ?? null; }),
        borderColor: crimeColor(tipo),
        backgroundColor: crimeColor(tipo),
        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 5,
        tension: 0.15,
        spanGaps: true,
      };
    });

    return new Chart(canvas, {
      type: "line",
      data: { labels: anos, datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "nearest", intersect: false },
        scales: {
          x: {
            grid: { color: baseGridColor() },
            ticks: { color: baseTickColor() },
          },
          y: {
            type: opts.logScale ? "logarithmic" : "linear",
            grid: { color: baseGridColor() },
            ticks: {
              color: baseTickColor(),
              callback: function (v) { return fmtInt(v); },
            },
            title: {
              display: true,
              text: opts.logScale ? "Casos no estado (escala log)" : "Casos no estado",
              color: baseTickColor(),
            },
          },
        },
        plugins: {
          legend: { display: !!opts.showLegend, labels: { color: baseTickColor() } },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return ctx.dataset.label + ": " + fmtInt(ctx.parsed.y);
              },
            },
          },
        },
      },
    });
  }

  /**
   * Sazonalidade mensal (barras) para um único tipo de crime, com * nos
   * meses em destaque (post-hoc Mann-Whitney/Holm-Bonferroni já calculado
   * pela notebook -- este gráfico só visualiza, não recalcula nada).
   * destaques: [{tipo_crime, mes, mes_nome, media_casos, destaque_5pct, direcao}]
   */
  function renderSeasonalityChart(canvas, destaquesTipo) {
    var meses = destaquesTipo.slice().sort(function (a, b) { return a.mes - b.mes; });
    var cor = crimeColor(meses[0] ? meses[0].tipo_crime : "");

    var chart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: meses.map(function (m) { return m.mes_nome; }),
        datasets: [
          {
            label: "Média de casos por mês",
            data: meses.map(function (m) { return m.media_casos; }),
            backgroundColor: cor,
            borderRadius: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false }, ticks: { color: baseTickColor() } },
          y: {
            grid: { color: baseGridColor() },
            ticks: { color: baseTickColor() },
            title: { display: true, text: "Média de casos/mês", color: baseTickColor() },
          },
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                var m = meses[ctx.dataIndex];
                var base = "Média: " + m.media_casos.toFixed(0) + " casos/mês";
                if (m.destaque_5pct) {
                  base += " — destaque (" + m.direcao + ", p ajustado=" + m.p_valor_ajustado_holm.toExponential(1) + ")";
                }
                return base;
              },
            },
          },
        },
      },
    });

    return chart;
  }

  /**
   * Heatmap 5x5 de correlação, em CSS grid puro (sem plugin de matrix) --
   * matriz: objeto { tipo_a: { tipo_b: rho, ... }, ... } (a partir do
   * inferencial_correlacao_matriz_*.json, orient="records" convertido em
   * dicionário pelo caller).
   */
  function renderCorrelationHeatmap(container, matrizPorLinha, ordem) {
    ordem = ordem || CRIME_ORDER;
    container.innerHTML = "";
    container.style.display = "grid";
    container.style.gridTemplateColumns = "auto repeat(" + ordem.length + ", 1fr)";
    container.style.gap = "2px";
    container.style.fontSize = "0.78rem";

    function cell(text, style) {
      var div = document.createElement("div");
      div.textContent = text;
      div.style.padding = "0.5rem";
      div.style.textAlign = "center";
      Object.assign(div.style, style || {});
      return div;
    }

    container.appendChild(cell(""));
    ordem.forEach(function (tipo) {
      container.appendChild(
        cell(tipo, { color: "var(--ink-secondary)", fontWeight: 600, writingMode: "horizontal-tb" })
      );
    });

    ordem.forEach(function (linha) {
      container.appendChild(cell(linha, { color: "var(--ink-secondary)", fontWeight: 600, textAlign: "left" }));
      ordem.forEach(function (coluna) {
        var rho = matrizPorLinha[linha] ? matrizPorLinha[linha][coluna] : null;
        var bg = "var(--grid)";
        var fg = "var(--ink-primary)";
        if (typeof rho === "number") {
          var intensidade = Math.min(Math.abs(rho), 1);
          if (rho >= 0) {
            bg = "rgba(42, 120, 214, " + (0.12 + intensidade * 0.75) + ")";
          } else {
            bg = "rgba(179, 49, 44, " + (0.12 + intensidade * 0.75) + ")";
          }
          if (intensidade > 0.55) fg = "#fff";
        }
        container.appendChild(
          cell(typeof rho === "number" ? rho.toFixed(2) : "—", { background: bg, color: fg, borderRadius: "3px" })
        );
      });
    });
  }

  return {
    CRIME_ORDER: CRIME_ORDER,
    crimeColor: crimeColor,
    renderLegend: renderLegend,
    renderTrendChart: renderTrendChart,
    renderSeasonalityChart: renderSeasonalityChart,
    renderCorrelationHeatmap: renderCorrelationHeatmap,
    fmtInt: fmtInt,
  };
})();
