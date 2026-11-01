"""Gera guias.html e guia-<slug>.html no site, e as chaves de titulo no i18n.js.
Uso: python3 build.py /home/claude/footfall-site"""
import sys, os, re, importlib
sys.path.insert(0, os.path.dirname(__file__))
from meta import GUIDES
import pt, en, es
BODIES = {'pt': pt.BODY, 'en': en.BODY, 'es': es.BODY}
SITE = sys.argv[1]
LANGS = ['en', 'pt', 'es']

UI = {
    'hub_title': {'en': 'Guides', 'pt': 'Guias', 'es': 'Guías'},
    'hub_sub': {'en': 'Everything you need to survive your first weeks in Footfall, straight from how the game works.',
                'pt': 'Tudo o que você precisa para sobreviver às primeiras semanas no Footfall, direto de como o jogo funciona.',
                'es': 'Todo lo que necesitas para sobrevivir tus primeras semanas en Footfall, directo de cómo funciona el juego.'},
    'prev': {'en': '← Previous', 'pt': '← Anterior', 'es': '← Anterior'},
    'next': {'en': 'Next →', 'pt': 'Próximo →', 'es': 'Siguiente →'},
    'all': {'en': 'All guides', 'pt': 'Todos os guias', 'es': 'Todas las guías'},
    'safe': {'en': 'Play with your head up: never while driving, and never enter real buildings or private land because of the game.',
             'pt': 'Jogue de cabeça erguida: nunca dirigindo, e nunca entre em prédios ou terrenos de verdade por causa do jogo.',
             'es': 'Juega con la cabeza en alto: nunca manejando, y nunca entres en edificios o terrenos reales por el juego.'},
}

FLAGS = '''    <div class="langs" role="group" aria-label="Language">
      <button type="button" class="flag" data-set="en" aria-pressed="true" title="English"><img class="px" src="img/flags/en.png" alt="English" width="18" height="12"></button>
      <button type="button" class="flag" data-set="pt" aria-pressed="false" title="Português"><img class="px" src="img/flags/pt.png" alt="Português" width="18" height="12"></button>
      <button type="button" class="flag" data-set="es" aria-pressed="false" title="Español"><img class="px" src="img/flags/es.png" alt="Español" width="18" height="12"></button>
    </div>'''

def shell(page, title_en, desc_en, main):
    return f'''<!doctype html>
<html lang="en" data-page="{page}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title_en}</title>
<meta name="description" content="{desc_en}">
<meta name="theme-color" content="#0b0a10">
<link rel="icon" type="image/png" href="img/icone.png">
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Footfall"><img class="px" src="img/logo.png" alt="Footfall" width="148" height="58"></a>
    <nav aria-label="Pages">
      <a href="index.html#jogo" data-i18n="nav.game">The game</a>
      <a href="guias.html" data-i18n="nav.guides">Guides</a>
      <a href="wiki/index.html">Wiki</a>
      <a class="go bevel" href="index.html#baixar" data-i18n="nav.download">Download</a>
    </nav>
{FLAGS}
  </div>
</header>
<main class="doc">
{main}
</main>
<footer class="foot">
  <div class="wrap">
    <img class="px" src="img/logo.png" alt="Footfall" width="148" height="58">
    <nav aria-label="Footer">
      <a href="index.html" data-i18n="ft.home">Home</a>
      <a href="guias.html" data-i18n="nav.guides">Guides</a>
      <a href="wiki/index.html">Wiki</a>
      <a href="privacidade.html" data-i18n="ft.privacy">Privacy policy</a>
      <a href="excluir-conta.html" data-i18n="ft.delete">Delete account</a>
      <a href="mailto:contato@footfall.pcpastre.com">contato@footfall.pcpastre.com</a>
    </nav>
  </div>
  <div class="wrap" style="margin-top:14px" data-i18n="ft.copy">© 2026 Footfall · Made in Brazil</div>
</footer>
<script src="i18n.js"></script>
</body>
</html>
'''

