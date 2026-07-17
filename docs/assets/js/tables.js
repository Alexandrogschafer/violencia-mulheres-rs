// Tabelas pesquisáveis/ordenáveis em JS puro (sem dependência externa).
// Usado tanto para a tabela grande de municípios quanto para a visão em
// tabela de cada gráfico (o par de acessibilidade exigido para todo gráfico).
window.SiteTables = (function () {
  function cmp(a, b, numeric) {
    if (numeric) {
      var na = Number(a),
        nb = Number(b);
      if (Number.isNaN(na)) na = -Infinity;
      if (Number.isNaN(nb)) nb = -Infinity;
      return na - nb;
    }
    return String(a).localeCompare(String(b), "pt-BR");
  }

  // columns: [{ key, label, numeric, format(value) }]
  // rows: array of plain objects
  // opts: { searchable, searchPlaceholder, caption, defaultSort: {key, dir} }
  function renderTable(container, columns, rows, opts) {
    opts = opts || {};
    var state = {
      sortKey: (opts.defaultSort && opts.defaultSort.key) || null,
      sortDir: (opts.defaultSort && opts.defaultSort.dir) || "asc",
      query: "",
    };

    container.innerHTML = "";

    if (opts.searchable) {
      var controls = document.createElement("div");
      controls.className = "table-controls";
      var input = document.createElement("input");
      input.type = "search";
      input.placeholder = opts.searchPlaceholder || "Pesquisar…";
      input.addEventListener("input", function () {
        state.query = input.value.trim().toLowerCase();
        renderBody();
      });
      var meta = document.createElement("span");
      meta.className = "table-meta";
      controls.appendChild(input);
      controls.appendChild(meta);
      container.appendChild(controls);
      state._meta = meta;
    }

    var scroll = document.createElement("div");
    scroll.className = "table-scroll";
    var table = document.createElement("table");
    if (opts.caption) {
      var caption = document.createElement("caption");
      caption.textContent = opts.caption;
      table.appendChild(caption);
    }
    var thead = document.createElement("thead");
    var headRow = document.createElement("tr");
    function activateSort(col) {
      if (state.sortKey === col.key) {
        state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
      } else {
        state.sortKey = col.key;
        state.sortDir = col.numeric ? "desc" : "asc";
      }
      columns.forEach(function (c) {
        var h = headRow.querySelector('th[data-key="' + c.key + '"]');
        var active = c.key === state.sortKey;
        h.setAttribute("data-sort", active ? state.sortDir : "");
        h.setAttribute("aria-sort", active ? (state.sortDir === "asc" ? "ascending" : "descending") : "none");
      });
      renderBody();
    }
    columns.forEach(function (col) {
      var th = document.createElement("th");
      th.textContent = col.label;
      th.dataset.key = col.key;
      th.setAttribute("data-sort", state.sortKey === col.key ? state.sortDir : "");
      th.setAttribute("scope", "col");
      // Cabeçalho ordenável precisa ser operável por teclado, não só por
      // clique de mouse -- tabindex + role="button" + Enter/Espaço.
      th.setAttribute("tabindex", "0");
      th.setAttribute("role", "button");
      th.setAttribute(
        "aria-sort",
        state.sortKey === col.key ? (state.sortDir === "asc" ? "ascending" : "descending") : "none"
      );
      th.addEventListener("click", function () {
        activateSort(col);
      });
      th.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " " || ev.key === "Spacebar") {
          ev.preventDefault();
          activateSort(col);
        }
      });
      headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);
    var tbody = document.createElement("tbody");
    table.appendChild(tbody);
    scroll.appendChild(table);
    container.appendChild(scroll);

    function renderBody() {
      var filtered = rows;
      if (state.query) {
        filtered = rows.filter(function (row) {
          return columns.some(function (col) {
            return String(row[col.key] ?? "").toLowerCase().indexOf(state.query) !== -1;
          });
        });
      }
      if (state.sortKey) {
        var col = columns.find(function (c) {
          return c.key === state.sortKey;
        });
        filtered = filtered.slice().sort(function (a, b) {
          var r = cmp(a[state.sortKey], b[state.sortKey], col && col.numeric);
          return state.sortDir === "asc" ? r : -r;
        });
      }
      tbody.innerHTML = "";
      filtered.forEach(function (row) {
        var tr = document.createElement("tr");
        columns.forEach(function (col) {
          var td = document.createElement("td");
          var value = row[col.key];
          td.textContent = col.format ? col.format(value, row) : value ?? "—";
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      if (state._meta) {
        state._meta.textContent = filtered.length + " de " + rows.length + " linhas";
      }
    }

    renderBody();
  }

  // Liga um botão "ver como tabela" a um par canvas/tabela dentro do mesmo
  // figure.chart-figure -- alterna a visibilidade sem duplicar dado algum.
  function wireToggle(figureEl) {
    var btn = figureEl.querySelector(".btn-toggle");
    var canvasWrap = figureEl.querySelector(".chart-canvas-wrap");
    var tableView = figureEl.querySelector(".table-view");
    if (!btn || !canvasWrap || !tableView) return;
    btn.addEventListener("click", function () {
      var showingTable = tableView.classList.toggle("is-visible");
      canvasWrap.classList.toggle("is-hidden", showingTable);
      btn.setAttribute("aria-pressed", String(showingTable));
      btn.textContent = showingTable ? "Ver gráfico" : "Ver como tabela";
    });
  }

  return { renderTable: renderTable, wireToggle: wireToggle };
})();
