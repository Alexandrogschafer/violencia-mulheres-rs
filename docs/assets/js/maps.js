// Mapa interativo Leaflet -- choropleth client-side, com seletor de tipo de
// crime. Reaproveita a mesma rampa sequencial azul (claro->escuro) usada nos
// mapas estáticos gerados por src/analysis/mapa_choropleth.py, para manter a
// mesma linguagem visual entre o mapa interativo e as figuras PNG.
window.SiteMaps = (function () {
  var RAMPA_SEQUENCIAL_AZUL = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
  ];
  var COR_SEM_DADO = "#c9c7c0";

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

  // Interpola dentro da rampa de 13 tons (mesma lógica de uma
  // LinearSegmentedColormap contínua do matplotlib).
  function rampColor(t) {
    t = Math.max(0, Math.min(1, t));
    var n = RAMPA_SEQUENCIAL_AZUL.length - 1;
    var pos = t * n;
    var i0 = Math.floor(pos);
    var i1 = Math.min(i0 + 1, n);
    var frac = pos - i0;
    var c0 = hexToRgb(RAMPA_SEQUENCIAL_AZUL[i0]);
    var c1 = hexToRgb(RAMPA_SEQUENCIAL_AZUL[i1]);
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

    var map = L.map(elementId, { scrollWheelZoom: false }).setView([-30.0, -53.2], 6.4);
    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      maxZoom: 12,
    }).addTo(map);

    // Atribuição do Leaflet por padrão também fica no canto inferior
    // direito -- move pra esquerda pra não sobrepor a legenda customizada
    // (opts.legendId), que fica no inferior direito quando usada como
    // overlay (ver .map-legend-overlay em site.css).
    map.attributionControl.setPosition("bottomleft");

    // O container pode não ter o tamanho final ainda no momento em que o
    // Leaflet mede a área disponível (fontes/layout assíncronos, troca de
    // aba, etc.) -- invalidateSize() força um recálculo depois que o
    // layout assenta, evitando tiles cortados/mapa mal centralizado.
    setTimeout(function () {
      map.invalidateSize();
    }, 150);

    var geoLayer = null;
    var infoBox = document.getElementById(opts.infoId);

    function valoresDoTipo(tipo) {
      return taxasPorTipo.taxas[tipo] || {};
    }

    function corPara(tipo, valores, municipio) {
      var v = valores[municipio];
      if (v === undefined || v === null) return COR_SEM_DADO;
      var vals = Object.values(valores);
      var min = Math.min.apply(null, vals);
      var max = Math.max.apply(null, vals);
      var t = max > min ? (v - min) / (max - min) : 0.5;
      return rampColor(t);
    }

    function desenhar(tipo) {
      var valores = valoresDoTipo(tipo);
      if (geoLayer) map.removeLayer(geoLayer);
      var camadaDestaque = null;
      geoLayer = L.geoJSON(geojson, {
        style: function (feature) {
          var emDestaque = destaque && feature.properties.municipio === destaque;
          return {
            fillColor: corPara(tipo, valores, feature.properties.municipio),
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
      atualizarLegenda(tipo, valores);
      if (camadaDestaque) {
        camadaDestaque.bringToFront();
        map.fitBounds(camadaDestaque.getBounds(), { padding: [60, 60], maxZoom: 10 });
      }
    }

    function atualizarLegenda(tipo, valores) {
      var legendEl = document.getElementById(opts.legendId);
      if (!legendEl) return;
      var vals = Object.values(valores);
      var min = Math.min.apply(null, vals);
      var max = Math.max.apply(null, vals);
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
          '<span class="ramp" style="background:' + rampColor(t) + '"></span>' + v.toFixed(1) + " ";
      }
      html += '<span class="ramp" style="background:' + COR_SEM_DADO + '"></span>sem dado';
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
