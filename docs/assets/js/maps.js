// Mapa interativo Leaflet -- choropleth client-side, com seletor de tipo de
// crime. A rampa sequencial (tons) vem de taxasPorTipo.paleta (JSON gerado
// por build_site_data.py, que lê de src/analysis/mapa_choropleth.py -- a
// mesma paleta oficial usada nas figuras estáticas do capítulo/artigo, ver
// PALETA_OFICIAL em figuras_capitulo.py), não mais hardcoded aqui -- assim
// uma troca de paleta lá se reflete aqui sem editar este arquivo.
window.SiteMaps = (function () {
  var COR_SEM_DADO = "#e1e0d9";
  // Município abaixo do piso populacional: preenchimento sólido próprio,
  // fora da rampa quantitativa. Cinza neutro mais claro que o das figuras
  // estáticas do capítulo (mapa_choropleth.py, COR_ABAIXO_PISO, #c5c0b1),
  // de propósito: aqui deve recuar diante da rampa fria. Não clarear mais:
  // perto de #dcdad5 fica indistinguível de COR_SEM_DADO.
  var COR_ABAIXO_PISO = "#d4d3d0";
  // No zoom 11 o menor município da malha (São Vendelino) ocupa ~100 px;
  // acima disso a tela vira um único preenchimento, sem nada de referência.
  var ZOOM_MAXIMO = 11;
  var MARGEM_LIMITES = 0.05;
  var ATRIBUICAO_FONTES =
    'Malha municipal: <a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html">IBGE</a> · Dados: SSP/RS';

  function hexToRgb(hex) {
    var v = parseInt(hex.replace("#", ""), 16);
    return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
  }
  function rgbToHex(rgb) {
    return (
      "#" +
      rgb
        .map(function (c) {
          return Math.round(c).toString(16).padStart(2, "0");
        })
        .join("")
    );
  }

  // Interpola dentro dos tons de `ramp` (mesma lógica de uma
  // LinearSegmentedColormap contínua do matplotlib) -- `ramp` vem de
  // taxasPorTipo.paleta, gravado por build_site_data.py.
  function rampColor(ramp, t) {
    t = Math.max(0, Math.min(1, t));
    var n = ramp.length - 1;
    var pos = t * n;
    var i0 = Math.floor(pos);
    var i1 = Math.min(i0 + 1, n);
    var frac = pos - i0;
    var c0 = hexToRgb(ramp[i0]);
    var c1 = hexToRgb(ramp[i1]);
    var mix = c0.map(function (v, idx) {
      return v + (c1[idx] - v) * frac;
    });
    return rgbToHex(mix);
  }

  // opts.destacarMunicipio: nome (maiúsculas, como no geojson) de um único
  // município a enquadrar/realçar -- usado pelas páginas de estudo de caso
  // para reaproveitar este mesmo mapa estadual, só mudando o enquadramento
  // inicial. Sem esse opt, comportamento idêntico ao mapa estadual completo.
  function initMap(elementId, geojson, taxasPorTipo, opts) {
    opts = opts || {};
    var tipos = Object.keys(taxasPorTipo.taxas);
    var tipoAtual = opts.tipoInicial || tipos[0];
    var destaque = opts.destacarMunicipio || null;

    // Sem mapa-base: só os polígonos municipais sobre o fundo do contêiner
    // (ver #map em site.css). Fora da malha não há nada para ver, então o
    // enquadramento e o arraste ficam presos aos limites dela (com a pequena
    // folga de MARGEM_LIMITES), e o zoom mínimo é o que mostra o estado
    // inteiro no tamanho atual do contêiner. zoomSnap fracionário: sem tiles
    // não há imagem a borrar, e o estado aproveita melhor a área do mapa.
    var limites = L.geoJSON(geojson).getBounds();
    var map = L.map(elementId, {
      scrollWheelZoom: false,
      zoomSnap: 0.25,
      maxZoom: ZOOM_MAXIMO,
      maxBounds: limites.pad(MARGEM_LIMITES),
      maxBoundsViscosity: 1,
    });

    function ajustarZoomMinimo() {
      // getBoundsZoom limita o resultado ao minZoom vigente -- zera antes,
      // senão o mínimo nunca desce quando o contêiner encolhe.
      map.options.minZoom = 0;
      map.setMinZoom(map.getBoundsZoom(limites));
    }
    ajustarZoomMinimo();
    map.fitBounds(limites);
    map.on("resize", ajustarZoomMinimo);

    map.attributionControl.addAttribution(ATRIBUICAO_FONTES);

    // Atribuição do Leaflet por padrão também fica no canto inferior
    // direito -- move pra esquerda pra não sobrepor a legenda customizada
    // (opts.legendId), que fica no inferior direito quando usada como
    // overlay (ver .map-legend-overlay em site.css).
    map.attributionControl.setPosition("bottomleft");

    // O container pode não ter o tamanho final ainda no momento em que o
    // Leaflet mede a área disponível (fontes/layout assíncronos, troca de
    // aba, etc.) -- invalidateSize() força um recálculo depois que o
    // layout assenta, evitando mapa mal centralizado.
    setTimeout(function () {
      map.invalidateSize();
    }, 150);

    var geoLayer = null;
    var infoBox = document.getElementById(opts.infoId);

    // Auditoria metodológica, item 8: o mapa continua mostrando os 497
    // municípios (nunca esconde nenhum) -- mas, como nas figuras do
    // capítulo e na tabela de municípios (piso de 5.000 hab.), os
    // municípios abaixo do piso saem da rampa quantitativa (cor sólida
    // própria, ver COR_ABAIXO_PISO e corPara) e são marcados como
    // instáveis no popup, para não apresentar como diretamente comparável
    // um valor que o manuscrito trata como estatisticamente instável.
    var abaixoDoPiso = {};
    (taxasPorTipo.municipios_abaixo_piso || []).forEach(function (m) {
      abaixoDoPiso[m] = true;
    });
    function fmtPiso(n) {
      return Number(n).toLocaleString("pt-BR");
    }

    function valoresDoTipo(tipo) {
      return taxasPorTipo.taxas[tipo] || {};
    }

    function dominioDoTipo(tipo) {
      return (taxasPorTipo.dominio_por_tipo || {})[tipo] || { min: 0, max: 0 };
    }

    function corPara(tipo, valores, municipio, dominio) {
      // Abaixo do piso: cor sólida própria, fora da rampa quantitativa --
      // não entra no min/max (já calculado sem eles em build_site_data.py),
      // então nem tenta posicionar esses municípios na escala.
      if (abaixoDoPiso[municipio]) return COR_ABAIXO_PISO;
      var v = valores[municipio];
      if (v === undefined || v === null) return COR_SEM_DADO;
      var t = dominio.max > dominio.min ? (v - dominio.min) / (dominio.max - dominio.min) : 0.5;
      return rampColor(taxasPorTipo.paleta, t);
    }

    function desenhar(tipo) {
      var valores = valoresDoTipo(tipo);
      var dominio = dominioDoTipo(tipo);
      if (geoLayer) map.removeLayer(geoLayer);
      var camadaDestaque = null;
      geoLayer = L.geoJSON(geojson, {
        style: function (feature) {
          var emDestaque = destaque && feature.properties.municipio === destaque;
          return {
            fillColor: corPara(tipo, valores, feature.properties.municipio, dominio),
            weight: emDestaque ? 3 : 0.6,
            color: emDestaque ? "#0b0b0b" : "#ffffff",
            fillOpacity: 0.9,
          };
        },
        onEachFeature: function (feature, layer) {
          var municipio = feature.properties.municipio;
          var v = valores[municipio];
          var texto =
            "<strong>" +
            municipio +
            "</strong><br>" +
            tipo +
            ": " +
            (v === undefined || v === null ? "sem dado" : v.toFixed(1) + " / 100 mil hab.");
          if (abaixoDoPiso[municipio]) {
            texto +=
              '<br><span class="muted small">População abaixo de ' +
              fmtPiso(taxasPorTipo.piso_populacional_instabilidade) +
              " hab. — taxa instável, poucos casos podem deslocá-la muito. Não comparável diretamente aos demais municípios.</span>";
          }
          layer.bindTooltip(texto, { sticky: true });
          layer.on({
            mouseover: function (e) {
              e.target.setStyle({ weight: 2, color: "#0b0b0b" });
            },
            mouseout: function (e) {
              geoLayer.resetStyle(e.target);
            },
            click: function () {
              if (infoBox) infoBox.innerHTML = texto;
            },
          });
          if (destaque && municipio === destaque) camadaDestaque = layer;
        },
      }).addTo(map);
      atualizarLegenda(tipo, dominio);
      if (camadaDestaque) {
        camadaDestaque.bringToFront();
        map.fitBounds(camadaDestaque.getBounds(), { padding: [60, 60], maxZoom: 10 });
      }
    }

    function atualizarLegenda(tipo, dominio) {
      var legendEl = document.getElementById(opts.legendId);
      if (!legendEl) return;
      var min = dominio.min;
      var max = dominio.max;
      var passos = 5;
      var html =
        "<strong>" +
        tipo +
        "</strong> — taxa por 100 mil hab. (" +
        taxasPorTipo.ano_inicio +
        "–" +
        taxasPorTipo.ano_fim +
        ")<br>";
      for (var i = 0; i <= passos; i++) {
        var t = i / passos;
        var v = min + t * (max - min);
        html +=
          '<span class="ramp" style="background:' + rampColor(taxasPorTipo.paleta, t) + '"></span>' + v.toFixed(1) + " ";
      }
      html += '<span class="ramp" style="background:' + COR_SEM_DADO + '"></span>sem dado';
      var nAbaixoPiso = (taxasPorTipo.municipios_abaixo_piso || []).length;
      if (nAbaixoPiso > 0) {
        // Entrada própria, fora da rampa quantitativa (mesmo texto das
        // figuras estáticas do capítulo, ver mapa_choropleth.py) -- não é
        // mais uma nota textual solta, é um item de legenda com a mesma
        // amostra de cor usada no preenchimento desses municípios.
        html +=
          '<br><span class="ramp" style="background:' +
          COR_ABAIXO_PISO +
          '"></span>População inferior a ' +
          fmtPiso(taxasPorTipo.piso_populacional_instabilidade) +
          " hab.";
        html +=
          '<br><span class="muted small">' +
          nAbaixoPiso +
          " municípios (marcados no mapa ao passar o mouse) têm taxa instável — poucos casos deslocam muito o valor. Não são diretamente comparáveis aos demais.</span>";
      }
      legendEl.innerHTML = html;
    }

    desenhar(tipoAtual);

    return {
      trocarTipo: function (tipo) {
        tipoAtual = tipo;
        desenhar(tipo);
      },
      tipos: tipos,
    };
  }

  return { initMap: initMap };
})();
