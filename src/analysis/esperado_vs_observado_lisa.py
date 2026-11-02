"""Esperado sob a taxa estadual frente ao observado, nos 68 pares significativos do LISA.

Esperado = pessoas-ano do município em 2018-2025 × taxa estadual do desfecho / 100 mil. As
pessoas-ano são a soma das oito populações anuais, o mesmo denominador da taxa que entra no
LISA, e correspondem a "população × 8 anos". A taxa estadual é a soma dos eventos sobre a
soma das pessoas-ano dos 497, sem o "NÃO INFORMADO", como no LISA. Como verificação, o
esperado também é calculado com a população de 2025 × 8.

Poisson na direção do quadrante: AA e AB (o próprio município é alto) usam P(X ≥ obs); BB e BA
(o próprio município é baixo) usam P(X ≤ obs). É descritivo e não substitui o LISA: o esperado
ignora a vizinhança, e os 68 pares não são independentes.

Uso: python -m src.analysis.esperado_vs_observado_lisa
"""

from pathlib import Path

import pandas as pd
from scipy.stats import poisson

from src.analysis.caracterizacao_municipios_significativos import br, carregar, componentes, markdown
from src.analysis.mapa_choropleth import carregar_taxa_periodo
from src.analysis.moran_lisa_assuncao_reis import ANO_FIM, ANO_INICIO, TIPOS_MORAN

SAIDA = Path(__file__).resolve().parent.parent.parent / "outputs" / "tables" / "esperado_vs_observado_lisa.md"
LIMIAR = 5
N_PARES = 68
N_BLOCO_NORTE = 21
ALTO = {"AA", "AB"}


def calcular() -> tuple[pd.DataFrame, dict, list[str]]:
    d = carregar()
    sig = d["sig"]
    if len(sig) != N_PARES:
        raise ValueError(f"{len(sig)} pares significativos, esperados {N_PARES}.")
    taxas = {t: carregar_taxa_periodo(t, ANO_INICIO, ANO_FIM).set_index("municipio") for t in TIPOS_MORAN}
    estadual = {t: x["casos_total"].sum() / x["populacao_pessoas_ano"].sum() * 100_000 for t, x in taxas.items()}
    linhas = []
    for _, r in sig.iterrows():
        t, m, q = r["tipo_crime"], r["municipio"], r["categoria"]
        x = taxas[t].loc[m]
        obs = int(x["casos_total"])
        esp = x["populacao_pessoas_ano"] * estadual[t] / 100_000
        esp_2025 = d["pop"][m] * 8 * estadual[t] / 100_000
        p = poisson.sf(obs - 1, esp) if q in ALTO else poisson.cdf(obs, esp)
        linhas.append({"municipio": m, "desfecho": t, "quadrante": q, "observado": obs, "esperado": esp,
                       "esperado_pop2025x8": esp_2025, "razao": obs / esp, "p_poisson": p})
    pares = pd.DataFrame(linhas).sort_values(["quadrante", "desfecho", "esperado"])

    aa = sorted(d["quadrante"].index[d["quadrante"] == "AA"])
    blocos = componentes(aa, d["vizinhos"])
    norte = blocos[0]
    if len(norte) != N_BLOCO_NORTE:
        raise ValueError(f"Maior bloco AA tem {len(norte)} municípios, esperados {N_BLOCO_NORTE}.")
    return pares, estadual, norte


def contagem(p: pd.DataFrame, por: str) -> pd.DataFrame:
    g = p.groupby(por)
    t = pd.DataFrame({
        "Pares": g.size(),
        f"Esperado < {LIMIAR}": g["esperado"].apply(lambda s: int((s < LIMIAR).sum())),
        f"Sobrevivem (esperado ≥ {LIMIAR})": g["esperado"].apply(lambda s: int((s >= LIMIAR).sum())),
        f"Esperado < {LIMIAR}, pop. 2025 × 8": g["esperado_pop2025x8"].apply(lambda s: int((s < LIMIAR).sum())),
        "Poisson p < 0,05": g["p_poisson"].apply(lambda s: int((s < 0.05).sum())),
        f"Esperado ≥ {LIMIAR} e Poisson p < 0,05": g.apply(lambda x: int(((x["esperado"] >= LIMIAR) & (x["p_poisson"] < 0.05)).sum())),
    })
    t.loc["Total"] = t.sum()
    return t.reset_index().rename(columns={por: por.capitalize(), "index": por.capitalize()})


