# bastos_camboim_2025

## Referência (ABNT completa, conforme a folha de rosto do PDF)

BASTOS, Tiago Luiz; CAMBOIM, Silvana Philippi. Comparação e Análise de Métodos de Disponibilização e Publicação de Mapas Topográficos na Web. **Revista Brasileira de Cartografia**, v. 77, 2025. DOI: 10.14393/rbcv77n0a-75024. ISSN 1808-0936.

(Folha de rosto p. 1; recebido 08.2024, aceito 02.2025.)

## O que é (2-3 linhas)

Artigo de pesquisa aplicada/experimental: desenvolve um mapa interativo de teste e compara três métodos de disponibilização de mapas topográficos na web (WMS, GeoJSON, Vector Tiles), usando a base cartográfica vetorial contínua do Rio de Janeiro na escala 1:25.000 (IBGE), avaliando desempenho, interação e qualidade gráfica (p. 1, resumo).

## Afirmações centrais (com página)

1. Foram comparadas três abordagens: Método 1 — WMS (GeoServer, estilos SLD); Método 2 — arquivos GeoJSON (estilo CSS no cliente); Método 3 — Vector Tiles (GeoServer/WMTS, formato MVT, estilo CSS no cliente) (p. 10-11).
2. Base de dados: Base Cartográfica Vetorial Contínua do RJ, escala 1:25.000 (RJ25), ET-EDGV 3.0, 33 classes selecionadas de 19 categorias, ~2,25 GB no total (p. 5-6).
3. Nos testes de desempenho (Quadro 8, duas áreas de teste, 5 execuções cada), Vector Tiles teve o melhor resultado: tempo médio de renderização 5,25-5,73s e 1,4-1,8 MB transferidos; GeoJSON teve tempo similar (5,79-5,83s) mas 107 MB transferidos — numa área ~60 vezes menor que a do WMS; WMS teve o pior tempo (14,58-15,89s) com 6,3-7,4 MB (p. 14-15).
4. Quanto à interação do usuário: WMS oferece interação limitada (imagens estáticas, só recuperação via GetFeatureInfo por pixel); GeoJSON e Vector Tiles permitem interação avançada com objetos vetoriais individuais (busca, rotas, animação) (p. 15-16).
5. Conclusão: "se revelou a melhor solução dentre as três abordagens" (citação literal, <15 palavras) refere-se ao Vector Tiles — GeoJSON foi classificado como a solução "menos adequada para a publicação de um grande volume de dados geoespaciais"; WMS continua sendo o padrão adotado pela INDE, mas os autores apontam que ele e o padrão SLD estão sendo substituídos por novas OGC APIs (p. 17-18).

## Respostas às perguntas dirigidas

**Quais abordagens foram comparadas, com que dados e que critérios?** Três abordagens (WMS, GeoJSON, Vector Tiles), com a base cartográfica RJ25 do IBGE (escala 1:25.000, ET-EDGV 3.0, 33 classes). Critérios de comparação: estrutura e volume de dados, eficiência/desempenho de processamento e renderização, flexibilidade de interação do usuário, e qualidade gráfica (fidelidade visual da simbolização) (p. 13).

**Qual o resultado por critério?**
- *Volume de dados/desempenho de renderização* (p. 14-15): Vector Tiles venceu (menor volume: 1,4-1,8 MB; tempo médio 5,25-5,73s); GeoJSON teve tempo parecido mas volume muito maior (107 MB, em área ~60x menor); WMS foi o mais lento (14,58-15,89s).
- *Interação do usuário* (p. 15-16): WMS limitada (imagem estática); GeoJSON e Vector Tiles permitem interação rica com feições individuais.
- *Qualidade gráfica* (p. 16-17): sem grandes variações entre os três métodos, mas com ressalva metodológica explícita — não foram feitos testes de legibilidade, leitura de mapa ou percepção da simbologia; "qualidade gráfica" foi definida apenas como fidelidade de reprodução visual dos símbolos escolhidos, não como eficácia comunicativa. WMS depende de regras por nível de zoom (raster, generalização não tratada); GeoJSON e Vector Tiles mantêm qualidade em qualquer zoom (vetorial); Vector Tiles teve problema técnico com texturas/hachuras em PNG (travamento), contornado usando cores sólidas.

**Há recomendação por contexto de uso?** Não é uma recomendação por contexto de uso distinto (não há uma matriz do tipo "use X quando A, Y quando B") — os autores fazem uma classificação geral de adequação: Vector Tiles é apontado como a melhor solução das três para publicação de mapas topográficos na web (grande volume de dados, bom desempenho, boa interatividade); GeoJSON é desaconselhado especificamente para grandes volumes de dados (só viável na área de teste reduzida usada no artigo); WMS é reconhecido como o padrão ainda vigente na INDE (interoperável via SLD) mas apontado como tecnologicamente ultrapassado, com recomendação explícita de que a INDE se prepare para a transição às novas OGC APIs (p. 17-18).

## Não responde a

- Não trata de mapas temáticos/coropléticos nem de classificação de dados estatísticos (número de classes, quantis) — o objeto são mapas topográficos de referência (feições físicas: hidrografia, relevo, transporte etc.), não mapas de taxas ou indicadores.
- Não faz testes de legibilidade ou percepção com usuários reais — os próprios autores destacam essa ausência como limitação e item de pesquisa futura (p. 16, 19).
- Não trata de mapas de violência, saúde pública ou epidemiologia — é puramente sobre arquitetura técnica de publicação web de dados topográficos.
