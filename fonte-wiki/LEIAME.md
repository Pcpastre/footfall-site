# Fonte da wiki

A wiki (`../wiki/`) é gerada. Não edite os .html de lá: edite aqui e gere de novo.

- `paginas/*.html`: os textos (pt-BR), um por página, com a linha de metadados no topo.
- `data/*.json`: os dados tirados do código do jogo por `extract.py` (itens, receitas, saque, zumbis, base, corpo, regras).
- `build_wiki.py`: monta `wiki/` (páginas de texto, uma ficha por item, por lugar, índices, busca).

Para atualizar depois de mudar o jogo:

    python3 fonte-wiki/extract.py --src <pasta do jogo> --out fonte-wiki/data
    python3 fonte-wiki/build_wiki.py . <pasta do jogo>

O segundo argumento do build é a pasta do jogo (para os ícones dos itens).
