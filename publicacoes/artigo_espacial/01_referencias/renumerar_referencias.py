"""Renumera as citações do manuscrito do artigo espacial em ordem de primeira aparição.

Fonte única: o próprio manuscrito (`02_texto/artigo_espacial.md`). Não há cópia paralela com chaves,
para que nenhuma edição feita direto no manuscrito se perca numa renumeração.

Como citar:
- citações já numeradas, como `[2,4]`, são lidas pela lista «## Referências» ao fim do manuscrito;
- uma citação nova é escrita com a chave da referência, como `{bahia}` ou `{oliveira,barros}`;
- a chave precisa existir em `referencias.json`, que guarda o texto Vancouver de cada uma.

O que o script faz:
1. traduz números e chaves para chaves;
2. renumera pela ordem de primeira aparição;
3. reescreve as citações e a lista no manuscrito;
4. atualiza, em `referencias_vancouver.md`, a lista e a tabela de marcadores (ID → números);
5. atualiza, em `verificacao_referencias.md`, a última coluna do resumo e os «**Referência N.**» e
   «(referência N)».

Os IDs das linhas da tabela de marcadores seguem a ordem do texto. Uma citação nova pede uma linha
nova na tabela, na posição certa. Se o número de linhas não bater com o de citações, o script para.

Uso, a partir de publicacoes/artigo_espacial/:
    python3 01_referencias/renumerar_referencias.py              # renumera e grava
    python3 01_referencias/renumerar_referencias.py --verificar  # só confere; sai com 1 se houver erro
"""

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MANUSCRITO = BASE / "02_texto" / "artigo_espacial.md"
REFS_JSON = BASE / "01_referencias" / "referencias.json"
VANCOUVER = BASE / "01_referencias" / "referencias_vancouver.md"
VERIFICACAO = BASE / "01_referencias" / "verificacao_referencias.md"
LIMITE_RESS = 30
LARGURA = 90
CITACAO = re.compile(r"\[(\d+(?:,\d+)*)\]|\{([a-z0-9_]+(?:,[a-z0-9_]+)*)\}")


def normaliza(texto: str) -> str:
    return " ".join(texto.split())


def separa(manuscrito: str) -> tuple[str, str]:
    marco = "\n## Referências"
    if marco not in manuscrito:
        return manuscrito.rstrip("\n"), ""
    corpo, resto = manuscrito.split(marco, 1)
    return corpo.rstrip("\n"), resto


def lista_atual(resto: str, refs: dict[str, str]) -> dict[int, str]:
    """Número → chave, casando o texto de cada item da lista com referencias.json."""
    por_texto = {normaliza(v): k for k, v in refs.items()}
    itens = re.findall(r"^(\d+)\. (.*?)(?=\n\s*\n\d+\. |\n*\Z)", resto, flags=re.M | re.S)
    mapa, sem_par = {}, []
    for numero, texto in itens:
        chave = por_texto.get(normaliza(texto))
        if chave is None:
            sem_par.append((numero, texto))
        else:
            mapa[int(numero)] = chave
    # Texto alterado só em referencias.json (DOI novo, máscara para avaliação cega): se sobra um único
    # item sem par e uma única chave sem uso, os dois se casam. Mais de um caso é ambíguo e para.
    livres = [k for k in refs if k not in mapa.values()]
    if len(sem_par) == 1 and len(livres) == 1:
        numero, _ = sem_par[0]
        mapa[int(numero)] = livres[0]
        print(f"Item {numero} casado com a chave «{livres[0]}», única sem uso: o texto mudou em "
              "referencias.json e a lista será regravada.")
    elif sem_par:
        numero, texto = sem_par[0]
        sys.exit(f"Item {numero} da lista não está em referencias.json: {normaliza(texto)[:80]}...")
    return mapa


def grupos(corpo: str, num_para_chave: dict[int, str], refs: dict[str, str]) -> list[list[str]]:
    saida = []
    for m in CITACAO.finditer(corpo):
        if m.group(1):
            nums = [int(x) for x in m.group(1).split(",")]
            faltam = [n for n in nums if n not in num_para_chave]
            if faltam:
                sys.exit(f"Citação {m.group(0)} usa número fora da lista: {faltam}")
            saida.append([num_para_chave[n] for n in nums])
        else:
            chaves = m.group(2).split(",")
            faltam = [k for k in chaves if k not in refs]
            if faltam:
                sys.exit(f"Chave sem referência em referencias.json: {faltam}")
            saida.append(chaves)
    return saida


def reescreve_corpo(corpo: str, num_para_chave: dict[int, str], nova: dict[str, int]) -> str:
    def troca(m: re.Match) -> str:
        chaves = [num_para_chave[int(x)] for x in m.group(1).split(",")] if m.group(1) else m.group(2).split(",")
        return "[" + ",".join(str(n) for n in sorted(nova[k] for k in chaves)) + "]"

    paragrafos = corpo.split("\n\n")
    for i, p in enumerate(paragrafos):
        tinha_chave = re.search(r"\{[a-z0-9_,]+\}", p) is not None
        p = CITACAO.sub(troca, p)
        if tinha_chave and not p.lstrip().startswith(("#", "-", "|", "<!--")):
            p = textwrap.fill(normaliza(p), LARGURA)
        paragrafos[i] = p
    return "\n\n".join(paragrafos)


def monta_lista(ordem: list[str], refs: dict[str, str]) -> str:
    itens = []
    for i, chave in enumerate(ordem, 1):
        recuo = " " * (len(str(i)) + 2)
        itens.append(textwrap.fill(f"{i}. {refs[chave]}", 100, subsequent_indent=recuo,
                                   break_long_words=False, break_on_hyphens=False))
    return "\n\n".join(itens)