def hub():
    parts = []
    for L in LANGS:
        cards = []
        for i, (slug, icon, t) in enumerate(GUIDES, 1):
            name, summ = t[L]
            cards.append(f'<a class="guide-card" href="guia-{slug}.html"><img class="px" src="{icon}" alt="" width="64" height="64">'
                         f'<b><span class="n">{i:02d}</span>{name}</b><span>{summ}</span></a>')
        hidden = '' if L == 'en' else ' hidden'
        parts.append(f'''<div data-lang="{L}"{hidden}>
<h1>{UI['hub_title'][L]}</h1>
<p class="sub">{UI['hub_sub'][L]}</p>
<div class="guides">
{chr(10).join(cards)}
</div>
<div class="tip"><b>{ {'en':'Want every number?','pt':'Quer todos os números?','es':'¿Quieres todos los números?'}[L] }</b>{ {'en':'The <a href="wiki/index.html">Footfall wiki</a> (in Portuguese for now) has every item, place, zombie and mechanic straight from the game code.','pt':'A <a href="wiki/index.html">wiki do Footfall</a> tem cada item, lugar, zumbi e mecânica, direto do código do jogo.','es':'La <a href="wiki/index.html">wiki de Footfall</a> (por ahora en portugués) tiene cada objeto, lugar, zombi y mecánica, directo del código del juego.'}[L] }</div>
<div class="tip warn"><b>{ {'en':'Before you go out','pt':'Antes de sair','es':'Antes de salir'}[L] }</b>{UI['safe'][L]}</div>
</div>''')
    return shell('guias', 'Footfall — Guides', UI['hub_sub']['en'], '\n'.join(parts))

def guide(idx):
    slug, icon, t = GUIDES[idx]
    prev = GUIDES[idx - 1] if idx > 0 else None
    nxt = GUIDES[idx + 1] if idx + 1 < len(GUIDES) else None
    parts = []
    for L in LANGS:
        name, summ = t[L]
        nav = []
        if prev:
            nav.append(f'<a href="guia-{prev[0]}.html">{UI["prev"][L]}<br><small>{prev[2][L][0]}</small></a>')
        else:
            nav.append(f'<a href="guias.html">← {UI["all"][L]}</a>')
        if nxt:
            nav.append(f'<a class="nx" href="guia-{nxt[0]}.html">{UI["next"][L]}<br><small>{nxt[2][L][0]}</small></a>')
        else:
            nav.append(f'<a class="nx" href="guias.html">{UI["all"][L]} →</a>')
        hidden = '' if L == 'en' else ' hidden'
        parts.append(f'''<div data-lang="{L}"{hidden}>
<p class="crumbs"><a href="guias.html">{UI['hub_title'][L]}</a> / {idx + 1:02d}</p>
<img class="gicon px" src="{icon}" alt="" width="72" height="72">
<h1>{name}</h1>
<p class="sub">{summ}</p>
{BODIES[L][slug].strip()}
<nav class="gnav">{''.join(nav)}</nav>
</div>''')
    return shell('guia-' + slug, f'Footfall — Guide: {t["en"][0]}', t['en'][1], '\n'.join(parts))

with open(os.path.join(SITE, 'guias.html'), 'w') as f:
    f.write(hub())
for i in range(len(GUIDES)):
    with open(os.path.join(SITE, f'guia-{GUIDES[i][0]}.html'), 'w') as f:
        f.write(guide(i))

# Titulos e o link "Guias" no i18n.js (entre os marcadores, para poder gerar de novo)
p = os.path.join(SITE, 'i18n.js')
js = open(p).read()
GUIA = {'en': 'Guide', 'pt': 'Guia', 'es': 'Guía'}
for L in LANGS:
    keys = {'title.guias': f'Footfall — {UI["hub_title"][L]}', 'nav.guides': UI['hub_title'][L]}
    for slug, _, t in GUIDES:
        keys['title.guia-' + slug] = f'Footfall — {GUIA[L]}: {t[L][0]}'
    body = ''.join(f"      '{k}': '{v}',\n" for k, v in keys.items())
    block = f"      /* guias:{L} */\n{body}      /* /guias:{L} */\n"
    js = re.sub(rf"      /\* guias:{L} \*/\n.*?      /\* /guias:{L} \*/\n", '', js, flags=re.S)
    m = re.search(rf"\n    {L}: {{\n", js)
    assert m, L
    js = js[:m.end()] + block + js[m.end():]
open(p, 'w').write(js)
print('ok', len(GUIDES), 'guias')
