// Estudos de caso municipais -- registry + renderização.
//
// Modularidade: cada item de ESTUDOS_DE_CASO descreve um município já
// processado por um notebook próprio (notebooks/estudo_<municipio>.ipynb),
// que persiste seus resultados em outputs/reports/<prefixo>_*.csv (mesmo
// padrão de src/build_site_data.py, que já converte QUALQUER csv novo em
// outputs/reports/ para JSON automaticamente -- nenhum código novo é
// necessário ali para um município adicional).
//
// A página pública mostra uma versão SIMPLIFICADA dos resultados (poucos
// cards, uma comparação em linguagem simples, 2 gráficos + o mapa) --
// não é uma reimplementação nem um recálculo: todo número aqui vem direto
// dos JSONs já publicados em assets/data/reports/, os mesmos que a análise
// técnica completa usa. As tabelas técnicas completas (ranking, LISA,
// tendência, sazonalidade, séries anuais) continuam publicadas em
// assets/data/reports/ e no notebook -- só não são exibidas nesta página.
//
// Para adicionar um novo município: 1) instrumentar seu notebook do mesmo
// jeito (to_csv em outputs/reports/, savefig em outputs/figures/);
// 2) adicionar uma entrada em ESTUDOS_DE_CASO com uma função `render`
// própria, reaproveitando as funções utilitárias já existentes aqui.

