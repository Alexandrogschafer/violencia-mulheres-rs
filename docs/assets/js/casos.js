// Estudos de caso municipais -- registry + renderização.
//
// Modularidade: cada item de ESTUDOS_DE_CASO descreve um município já
// processado por um notebook próprio (notebooks/estudo_<municipio>.ipynb),
// que persiste seus resultados em outputs/reports/<prefixo>_*.csv (mesmo
// padrão de src/build_site_data.py, que já converte QUALQUER csv novo em
// outputs/reports/ para JSON automaticamente -- nenhum código novo é
// necessário ali para um município adicional). O que É específico por
// município é a função `render`: cada estudo tem sua própria seleção de
// comparações (aqui, COREDE Fronteira Oeste e efeito fronteira/porte), então
// o texto interpretativo e a lista de gráficos são escritos à mão por
// estudo -- os COMPONENTES (tiles, tabela, mapa, galeria) são compartilhados
// via as funções utilitárias abaixo. Para adicionar um novo município:
// 1) instrumentar seu notebook do mesmo jeito (to_csv em outputs/reports/,
//    savefig em outputs/figures/); 2) adicionar uma entrada em
//    ESTUDOS_DE_CASO com uma função `render` própria, reaproveitando as
//    funções utilitárias já existentes aqui.

