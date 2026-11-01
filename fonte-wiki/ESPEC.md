# Wiki do Footfall — especificação para quem escreve páginas

Objetivo: uma wiki no nível de profundidade do PZwiki (Project Zomboid), em **português do Brasil**, tirada **só do código** do jogo em `/mnt/user-data/outputs/footfall` (lib/game/*.dart, lib/screens/*.dart). Nunca invente: todo número, nome de botão e regra tem que existir no código. Se o código e um texto da interface discordarem, vale o código, e anote a discordância no fim do seu relatório (não na página).

## Onde a wiki vai morar
Site estático, pasta `wiki/` do site. Todas as páginas ficam no mesmo nível, então links são relativos e simples:
- página de texto: `<slug>.html` (os slugs estão na sua lista)
- item: `item-<id>.html`, onde `<id>` é a chave do mapa `items` em lib/game/items.dart (ex.: `item-faca.html`, `item-bandagem.html`)
- tipo de zumbi: `zumbi-<id>.html`, com o id do enum/classe em lib/game/zclass.dart
- tipo de lugar: `lugar-<categoria>.html`, com a categoria de lib/game/poi.dart (ex.: `lugar-saude.html`)
- memória: `memoria-<id>.html` (entrega, jorge, plantao, voz, quinta, cofre, corvo)
Linke generosamente para itens, zumbis, lugares e outras páginas da wiki, como o PZwiki faz.

## Formato do arquivo
Um arquivo por página em `/home/claude/wiki_src/paginas/<slug>.html`. A primeira linha é um comentário de metadados:
`<!-- titulo: Título da página | categoria: Personagem | resumo: Uma frase curta. -->`
Depois, só o corpo em HTML (sem <html>, <head>, <body>, sem <h1>: o gerador põe o título). Use:
- `<h2>`, `<h3>`, `<p>`, `<ul>/<ol>`, `<b>`, `<i>`, `<a href>`
- `<kbd>` para o texto exato de um botão/menu do jogo (como aparece na interface em português)
- tabelas sempre dentro de `<div class="tbl"><table>…</table></div>`, com `<th>` no cabeçalho
- `<div class="tip"><b>Título</b>texto</div>` para dicas e `<div class="tip warn"><b>Título</b>texto</div>` para avisos
- `<ol class="steps">` para passo a passo
Categorias válidas: Começo, Personagem, Saúde, Mundo, Combate, Saque, Base, Social, Corvo e rádio, Memórias.

## Estilo
Texto de wiki: direto, completo, organizado em seções, com números exatos e tabelas sempre que houver uma lista de valores (ex.: tempo de cada móvel, dano de cada arma, custo de cada receita). Segunda pessoa ("você"). Explique a regra e depois o que ela significa na prática. Sem enrolação, sem emojis. Cada página deve ser tão completa quanto o código permite: todas as variantes, todos os casos especiais, todos os multiplicadores.

## Proibido
- Spoilers das memórias (o que acontece na história, quem morre, o final). Nas memórias, só: onde achar o livro, quem é o protagonista (uma linha), o tipo de desafio em termos gerais, a recompensa e dicas gerais de jogo.
- Inventar números ou mecânicas. Se não achar no código, não escreva.
- Editar qualquer arquivo fora de `/home/claude/wiki_src/paginas/`.
