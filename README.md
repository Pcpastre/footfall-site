# footfall-site

Site do Footfall publicado em https://footfall.pcpastre.com (GitHub Pages).

- `index.html`: apresentação, recursos, imagens, baixar e apoiar
- `privacidade.html`: política de privacidade
- `excluir-conta.html`: como excluir a conta
- `guias.html` e `guia-*.html`: guias de como jogar (8), nos três idiomas, gerados por `python3 fonte-guias/build.py .` (textos em `fonte-guias/pt.py`, `en.py`, `es.py`)
- `site.js`: a tempestade da capa (igual à tela inicial do jogo) e os links
- `i18n.js`: idiomas (inglês padrão, português e espanhol; bandeiras no topo, `?lang=pt|en|es` na URL)
- `img/`: arte tirada dos sprites do jogo; `fonts/`: Jersey 10 (licença OFL)

## Links (sem mexer no código)

No Supabase → Table Editor:
- `links`: Instagram e TikTok (os mesmos do app)
- `site_links`: `playstore`, `apk` e `apoio` (Patreon)

Preencha a coluna `url` com `https://...`. Vazio = o botão aparece como "em breve".
