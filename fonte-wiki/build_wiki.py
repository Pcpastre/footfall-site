"""Gera a wiki do Footfall (pt) em <site>/wiki a partir de data/*.json e paginas/*.html.
Uso: python3 build_wiki.py <pasta do site> [<pasta do jogo>]"""
import html, json, os, re, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1]
GAME = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/footfall'
OUT = os.path.join(SITE, 'wiki')
D = lambda n: json.load(open(os.path.join(HERE, 'data', n + '.json')))
ITEMS, WHERE, LOOT, RECIPES, ZOMB, BASE, BODY, CHARS = (D('items'), D('items_where'), D('loot'), D('recipes'),
                                                       D('zombies'), D('base'), D('body'), D('characters'))
IT = {i['id']: i for i in ITEMS['items']}
CATS = LOOT['categories']
for _z in ZOMB['classes']:
    _z['id'] = _z['id'] or _z['name']
ZC = {z['id']: z for z in ZOMB['classes']}
e = html.escape

KIND = {'arma': 'Armas', 'medico': 'Médico', 'comida': 'Comida e bebida', 'material': 'Materiais',
        'ferramenta': 'Ferramentas', 'roupa': 'Roupas e equipamento'}
KIND1 = {'arma': 'Arma', 'medico': 'Médico', 'comida': 'Comida/bebida', 'material': 'Material',
         'ferramenta': 'Ferramenta', 'roupa': 'Roupa/equipamento'}
RAR = {'comum': 'Comum', 'incomum': 'Incomum', 'raro': 'Raro', 'lendario': 'Lendário'}
PART = {'cabeca': 'Cabeça', 'tronco': 'Tronco', 'bracos': 'Braços', 'maos': 'Mãos', 'pernas': 'Pernas', 'pes': 'Pés'}
ATK = {'mordida': 'Mordida', 'arranhao': 'Arranhão', 'golpe': 'Golpe', 'tiro': 'Tiro'}
CAT_ORDER = ['Começo', 'Personagem', 'Saúde', 'Mundo', 'Saque', 'Combate', 'Base', 'Social', 'Corvo e rádio', 'Memórias']


def num(v, d=2):
    if v is None:
        return '∞'
    if isinstance(v, float):
        s = f'{v:.{d}f}'.rstrip('0').rstrip('.')
        return s.replace('.', ',')
    return str(v)


def pct(v):
    return num(round(v * 100, 1), 1) + '%'


def ilink(iid, icon=True):
    it = IT.get(iid)
    if not it:
        return e(iid)
    img = f'<img class="ic px" src="img/itens/{iid}.png" alt="" width="24" height="24">' if icon else ''
    return f'<a class="il" href="item-{iid}.html">{img}{e(it["name"])}</a>'


def clink(cat):
    c = CATS.get(cat)
    return f'<a href="lugar-{cat}.html">{e(c["label"]) if c else e(cat)}</a>'


def tbl(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


# --- paginas de texto escritas a mao -------------------------------------------------------------
PAGES = {}  # slug -> dict(titulo, categoria, resumo, corpo)
for fn in sorted(os.listdir(os.path.join(HERE, 'paginas'))):
    if not fn.endswith('.html'):
        continue
    src = open(os.path.join(HERE, 'paginas', fn)).read()
    m = re.match(r'\s*<!--(.*?)-->', src, re.S)
    meta = {}
    if m:
        for part in m.group(1).split('|'):
            if ':' in part:
                k, v = part.split(':', 1)
                meta[k.strip()] = v.strip()
        src = src[m.end():]
    slug = fn[:-5]
    PAGES[slug] = {'titulo': meta.get('titulo', slug), 'categoria': meta.get('categoria', 'Mundo'),
                   'resumo': meta.get('resumo', ''), 'corpo': src.strip()}


# --- casca ---------------------------------------------------------------------------------------
def nav_side(active):
    groups = {}
    for slug, p in PAGES.items():
        if slug.startswith(('zumbi-', 'memoria-')):
            continue
        groups.setdefault(p['categoria'], []).append((slug, p['titulo']))
    out = []
    for cat in CAT_ORDER + sorted(set(groups) - set(CAT_ORDER)):
        if cat not in groups:
            continue
        items = ''.join(f'<li><a href="{s}.html"{" aria-current=page" if s == active else ""}>{e(t)}</a></li>'
                        for s, t in sorted(groups[cat], key=lambda x: x[1]))
        out.append(f'<details open><summary>{e(cat)}</summary><ul>{items}</ul></details>')
    extra = ''.join(f'<li><a href="{s}.html"{" aria-current=page" if s == active else ""}>{t}</a></li>'
                    for s, t in [('itens', 'Todos os itens'), ('lugares', 'Lugares'), ('zumbis-lista', 'Tipos de zumbi'),
                                 ('memorias-lista', 'As memórias')])
    return f'<details open><summary>Índices</summary><ul>{extra}</ul></details>' + ''.join(out)


def page(slug, title, body, summary='', crumbs=None, cat=None):
    crumbs = crumbs or ([('index.html', 'Wiki')] + ([(None, cat)] if cat else []))
    cr = ' / '.join(f'<a href="{h}">{e(t)}</a>' if h else e(t) for h, t in crumbs)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)} — Wiki do Footfall</title>
