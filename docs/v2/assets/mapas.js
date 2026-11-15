(function () {
  // Rampa Purples e cores de exceção — valores idênticos aos de mapa_choropleth.py,
  // lidos do portal publicado. Não alterar aqui: a fonte é o pipeline.
  const RAMPA = ["#ebe9f3","#e0dfee","#d2d2e7","#c2c3df","#b2b2d5","#a29fcb","#928fc3",
                 "#827fbb","#7669af","#6950a3","#5e3a98","#52238d","#470f84"];
  const COR_SEM_DADO = "#e1e0d9";
  const COR_ABAIXO_PISO = "#c5c0b1";
  const PISO = 5000;
  const TIPOS = ["Ameaça","Lesão Corporal","Estupro","Feminicídio Tentado","Feminicídio Consumado"];

  const fmtInt = n => n.toLocaleString("pt-BR");
  const fmtTaxa = n => (n === null || n === undefined) ? "—"
    : n.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const titulo = s => s.toLowerCase()
    .replace(/(^|[\s'\-])([a-zà-ú])/g, (m,a,b) => a + b.toUpperCase())
    .replace(/\b(Da|De|Do|Das|Dos|E)\b/g, w => w.toLowerCase());

  let RESUMO = null, PORMUN = {}, GEO = null, mapa = null, camada = null;
  let tipo = "Ameaça", medida = "taxa", selecionado = null;
  const $ = s => document.querySelector(s);

  function valor(mun, t) {
    const r = PORMUN[mun];
    if (!r) return null;
    return medida === "taxa" ? r["t_" + t] : r["c_" + t];
  }

  function dominio() {
    const vals = RESUMO.filter(r => r.pop_media >= PISO)
      .map(r => medida === "taxa" ? r["t_" + tipo] : r["c_" + tipo])
      .filter(v => v !== null && v !== undefined);
    return [Math.min(...vals), Math.max(...vals)];
  }

  function cor(mun) {
    const r = PORMUN[mun];
    if (!r) return COR_SEM_DADO;
    if (r.pop_media < PISO) return COR_ABAIXO_PISO;
    const v = valor(mun, tipo);
    if (v === null || v === undefined) return COR_SEM_DADO;
    const [min, max] = dominio();
    const f = max > min ? (v - min) / (max - min) : 0;
    return RAMPA[Math.min(RAMPA.length - 1, Math.max(0, Math.round(f * (RAMPA.length - 1))))];
  }

  function estilo(feature) {
    const mun = feature.properties.municipio;
    return {
      fillColor: cor(mun),
      fillOpacity: 0.92,
      color: mun === selecionado ? "#1e1b24" : "#ffffff",
      weight: mun === selecionado ? 2.2 : 0.4
    };
  }

  function legenda() {
    const [min, max] = dominio();
    const passos = RAMPA.map((c, i) => {
      const v = min + (max - min) * (i / (RAMPA.length - 1));
      return `<span class="ramp-step" style="background:${c}" title="${fmtTaxa(v)}"></span>`;
    }).join("");
    const rot = medida === "taxa" ? "taxa por 100 mil hab." : "casos registrados";
    $("#legenda").innerHTML =
      `<div class="ramp-row"><span class="ramp-min">${medida === "taxa" ? fmtTaxa(min) : fmtInt(Math.round(min))}</span>` +
      passos +
      `<span class="ramp-max">${medida === "taxa" ? fmtTaxa(max) : fmtInt(Math.round(max))}</span></div>` +
      `<div class="ramp-leg">${rot} · <span class="sw" style="background:${COR_ABAIXO_PISO}"></span> menos de 5.000 hab. (231 municípios)` +
      ` · <span class="sw" style="background:${COR_SEM_DADO}"></span> sem dado</div>`;
  }

  function painel(mun) {
    const r = PORMUN[mun];
    if (!r) return;
    const abaixo = r.pop_media < PISO;
    $("#painel").hidden = false;
    $("#painel-vazio").hidden = true;
    $("#painel-nome").textContent = titulo(mun);
    $("#painel-pop").innerHTML =
      `${fmtInt(r.pop_media)} habitantes (média 2018–2025) · <strong>${fmtInt(r.c_geral)}</strong> registros no período` +
      (abaixo ? ' <span class="flag">abaixo do piso de 5.000</span>' : "");
    $("#painel-linhas").innerHTML = TIPOS.map(t => `
      <tr${t === tipo ? ' class="is-ativo"' : ""}>
        <td>${t}</td>
        <td class="num">${fmtInt(r["c_" + t])}</td>
        <td class="num">${fmtTaxa(r["t_" + t])}</td>
      </tr>`).join("");
    $("#painel-link").href = "municipios.html?municipio=" + encodeURIComponent(mun);
  }

  function redesenhar() {
    if (camada) camada.setStyle(estilo);
    legenda();
    if (selecionado) painel(selecionado);
  }

  Promise.all([
    fetch("../assets/data/maps/municipios_rs.geojson").then(r => r.json()),
    fetch("../assets/data/tables/municipios_resumo_periodo.json").then(r => r.json())
  ]).then(([g, r]) => {
    GEO = g; RESUMO = r;
    r.forEach(x => { PORMUN[x.municipio] = x; });

    // O contêiner precisa estar visível ANTES de criar o mapa: num elemento
    // escondido ele mede 0x0 e o Leaflet não se recupera sozinho.
    $("#carregando").hidden = true;
    $("#mapa-bloco").hidden = false;

    mapa = L.map("mapa", { scrollWheelZoom: false, zoomControl: true });
    // Sem basemap de tiles: para um coroplético municipal o fundo cartográfico
    // acrescenta pouco, e evita depender de CDN externo.
    mapa.attributionControl.addAttribution("Malha: IBGE · Dados: SSP/RS");

    camada = L.geoJSON(GEO, {
      style: estilo,
      onEachFeature: (f, layer) => {
        const mun = f.properties.municipio;
        layer.bindTooltip(() => {
          const v = valor(mun, tipo);
          return `<strong>${titulo(mun)}</strong><br>${medida === "taxa"
            ? fmtTaxa(v) + " por 100 mil" : fmtInt(v) + " casos"}`;
        }, { sticky: true });
        layer.on("click", () => { selecionado = mun; redesenhar(); painel(mun); });
        layer.on("mouseover", e => e.target.setStyle({ weight: 1.6, color: "#1e1b24" }));
        layer.on("mouseout", e => camada.resetStyle(e.target));
      }
    }).addTo(mapa);

    mapa.fitBounds(camada.getBounds(), { padding: [8, 8] });
    legenda();

    // rede de segurança: se o contêiner mudar de tamanho depois da criação
    // (fontes carregando, barra de rolagem aparecendo), o Leaflet reavalia.
    requestAnimationFrame(() => {
      mapa.invalidateSize();
      mapa.fitBounds(camada.getBounds(), { padding: [8, 8] });
    });
    window.addEventListener("resize", () => mapa.invalidateSize());

    document.querySelectorAll("[data-tipo]").forEach(b => b.addEventListener("click", () => {
      tipo = b.dataset.tipo;
      document.querySelectorAll("[data-tipo]").forEach(x => x.classList.toggle("is-on", x === b));
      redesenhar();
    }));
    document.querySelectorAll("[data-medida]").forEach(b => b.addEventListener("click", () => {
      medida = b.dataset.medida;
      document.querySelectorAll("[data-medida]").forEach(x => x.classList.toggle("is-on", x === b));
      $("#aviso-casos").hidden = medida !== "casos";
      redesenhar();
    }));
  }).catch(() => { $("#carregando").textContent = "Não foi possível carregar o mapa."; });
})();