(function () {
  "use strict";

  var DATA = "assets/data/";

  function fetchJSON(caminho) {
    return fetch(DATA + caminho).then(function (r) {
      return r.json();
    });
  }

  function fmtN(n) {
    return Number(n).toLocaleString("pt-BR");
  }

  // ---------- componentes reaproveitáveis por qualquer estudo de caso ----------

  // layout: "grid" (padrão, várias colunas) ou "stack" (uma figura por
  // linha, largura total -- melhor pra figuras largas/baixas, tipo small
  // multiples, onde encolher pra meia tela prejudica a leitura).
  function montarGaleria(container, itens, layout) {
    container.innerHTML = "";
    container.className = layout === "stack" ? "gallery-stack" : "gallery";
    itens.forEach(function (item) {
      var fig = document.createElement("figure");
      var img = document.createElement("img");
      img.src = DATA + "figures/" + item.arquivo;
      img.alt = item.alt;
      img.loading = "lazy";
      var caption = document.createElement("figcaption");
      caption.textContent = item.legenda;
      fig.appendChild(img);
      fig.appendChild(caption);
      container.appendChild(fig);
    });
  }

  function montarMapaFoco(mapElId, selectElId, legendElId, municipioGeo, tipoInicial) {
    Promise.all([
      fetchJSON("maps/municipios_rs.geojson"),
      fetchJSON("maps/taxa_por_municipio.json"),
    ]).then(function (res) {
      var geojson = res[0];
      var taxas = res[1];
      var select = document.getElementById(selectElId);
      Object.keys(taxas.taxas).forEach(function (tipo) {
        var opt = document.createElement("option");
        opt.value = tipo;
        opt.textContent = tipo;
        select.appendChild(opt);
      });
      select.value = tipoInicial;
      var mapa = SiteMaps.initMap(mapElId, geojson, taxas, {
        tipoInicial: tipoInicial,
        legendId: legendElId,
        destacarMunicipio: municipioGeo,
      });
      select.addEventListener("change", function () {
        mapa.trocarTipo(select.value);
      });
    });
  }

  // ---------- Uruguaiana ----------

  // Rótulo de comparação em linguagem simples -- a categoria (abaixo/
  // próxima/acima) é decidida aqui, curada para casar com a leitura já
  // publicada no notebook; o número exibido (razão, taxas) vem sempre do
  // JSON, nunca recalculado.
  var LEITURA_POR_TIPO = {
    "Ameaça": { rotulo: "Próxima da média estadual", nota: "levemente abaixo" },
    "Estupro": { rotulo: "Acima da média estadual", nota: null },
    "Feminicídio Consumado": { rotulo: "Acima da média estadual", nota: "poucos casos — variação grande de ano a ano" },
    "Feminicídio Tentado": { rotulo: "Acima da média estadual", nota: "poucos casos — variação grande de ano a ano" },
    "Lesão Corporal": { rotulo: "Acima da média estadual", nota: "principal destaque do município" },
  };

  function templateUruguaiana() {
    return (
      '<section class="card">' +
      "<p>Uruguaiana é o <strong>primeiro estudo de caso municipal</strong> do portal. A análise usa a " +
      "mesma base de dados e a mesma metodologia do estudo estadual, aplicada só a este município, para " +
      "responder a uma pergunta simples: os padrões observados no Rio Grande do Sul também aparecem em " +
      "Uruguaiana?</p>" +
      "</section>" +
      '<section>' +
      "<h2>Uruguaiana em números</h2>" +
      '<div id="uru-tiles" class="stat-row"></div>' +
      "</section>" +
      '<section>' +
      "<h2>Comparação com o estado</h2>" +
      '<p class="muted small">Taxa por 100 mil hab. acumulada (2012–2025), por tipo de crime, comparada com a média do Rio Grande do Sul.</p>' +
      '<div id="uru-comparacao"></div>' +
      "</section>" +
      '<section>' +
      "<h2>Principais conclusões</h2>" +
      "<ul>" +
      "<li>Uruguaiana tem taxas acima da média estadual em quatro dos cinco tipos de crime analisados.</li>" +
      "<li>Lesão corporal é o principal destaque do município e faz parte de uma área regional com taxas elevadas.</li>" +
      "<li>Ameaça e lesão corporal vêm caindo nos últimos anos em Uruguaiana.</li>" +
      "<li>O aumento de estupro observado no estado como um todo não apareceu da mesma forma em Uruguaiana.</li>" +
      "<li>O município fica acima da média, mas não é um caso extremamente diferente do restante do Rio Grande do Sul.</li>" +
      "</ul>" +
      "</section>" +
      '<section>' +
      "<h2>Visualizações</h2>" +
      '<div id="uru-galeria"></div>' +
      '<div class="map-controls"><label for="uru-select-mapa" class="small muted">Tipo de crime:</label><select id="uru-select-mapa"></select></div>' +
      '<div class="map-frame">' +
      '<div id="uru-map" class="case-map" role="application" aria-label="Mapa interativo do RS enquadrado em Uruguaiana"></div>' +
      '<div class="map-legend map-legend-overlay">' +
      '<div class="map-legend-title">Taxa por 100 mil habitantes</div>' +
      '<div id="uru-map-legend"></div>' +
      "</div>" +
      "</div>" +
      "</section>" +
      '<div class="callout">' +
      "<h2>Leitura geral</h2>" +
      "<p>Uruguaiana apresenta níveis de violência contra as mulheres geralmente superiores à média estadual, " +
      "especialmente em lesão corporal. Apesar disso, o município não se comporta de forma completamente " +
      "diferente do restante do Rio Grande do Sul. Alguns padrões estaduais aparecem localmente, enquanto " +
      "outros não, reforçando a importância de analisar cada município separadamente.</p>" +
      "</div>" +
      '<section>' +
      "<h2>Cuidados na interpretação</h2>" +
      '<div class="callout warn"><p style="margin:0">Registros de feminicídio envolvem poucos casos e podem variar muito de um ano para outro.</p></div>' +
      '<div class="callout warn"><p style="margin:0">Resultados municipais têm mais variação que resultados estaduais — a base de comparação é bem menor.</p></div>' +
      '<div class="callout warn"><p style="margin:0">Comparações com outros municípios são descritivas — não provam que a localização na fronteira seja a causa das diferenças.</p></div>' +
      "</section>" +
      '<section class="cta-row">' +
      '<a class="btn-primary" href="https://github.com/Alexandrogschafer/violencia-mulheres-rs/blob/master/notebooks/estudo_uruguaiana.ipynb">Consultar análise técnica completa →</a>' +
      '<a class="btn-secondary" href="dados.html">Baixar os dados utilizados</a>' +
      "</section>"
    );
  }

  function renderUruguaiana(container) {
    container.innerHTML = templateUruguaiana();

    Promise.all([
      fetchJSON("reports/uruguaiana_perfil.json"),
      fetchJSON("reports/uruguaiana_resumo_corede.json"),
      fetchJSON("tables/uruguaiana_populacao_censo.json"),
    ]).then(function (res) {
      var perfil = res[0];
      var resumo = res[1][0];
      var censo = res[2];

      // Uruguaiana em números
      var geral = (resumo.media_taxa_geral_uruguaiana_2012_2025 / resumo.media_taxa_geral_estado_2012_2025 - 1) * 100;
      var tilesEl = document.getElementById("uru-tiles");
      tilesEl.innerHTML = "";
      [
        { valor: fmtN(censo.populacao_censo), label: "📍 População — Censo " + censo.ano_censo + " (IBGE)" },
        { valor: "COREDE " + resumo.corede, label: "🗺️ Posição regional — maior cidade da região (" + resumo.pct_populacao_corede_2025 + "% da população em 2025)" },
        { valor: (geral >= 0 ? "+" : "") + geral.toFixed(0) + "%", label: "⚖️ Taxa geral de violência vs. média estadual" },
        { valor: "Lesão Corporal", label: "⚠️ Tipo de violência com maior destaque" },
      ].forEach(function (t) {
        var tile = document.createElement("div");
        tile.className = "stat-tile";
        tile.innerHTML = '<div class="value">' + t.valor + "</div>" + '<div class="label">' + t.label + "</div>";
        tilesEl.appendChild(tile);
      });

      // Comparação com o estado
      var compEl = document.getElementById("uru-comparacao");
      compEl.className = "compare-list";
      compEl.innerHTML = "";
      perfil.forEach(function (row) {
        var leitura = LEITURA_POR_TIPO[row.tipo_crime] || { rotulo: "", nota: null };
        var item = document.createElement("div");
        item.className = "compare-item";
        item.innerHTML =
          '<span class="swatch" style="background:' + SiteCharts.crimeColor(row.tipo_crime) + '"></span>' +
          '<span class="compare-tipo">' + row.tipo_crime + "</span>" +
          '<span class="compare-label">' + leitura.rotulo + (leitura.nota ? " <span class=\"muted small\">(" + leitura.nota + ")</span>" : "") + "</span>" +
          '<span class="compare-valor small muted">' + row.taxa_uruguaiana.toFixed(1) + " vs. " + row.taxa_estado.toFixed(1) + " / 100 mil hab.</span>";
        compEl.appendChild(item);
      });

      // Visualizações
      montarGaleria(
        document.getElementById("uru-galeria"),
        [
          { arquivo: "uruguaiana_perfil_taxa_vs_estado.png", alt: "Uruguaiana vs. média estadual, taxa por 100 mil hab., acumulada 2012-2025", legenda: "Uruguaiana vs. média estadual — taxa por 100 mil hab. (2012–2025)" },
          { arquivo: "uruguaiana_serie_anual.png", alt: "Evolução anual de Uruguaiana por tipo de crime, 2012-2026", legenda: "Evolução anual por tipo de crime (2012–2026, 2026 parcial)" },
        ],
        "stack"
      );
      montarMapaFoco("uru-map", "uru-select-mapa", "uru-map-legend", "URUGUAIANA", "Lesão Corporal");
    });
  }

  // ---------- registry ----------

  var ESTUDOS_DE_CASO = [
    { id: "uruguaiana", nome: "Uruguaiana", render: renderUruguaiana },
  ];

  // ---------- boot ----------

  document.addEventListener("DOMContentLoaded", function () {
    var conteudo = document.getElementById("conteudo-casos");
    var seletor = document.getElementById("seletor-casos");
    var select = document.getElementById("select-caso");

    if (ESTUDOS_DE_CASO.length > 1) {
      seletor.style.display = "";
      ESTUDOS_DE_CASO.forEach(function (caso) {
        var opt = document.createElement("option");
        opt.value = caso.id;
        opt.textContent = caso.nome;
        select.appendChild(opt);
      });
      select.addEventListener("change", function () {
        var caso = ESTUDOS_DE_CASO.filter(function (c) { return c.id === select.value; })[0];
        caso.render(conteudo);
      });
    }

    ESTUDOS_DE_CASO[0].render(conteudo);
  });
})();
