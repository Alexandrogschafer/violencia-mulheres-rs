(function () {
  const TABELAS = "../assets/data/tables/";
  const RELATORIOS = "../assets/data/reports/";
  const HEX = {
    "Ameaça": "#2a78d6", "Estupro": "#1baf7a", "Feminicídio Consumado": "#eda100",
    "Feminicídio Tentado": "#008300", "Lesão Corporal": "#4a3aa7"
  };
  const ORDEM = ["Ameaça", "Lesão Corporal", "Estupro", "Feminicídio Tentado", "Feminicídio Consumado"];
  const MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"];

  const num = (n, d = 2) => n === null || n === undefined ? "—"
    : n.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
  const pval = p => p === 0 ? "< 0,000001" : (p < 0.0001 ? p.toExponential(1).replace(".", ",") : num(p, 4));
  const $ = s => document.querySelector(s);
  const ptBR = v => typeof v === "number" ? v.toLocaleString("pt-BR") : v;
  const tickPt = { callback: v => ptBR(v) };
  const tipPt = {
    callbacks: {
      label: c => `${c.dataset.label}: ${ptBR(c.parsed.y ?? c.parsed.x)}`
    }
  };

  function tabela(cabecalho, linhas) {
    return `<table class="teste-tab">
      <thead><tr>${cabecalho.map((c, i) => `<th${i ? ' class="num"' : ""}>${c}</th>`).join("")}</tr></thead>
      <tbody>${linhas.map(l => `<tr>${l.map((c, i) => `<td${i ? ' class="num"' : ""}>${c}</td>`).join("")}</tr>`).join("")}</tbody>
    </table>`;
  }

  const selo = sig => sig
    ? '<span class="selo sim">significativo</span>'
    : '<span class="selo nao">não significativo</span>';

  Promise.all([
    "totais_anuais_estado", "inferencial_tendencia_anual", "inferencial_sazonalidade_kruskal",
    "inferencial_sazonalidade_destaques", "inferencial_correlacao_pares_taxa_por_100mil_hab",
    "inferencial_quebra_estrutural_chow"
  ].map(f => fetch((f === "totais_anuais_estado" ? TABELAS : RELATORIOS) + f + ".json").then(r => r.json())))
  .then(([serie, tend, kruskal, destaques, corr, chow]) => {

    /* ---------- 1. Tendência ---------- */
    const anos = [...new Set(serie.map(r => r.ano))].filter(a => a >= 2018 && a <= 2025).sort();
    const porTipo = {};
    serie.forEach(r => {
      if (r.ano < 2018 || r.ano > 2025) return;
      (porTipo[r.tipo_crime] = porTipo[r.tipo_crime] || {})[r.ano] = r.casos_total;
    });
    new Chart($("#g-tendencia"), {
      type: "line",
      data: {
        labels: anos,
        datasets: ORDEM.filter(t => porTipo[t]).map(t => ({
          label: t, data: anos.map(a => porTipo[t][a] ?? null),
          borderColor: HEX[t], backgroundColor: HEX[t], borderWidth: 2, tension: .25, pointRadius: 2
        }))
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: { legend: { position: "top", labels: { boxWidth: 12, font: { family: "Outfit", size: 12 } } }, tooltip: tipPt },
        scales: {
          y: { type: "logarithmic", title: { display: true, text: "Casos no estado (escala logarítmica)" }, ticks: tickPt },
          x: { grid: { display: false } }
        }
      }
    });
    const tOrd = ORDEM.map(t => tend.find(r => r.tipo_crime === t)).filter(Boolean);
    $("#t-tendencia").innerHTML = tabela(
      ["Tipo", "Inclinação (casos/ano)", "R²", "p (regressão)", "τ de Kendall", "p (Mann-Kendall)"],
      tOrd.map(r => [
        r.tipo_crime + " " + selo(r.significativo_linregress_5pct),
        num(r.slope, 1), num(r.r2, 3), pval(r.p_valor_linregress),
        num(r.kendall_tau, 3), pval(r.p_valor_mann_kendall)
      ]));
    const sobem = tOrd.filter(r => r.significativo_linregress_5pct && r.slope > 0).map(r => r.tipo_crime);
    const caem = tOrd.filter(r => r.significativo_linregress_5pct && r.slope < 0).map(r => r.tipo_crime);
    $("#r-tendencia").textContent =
      `Entre 2018 e 2025, ${caem.join(", ")} ${caem.length > 1 ? "caem" : "cai"} de forma significativa a 5%; ` +
      `${sobem.join(", ")} ${sobem.length > 1 ? "sobem" : "sobe"}. ` +
      `Os demais não atingem significância — com oito anos de série, o poder estatístico é baixo.`;
    $("#s-tendencia").textContent = `${caem.length} em queda, ${sobem.length} em alta`;

    /* ---------- 2. Sazonalidade ---------- */
    let tipoSaz = "Ameaça";
    let chartSaz = null;

    function desenhaSaz() {
      const d = destaques.filter(x => x.tipo_crime === tipoSaz).sort((a, b) => a.mes - b.mes);
      const sig = (kruskal.find(r => r.tipo_crime === tipoSaz) || {}).significativo_5pct;
      if (chartSaz) chartSaz.destroy();
      chartSaz = new Chart($("#g-sazonalidade"), {
        type: "bar",
        data: {
          labels: MESES,
          datasets: [{
            label: "Média de casos por mês",
            data: d.map(x => x.media_casos),
            backgroundColor: d.map(x => x.destaque_5pct ? HEX[tipoSaz] : "#c2c3df"),
            borderRadius: 5
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: tipPt,
            title: {
              display: true,
              text: tipoSaz + " — média de casos no estado por mês, 2018–2025"
                    + (sig ? "  (meses em destaque: diferença significativa)" : "  (sem sazonalidade detectável)"),
              font: { family: "Outfit", size: 13, weight: "500" },
              color: "#474252",
              padding: { bottom: 14 }
            }
          },
          scales: {
            y: { beginAtZero: true, title: { display: true, text: "Média de casos" }, ticks: tickPt },
            x: { grid: { display: false } }
          }
        }
      });
      const ac = d.filter(x => x.destaque_5pct && x.direcao === "acima").map(x => x.mes_nome);
      const ab = d.filter(x => x.destaque_5pct && x.direcao === "abaixo").map(x => x.mes_nome);
      $("#r-saz-tipo").textContent = sig
        ? `Em ${tipoSaz}, destacam-se para cima ${ac.join(", ") || "nenhum mês"}; para baixo, ${ab.join(", ") || "nenhum mês"}.`
        : `${tipoSaz} não apresenta diferença significativa entre os meses.`;
    }

    document.querySelectorAll("[data-saz]").forEach(b => b.addEventListener("click", () => {
      tipoSaz = b.dataset.saz;
      document.querySelectorAll("[data-saz]").forEach(x => x.classList.toggle("is-on", x === b));
      desenhaSaz();
    }));
    desenhaSaz();

    $("#t-sazonalidade").innerHTML = tabela(
      ["Tipo", "n", "H de Kruskal-Wallis", "p"],
      ORDEM.map(t => kruskal.find(r => r.tipo_crime === t)).filter(Boolean).map(r =>
        [r.tipo_crime + " " + selo(r.significativo_5pct), r.n_obs, num(r.estatistica_h, 2), pval(r.p_valor)]));
    const sazSig = ORDEM.filter(t => (kruskal.find(r => r.tipo_crime === t) || {}).significativo_5pct);
    $("#r-sazonalidade").textContent =
      `${sazSig.join(" e ")} ${sazSig.length > 1 ? "apresentam" : "apresenta"} diferença significativa entre os meses; ` +
      `os demais não. Feminicídio não mostra sazonalidade detectável — esperado para eventos raros, com contagem mensal pequena. ` +
      `Use o seletor acima para ver cada tipo.`;
    $("#s-sazonalidade").textContent = `${sazSig.length} de 5 tipos com variação mensal`;

    /* ---------- 3. Correlação ---------- */
    const cOrd = [...corr].sort((a, b) => b.rho - a.rho);
    $("#t-correlacao").innerHTML = tabela(
      ["Par de tipos", "ρ de Spearman", "p"],
      cOrd.map(r => [`${r.tipo_crime_a} × ${r.tipo_crime_b} ` + selo(r.significativo_5pct), num(r.rho, 3), pval(r.p_valor)]));
    new Chart($("#g-correlacao"), {
      type: "bar",
      data: {
        labels: cOrd.map(r => r.tipo_crime_a + " × " + r.tipo_crime_b),
        datasets: [{ label: "ρ de Spearman", data: cOrd.map(r => r.rho), backgroundColor: "#7563a8", borderRadius: 5 }]
      },
      options: {
        indexAxis: "y", responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => "ρ = " + c.parsed.x.toLocaleString("pt-BR", { minimumFractionDigits: 3, maximumFractionDigits: 3 }) } } },
        scales: {
          x: { min: 0, max: 1, title: { display: true, text: "ρ de Spearman (taxa por 100 mil, entre municípios)" }, ticks: { callback: v => v.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) } },
          y: { grid: { display: false }, ticks: { font: { size: 11 } } }
        }
      }
    });
    const forte = cOrd[0];
    $("#r-correlacao").textContent =
      `O par mais associado é ${forte.tipo_crime_a} × ${forte.tipo_crime_b}, com ρ = ${num(forte.rho, 2)}: ` +
      `municípios com taxa alta num tendem a tê-la alta no outro. As demais associações são bem mais fracas, ` +
      `o que indica que os tipos de violência não se distribuem todos do mesmo jeito pelo território.`;
    $("#s-correlacao").textContent = `par mais forte: ρ = ${num(forte.rho, 2)}`;

    /* ---------- 4. Quebra estrutural ---------- */
    const chOrd = ORDEM.map(t => chow.find(r => r.tipo_crime === t)).filter(Boolean);
    $("#t-quebra").innerHTML = tabela(
      ["Tipo", "Meses antes", "Meses depois", "F de Chow", "p"],
      chOrd.map(r => [r.tipo_crime + " " + selo(r.significativo_5pct), r.n_meses_pre, r.n_meses_pos, num(r.estatistica_f, 2), pval(r.p_valor)]));
    new Chart($("#g-quebra"), {
      type: "bar",
      data: {
        labels: chOrd.map(r => r.tipo_crime),
        datasets: [
          { label: "Inclinação antes (casos/mês)", data: chOrd.map(r => r.slope_pre), backgroundColor: "#c2c3df", borderRadius: 5 },
          { label: "Inclinação depois", data: chOrd.map(r => r.slope_pos), backgroundColor: "#7563a8", borderRadius: 5 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: "top", labels: { boxWidth: 12, font: { family: "Outfit", size: 12 } } }, tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}` } } },
        scales: {
          y: { title: { display: true, text: "Variação de casos por mês" }, ticks: { callback: v => v.toLocaleString("pt-BR", { maximumFractionDigits: 1 }) } },
          x: { grid: { display: false }, ticks: { font: { size: 11 } } }
        }
      }
    });
    const qSig = chOrd.filter(r => r.significativo_5pct).map(r => r.tipo_crime);
    $("#r-quebra").textContent =
      `${qSig.join(", ")} apresentam quebra significativa em torno de maio de 2024. ` +
      `A inclinação muda de sinal em vários tipos: séries que vinham caindo passam a subir. ` +
      `O teste localiza a mudança no tempo, não estabelece que as enchentes a causaram.`;
    $("#s-quebra").textContent = `${qSig.length} de 5 tipos com quebra`;

    $("#carregando").hidden = true;
    $("#conteudo").hidden = false;
  }).catch(e => { $("#carregando").textContent = "Não foi possível carregar os resultados."; });
})();
