(function () {
  const TIPOS = ["Ameaça","Lesão Corporal","Estupro","Feminicídio Tentado","Feminicídio Consumado"];
  const $ = s => document.querySelector(s);

  fetch("../assets/data/tables/municipios_resumo_periodo.json").then(r => r.json()).then(resumo => {
    $("#n-municipios").textContent = resumo.length.toLocaleString("pt-BR");
    $("#n-registros").textContent = resumo.reduce((s, r) => s + r.c_geral, 0).toLocaleString("pt-BR");

    $("#baixar-resumo").addEventListener("click", () => {
      const cab = ["municipio","populacao_media_2018_2025"]
        .concat(TIPOS.flatMap(t => ["casos_" + t, "taxa_" + t]))
        .concat(["casos_geral"]);
      const linhas = resumo.map(r => [r.municipio, r.pop_media]
        .concat(TIPOS.flatMap(t => [r["c_" + t], r["t_" + t] ?? ""]))
        .concat([r.c_geral]));
      const csv = [cab.join(",")].concat(linhas.map(l => l.join(","))).join("\n");
      const url = URL.createObjectURL(new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8" }));
      const a = document.createElement("a");
      a.href = url; a.download = "violencia_rs_municipios_2018_2025.csv"; a.click();
      URL.revokeObjectURL(url);
    });
  });
})();
