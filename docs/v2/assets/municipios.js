(function () {
  const CRIME_COLOR = {
    "Ameaça": "var(--crime-ameaca)",
    "Estupro": "var(--crime-estupro)",
    "Feminicídio Consumado": "var(--crime-fem-consumado)",
    "Feminicídio Tentado": "var(--crime-fem-tentado)",
    "Lesão Corporal": "var(--crime-lesao)"
  };
  const HEX = {
    "Ameaça": "#2a78d6", "Estupro": "#1baf7a", "Feminicídio Consumado": "#eda100",
    "Feminicídio Tentado": "#008300", "Lesão Corporal": "#4a3aa7"
  };
  const PISO = 5000;
  const fmtInt = n => n.toLocaleString("pt-BR");
  const fmtTaxa = n => (n === null || n === undefined) ? "—" : n.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

  let SERIE = null, RESUMO = null, chart = null;
  const $ = s => document.querySelector(s);

  function titulo(nome) {
    return nome.toLowerCase().replace(/(^|[\s'\-])([a-zà-ú])/g, (m, a, b) => a + b.toUpperCase())
      .replace(/\b(Da|De|Do|Das|Dos|E)\b/g, w => w.toLowerCase());
  }

  // medianas estaduais entre municípios elegíveis (>= piso), por tipo
  function medianas(tipos) {
    const eleg = RESUMO.filter(r => r.pop_media >= PISO);
    const out = {};
    tipos.forEach(t => {
      const v = eleg.map(r => r["t_" + t]).filter(x => x !== null).sort((a, b) => a - b);
      out[t] = v.length % 2 ? v[(v.length - 1) / 2] : (v[v.length / 2 - 1] + v[v.length / 2]) / 2;
    });
    out._n = eleg.length;
    return out;
  }

  function ranking(tipo, valor) {
    const eleg = RESUMO.filter(r => r.pop_media >= PISO && r["t_" + tipo] !== null)
      .sort((a, b) => b["t_" + tipo] - a["t_" + tipo]);
    const pos = eleg.findIndex(r => r["t_" + tipo] <= valor) + 1;
    return { pos: pos || eleg.length, n: eleg.length };
  }

  function render(nome) {
    const reg = RESUMO.find(r => r.municipio === nome);
    const ser = SERIE.municipios[nome];
    if (!reg || !ser) return;

    const tipos = SERIE.tipos;
    const med = medianas(tipos);
    const abaixoPiso = reg.pop_media < PISO;

    $("#vazio").hidden = true;
    $("#perfil").hidden = false;

    $("#perfil-nome").textContent = titulo(nome);
    $("#perfil-meta").innerHTML =
      `População média 2018–2025: <strong>${fmtInt(reg.pop_media)}</strong> habitantes · ` +
      `<strong>${fmtInt(reg.c_geral)}</strong> registros no período`;

    $("#aviso-piso").hidden = !abaixoPiso;

    // cartões
    $("#cartoes").innerHTML = tipos.map(t => {
      const taxa = reg["t_" + t], casos = reg["c_" + t];
      const r = abaixoPiso ? null : ranking(t, taxa);
      const acima = taxa > med[t];
      return `<div class="mcard">
        <span class="mcard-tipo" style="color:${CRIME_COLOR[t]}">${t}</span>
        <span class="mcard-taxa">${fmtTaxa(taxa)}</span>
        <span class="mcard-un">por 100 mil hab. · ${fmtInt(casos)} casos</span>
        <span class="mcard-cmp">${abaixoPiso
          ? `<span class="cmp-na">Sem ranking: município abaixo de 5.000 hab.</span>`
          : `<span class="cmp-pos">${r.pos}º entre ${r.n} municípios comparáveis</span>
             <span class="cmp-med ${acima ? "up" : "down"}">${acima ? "Acima" : "Abaixo"} da mediana, de ${fmtTaxa(med[t])}</span>`}</span>
      </div>`;
    }).join("");

    // gráfico: série anual de casos
    const ctx = $("#grafico").getContext("2d");
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: SERIE.anos,
        datasets: tipos.map((t, i) => ({
          label: t,
          data: ser.c[i],
          borderColor: HEX[t],
          backgroundColor: HEX[t],
          borderWidth: 2,
          tension: 0.25,
          pointRadius: 2
        }))
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { position: "top", labels: { boxWidth: 12, font: { family: "Outfit", size: 12 } } },
          tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toLocaleString("pt-BR")}` } }
        },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: "Casos no ano" }, ticks: { callback: v => v.toLocaleString("pt-BR") } },
          x: { grid: { display: false } }
        }
      }
    });

    history.replaceState(null, "", "?municipio=" + encodeURIComponent(nome));
  }

  function montarLista() {
    $("#lista").innerHTML = RESUMO.map(r => `<option value="${titulo(r.municipio)}"></option>`).join("");
  }

  const chave = s => s.trim().toUpperCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

  function resolver() {
    const q = chave($("#busca").value);
    if (!q) return { erro: "Digite o nome de um município, ou clique no campo para ver a lista." };
    const exato = RESUMO.find(r => chave(r.municipio) === q);
    if (exato) return { nome: exato.municipio };
    const parcial = RESUMO.filter(r => chave(r.municipio).startsWith(q));
    if (parcial.length === 1) return { nome: parcial[0].municipio };
    if (parcial.length > 1)
      return { erro: `${parcial.length} municípios começam com “${$("#busca").value.trim()}”. Escolha um na lista do campo.` };
    return { erro: "Nenhum município com esse nome. Clique no campo para ver a lista completa." };
  }

  function visualizar() {
    const r = resolver();
    const erro = $("#erro");
    if (r.erro) { erro.hidden = false; erro.textContent = r.erro; return; }
    erro.hidden = true;
    $("#busca").value = titulo(r.nome);
    render(r.nome);
    $("#perfil").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  Promise.all([
    fetch("../assets/data/tables/municipios_serie_anual.json").then(r => r.json()),
    fetch("../assets/data/tables/municipios_resumo_periodo.json").then(r => r.json())
  ]).then(([s, r]) => {
    SERIE = s; RESUMO = r;
    montarLista();
    $("#consulta").hidden = false;
    $("#carregando").hidden = true;

    $("#btn").addEventListener("click", visualizar);
    $("#busca").addEventListener("keydown", e => { if (e.key === "Enter") visualizar(); });
    $("#busca").addEventListener("input", () => { $("#erro").hidden = true; });
    document.querySelectorAll("[data-atalho]").forEach(b =>
      b.addEventListener("click", () => {
        $("#busca").value = titulo(b.dataset.atalho);
        visualizar();
      }));

    const q = new URLSearchParams(location.search).get("municipio");
    if (q && SERIE.municipios[q.toUpperCase()]) {
      $("#busca").value = titulo(q.toUpperCase());
      render(q.toUpperCase());
    }
  }).catch(() => {
    $("#carregando").textContent = "Não foi possível carregar os dados.";
  });
})();