def conta_palavras(corpo: str) -> int:
    """Critério de 00_protocolo/limite_palavras_ress.md: token com letra ou dígito, da Introdução à
    Conclusão, com subtítulos e chamadas de referência, sem comentários HTML. As seções de nível 2
    depois da Conclusão (disponibilidade de dados, uso de IA) são declarações e ficam fora."""
    sem_comentario = re.sub(r"<!--.*?-->", "", corpo, flags=re.S)
    trecho = sem_comentario[sem_comentario.index("## Introdução"):]
    conclusao = trecho.index("\n## Conclusão")
    depois = trecho.find("\n## ", conclusao + 1)
    if depois != -1:
        trecho = trecho[:depois]
    return sum(1 for t in trecho.replace("**", "").split() if re.search(r"[0-9A-Za-zÀ-ÿ]", t))


def ids_da_tabela(vancouver: str) -> list[str]:
    return re.findall(r"^\|(?: \d+ \|)? (A\w+) \| [^|]* \|$", vancouver, flags=re.M)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verificar", action="store_true", help="só confere, sem gravar")
    args = parser.parse_args()

    refs = json.loads(REFS_JSON.read_text(encoding="utf-8"))
    corpo, resto = separa(MANUSCRITO.read_text(encoding="utf-8"))
    num_para_chave = lista_atual(resto, refs)
    gs = grupos(corpo, num_para_chave, refs)

    ordem: list[str] = []
    for g in gs:
        for k in g:
            if k not in ordem:
                ordem.append(k)
    nova = {k: i + 1 for i, k in enumerate(ordem)}

    erros = []
    if re.search(r"\[n(,n)*\]", corpo):
        erros.append("há marcador [n] sem referência no corpo")
    if len(ordem) > LIMITE_RESS:
        erros.append(f"{len(ordem)} referências, acima do limite de {LIMITE_RESS}")
    nao_citadas = set(num_para_chave.values()) - set(ordem)
    if nao_citadas:
        erros.append(f"referências da lista atual que deixariam de ser citadas: {sorted(nao_citadas)}")
    vancouver = VANCOUVER.read_text(encoding="utf-8")
    ids = ids_da_tabela(vancouver)
    if len(ids) != len(gs):
        erros.append(f"a tabela de marcadores de referencias_vancouver.md tem {len(ids)} linhas e o "
                     f"manuscrito tem {len(gs)} citações; acrescente ou retire linhas antes de renumerar")

    if args.verificar:
        mudou = any(num_para_chave.get(n) != k for k, n in nova.items()) or "{" in "".join(
            m.group(0) for m in CITACAO.finditer(corpo))
        if mudou:
            erros.append("a numeração atual não segue a ordem de primeira aparição (rode sem --verificar)")
        print(f"{len(ordem)} referências; {len(gs)} citações; {conta_palavras(corpo)} palavras no corpo")
        for e in erros:
            print("ERRO:", e)
        sys.exit(1 if erros else 0)

    if erros:
        sys.exit("Nada gravado:\n- " + "\n- ".join(erros))

    novo_corpo = reescreve_corpo(corpo, num_para_chave, nova)
    cabecalho = ("\n\n## Referências\n\n<!-- Lista gerada por 01_referencias/renumerar_referencias.py "
                 "em ordem de primeira aparição. Não editar à mão. -->\n\n")
    lista = monta_lista(ordem, refs)
    MANUSCRITO.write_text(novo_corpo + cabecalho + lista + "\n", encoding="utf-8")

    # referencias_vancouver.md: tabela de marcadores e lista
    linhas = "\n".join(f"| {i} | {id_} | {','.join(str(n) for n in sorted(nova[k] for k in g))} |"
                       for i, (id_, g) in enumerate(zip(ids, gs), 1))
    vancouver = re.sub(r"(\| Ordem \| ID \| Números \|\n\|---\|---\|---\|\n)(?:\|.*\|\n?)+",
                       lambda m: m.group(1) + linhas + "\n", vancouver)
    vancouver = re.sub(r"(## Lista\n\n).*?(\n## |\Z)", lambda m: m.group(1) + lista + "\n" + m.group(2),
                       vancouver, flags=re.S)
    vancouver = re.sub(r"São \d+ referências; o limite", f"São {len(ordem)} referências; o limite", vancouver)
    VANCOUVER.write_text(vancouver, encoding="utf-8")

    # verificacao_referencias.md: resumo e números das entradas
    numeros_id = {id_: ", ".join(str(n) for n in sorted(nova[k] for k in g)) for id_, g in zip(ids, gs)}
    verif = VERIFICACAO.read_text(encoding="utf-8")

    def resumo(m: re.Match) -> str:
        id_ = m.group(2)
        return m.group(1) + numeros_id[id_] + m.group(3) if id_ in numeros_id else m.group(0)

    verif = re.sub(r"^(\| (A\w+) \|.*\| )[^|]*( \|)$", resumo, verif, flags=re.M)
    antigo = lambda n: nova[num_para_chave[n]] if n in num_para_chave else n  # noqa: E731
    verif = re.sub(r"\*\*Referência (\d+)\.\*\*", lambda m: f"**Referência {antigo(int(m.group(1)))}.**", verif)
    verif = re.sub(r"\(referência (\d+)\)", lambda m: f"(referência {antigo(int(m.group(1)))})", verif)
    verif = re.sub(r"São \d+ referências na lista", f"São {len(ordem)} referências na lista", verif)
    VERIFICACAO.write_text(verif, encoding="utf-8")

    print("ordem:", " ".join(f"{nova[k]}={k}" for k in ordem))
    print(f"{len(ordem)} referências; {len(gs)} citações; {conta_palavras(novo_corpo)} palavras no corpo")


if __name__ == "__main__":
    main()