<meta name="description" content="{e(summary or title)}">
<meta name="theme-color" content="#0b0a10">
<link rel="icon" type="image/png" href="../img/icone.png">
<link rel="stylesheet" href="../estilo.css">
<link rel="stylesheet" href="wiki.css">
</head>
<body class="wiki">
<header class="top">
  <div class="wrap">
    <a class="brand" href="../index.html" aria-label="Footfall"><img class="px" src="../img/logo.png" alt="Footfall" width="148" height="58"></a>
    <a class="wk" href="index.html">Wiki</a>
    <form class="busca" role="search" action="busca.html"><input type="search" name="q" placeholder="Buscar na wiki" aria-label="Buscar na wiki" autocomplete="off"><div class="sug" hidden></div></form>
    <button type="button" class="menu" aria-expanded="false" aria-controls="side">Seções</button>
  </div>
</header>
<div class="wiki-wrap">
<nav class="side" id="side" aria-label="Seções da wiki">{nav_side(slug)}</nav>
<main class="doc wdoc">
<p class="crumbs">{cr}</p>
<h1>{e(title)}</h1>
{f'<p class="sub">{e(summary)}</p>' if summary else ''}
{body}
</main>
</div>
<footer class="foot">
  <div class="wrap">
    <img class="px" src="../img/logo.png" alt="Footfall" width="148" height="58">
    <nav aria-label="Rodapé">
      <a href="../index.html">Site</a>
      <a href="../guias.html">Guias</a>
      <a href="index.html">Wiki</a>
      <a href="../privacidade.html">Política de privacidade</a>
      <a href="mailto:contato@footfall.pcpastre.com">contato@footfall.pcpastre.com</a>
    </nav>
  </div>
  <div class="wrap" style="margin-top:14px">Wiki gerada a partir do código do jogo. Valores podem mudar entre versões.</div>