(function () {
  "use strict";

  var DATA = "assets/data/";

  function fetchJSON(caminho) {
    return fetch(DATA + caminho).then(function (r) {
      return r.json();
    });
  }

  function el(tag, className, html) {
    var e = document.createElement(tag);
    if (className) e.className = className;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  // ---------- componentes reaproveitáveis por qualquer estudo de caso ----------

  function montarTilesRazao(container, perfil, tituloTaxa) {
    container.innerHTML = "";
    container.className = "stat-row";
    perfil.forEach(function (row) {
      var acima = row.razao_uru_estado > 1;
      var tile = el("div", "stat-tile");
      tile.innerHTML =
        '<div class="value"><span class="swatch" style="background:' +
        SiteCharts.crimeColor(row.tipo_crime) +
        '"></span>' +
        row.razao_uru_estado.toFixed(2) +
        "×</div>" +
        '<div class="label">' +
        row.tipo_crime +
        " — taxa " +
        (acima ? "acima" : "abaixo") +
        " da " +
        tituloTaxa +
        " (" +
        row.taxa_uruguaiana.toFixed(1) +
        " vs. " +
        row.taxa_estado.toFixed(1) +
        " / 100 mil hab.)</div>";
      container.appendChild(tile);
    });
  }

  function montarGaleria(container, itens) {
    container.innerHTML = "";
    container.className = "gallery";
    itens.forEach(function (item) {
      var fig = el("figure");
      var img = document.createElement("img");
      img.src = DATA + "figures/" + item.arquivo;
      img.alt = item.alt;
      img.loading = "lazy";
      var caption = el("figcaption", null, item.legenda);
      fig.appendChild(img);
      fig.appendChild(caption);
      container.appendChild(fig);
    });
  }

  function montarTabela(container, columns, rows, opts) {
    SiteTables.renderTable(container, columns, rows, opts || {});
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

  function templateUruguaiana() {
    return (
      '<section class="card">' +
      "<h2>Introdução ao estudo</h2>" +
      "<p>Recorte de um único município sobre as três camadas já construídas na análise estadual: " +
      "Camada 1 (dados), Camada 2 (tendência e sazonalidade) e Camada 3 (autocorrelação espacial e clusters LISA). " +
      "Este estudo não reimplementa nenhuma estatística — só filtra as mesmas tabelas/funções da pipeline " +
      "para Uruguaiana e compara contra o estado.</p>" +
      "<p><strong>Por que Uruguaiana:</strong> maior cidade do COREDE Fronteira Oeste, na fronteira com a " +
      "Argentina (junto com Barra do Quaraí) às margens do rio Uruguai — um caso de interesse para checar se " +
      "municípios de fronteira têm um padrão de violência diferente do resto do estado, e se os achados " +
      "estaduais da Camada 2/3 se replicam num município específico ou não.</p>" +
      '<p class="small muted"><a href="https://github.com/Alexandrogschafer/violencia-mulheres-rs/blob/master/notebooks/estudo_uruguaiana.ipynb">Ver notebook completo →</a></p>' +
      "</section>" +
      '<section class="card">' +
      "<h2>Caracterização do município</h2>" +
      '<div id="uru-caracterizacao"></div>' +
      "<p>O COREDE Fronteira Oeste tem 13 municípios: Alegrete, Barra do Quaraí, Itacurubi, Itaqui, Maçambará, " +
      "Manoel Viana, Quaraí, Rosário do Sul, Santa Margarida do Sul, Santana do Livramento, São Borja, São " +
      "Gabriel e Uruguaiana.</p>" +
      "</section>" +
      '<section class="card">' +
      "<h2>Principais indicadores</h2>" +
      "<p class=\"muted small\">Taxa acumulada por 100 mil hab. (2012–2025) em Uruguaiana vs. taxa média do estado, por tipo de crime. " +
      "Feminicídio Consumado e Feminicídio Tentado são categorias raras (poucas dezenas de casos acumulados em 14 anos) — a taxa " +
      "por 100 mil hab. é estatisticamente instável nesses dois tipos.</p>" +
      '<div id="uru-tiles"></div>' +
      "</section>" +
      '<section class="card">' +
      "<h2>Gráficos</h2>" +
      "<p class=\"muted small\">Figuras geradas por <code>notebooks/estudo_uruguaiana.ipynb</code>, reproduzidas sem alteração.</p>" +
      '<div id="uru-galeria"></div>' +
      "</section>" +
      '<section class="card">' +
      "<h2>Mapas</h2>" +
      "<p class=\"muted small\">Mesmo mapa estadual interativo da página <a href=\"mapas.html\">Mapas</a>, enquadrado em Uruguaiana " +
      "(contorno destacado). O Índice de Moran Global é uma estatística única para o estado inteiro — não tem \"valor para " +
      "Uruguaiana\"; o LISA (tabela abaixo) é a estatística local, com leitura direta para o município.</p>" +
      '<div class="map-controls"><label for="uru-select-mapa" class="small muted">Tipo de crime:</label><select id="uru-select-mapa"></select></div>' +
      '<div id="uru-map" role="application" aria-label="Mapa interativo do RS enquadrado em Uruguaiana"></div>' +
      '<div id="uru-map-legend" class="map-legend" style="margin-top:0.75rem"></div>' +
      '<h3 class="small" style="margin-top:1.25rem">Classificação LISA (2021–2025)</h3>' +
      '<div id="uru-tabela-lisa" class="table-scroll"></div>' +
      "</section>" +
      '<section class="card">' +
      "<h2>Tabelas</h2>" +
      '<h3 class="small">Ranking e percentil estadual (taxa média 2012–2025, municípios com 5.000+ hab. em 2025)</h3>' +
      '<div id="uru-tabela-ranking" class="table-scroll" style="margin-bottom:1.5rem"></div>' +
      '<h3 class="small">Tendência anual (2018–2025) — Uruguaiana vs. estado</h3>' +
      '<div id="uru-tabela-tendencia" class="table-scroll" style="margin-bottom:1.5rem"></div>' +
      '<h3 class="small">Sazonalidade mensal (2018–2026) — Uruguaiana vs. estado</h3>' +
      '<div id="uru-tabela-sazonalidade" class="table-scroll" style="margin-bottom:1.5rem"></div>' +
      '<h3 class="small">Taxa geral anual — Uruguaiana, COREDE Fronteira Oeste e estado (2012–2025)</h3>' +
      '<div id="uru-tabela-corede" class="table-scroll" style="margin-bottom:1.5rem"></div>' +
      '<h3 class="small">Taxa geral anual — efeito fronteira vs. efeito porte (2012–2025)</h3>' +
      '<div id="uru-tabela-porte" class="table-scroll"></div>' +
      "</section>" +
      '<section class="card">' +
      "<h2>Principais resultados</h2>" +
      "<ul>" +
      "<li><strong>Tendência (2018-2025):</strong> a queda de Ameaça observada no estado (p=0,010) se replica em Uruguaiana, e com " +
      "sinal ainda mais forte localmente (p=0,0004, Mann-Kendall p=0,0017). Já a alta de Estupro que é significativa no estado " +
      "(p=0,023) não aparece em Uruguaiana (p=0,553, sem tendência detectável). Na direção oposta, Lesão Corporal tem queda " +
      "significativa em Uruguaiana (p=0,011) que o estado como um todo não mostra (p=0,078) — um padrão que é local, não visível " +
      "na agregação estadual.</li>" +
      "<li><strong>Sazonalidade:</strong> Ameaça e Estupro têm diferença significativa entre meses no estado, mas não em Uruguaiana " +
      "isoladamente (p=0,229 e p=0,403) — n baixo por mês num único município reduz bastante o poder do teste. Lesão Corporal é a " +
      "exceção: sazonalidade significativa tanto no estado (p=5,9e-12) quanto em Uruguaiana (p=0,043, mais marginal).</li>" +
      "<li><strong>Ranking:</strong> acima da mediana estadual nos 5 tipos de crime, com destaque para Lesão Corporal (top 11,3%).</li>" +
      "<li><strong>Contexto espacial:</strong> hot spot (Alto-Alto) só em Lesão Corporal — Uruguaiana faz parte de uma mancha " +
      "regional de taxa alta nesse tipo específico, mas não em Ameaça/Estupro.</li>" +
      "<li><strong>Região:</strong> consistentemente um pouco acima do resto do COREDE Fronteira Oeste e do estado, sem uma " +
      "ruptura clara de padrão.</li>" +
      "<li><strong>Porte vs. fronteira:</strong> o achado mais contraintuitivo — a hipótese de \"cidade de fronteira tem mais " +
      "violência\" não se sustenta nesta comparação de 5 municípios; os polos do interior sem fronteira (Santa Cruz do Sul, " +
      "Bento Gonçalves, Erechim) têm taxa geral média mais alta que as duas cidades de fronteira (Uruguaiana e Bagé).</li>" +
      "</ul>" +
      '<div class="callout">' +
      "<h4>Leitura geral</h4>" +
      "<p>Uruguaiana não é um caso atípico dramático — está consistentemente acima da mediana/média estadual e regional, mas por " +
      "margens moderadas, e o único cluster espacial local significativo é em Lesão Corporal. O achado mais informativo talvez " +
      "seja metodológico: tendência e sazonalidade estaduais nem sempre se replicam no nível de um único município (Estupro é o " +
      "exemplo mais claro), o que é um lembrete de que a Camada 2 descreve o estado como um todo, não necessariamente cada " +
      "município individualmente.</p>" +
      "</div>" +
      "</section>" +
      '<section class="card">' +
      "<h2>Limitações do estudo</h2>" +
      '<div class="callout warn">' +
      "<h4>Comparação de porte/fronteira é descritiva, não um teste estatístico</h4>" +
      "<p>A comparação da Seção 6 (efeito fronteira vs. efeito porte) usa poucos municípios (n=1 e n=3 por grupo) — não tem poder " +
      "estatístico para separar \"efeito fronteira\" de variação normal entre municípios de porte parecido. Não deve ser lida como " +
      "prova de que fronteira não importa, só como um achado que não confirma a hipótese inicial e merece investigação com mais " +
      "municípios de cada grupo antes de qualquer conclusão mais forte.</p>" +
      "</div>" +
      '<div class="callout warn">' +
      "<h4>Poder estatístico menor que a análise estadual</h4>" +
      "<p>Com um único município, o tamanho de amostra por mês/ano é bem menor que a soma do estado — isso reduz o poder dos " +
      "testes de tendência e sazonalidade. Um resultado \"não significativo\" em Uruguaiana não significa necessariamente \"sem " +
      "padrão real ali\", só \"não detectável com esse tamanho de amostra\".</p>" +
      "</div>" +
      '<div class="callout warn">' +
      "<h4>Feminicídio Consumado e Tentado têm poucos casos</h4>" +
      "<p>Poucas dezenas de casos acumulados em 14 anos — a taxa por 100 mil hab. é estatisticamente instável nessas duas " +
      "categorias (1-2 casos a mais ou a menos move a taxa proporcionalmente muito mais do que em Ameaça/Lesão Corporal).</p>" +
      "</div>" +
      "<p class=\"small muted\">Ver também as limitações gerais de dados (população, ano parcial de 2026, etc.) na página " +
      '<a href="metodologia.html">Metodologia</a>.</p>' +
      "</section>"
    );
  }

  function renderUruguaiana(container) {
    container.innerHTML = templateUruguaiana();

    Promise.all([
      fetchJSON("reports/uruguaiana_perfil.json"),
      fetchJSON("reports/uruguaiana_resumo_corede.json"),
      fetchJSON("reports/uruguaiana_ranking_percentil.json"),
      fetchJSON("reports/uruguaiana_lisa.json"),
      fetchJSON("reports/uruguaiana_comparacao_tendencia.json"),
      fetchJSON("reports/uruguaiana_comparacao_sazonalidade.json"),
      fetchJSON("reports/uruguaiana_comparacao_corede.json"),
      fetchJSON("reports/uruguaiana_comparacao_porte.json"),
    ]).then(function (res) {
      var perfil = res[0];
      var resumoCorede = res[1][0];
      var ranking = res[2];
      var lisa = res[3];
      var compTendencia = res[4];
      var compSazonalidade = res[5];
      var compCorede = res[6];
      var compPorte = res[7];

      // Caracterização
      var carac = document.getElementById("uru-caracterizacao");
      carac.innerHTML =
        "<p>População (2025): <strong>" +
        resumoCorede.populacao_2025.toLocaleString("pt-BR") +
        "</strong> habitantes. Pertence ao <strong>COREDE " +
        resumoCorede.corede +
        "</strong>, do qual representa <strong>" +
        resumoCorede.pct_populacao_corede_2025 +
        "%</strong> da população regional (2025) — a maior cidade da região.</p>";

      // Indicadores
      montarTilesRazao(document.getElementById("uru-tiles"), perfil, "taxa estadual");

      // Galeria
      montarGaleria(document.getElementById("uru-galeria"), [
        { arquivo: "uruguaiana_perfil_taxa_vs_estado.png", alt: "Uruguaiana vs. média estadual, taxa por 100 mil hab., acumulada 2012-2025", legenda: "Uruguaiana vs. média estadual — taxa por 100 mil hab. (acumulada 2012–2025)" },
        { arquivo: "uruguaiana_serie_anual.png", alt: "Série anual de Uruguaiana por tipo de crime, 2012-2026", legenda: "Série anual por tipo de crime (2012–2026, 2026 parcial)" },
        { arquivo: "uruguaiana_serie_mensal.png", alt: "Série mensal de Uruguaiana por tipo de crime, 2018-2026", legenda: "Série mensal por tipo de crime (2018–2026, 2026 parcial)" },
        { arquivo: "uruguaiana_ranking_percentil.png", alt: "Posição de Uruguaiana no ranking estadual por taxa", legenda: "Posição no ranking estadual por taxa (média 2012–2025)" },
        { arquivo: "uruguaiana_vs_corede_vs_estado.png", alt: "Uruguaiana vs. COREDE Fronteira Oeste vs. estado, taxa geral 2012-2025", legenda: "Uruguaiana vs. COREDE Fronteira Oeste vs. estado — taxa geral (2012–2025)" },
        { arquivo: "uruguaiana_porte_fronteira.png", alt: "Uruguaiana — efeito fronteira vs. efeito porte, 2012-2025", legenda: "Efeito fronteira vs. efeito porte (2012–2025)" },
      ]);

      // Mapa
      montarMapaFoco("uru-map", "uru-select-mapa", "uru-map-legend", "URUGUAIANA", "Lesão Corporal");

      // Tabela LISA
      montarTabela(
        document.getElementById("uru-tabela-lisa"),
        [
          { key: "tipo_crime", label: "Tipo de crime" },
          { key: "categoria_lisa", label: "Classificação LISA" },
          { key: "taxa_2021_2025", label: "Taxa (2021-2025)", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "moran_local_i", label: "Moran local I", numeric: true, format: function (v) { return v.toFixed(3); } },
          { key: "p_valor_permutacao", label: "p-valor", numeric: true, format: function (v) { return v.toFixed(3); } },
        ],
        lisa,
        { caption: "LISA por tipo de crime (só os 3 tipos com Moran Global estadual significativo)" }
      );

      // Tabela ranking
      montarTabela(
        document.getElementById("uru-tabela-ranking"),
        [
          { key: "tipo_crime", label: "Tipo de crime" },
          { key: "posicao", label: "Posição", numeric: true },
          { key: "n_elegiveis", label: "De (município elegíveis)", numeric: true },
          { key: "top_pct", label: "Top %", numeric: true, format: function (v) { return v.toFixed(1) + "%"; } },
          { key: "taxa_uruguaiana", label: "Taxa Uruguaiana", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "mediana_estadual", label: "Mediana estadual", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "acima_da_mediana", label: "Acima da mediana", format: function (v) { return v ? "Sim" : "Não"; } },
        ],
        ranking,
        { defaultSort: { key: "posicao", dir: "asc" } }
      );

      // Tabela tendência
      montarTabela(
        document.getElementById("uru-tabela-tendencia"),
        [
          { key: "tipo_crime", label: "Tipo de crime" },
          { key: "slope_uruguaiana", label: "Inclinação (Uruguaiana)", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "p_valor_linregress_uruguaiana", label: "p (Uruguaiana)", numeric: true, format: function (v) { return v.toExponential(2); } },
          { key: "significativo_linregress_5pct_uruguaiana", label: "Sig. (Uruguaiana)", format: function (v) { return v ? "Sim" : "Não"; } },
          { key: "slope_estado", label: "Inclinação (estado)", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "p_valor_linregress_estado", label: "p (estado)", numeric: true, format: function (v) { return v.toExponential(2); } },
          { key: "significativo_linregress_5pct_estado", label: "Sig. (estado)", format: function (v) { return v ? "Sim" : "Não"; } },
        ],
        compTendencia
      );

      // Tabela sazonalidade
      montarTabela(
        document.getElementById("uru-tabela-sazonalidade"),
        [
          { key: "tipo_crime", label: "Tipo de crime" },
          { key: "estatistica_h_uruguaiana", label: "H (Uruguaiana)", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "p_valor_uruguaiana", label: "p (Uruguaiana)", numeric: true, format: function (v) { return v.toExponential(2); } },
          { key: "significativo_5pct_uruguaiana", label: "Sig. (Uruguaiana)", format: function (v) { return v ? "Sim" : "Não"; } },
          { key: "estatistica_h_estado", label: "H (estado)", numeric: true, format: function (v) { return v.toFixed(2); } },
          { key: "p_valor_estado", label: "p (estado)", numeric: true, format: function (v) { return v.toExponential(2); } },
          { key: "significativo_5pct_estado", label: "Sig. (estado)", format: function (v) { return v ? "Sim" : "Não"; } },
        ],
        compSazonalidade
      );

      // Tabela COREDE (série anual)
      montarTabela(
        document.getElementById("uru-tabela-corede"),
        [
          { key: "ano", label: "Ano", numeric: true },
          { key: "uruguaiana", label: "Uruguaiana", numeric: true, format: function (v) { return v.toFixed(1); } },
          { key: "corede_resto", label: "COREDE (sem Uruguaiana)", numeric: true, format: function (v) { return v.toFixed(1); } },
          { key: "estado", label: "Estado", numeric: true, format: function (v) { return v.toFixed(1); } },
        ],
        compCorede,
        { defaultSort: { key: "ano", dir: "desc" } }
      );

      // Tabela porte/fronteira (série anual)
      montarTabela(
        document.getElementById("uru-tabela-porte"),
        [
          { key: "ano", label: "Ano", numeric: true },
          { key: "uruguaiana", label: "Uruguaiana", numeric: true, format: function (v) { return v.toFixed(1); } },
          { key: "bage", label: "Bagé", numeric: true, format: function (v) { return v.toFixed(1); } },
          { key: "grupo_porte_sem_fronteira", label: "Santa Cruz/Bento Gonç./Erechim (média)", numeric: true, format: function (v) { return v.toFixed(1); } },
          { key: "estado", label: "Estado", numeric: true, format: function (v) { return v.toFixed(1); } },
        ],
        compPorte,
        { defaultSort: { key: "ano", dir: "desc" } }
      );
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
