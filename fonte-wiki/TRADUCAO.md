# Como traduzir uma página da wiki

Fonte: `fonte-wiki/paginas/<slug>.html` (pt-BR). Destino: `fonte-wiki/paginas_en/<slug>.html` (inglês dos EUA) ou `fonte-wiki/paginas_es/<slug>.html` (espanhol latino-americano neutro, "tú"). **Mesmo nome de arquivo (slug em português).**

Regras:
1. Linha 1: o comentário de metadados com os MESMOS campos, traduzindo os valores de `titulo` e `resumo`; `categoria` também traduzida usando exatamente: en — Getting started, Character, Health, World, Looting, Combat, Base, Social, Crow and radio, Memories; es — Comienzo, Personaje, Salud, Mundo, Saqueo, Combate, Base, Social, Cuervo y radio, Memorias. (pt: Começo, Personagem, Saúde, Mundo, Saque, Combate, Base, Social, Corvo e rádio, Memórias.)
2. Mesma estrutura HTML, mesmas tags e classes, mesmos `href` (NÃO traduza slugs nem ids: `item-faca.html`, `lugar-saude.html`, `zumbi-chefe.html`, `feridas.html` ficam iguais). Mesmos números, unidades métricas, mesmas tabelas com as mesmas linhas.
3. Texto dentro de `<kbd>`: use o rótulo exato do jogo no idioma, do mapa de tradução do jogo `/mnt/user-data/outputs/footfall/assets/i18n/en.json` ou `es.json` (chave = texto em português). Sem chave exata: traduza naturalmente no mesmo estilo de maiúsculas.
4. Nomes de itens: use `name_en` / `name_es` de `/home/claude/footfall-site/fonte-wiki/data/items.json`. Zumbis: `label_en`/`label_es` em `data/zombies.json`. Lugares: `label_en`/`label_es` em `data/loot.json` (categories). Profissões, traços, habilidades, receitas, móveis, feridas, moodles: os campos `_en`/`_es` dos JSON em `data/` ou os mapas de tradução do jogo. Selos = stamps (en) / sellos (es). Memórias (títulos da estante): en — The last delivery, Old Jorge, The night shift, The crow's voice, Thursday duty, The vault, The crow; es — La última entrega, Don Jorge, La guardia, La voz del cuervo, Guardia del jueves, La bóveda, El cuervo.
5. Não acrescente nem tire fatos. Não traduza código (`<code>`).
6. Ao terminar cada arquivo, confira que a sequência de tags é a mesma da fonte (um script simples com regex `<[a-z0-9]+` serve) e que todos os `href` são idênticos.