</footer>
<script src="wiki.js" defer></script>
</body>
</html>
'''


def write(slug, content):
    with open(os.path.join(OUT, slug + '.html'), 'w') as f:
        f.write(content)


# --- itens ---------------------------------------------------------------------------------------
REC_OUT, REC_IN, REC_TOOL = {}, {}, {}
for r in RECIPES['recipes']:
    if r.get('output'):
        REC_OUT.setdefault(r['output'], []).append(r)
    for k in r.get('inputs', {}):
        REC_IN.setdefault(k, []).append(r)
    for k in r.get('tools', []):
        REC_TOOL.setdefault(k, []).append(r)
for b in BASE.get('furniture', []):
    for k in (b.get('cost') or {}):
        pass


def recipe_row(r):
    ins = ', '.join(f'{ilink(k)} ×{v}' for k, v in r.get('inputs', {}).items()) or '—'
    tools = ', '.join(ilink(k) for k in r.get('tools', [])) or '—'
    if r.get('output'):
        out = f'{ilink(r["output"])} ×{r.get("qty", 1)}'
    elif r.get('furniture'):
        out = e(r['name']) + ' (móvel)'
    else:
        out = e(r['name'])
    st = {'fogo': 'Fogo', 'bancada': 'Bancada', 'nenhuma': '—'}.get(r.get('station'), e(str(r.get('station'))))
    sk = f'{e(r.get("skill_name") or "")} {r.get("minLevel") or ""}'.strip() or '—'
    return [f'<b>{e(r["name"])}</b>', ins, tools, st, sk, out]


TREAT_ITEMS = {}
for t in BODY.get('treatments', []):
    for k in (t.get('items') or []) + (t.get('tools_not_consumed') or []):
        TREAT_ITEMS.setdefault(k, []).append(t['label'])


def infobox(it):
    rows = [('Tipo', KIND1.get(it['kind'], it['kind'])), ('Raridade', f'<span class="r-{it["rarity"]}">{RAR.get(it["rarity"], it["rarity"])}</span>'),
            ('Peso', num(it['weight']) + ' kg')]
    d = it.get('derived', {})
    if d.get('slot'):
        rows.append(('Onde vai', e(str(d['slot']))))
    if d.get('ref_price'):
        rows.append(('Preço de referência', f'{d["ref_price"]} selos'))
    names = f'<p class="alt">en: {e(it.get("name_en") or "—")}<br>es: {e(it.get("name_es") or "—")}</p>'
    trs = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows)
    return (f'<aside class="infobox"><img class="px" src="img/itens/{it["id"]}.png" alt="" width="96" height="96">'
            f'<b>{e(it["name"])}</b>{names}<table>{trs}</table></aside>')


def item_body(it):
    d = it.get('derived', {})
    parts = [infobox(it)]
    if it.get('note'):
        parts.append(f'<p class="lead2">{e(it["note"])}</p>')
    w = it.get('weapon')
    if w:
        rows = []
        if d.get('firearm') or d.get('bow') or w.get('ranged'):
            rows += [('Dano por tiro', num(w['damage']) + (f' × {w["pellets"]} chumbos' if (w.get('pellets') or 1) > 1 else '')),
                     ('Alcance', num(w['reach']) + ' m'), ('Pente', num(w.get('mag'))), ('Recarga', num(w.get('reload')) + ' s'),
                     ('Intervalo entre tiros', num(w.get('cooldown')) + ' s')]
            if d.get('burst', 1) > 1:
                rows.append(('Rajada', f'{d["burst"]} tiros'))
            if w.get('ammo'):
                rows.append(('Munição', ilink(w['ammo'])))
            nz = w.get('noise')
            rows.append(('Barulho no mapa', 'raio de tiro (150 m)' if nz == 999 else (num(nz) + ' m' if nz else '—')))
        else:
            rows += [('Dano', num(w['damage'])), ('Alcance', num(w['reach']) + ' m'), ('Intervalo', num(w.get('cooldown')) + ' s'),
                     ('Arco do golpe', num(w.get('arcDeg')) + '°'), ('Alvos por golpe', num(w.get('maxTargets'))),
                     ('Durabilidade', 'não gasta' if d.get('infinite_durability') else num(w.get('durability')))]
        if d.get('damage_per_second'):
            rows.append(('Dano por segundo (teórico)', num(d['damage_per_second'], 1)))
        parts.append('<h2>Arma</h2>' + tbl(['Atributo', 'Valor'], rows, 'kv'))
    food = []
    if it.get('kcal'):
        food.append(('Calorias', f'{it["kcal"]} kcal'))
    if it.get('ml'):
        food.append(('Água', f'{it["ml"]} ml'))
    if it.get('shelfLife_days'):
        food.append(('Validade', num(it['shelfLife_days'], 1) + ' dias'))
    elif it.get('edible') and not it.get('perishable'):
        food.append(('Validade', 'não estraga'))
    if food:
        parts.append('<h2>Alimento</h2>' + tbl(['Atributo', 'Valor'], food, 'kv'))
    med = []
    if it.get('heal'):
        med.append(('Cura', f'{it["heal"]} de vida'))
    if it.get('bandage'):
        med.append(('Serve para enfaixar', 'sim'))
    if it['id'] in TREAT_ITEMS:
        med.append(('Usado em', ', '.join(e(x) for x in TREAT_ITEMS[it['id']])))
    if med:
        parts.append('<h2>Médico</h2>' + tbl(['Atributo', 'Valor'], med, 'kv') +
                     '<p>Veja <a href="tratamento.html">Tratamento</a> e <a href="feridas.html">Feridas</a>.</p>')
    gear = []
    if it.get('pockets'):
        gear.append(('Bolsos', f'+{num(it["pockets"])} kg'))
    if it.get('bagKg'):
        gear.append(('Capacidade', f'{num(it["bagKg"])} kg'))
    if d.get('warmth') is not None and it['kind'] == 'roupa':
        gear.append(('Calor', num(d['warmth'])))
    if d.get('heavy'):
        gear.append(('Roupa pesada (calor)', 'sim'))
    if d.get('armor_material'):
        gear.append(('Material', e(d['armor_material'])))
    if d.get('armor_wear_per_bite'):
        gear.append(('Desgaste por mordida', num(d['armor_wear_per_bite'])))
    if gear:
        parts.append('<h2>Equipamento</h2>' + tbl(['Atributo', 'Valor'], gear, 'kv') + '<p>Veja <a href="mochila-e-peso.html">Mochila e peso</a> e <a href="costura-e-roupas.html">Costura e roupas</a>.</p>')
    if d.get('armor_block'):
        heads = ['Parte'] + [ATK[a] for a in ATK]
        rows = []
        for part_, by in d['armor_block'].items():
            rip = d.get('armor_block_ripped', {}).get(part_, {})
            rows.append([PART.get(part_, part_)] + [f'{pct(by.get(a, 0))} <small>(rasgada {pct(rip.get(a, 0))})</small>' for a in ATK])
        parts.append('<h2>Proteção</h2><p>Chance de a roupa segurar cada tipo de ataque na parte que cobre.</p>' + tbl(heads, rows))
    # onde achar
    wh = WHERE.get(it['id'], {})
    where = []
    pools = wh.get('pools', [])
    if pools:
        rows = []
        for p in sorted(pools, key=lambda x: -x['tier_share']):
            furn = ', '.join(e(f) for f in (wh.get('furniture', {}).get(p['category'], {}) or {}))
            rows.append([clink(p['category']), pct(p['tier_share']), furn or '—'])
        where.append('<p>Chance mostrada: a parte que este item ocupa entre os itens da mesma raridade naquele tipo de lugar.</p>' +
                     tbl(['Lugar', 'Chance na raridade', 'Móveis'], rows))
    if wh.get('zombies'):
        where.append('<h3>Em zumbis</h3>' + tbl(['Zumbi', 'Chance', 'Máx.'],
                     [[f'<a href="zumbi-{z["class"]}.html">{e(ZC.get(z["class"], {}).get("label", z["class"]))}</a>', pct(z['chance']), num(z['max'])] for z in wh['zombies']]))
    other = wh.get('other') or []
    OTH = {'corpse': 'corpos de zumbi (bolsos)', 'backpack': 'mochila de zumbi mochileiro', 'special_pool': 'móveis especiais de alguns cômodos',
           'recipe': 'receita', 'starter_kit': 'kit inicial', 'very_rare': 'achado raríssimo ao entrar nos lugares', 'flare': 'caixa de resgate / sinalizador',
           'skin': 'conjunto de roupa raro'}
    if other:
        txt = ', '.join(sorted({OTH.get(o if isinstance(o, str) else o.get('kind', ''), str(o if isinstance(o, str) else o.get('kind', ''))) for o in other}))
        where.append(f'<p>Também: {e(txt)}.</p>')
    if it['id'] in REC_OUT:
        where.append('<p>Fabricado por receita (veja abaixo).</p>')
    if where:
        parts.append('<h2>Onde achar</h2>' + ''.join(where))
    elif it['id'].startswith('memoria_'):
        parts.append('<h2>Onde achar</h2><p>Veja <a href="memorias.html">Memórias</a>.</p>')
    # receitas
    rs = []
    for title, src in [('Como fazer', REC_OUT), ('Usado como ingrediente', REC_IN), ('Usado como ferramenta', REC_TOOL)]:
        lst = src.get(it['id'])
        if lst:
            rs.append(f'<h3>{title}</h3>' + tbl(['Receita', 'Ingredientes', 'Ferramentas', 'Onde', 'Habilidade', 'Resultado'], [recipe_row(r) for r in lst]))
    if rs:
        parts.append('<h2>Receitas</h2>' + ''.join(rs))
    parts.append(f'<p class="code">Código: <code>{e(it["id"])}</code></p>')
    return '\n'.join(parts)


def items_index():
    out = ['<p>Todos os itens do jogo, com os valores do código. Toque no nome para ver a ficha completa.</p>',
           '<p class="filtro"><input type="search" placeholder="Filtrar itens" aria-label="Filtrar itens" data-filtro></p>']
    for kind, label in KIND.items():
        lst = sorted([i for i in ITEMS['items'] if i['kind'] == kind], key=lambda x: x['name'])
        if kind == 'arma':
            rows = [[ilink(i['id']), RAR[i['rarity']], num(i['weight']), num(i['weapon']['damage']) if i.get('weapon') else '—',
                     (num(i['weapon']['reach']) + ' m') if i.get('weapon') else '—',
                     ('fogo' if i.get('derived', {}).get('firearm') else 'arco' if i.get('derived', {}).get('bow') else 'branca' if i.get('weapon') else '—')] for i in lst]
            head = ['Item', 'Raridade', 'Peso', 'Dano', 'Alcance', 'Tipo']
        elif kind == 'comida':
            rows = [[ilink(i['id']), RAR[i['rarity']], num(i['weight']), i.get('kcal') or '—', i.get('ml') or '—',
                     num(i.get('shelfLife_days'), 1) if i.get('shelfLife_days') else '—'] for i in lst]
            head = ['Item', 'Raridade', 'Peso', 'kcal', 'ml', 'Validade (dias)']
        elif kind == 'roupa':
            rows = [[ilink(i['id']), RAR[i['rarity']], num(i['weight']), e(str(i.get('derived', {}).get('slot') or '—')),
                     ('+' + num(i['pockets']) + ' kg') if i.get('pockets') else ('mochila ' + num(i['bagKg']) + ' kg' if i.get('bagKg') else '—')] for i in lst]
            head = ['Item', 'Raridade', 'Peso', 'Lugar no corpo', 'Carga']
        else:
            rows = [[ilink(i['id']), RAR[i['rarity']], num(i['weight']), e(i.get('note') or '')[:110]] for i in lst]
            head = ['Item', 'Raridade', 'Peso', 'Nota']
        out.append(f'<h2 id="{kind}">{label} <small>({len(lst)})</small></h2>' + tbl(head, rows, 'filt'))
    return '\n'.join(out)


# --- lugares -------------------------------------------------------------------------------------
def place_body(cid):
    c = CATS[cid]
    parts = [f'<p>Lugares de verdade do mapa (OpenStreetMap) que o jogo trata como <b>{e(c["label"])}</b>. '
             f'Veja também <a href="saque.html">Saque</a>.</p>']
    rows = [('Guardas no máximo (pontos dominados)', num(c.get('guards'))),]
    it = c.get('interior') or {}
    if it.get('zombies'):
        rows.append(('Zumbis dentro', f'{it["zombies"][0]} a {it["zombies"][1]}'))
    if it.get('typical_size_m'):
        rows.append(('Tamanho típico', f'{it["typical_size_m"][0]} a {it["typical_size_m"][1]} m'))
    parts.append(tbl(['Atributo', 'Valor'], rows, 'kv'))
    qf = c.get('quick_loot_furniture') or []
    if qf:
        parts.append('<h2>Pela porta</h2><p>Móveis da entrada, rápidos e sem itens raros.</p>' +
                     tbl(['Móvel', 'Tempo', 'Barulho'], [[e(f['name']), num(f['seconds']) + ' s', f'{e(f["noise_label"])} (~{num(f["noise_radius_m"], 0)} m)'] for f in qf]))
    floors = (it.get('ground_floor') or []) + (it.get('upper_floors') or [])
    if floors:
        rows = []
        for fl in floors:
            for room in fl.get('rooms', []):
                furn = [f for f in room.get('furniture', []) if f.get('lootable')]
                if not furn:
                    continue
                fk = LOOT['furniture_kinds']
                rows.append([e(room['room']) + (' <small>(trancado)</small>' if room.get('locked') else ''),
                             '<br>'.join(f'{e(f["name"])}' + (f' <small>{num(fk[f["name"]]["seconds"])} s, {e(fk[f["name"]]["noise_label"])}</small>' if f['name'] in fk else '') for f in furn)])
        if rows:
            parts.append('<h2>Entrando</h2><p>Cômodos e móveis que dá para vasculhar dentro do prédio. Dentro, os raros têm mais chance.</p>' +
                         tbl(['Cômodo', 'Móveis'], rows))
    ls = c.get('loot_stats') or {}
    if ls:
        rows = []
        for iid, s in sorted(ls.items(), key=lambda kv: (['comum', 'incomum', 'raro', 'lendario'].index(kv[1]['rarity']) if kv[1]['rarity'] in RAR else 9, -kv[1]['tier_share'])):
            rows.append([ilink(iid), RAR.get(s['rarity'], s['rarity']), pct(s['tier_share'])])
        parts.append('<h2>O que sai daqui</h2><p>Cada item sorteado primeiro tira a raridade e depois um item daquela raridade; a coluna mostra a parte do item dentro da raridade.</p>' +
                     tbl(['Item', 'Raridade', 'Chance na raridade'], rows))
    zs = ZOMB.get('by_place', {}).get(cid)
    if zs:
        parts.append('<h2>Zumbis especiais por perto</h2><p>' + ', '.join(sorted({f'<a href="zumbi-{z}.html">{e(ZC[z]["label"])}</a>' for z in zs if z in ZC})) +
                     '. Veja <a href="zumbis.html">Zumbis</a>.</p>')
    mem = {'saude': 'plantao', 'casa': 'jorge', 'eletronicos': 'voz', 'policia': 'quinta', 'bunker': 'cofre'}.get(cid)
    if mem:
        parts.append(f'<div class="tip"><b>Memória</b>Um livro de memória pode aparecer nos móveis de dentro: veja <a href="memoria-{mem}.html">a memória</a>.</div>')
    return '\n'.join(parts)


def places_index():
    rows = [[f'<a href="lugar-{k}.html">{e(c["label"])}</a>', num(c.get('guards')),
             len(c.get('loot_stats') or {})] for k, c in CATS.items()]
    return '<p>Cada lugar do mapa cai numa categoria, e a categoria decide os móveis, o saque e os zumbis.</p>' + tbl(['Categoria', 'Guardas (máx.)', 'Itens possíveis'], rows)


def zombies_index():
    rows = []
    for z in ZOMB['classes']:
        rows.append([f'<a href="zumbi-{z["id"]}.html">{e(z["label"])}</a>', '×' + num(z['hp']), '×' + num(z['speed']),
                     '×' + num(z['head']), '×' + num(z['torso']), 'sim' if z.get('fireproof') else '—'])
    return ('<p>Multiplicadores sobre o zumbi comum. Cabeça e tronco: quanto do dano entra naquela parte (menor = mais protegido). Veja <a href="zumbis.html">Zumbis</a>.</p>' +
            tbl(['Tipo', 'Vida', 'Velocidade', 'Dano na cabeça', 'Dano no tronco', 'Não pega fogo'], rows))


def memories_index():
    lst = [s for s in PAGES if s.startswith('memoria-')]
    return '<p>As histórias jogáveis da estante do depósito do rádio. Sem spoilers: só onde achar, desafio e recompensa. Veja <a href="memorias.html">Memórias</a>.</p><ul>' + \
        ''.join(f'<li><a href="{s}.html">{e(PAGES[s]["titulo"])}</a> — {e(PAGES[s]["resumo"])}</li>' for s in sorted(lst)) + '</ul>'


def home():
    groups = {}
    for slug, p in PAGES.items():
        if slug.startswith(('zumbi-', 'memoria-')):
            continue
        groups.setdefault(p['categoria'], []).append((slug, p))
    cards = []
    for cat in CAT_ORDER:
        if cat not in groups:
            continue
        li = ''.join(f'<li><a href="{s}.html">{e(p["titulo"])}</a></li>' for s, p in sorted(groups[cat], key=lambda x: x[1]['titulo']))
        cards.append(f'<section class="wcat bevel"><h2>{e(cat)}</h2><ul>{li}</ul></section>')
    n_items = len(ITEMS['items'])
    idx = (f'<div class="wstats"><a class="bevel" href="itens.html"><b>{n_items}</b>itens</a><a class="bevel" href="lugares.html"><b>{len(CATS)}</b>tipos de lugar</a>'
           f'<a class="bevel" href="zumbis-lista.html"><b>{len(ZOMB["classes"])}</b>tipos de zumbi</a><a class="bevel" href="receitas.html"><b>{len(RECIPES["recipes"])}</b>receitas</a>'
           f'<a class="bevel" href="tracos.html"><b>{len(CHARS["traits"])}</b>traços</a></div>')
    return ('<p class="lead">A enciclopédia do Footfall: cada mecânica, item, lugar e zumbi, com os números tirados direto do código do jogo. '
            'Começando agora? Leia os <a href="../guias.html">guias</a> primeiro.</p>' + idx + '<div class="wcats">' + ''.join(cards) + '</div>')


def search_index():
    idx = []
    for s, p in PAGES.items():
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', p['corpo']))).strip()
        idx.append({'t': p['titulo'], 'u': s + '.html', 'c': p['categoria'], 'r': p['resumo'], 'x': txt[:4000]})
    for i in ITEMS['items']:
        idx.append({'t': i['name'], 'u': f'item-{i["id"]}.html', 'c': 'Item · ' + KIND1.get(i['kind'], ''), 'r': i.get('note', '')[:120], 'i': i['id']})
    for k, c in CATS.items():
        idx.append({'t': c['label'], 'u': f'lugar-{k}.html', 'c': 'Lugar', 'r': ''})
    return idx


def build():
    os.makedirs(os.path.join(OUT, 'img', 'itens'), exist_ok=True)
    sp = os.path.join(GAME, 'assets', 'sprites')
    atlas = json.load(open(os.path.join(sp, 'itens.json')))
    im = Image.open(os.path.join(sp, 'itens.png')).convert('RGBA')
    c = atlas['cell']
    for iid, (x, y) in atlas['items'].items():
        im.crop((x, y, x + c, y + c)).save(os.path.join(OUT, 'img', 'itens', iid + '.png'), optimize=True)
    for f in ('wiki.css', 'wiki.js', 'busca.html.tpl'):
        pass
    shutil.copy(os.path.join(HERE, 'wiki.css'), OUT)
    shutil.copy(os.path.join(HERE, 'wiki.js'), OUT)
    # paginas de texto
    for s, p in PAGES.items():
        body = p['corpo']
        if s.startswith('zumbi-'):
            cat, crumbs = 'Combate', [('index.html', 'Wiki'), ('zumbis-lista.html', 'Tipos de zumbi')]
        elif s.startswith('memoria-'):
            cat, crumbs = 'Memórias', [('index.html', 'Wiki'), ('memorias-lista.html', 'Memórias')]
        else:
            cat, crumbs = p['categoria'], None
        write(s, page(s, p['titulo'], body, p['resumo'], crumbs, cat))
    for it in ITEMS['items']:
        write('item-' + it['id'], page('item-' + it['id'], it['name'], item_body(it), '',
                                       [('index.html', 'Wiki'), ('itens.html', 'Itens'), (f'itens.html#{it["kind"]}', KIND[it['kind']])]))
    for k in CATS:
        write('lugar-' + k, page('lugar-' + k, CATS[k]['label'], place_body(k), '', [('index.html', 'Wiki'), ('lugares.html', 'Lugares')]))
    write('itens', page('itens', 'Itens', items_index(), f'Os {len(ITEMS["items"])} itens do jogo.'))
    write('lugares', page('lugares', 'Lugares', places_index(), 'Os tipos de lugar do mapa.'))
    write('zumbis-lista', page('zumbis-lista', 'Tipos de zumbi', zombies_index(), 'Todos os tipos de zumbi e os multiplicadores.'))
    write('memorias-lista', page('memorias-lista', 'As memórias', memories_index(), 'As histórias jogáveis.'))
    write('busca', page('busca', 'Buscar', '<div id="resultados" aria-live="polite"></div>'))
    write('index', page('index', 'Wiki do Footfall', home(), '', [('../index.html', 'Footfall')]))
    with open(os.path.join(OUT, 'busca.json'), 'w') as f:
        json.dump(search_index(), f, ensure_ascii=False, separators=(',', ':'))
    # links quebrados
    names = set(os.listdir(OUT))
    bad = {}
    for fn in names:
        if fn.endswith('.html'):
            for h in re.findall(r'href="([^"#?:]+\.html)', open(os.path.join(OUT, fn)).read()):
                if h.startswith('../'):
                    continue
                if h not in names:
                    bad.setdefault(h, set()).add(fn)
    print('paginas:', len([n for n in names if n.endswith('.html')]))
    for h, srcs in sorted(bad.items()):
        print('LINK QUEBRADO', h, '<-', ', '.join(sorted(srcs))[:200])


build()