def fmt_p(p: float) -> str:
    return "< 0,0001" if p < 1e-4 else br(p, 4)


def tabela_pares(p: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Município": p["municipio"], "Desfecho": p["desfecho"], "Quadrante": p["quadrante"],
        "Observado": p["observado"], "Esperado": p["esperado"].map(lambda v: br(v, 2)),
        "Obs./esp.": p["razao"].map(lambda v: br(v, 2)), "Poisson, direção do quadrante": p["p_poisson"].map(fmt_p),
        f"Esperado ≥ {LIMIAR}": p["esperado"].map(lambda v: "sim" if v >= LIMIAR else "não"),
    })


def main() -> None:
    p, estadual, norte = calcular()
    pn = p[p["municipio"].isin(norte)]
    por_mun = pn.groupby("municipio").agg(
        pares=("desfecho", "size"), algum=("esperado", lambda s: bool((s >= LIMIAR).any())),
        todos=("esperado", lambda s: bool((s >= LIMIAR).all())))
    algum_poisson = pn.assign(ok=(pn["esperado"] >= LIMIAR) & (pn["p_poisson"] < 0.05)).groupby("municipio")["ok"].any()
    caem = pn[pn["esperado"] < LIMIAR]
    alto = p["quadrante"].isin(ALTO)
    contra = p[(alto & (p["razao"] < 1)) | (~alto & (p["razao"] > 1))]
    taxa_txt = "; ".join(f"{t} {br(v, 2)}" for t, v in estadual.items())
    texto = f"""# Esperado sob a taxa estadual frente ao observado, nos pares significativos do LISA

São os {N_PARES} pares município-desfecho significativos no LISA de Assunção e Reis, 2018-2025 (semente 12345, 99.999 permutações, FDR sobre o p direcional). Gerada por `src/analysis/esperado_vs_observado_lisa.py`.

- **Esperado** = pessoas-ano do município em 2018-2025 × taxa estadual / 100 mil. As pessoas-ano são a soma das oito populações anuais, o mesmo denominador do LISA, e equivalem a "população × 8 anos". Como verificação, há também uma coluna com a população de 2025 × 8.
- **Taxa estadual por 100 mil pessoas-ano**, soma dos 497 municípios, sem "NÃO INFORMADO": {taxa_txt}.
- **Poisson na direção do quadrante:** P(X ≥ obs) em AA e AB; P(X ≤ obs) em BB e BA. É descritivo: não corrige para múltiplas comparações e ignora a vizinhança, que é o que o LISA mede.

## Por quadrante

{markdown(contagem(p, "quadrante"))}

## Por desfecho

{markdown(contagem(p, "desfecho"))}

## Bloco norte em AA ({len(norte)} municípios contíguos)

- **{int(por_mun['algum'].sum())} dos {len(norte)} municípios sobrevivem** ao critério de esperado ≥ {LIMIAR}, com ao menos um par acima do limiar. Em {int(por_mun['todos'].sum())} deles, todos os pares estão acima.
- O bloco tem {len(pn)} pares. {len(caem)} ficam abaixo do limiar: {", ".join(f"{r.municipio} ({r.desfecho}, esperado {br(r.esperado, 2)})" for r in caem.itertuples()) or "nenhum"}.
- Com esperado ≥ {LIMIAR} e também Poisson p < 0,05, sobrevivem {int(algum_poisson.sum())} dos {len(norte)}.

## Pares com o observado do lado oposto ao do quadrante

{len(contra)} pares estão num quadrante "alto" (AA ou AB) com o observado abaixo do esperado estadual. Nenhum está num quadrante "baixo" com o observado acima. Isso não é erro de cálculo. `esda.Moran_Local_Rate` padroniza as taxas pelo método de Assunção e Reis em torno da taxa estadual, mas o LISA centra esses valores na média deles. Essa média é negativa nos quatro desfechos, porque a maioria dos municípios, pequenos, fica abaixo da taxa estadual. Assim, "alto" no LISA quer dizer acima da média dos municípios, não acima da taxa estadual. Nesses pares, P(X ≥ obs) fica acima de 0,5 por construção.

{markdown(tabela_pares(contra))}

## Os {N_PARES} pares

{markdown(tabela_pares(p))}
"""
    SAIDA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
