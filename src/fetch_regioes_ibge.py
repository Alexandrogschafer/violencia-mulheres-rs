"""Busca o vínculo município -> Região Geográfica Imediata -> Região
Geográfica Intermediária (divisão do IBGE de 2017, que substituiu
microrregião/mesorregião como referência corrente) para os municípios do
RS -- usado como camada de agregação regional no capítulo (COREDEs, em
fetch_coredes.py, são a divisão administrativa estadual; esta aqui é a
divisão geográfica federal, fontes e propósitos diferentes).

Mesmo endpoint de localidades já usado em fetch_malha_municipios.py
(URL_LOCALIDADES) -- a resposta já vem com os campos "regiao-imediata" e,
aninhado nela, "regiao-intermediaria" por município, então não é preciso
nenhum endpoint adicional.

Uso: python -m src.fetch_regioes_ibge
"""

from pathlib import Path

from src.fetch_malha_municipios import URL_LOCALIDADES
from src.fetch_populacao import get_json, normaliza_municipio

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "tables"
    / "municipio_regioes_ibge.csv"
)

N_MUNICIPIOS_RS = 497


def busca_regioes() -> list[dict]:
    """Busca (codigo_ibge, municipio, regiao_imediata, regiao_intermediaria)
    para os municípios do RS. Nome do município normalizado no padrão do
    projeto (normaliza_municipio, mesma função de fetch_populacao.py) --
    necessário para depois juntar com violencia_anual_municipio_taxa.csv.
    """
    municipios = get_json(URL_LOCALIDADES)
    registros = []
    for m in municipios:
        ri = m["regiao-imediata"]
        rint = ri["regiao-intermediaria"]
        registros.append(
            {
                "codigo_ibge": str(m["id"]),
                "municipio": normaliza_municipio(m["nome"]),
                "regiao_imediata_id": ri["id"],
                "regiao_imediata": ri["nome"],
                "regiao_intermediaria_id": rint["id"],
                "regiao_intermediaria": rint["nome"],
            }
        )
    return registros


def main() -> None:
    registros = busca_regioes()

    if len(registros) != N_MUNICIPIOS_RS:
        raise ValueError(
            f"Esperava {N_MUNICIPIOS_RS} municípios do RS, a API devolveu {len(registros)}."
        )
    codigos = {r["codigo_ibge"] for r in registros}
    if len(codigos) != N_MUNICIPIOS_RS:
        raise ValueError(
            f"código_ibge duplicado: {N_MUNICIPIOS_RS} municípios mas só "
            f"{len(codigos)} códigos únicos."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(
            "codigo_ibge,municipio,regiao_imediata_id,regiao_imediata,"
            "regiao_intermediaria_id,regiao_intermediaria\n"
        )
        for r in registros:
            f.write(
                f"{r['codigo_ibge']},{r['municipio']},{r['regiao_imediata_id']},"
                f"\"{r['regiao_imediata']}\",{r['regiao_intermediaria_id']},"
                f"\"{r['regiao_intermediaria']}\"\n"
            )

    n_imediatas = len({r["regiao_imediata_id"] for r in registros})
    n_intermediarias = len({r["regiao_intermediaria_id"] for r in registros})
    print(
        f"Salvo em {OUTPUT_PATH} — {len(registros)}/{N_MUNICIPIOS_RS} municípios "
        f"validados, {n_imediatas} regiões imediatas, {n_intermediarias} regiões "
        "intermediárias."
    )


if __name__ == "__main__":
    main()
