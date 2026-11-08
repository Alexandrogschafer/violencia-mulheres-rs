"""Gera a versão de submissão do manuscrito, sem os comentários HTML.

Entrada: `artigo_espacial.md` (arquivo de trabalho, com notas internas em comentários HTML).
Saída: `artigo_espacial_submissao.md`, idêntica à entrada exceto pelos comentários removidos
e pelas linhas em branco que eles deixariam sobrando.

Os comentários trazem notas internas e caminhos de arquivo do repositório, que não devem
viajar com a submissão duplo-cega. Rodar de novo sempre que o arquivo de trabalho mudar:

    python gerar_versao_submissao.py
"""

import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ENTRADA = PASTA / "artigo_espacial.md"
SAIDA = PASTA / "artigo_espacial_submissao.md"

COMENTARIO = re.compile(r"[ \t]*<!--.*?-->[ \t]*\n?", re.DOTALL)


def main() -> int:
    texto = ENTRADA.read_text(encoding="utf-8")
    n = len(COMENTARIO.findall(texto))
    limpo = COMENTARIO.sub("", texto)
    limpo = re.sub(r"\n{3,}", "\n\n", limpo)  # um comentário entre parágrafos deixa linha em branco dupla

    if "<!--" in limpo or "-->" in limpo:
        print("ERRO: sobrou delimitador de comentário HTML na versão de submissão.", file=sys.stderr)
        return 1

    SAIDA.write_text(limpo, encoding="utf-8")
    print(f"{SAIDA.name}: {n} comentário(s) removido(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
