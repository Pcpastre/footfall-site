#!/usr/bin/env python3
"""Footfall wiki data extractor.

Reads the Flutter/Dart source of Footfall (read-only) and writes JSON data files for
the wiki into data/. Re-running regenerates everything.

    python3 /home/claude/wiki_src/extract.py [--src DIR] [--out DIR]

The Dart is parsed by dartparse.py (tokenizer + recursive-descent parser for constant
expressions). Unknown constructs raise DartParseError with file:line. Rules that
live inside function bodies (chances, thresholds) are pulled out with targeted
regexes via rx(), which also raises if the pattern disappears from the code.
"""
import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from dartparse import DartFile, DartParseError, Registry, plain, trailing_comment  # noqa: E402

SKIPPED = []  # (what, reason) for exotic entries that could not be parsed


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def rx(f, pattern, group=1, cast=float, flags=re.S, all_=False):
    """Regex over the comment-stripped code of DartFile f; raises if not found."""
    if all_:
        ms = list(re.finditer(pattern, f.code, flags))
        if not ms:
            raise DartParseError('%s: pattern not found: %s' % (f.name, pattern))
        return ms
    m = re.search(pattern, f.code, flags)
    if not m:
        raise DartParseError('%s: pattern not found: %s' % (f.name, pattern))
    if group is None:
        return m
    v = m.group(group)
    return cast(v) if cast else v


def num(s):
    v = float(s)
    return int(v) if v.is_integer() and '.' not in s else v


def src_snippet(f, anchor_regex):
    """Original source (with comments) of a getter/function starting at anchor, up to the
    end of its => expression (;) or its { } body."""
    m = re.search(anchor_regex, f.code)
    if not m:
        raise DartParseError('%s: anchor not found %s' % (f.name, anchor_regex))
    a = m.start()
    # skip to first '=>' or '{' after the anchor
    i = f.tok_at(m.end())
    while f.toks[i].val not in ('=>', '{'):
        i += 1
    if f.toks[i].val == '{':
        b = f.matching(f.toks[i].pos) + 1
    else:
        depth = 0
        j = i
        while True:
            t = f.toks[j]
            if t.kind == 'op' and t.val in '([{':
                depth += 1
            elif t.kind == 'op' and t.val in ')]}':
                depth -= 1
            elif t.val == ';' and depth == 0:
                break
            j += 1
        b = f.toks[j].end
    return '\n'.join(x.rstrip() for x in f.src[a:b].split('\n'))


def doc_above(f, pos):
    """/// doc comment lines right above offset pos."""
    ln = f.line_of(pos)
    out = []
    k = ln - 2
    while k >= 0 and f.lines[k].strip().startswith('//'):
        out.insert(0, f.lines[k].strip().lstrip('/').strip())
        k -= 1
    return ' '.join(out)


class I18n:
    def __init__(self, src):
        with open(os.path.join(src, 'assets/i18n/en.json'), encoding='utf-8') as fh:
            self.en = json.load(fh)
        with open(os.path.join(src, 'assets/i18n/es.json'), encoding='utf-8') as fh:
            self.es = json.load(fh)
        self.hits = self.miss = 0

    def add(self, d, key, value=None):
        """d[key_en], d[key_es] from d[key] (or value)."""
        s = d.get(key) if value is None else value
        if not isinstance(s, str) or not s:
            return d
        en, es = self.en.get(s), self.es.get(s)
        if en is None and es is None:
            self.miss += 1
        else:
            self.hits += 1
        d[key + '_en'] = en
        d[key + '_es'] = es
        return d


def ordered(d, first):
    out = {k: d[k] for k in first if k in d}
    out.update({k: v for k, v in d.items() if k not in out})
    return out


def write(out_dir, name, data):
    p = os.path.join(out_dir, name)
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(plain(data), fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return p


# ---------------------------------------------------------------------------
# items
# ---------------------------------------------------------------------------

def build_items(F, tr, ctx):
    fi, fa, fp, fs, fsc, fc, fl = (F['items.dart'], F['armor.dart'], F['appearance.dart'], F['prices.dart'],
                                   F['session_controller.dart'], F['combat.dart'], F['loot.dart'])
    items = fi.const('items')
    # section comments inside the map
    a = fi.decl_pos('items')
    b = fi.matching(fi.code.index('{', a))
    sections = fi.section_comments(a, b)

    mat = fa.const('armorMat')
    resist = fa.const('matResist')
    wear = fa.const('matWear')
    cloth_slot = fsc.const('_clothSlot')
    long_weapons = fsc.const('_longWeapons')
    warmth = fsc.const('_warmth')
    heavy = fsc.const('_heavy')
    head_lamps = fsc.const('headLamps')
    book_skills = fsc.const('bookSkills')
    prices = fs.const('refPrices')
    price_fallback = fs.switch_after(r'int refPrice\(')['cases']
    loot_weights = fl.const('lootWeights')
    mind_items = fi.const('mindItems')
    burst = rx(fc, r'if \(weapon\.auto\) burstLeft = (\d+)', cast=int) + 1
    default_mat = rx(fa, r'armorMat\[id\] \?\? ArmorMat\.(\w+)', cast=str)
    rip_cond = rx(fa, r'final cond = 1 - ([\d.]+) \* \(wear', cast=float)

    skins_raw = fp.const('skinStyles')
    skin_fields = ['id', 'name', 'description', 'color_part', 'tier', 'places']
    tier_names = fp.const('skinTierNames')
    skins = []
    for s in skins_raw:
        if len(s) != len(skin_fields):
            raise DartParseError('appearance.dart: skinStyles entry with %d fields' % len(s))
        d = dict(zip(skin_fields, s))
        d['tier_name'] = tier_names[d['tier']]
        d['item'] = 'roupa_' + d['id']
        d['story_only'] = d['id'] in fp.const('storySkins')
        d['zombie_only'] = d['id'] in fp.const('zombieSkins')
        tr.add(d, 'name')
        tr.add(d, 'description')
        skins.append(d)
    skin_by_item = {s['item']: s for s in skins}

    ammo_for = {}
    for iid, it in items.items():
        w = it.get('weapon')
        if w and w.get('ammo'):
            ammo_for.setdefault(w['ammo'], []).append(iid)

    out = []
    for iid, it in items.items():
        if it['id'] != iid:
            raise DartParseError('items.dart: key %s != id %s' % (iid, it['id']))
        m = re.search(r"'%s'\s*:\s*ItemDef\(" % re.escape(iid), fi.code[a:b])
        line = fi.line_of(a + m.start())
        sec = [t for (ln, t) in sections if ln < line]
        d = dict(it)
        tr.add(d, 'name')
        tr.add(d, 'note')
        d['perishable'] = it['shelfLife'] is not None
        d['edible'] = it['kcal'] > 0 or it['ml'] > 0
        if it['shelfLife'] is not None:
            d['shelfLife_days'] = it['shelfLife']['total_seconds'] / 86400
        derived = {}
        w = it['weapon']
        if w:
            derived['melee'] = not w['ranged']
            derived['firearm'] = bool(w['ranged'] and w['ammo'] != 'flecha')
            derived['bow'] = w['ammo'] == 'flecha'
            derived['burst'] = burst if w['auto'] else 1
            derived['infinite_durability'] = w['durability'] == 0
            derived['damage_per_shot'] = w['damage'] * w['pellets']
            derived['damage_per_second'] = round(w['damage'] * w['pellets'] / w['cooldown'], 2)
        slot = cloth_slot.get(iid)
        if slot is None and w:
            slot = 'costas' if iid in long_weapons else 'cinto'
        derived['slot'] = slot
        if it['armor']:
            m_ = mat.get(iid, default_mat)
            derived['armor_material'] = m_
            derived['armor_wear_per_bite'] = wear[m_]
            derived['armor_block'] = {part: {atk: round(cov * r, 4) for atk, r in resist[m_].items()}
                                      for part, cov in it['armor'].items()}
            derived['armor_block_ripped'] = {part: {atk: round(cov * r * (1 - rip_cond), 4)
                                                    for atk, r in resist[m_].items()}
                                             for part, cov in it['armor'].items()}
        if iid in warmth:
            derived['warmth'] = warmth[iid]
        if iid in heavy:
            derived['heavy'] = heavy[iid]
        if iid in head_lamps:
            derived['head_lamp'] = True
        if iid in mind_items:
            derived['mind_item'] = True
        if iid in book_skills:
            derived['book_skills'] = book_skills[iid]
        if iid in ammo_for:
            derived['ammo_for'] = ammo_for[iid]
        if iid in skin_by_item:
            derived['skin_style'] = skin_by_item[iid]['id']
        derived['loot_weight'] = loot_weights.get(iid, 1)
        derived['ref_price'] = prices.get(iid, price_fallback.get(it['rarity'], price_fallback['_default']))
        derived['ref_price_from_table'] = iid in prices
        d['derived'] = derived
        d['source_section'] = sec[-1] if sec else ''
        d['source_line'] = line
        out.append(ordered(d, ['id', 'name', 'name_en', 'name_es', 'kind', 'rarity', 'weight']))

    def kit(name):
        return [{'id': k, 'qty': v, 'name': items[k]['name']} for k, v in fi.const(name).items()]

    for k in items:
        ctx['item_ids'].add(k)
    ctx['items'] = items
    ctx['skins'] = skins

    data = {
        'items': out,
        'starter_kit': kit('starterKit'),
        'starter_kit_doc': doc_above(fi, fi.decl_pos('starterKit')),
        'first_character_bonus': kit('firstCharacterBonus'),
        'first_character_bonus_doc': doc_above(fi, fi.decl_pos('firstCharacterBonus')),
        'fists': fi.const('fists'),
        'mind_items': list(mind_items),
        'enums': {
            'ItemKind': list(fi.enum_values('ItemKind')),
            'Rarity': list(fi.enum_values('Rarity')),
            'ArmorMat': list(fa.enum_values('ArmorMat')),
            'Attack': list(fa.enum_values('Attack')),
        },
        'rarity_labels': fi.switch_after(r'String rarityLabel\(')['cases'],
        'armor': {
            'doc': doc_above(fa, fa.code.index('enum ArmorMat')),
            'material_resist': resist,
            'material_wear_per_bite': wear,
            'material_labels': fa.switch_after(r'String matLabel\(')['cases'],
            'default_material': default_mat,
            'item_material': mat,
            'ripped_at_wear': 100,
            'ripped_or_worn_factor': '1 - %s * wear/100 (rasgada = metade)' % rip_cond,
            'piece_block_formula': 'cover[part] * material_resist[mat][attack] * (1 - 0.5*wear/100); camadas: 1 - prod(1 - block)',
        },
        'equipment_slots': fsc.const('slots'),
        'equipment_slot_names': fsc.const('slotNames'),
        'cloth_slot': cloth_slot,
        'long_weapons': list(long_weapons),
        'warmth': warmth,
        'heavy': heavy,
        'price_fallback_by_rarity': price_fallback,
        'skins': {
            'styles': skins,
            'tier_names': tier_names,
            'tier_weight': fp.const('skinTierWeight'),
            'tier_stamps_duplicate': fp.const('skinTierStamps'),
            'tier_colors': ['#%06X' % (c & 0xFFFFFF) for c in fp.const('skinTierColors')],
            'skin_tones': ['#%06X' % (c & 0xFFFFFF) for c in fp.const('skinTones')],
            'hair_tones': ['#%06X' % (c & 0xFFFFFF) for c in fp.const('hairTones')],
            'shirt_tones': ['#%06X' % (c & 0xFFFFFF) for c in fp.const('shirtTones')],
        },
    }
    return data


# ---------------------------------------------------------------------------
# recipes
# ---------------------------------------------------------------------------

def build_recipes(F, tr, ctx):
    fc, fsc, fch = F['crafting.dart'], F['session_controller.dart'], F['character.dart']
    recipes = fc.const('recipes')
    mod_of = fsc.const('modOf')
    mod_names = fsc.const('modNames')
    skill_names = fch.const('skillNames')
    items = ctx['items']
    out = []
    for r in recipes:
        d = dict(r)
        tr.add(d, 'name')
        for k in list(d['inputs']) + list(d['tools']) + ([d['output']] if d['output'] else []):
            if k not in items:
                raise DartParseError('crafting.dart: recipe %s uses unknown item %s' % (d['id'], k))
        d['station'] = 'fogo' if d['needsFire'] else ('bancada' if d['needsBench'] else 'nenhuma')
        d['time_seconds'] = 0  # craft() is instant in session_controller
        d['skill_name'] = skill_names.get(d['skill']) if d['skill'] else None
        d['output_name'] = items[d['output']]['name'] if d['output'] else None
        d['input_names'] = {k: items[k]['name'] for k in d['inputs']}
        d['xp_only_with_skill'] = d['skill'] is not None
        if d['id'] in mod_of:
            d['mod'] = mod_of[d['id']]
            d['mod_name'] = mod_names[mod_of[d['id']]]
        out.append(d)
    ctx['recipes'] = out
    repair_gain = rx(fsc, r'final gain = full \* base \* pow\(([\d.]+), weaponRepairs\) \* \(1 \+ ([\d.]+) \* ch\.level\(\'mecanica\'\)\)', group=None)
    injury = rx(fsc, r"_rng\.nextDouble\(\) < max\(0\.0, ([\d.]+) - ([\d.]+) \* ch\.level\(r\.skill!\)\)", group=None)
    filt = rx(fsc, r"r\.id == 'R09' && _rng\.nextDouble\(\) < ([\d.]+)")
    return {
        'recipes': out,
        'kinds': sorted({r['kind'] for r in out}),
        'doc': doc_above(fc, fc.code.index('class Recipe')),
        'rules': {
            'time': 'Instantâneo (craft() não tem tempo de espera).',
            'xp': 'XP da receita vai para a habilidade da receita (sem skill = sem XP). Móvel refeito depois de desmontar não dá XP.',
            'repair': {
                'R06_base_fraction': rx(fsc, r"r\.id == 'R08' \? ([\d.]+) : ([\d.]+)", group=2),
                'R08_base_fraction': rx(fsc, r"r\.id == 'R08' \? ([\d.]+) : ([\d.]+)", group=1),
                'decay_per_repair': float(repair_gain.group(1)),
                'mecanica_bonus_per_level': float(repair_gain.group(2)),
                'formula': 'ganho = durabilidade_max * base * %s^reparos * (1 + %s * nível mecânica)'
                           % (repair_gain.group(1), repair_gain.group(2)),
            },
            'R09_fail_chance': filt,
            'tool_injury': {
                'skills': ['carpintaria', 'mecanica'],
                'base_chance': float(injury.group(1)),
                'minus_per_level': float(injury.group(2)),
                'wound': 'corte nas mãos',
            },
            'bench_limit': 'R14: só uma bancada por base',
            'max_garden_plots': rx(fsc, r'static const int maxPlots = (\d+)', cast=int),
        },
    }


# ---------------------------------------------------------------------------
# loot
# ---------------------------------------------------------------------------

def kind_dict(k, decor=False):
    return {'name': k['name'], 'seconds': k['seconds'], 'noise': k['noise'],
            'noise_radius_m': round(k['noise'] * 120, 1),
            'only': list(k['only']) if k.get('only') is not None else None}


def noise_label(n):
    return 'barulho alto' if n >= 0.18 else ('barulho médio' if n >= 0.1 else 'silencioso')


def resolve_cat_value(v, cat, where):
    """Resolve ternaries/switches on `cat` (interior.dart fixtures) for category cat."""
    if isinstance(v, dict) and 'if' in v:
        cond = v['if']
        if not re.fullmatch(r'cat == PoiCategory\.\w+( \|\| cat == PoiCategory\.\w+)*', cond):
            raise DartParseError('%s: cannot resolve condition %r' % (where, cond))
        cats = re.findall(r'PoiCategory\.(\w+)', cond)
        return resolve_cat_value(v['then'] if cat in cats else v['else'], cat, where)
    if isinstance(v, dict) and 'switch' in v:
        if v['switch'] != 'cat':
            raise DartParseError('%s: switch on %r' % (where, v['switch']))
        c = v['cases']
        return resolve_cat_value(c[cat] if cat in c else c['_default'], cat, where)
    return v


def case(sw, key):
    c = sw['cases']
    return c[key] if key in c else c.get('_default')


def build_loot(F, tr, ctx):
    fl, fp, fi, fsc, fb = (F['loot.dart'], F['poi.dart'], F['interior.dart'], F['session_controller.dart'],
                           F['bunker_floors.dart'])
    fr = F['rules.dart']
    items = ctx['items']
    cats = fp.enum_values('PoiCategory')
    kinds = fl.const('_kinds')
    extra = fl.const('_extraKinds')
    special_pool = fl.const('_specialPool')
    loot_weights = fl.const('lootWeights')
    named_fallback = {'Geladeira': fl.const('_fridge'), 'Gaveta': fl.const('_drawer'),
                      'Balcão': fl.const('_counter'), 'Caixa registradora': fl.const('_register')}
    shelf = fl.const('_shelf')
    default_quick = [fl.const(n) for n in ('_shelf', '_counter', '_stock')]
    rx(fl, r"_kinds\[c\] \?\? const \[_shelf, _counter, _stock\]", group=None)

    def kind_named(name):
        for lst in [extra] + list(kinds.values()):
            for k in lst:
                if k['name'] == name:
                    return k
        return named_fallback.get(name, shelf)

    decor = fi.const('decorFurniture')
    special_of = fi.const('_specialOf')
    locked = fi.const('_locked')
    no_window = fi.const('_noWindow')
    template = fi.switch_after(r'_template\(PoiCategory c\)')
    upper = fi.switch_after(r'_upperTemplate\(PoiCategory c\)')
    min_size = fi.switch_after(r'minSize\(PoiCategory c\)')
    typ_size = fi.switch_after(r'typicalSize\(PoiCategory c\)')
    zrange = fi.switch_after(r'zombieRange\(PoiCategory c\)')
    fixtures = fi.switch_after(r'_wallFixtures\(String type, PoiCategory cat\)')
    clutter = fi.switch_after(r'_floorClutter\(String type\)')
    near_door = fi.switch_after(r'String\? _nearDoor\(String type\)')
    front_n = rx(fi, r'mine\.take\((\d+)\)', cast=int)
    # furniture placed in code (not via _wallFixtures): gondola rows, truck, beds, desks...
    placed = {}
    rows_types = re.findall(r"type == '(\w+)'", rx(fi, r'bool _rows\(String type\) => ([^;]+);', cast=str))
    rx(fi, r"if \(_rows\(r\.type\)[^)]*\) \{\s*for [^{]*\{\s*for [^{]*\{\s*put\('Prateleira'.*?loot: mineShop\)", group=None)
    for t in rows_types:
        placed.setdefault(t, []).append({'name': 'Prateleira', 'max': None, 'rows': True, 'lootable': True})
    for m in re.finditer(r"if \(r\.type == '(\w+)'[^{]*\{\s*put\('([^']+)'[^;]*?loot: (false|mineShop)\);", fi.code):
        placed.setdefault(m.group(1), []).append({'name': m.group(2), 'max': None, 'lootable': m.group(3) != 'false'})
    m = rx(fi, r"if \(\(r\.type == '(\w+)' \|\| r\.type == '(\w+)'\)[^{]*\{.*?put\(r\.type == 'sala' \? '([^']+)' : '([^']+)'", group=None)
    placed.setdefault('sala', []).append({'name': m.group(3), 'max': None, 'lootable': False})
    placed.setdefault('salao_mesas', []).append({'name': m.group(4), 'max': None, 'lootable': False})

    # OSM tag mapping (categorize)
    osm = {c: {'amenity': [], 'shop': []} for c in cats}
    cat_body, _ = fp.body_of(r'PoiCategory\? categorize\(')
    blk_a = cat_body.index('if (a is String)')
    blk_s = cat_body.index('if (s is String)')
    for blk, key, var in ((cat_body[blk_a:blk_s], 'amenity', 'a'), (cat_body[blk_s:], 'shop', 's')):
        for m in re.finditer(r'if \((.+?)\) return PoiCategory\.(\w+);', blk):
            cond, c = m.group(1), m.group(2)
            for sm in re.finditer(r"(\w+)\.contains\(%s\)" % var, cond):
                osm[c][key].extend(list(fp.const(sm.group(1))))
            osm[c][key].extend(re.findall(r"%s == '(\w+)'" % var, cond))
        m = re.search(r'return PoiCategory\.(\w+);\s*\}\s*return null;', blk)
        if m and key == 'shop':
            osm[m.group(1)]['shop'].append('* (qualquer outra loja)')

    def pool_stats(pool):
        """Per item: copies, rarity, share of its rarity tier (weighted)."""
        tier_tot = {}
        for iid in pool:
            r = items[iid]['rarity']
            tier_tot[r] = tier_tot.get(r, 0) + loot_weights.get(iid, 1)
        st = {}
        for iid in pool:
            s = st.setdefault(iid, {'copies': 0, 'rarity': items[iid]['rarity'], 'weight': loot_weights.get(iid, 1)})
            s['copies'] += 1
        for iid, s in st.items():
            s['tier_share'] = round(s['copies'] * s['weight'] / tier_tot[s['rarity']], 4)
        return st

    def resolve_room(rt, cat):
        where = 'interior.dart:_wallFixtures(%s,%s)' % (rt, cat)
        fx = resolve_cat_value(case(fixtures, rt), cat, where) or []
        furn = []
        nd = case(near_door, rt)
        if nd:
            furn.append({'name': nd, 'width': None, 'depth': None, 'max': 1, 'near_door': True})
        for t in fx:
            furn.append({'name': t[0], 'width': t[1], 'depth': t[2], 'max': t[3]})
        furn.extend(dict(x) for x in placed.get(rt, []))
        for t in (case(clutter, rt) or []):
            furn.append({'name': t[0], 'width': t[1], 'depth': t[2], 'max': None, 'floor_clutter': True})
        for f in furn:
            f['lootable'] = f.get('lootable', True) and not f.get('floor_clutter') and f['name'] not in decor
        return {'room': rt, 'special': special_of.get(rt, ''), 'locked': rt in locked,
                'no_window': rt in no_window, 'furniture': furn}

    categories = {}
    for cid, c in cats.items():
        pool = c['loot']
        for iid in pool:
            if iid not in items:
                raise DartParseError('poi.dart: %s pool has unknown item %s' % (cid, iid))
        quick = kinds.get(cid, default_quick)
        tmpl = case(template, cid)
        up = case(upper, cid)
        d = {
            'id': cid,
            'label': c['label'],
            'color': '#%06X' % (c['color'] & 0xFFFFFF),
            'guards': c['guards'],
            'loot': pool,
            'loot_stats': pool_stats(pool),
            'osm_tags': osm[cid],
            'quick_loot_furniture': [dict(kind_dict(k), noise_label=noise_label(k['noise'])) for k in quick],
            'quick_loot_furniture_is_default': cid not in kinds,
            'interior': {
                'min_size_m': case(min_size, cid),
                'typical_size_m': case(typ_size, cid),
                'zombies': case(zrange, cid),
                'ground_floor': [{'depth_frac': band[0], 'rooms': [resolve_room(rt, cid) for rt in band[1]]}
                                 for band in tmpl],
                'upper_floors': [{'depth_frac': band[0], 'rooms': [resolve_room(rt, cid) for rt in band[1]]}
                                 for band in up],
            },
        }
        tr.add(d, 'label')
        categories[cid] = d
    ctx['categories'] = categories

    all_kinds = {}
    for lst in [extra] + list(kinds.values()) + [default_quick, list(named_fallback.values())]:
        for k in lst:
            if k['name'] not in all_kinds:
                all_kinds[k['name']] = dict(kind_dict(k), noise_label=noise_label(k['noise']))
    for c in categories.values():
        for fk in ('ground_floor', 'upper_floors'):
            for band in c['interior'][fk]:
                for room in band['rooms']:
                    for f in room['furniture']:
                        if f['lootable'] and f['name'] not in all_kinds:
                            k = kind_named(f['name'])
                            all_kinds[f['name']] = dict(kind_dict(k), name=f['name'], noise_label=noise_label(k['noise']),
                                                        implicit=True)
    for name in sorted(all_kinds):
        k = all_kinds[name]
        tr.add(k, 'name')
        k['resolved_as'] = kind_named(name)['name']

    # bunker underground (plans + furniture per room type, via regex over the case blocks)
    plans = fb.const('_plans')
    room_labels = fb.switch_after(r'String bunkerRoomLabel\(')['cases']
    body, off = fb.body_of(r'for \(var ri = 0; ri < rooms\.length; ri\+\+\) \{\s*final r = rooms\[ri\];\s*switch')
    bunker_rooms = {}
    parts = re.split(r"\n\s*case ", body)
    for p in parts[1:]:
        head = p.split(':', 1)[0]
        types = re.findall(r"'(\w+)'", head)
        names = re.findall(r"\('([^']+)', [\d.]+, [\d.]+(?:, (\d+))?\)", p)
        puts = re.findall(r"put\('([^']+)'[^;]*?(loot: false)?[,)][^;]*;", p)
        specials = re.findall(r"special: '(\w+)'", p) + re.findall(r"special: r\.type == '(\w+)' \? '(\w+)'", p)
        furn = []
        for n, mx in names:
            furn.append({'name': n, 'max': int(mx) if mx else None,
                         'lootable': n not in decor and n not in fb.const('bunkerUsables')})
        for n, nl in puts:
            if not any(f['name'] == n for f in furn):
                furn.append({'name': n, 'max': None,
                             'lootable': not nl and n not in decor and n not in fb.const('bunkerUsables')})
        for t in types:
            bunker_rooms[t] = {'label': room_labels.get(t, t), 'furniture': furn,
                               'special': [s if isinstance(s, str) else list(s) for s in specials]}
    bunker = {
        'theme_order': fb.const('bunkerThemeOrder'),
        'theme_labels': fb.switch_after(r'String bunkerThemeLabel\(')['cases'],
        'room_labels': room_labels,
        'usables': fb.const('bunkerUsables'),
        'plans': {k: {'w': v['w'], 'h': v['h'],
                      'rooms': [r['type'] for r in v['rooms']],
                      'doors': [dict(d) for d in v['doors']]} for k, v in plans.items()},
        'room_furniture': bunker_rooms,
        'doc': doc_above(fb, fb.code.index('class _BRoom')),
    }

    # special rules
    rare = rx(fr, r'static double rareChance\(double totalMeters\) =>\s*\(([\d.]+) \+ ([\d.]+) \* totalMeters / 1000\)\.clamp\(0\.0, ([\d.]+)\)', group=None)
    skin = rx(fsc, r'\(([\d.]+) \* rareMult \* \(1 \+ meters / (\d+)\)\)\.clamp\(0\.0, ([\d.]+)\)', group=None)
    flare = rx(fsc, r'final hard = km < (\d+) \? 0\.0 : min\(([\d.]+), ([\d.]+) \+ ([\d.]+) \* \(km - \d+\)\);'
                    r'.*?x < hard \+ ([\d.]+)\) \{\s*id = \'sinalizador_medio\'.*?x < hard \+ ([\d.]+)\) \{\s*id = \'sinalizador_facil\'',
               group=None)
    corpse_body, _ = fl.body_of(r'LootContainer makeCorpse\(')
    cm = re.search(r"rng\.nextDouble\(\) < ([\d.]+)\) got\.add\('pano'\).*?rng\.nextDouble\(\) < ([\d.]+) \? 0 : 1 \+ \(rng\.nextDouble\(\) < ([\d.]+) \? 1 : 0\)"
                   r".*?rng\.nextInt\((\d+)\).*?rng\.nextDouble\(\) < ([\d.]+)\) got\.add\('selo'\).*?LootContainer\(name, ([\d.]+), ([\d.]+), got\)",
                   corpse_body, re.S)
    if not cm:
        raise DartParseError('loot.dart: makeCorpse rules not recognised')
    ammo = rx(fl, r'box \? (\d+) \+ rng\.nextInt\((\d+)\) : (\d+) \+ rng\.nextInt\((\d+)\)', group=None)
    mc = rx(fl, r'final n = min\(kinds\.length, (\d+) \+ rng\.nextInt\((\d+)\)\);', group=None)
    empty = rx(fl, r'final count = rng\.nextDouble\(\) < ([\d.]+) \? 0 : (\d+) \+ rng\.nextInt\((\d+)\);', group=None)
    est = rx(fl, r"special == 'estoque'\) count = (\d+) \+ rng\.nextInt\((\d+)\)", group=None)
    sp = rx(fl, r"special == 'arsenal' \|\| special == 'remedios'\) count = (\d+) \+ rng\.nextInt\((\d+)\)", group=None)
    spc = rx(fl, r'pool != null && rng\.nextDouble\(\) < ([\d.]+)\)')
    fit = rx(fl, r'return rng\.nextDouble\(\) < ([\d.]+) \? pickWeighted\(list, rng\) : null;')
    inc = rx(fsc, r'r < rare \+ ([\d.]+) \? Rarity\.incomum')
    rm = rx(fsc, r'_rollItem\(p\.category, rareMult: f\.front \? ([\d.]+) : ([\d.]+)\)', group=None)
    bunker_rm = rx(fsc, r'rareMult: ([\d.]+) \+ ([\d.]+) \* l\)', group=None)
    rules = {
        'empty_container_chance': float(empty.group(1)),
        'items_per_container': [int(empty.group(2)), int(empty.group(2)) + int(empty.group(3)) - 1],
        'quick_loot_containers': [int(mc.group(1)), int(mc.group(1)) + int(mc.group(2)) - 1],
        'interior_front_containers': front_n,
        'interior_estoque_items': [int(est.group(1)), int(est.group(1)) + int(est.group(2)) - 1],
        'interior_arsenal_remedios_items': [int(sp.group(1)), int(sp.group(1)) + int(sp.group(2)) - 1],
        'special_pool_chance': spc,
        'fit_only_fallback_chance': fit,
        'ammo_loose': [int(ammo.group(3)), int(ammo.group(3)) + int(ammo.group(4)) - 1],
        'ammo_box': [int(ammo.group(1)), int(ammo.group(1)) + int(ammo.group(2)) - 1],
        'ammo_box_when': "móvel 'Arsenal trancado' ou sala especial arsenal/estoque",
        'rarity_roll': {
            'rare_chance_formula': 'clamp(%s + %s * km_andados_na_sessao, 0, %s) * rareMult(traço) * rareMult(móvel)'
                                   % (rare.group(1), rare.group(2), rare.group(3)),
            'rare_base': float(rare.group(1)), 'rare_per_km': float(rare.group(2)), 'rare_max': float(rare.group(3)),
            'uncommon_chance': inc,
            'common': 'o resto',
            'legendary': 'nunca sai do sorteio por raridade (só achados especiais/zumbis/história)',
            'fallback': 'se o lugar não tem item da raridade sorteada, desce para a raridade abaixo',
        },
        'rare_multiplier': {
            'quick_loot': 0,
            'interior_front': float(rm.group(1)),
            'interior_inside': float(rm.group(2)),
            'bunker_floor_formula': '%s + %s * andar' % (bunker_rm.group(1), bunker_rm.group(2)),
            'trait_sortudo': 1.1, 'trait_azarado': 0.9,
        },
        'very_rare_per_place': {
            'radio_posto': fsc.const('radioPerPlace'),
            'expansor': fsc.const('expansorPerPlace'),
            'note': 'Uma vez por lugar vasculhado por dentro, num móvel de dentro; chance / rareMult do traço.',
        },
        'flares_per_place': {
            'sinalizador_dificil': 'km<%s: 0; senão min(%s, %s + %s*(km-%s))' % (flare.group(1), flare.group(2),
                                                                              flare.group(3), flare.group(4), flare.group(1)),
            'sinalizador_medio': float(flare.group(5)),
            'sinalizador_facil': float(flare.group(6)) - float(flare.group(5)),
            'note': 'Faixas cumulativas: x < hard -> difícil; < hard+%s -> médio; < hard+%s -> fácil.'
                    % (flare.group(5), flare.group(6)),
        },
        'skin_chance': {
            'formula': 'clamp(%s * rareMult * (1 + metros/%s), 0, %s)' % skin.groups(),
            'base': float(skin.group(1)), 'meters_div': int(skin.group(2)), 'max': float(skin.group(3)),
            'place_bonus': rx(fsc, r'if \(s\.\$6\.contains\(c\.name\)\) k \*= (\d+);', cast=int),
            'note': 'Só dentro dos lugares (rareMult > 0). Uniformes de zumbi e roupas de história nunca saem.',
        },
        'corpse': {
            'pano_chance': float(cm.group(1)),
            'no_items_chance': float(cm.group(2)),
            'second_item_chance': float(cm.group(3)),
            'extra_ammo_max': int(cm.group(4)) - 1,
            'selo_chance': float(cm.group(5)),
            'search_seconds': float(cm.group(6)),
            'noise': float(cm.group(7)),
        },
    }
    return {
        'categories': categories,
        'furniture_kinds': all_kinds,
        'decor_furniture': list(decor),
        'special_pools': special_pool,
        'room_special': special_of,
        'locked_rooms': list(locked),
        'loot_weights': loot_weights,
        'corpse_loot': fl.const('corpseLoot'),
        'backpack_loot': fl.const('backpackLoot'),
        'bunker_underground': bunker,
        'rules': rules,
        'noise_note': 'noise 0..1; raio de audição = noise x 120 m',
    }


def build_items_where(ctx, loot, zombies, recipes, items_data):
    items = ctx['items']
    W = {iid: {'name': items[iid]['name'], 'rarity': items[iid]['rarity'], 'pools': [], 'furniture': {},
               'zombies': [], 'other': []} for iid in items}
    kinds = loot['furniture_kinds']
    special_pools = loot['special_pools']

    def mark(iid, cid, fname, room=None, special=False):
        e = W[iid]['furniture'].setdefault(cid, {}).setdefault(fname, {'quick': False, 'rooms': [],
                                                                      'via_special_pool': False})
        if room is None:
            e['quick'] = True
        elif room not in e['rooms']:
            e['rooms'].append(room)
        e['via_special_pool'] = e['via_special_pool'] or special

    for cid, c in loot['categories'].items():
        for iid, st in c['loot_stats'].items():
            W[iid]['pools'].append({'category': cid, 'copies': st['copies'], 'tier_share': st['tier_share']})
        pool = set(c['loot'])
        for k in c['quick_loot_furniture']:
            cand = pool if k['only'] is None else pool & set(k['only'])
            for iid in cand:
                mark(iid, cid, k['name'])
        for floor_key in ('ground_floor', 'upper_floors'):
            for band in c['interior'][floor_key]:
                for room in band['rooms']:
                    sp = set(special_pools.get(room['special'], []))
                    for f in room['furniture']:
                        if not f['lootable']:
                            continue
                        k = kinds[f['name']]
                        cand = (pool | sp) if k['only'] is None else set(k['only'])
                        for iid in cand:
                            mark(iid, cid, f['name'], room['room'], iid not in pool)
    for z in zombies['classes']:
        for e in z['loot']:
            W[e['item']]['zombies'].append({'class': z['name'], 'chance': e['chance'], 'max': e['max']})
        if z.get('skin_item') and z['skin_item'] in W:
            W[z['skin_item']]['zombies'].append({'class': z['name'], 'chance': zombies['skin_drop'], 'max': 1})
    for iid in loot['corpse_loot']:
        W[iid]['other'].append('corpse_loot')
    for iid in loot['backpack_loot']:
        W[iid]['other'].append('backpack_loot (zumbi mochileiro)')
    for sp, lst in special_pools.items():
        for iid in set(lst):
            W[iid]['other'].append('special_pool:' + sp)
    for r in recipes['recipes']:
        if r['output']:
            W[r['output']]['other'].append('recipe:%s' % r['id'])
    for e in items_data['starter_kit']:
        W[e['id']]['other'].append('starter_kit')
    for e in items_data['first_character_bonus']:
        W[e['id']]['other'].append('first_character_bonus')
    for k in ('radio_posto', 'expansor'):
        W[k]['other'].append('very_rare_per_place')
    for k in ('sinalizador_facil', 'sinalizador_medio', 'sinalizador_dificil'):
        W[k]['other'].append('flare_find_per_place')
    for s in ctx['skins']:
        if s['item'] in W:
            W[s['item']]['other'].append('skin:' + ('story' if s['story_only'] else 'zombie' if s['zombie_only'] else 'interior_loot'))
    refs = {iid: {} for iid in W}
    lib_root = ctx['lib_root']
    pat = re.compile(r"'(\w+)'")
    for root, _dirs, files in sorted(os.walk(lib_root)):
        for fn in sorted(files):
            if not fn.endswith('.dart'):
                continue
            rel = os.path.relpath(os.path.join(root, fn), lib_root)
            if rel in ('game/items.dart', 'game/prices.dart'):
                continue
            with open(os.path.join(root, fn), encoding='utf-8') as fh:
                for ln, line in enumerate(fh, 1):
                    for m in pat.finditer(line):
                        if m.group(1) in refs:
                            refs[m.group(1)].setdefault(rel, []).append(ln)
    for iid, w in W.items():
        w['referenced_in'] = {k: v for k, v in refs[iid].items()}
        w['other'] = sorted(set(w['other']))
        w['places'] = sorted({p['category'] for p in w['pools']} | set(w['furniture']))
        w['obtainable'] = bool(w['places'] or w['zombies'] or w['other'])
    return W


# ---------------------------------------------------------------------------
# characters
# ---------------------------------------------------------------------------

def build_characters(F, tr, ctx, lib_dir):
    fc, fsc = F['character.dart'], F['session_controller.dart']
    traits = fc.const('traits')
    profs = fc.const('professions')
    skill_names = fc.const('skillNames')
    tids = {t['id'] for t in traits}

    # Character getters
    cls_body, cls_off = fc.body_of(r'class Character \{')
    getters = {}
    for m in re.finditer(r'\n  (?:double|int|bool|String\?) (?:get )?(\w+)(\([^)]*\))?\s*(=>|\{)', cls_body):
        name = m.group(1)
        if name in ('has', 'level', 'gainXp', 'toJson', '_bump'):
            continue
        getters[name] = src_snippet(fc, r'(?:double|int|bool|String\?) (?:get )?%s\b' % re.escape(name))

    def effects_of(tid):
        out = []
        for g, code in getters.items():
            c = ' '.join(code.split())
            for m in re.finditer(r"if \(has\('%s'\)\) m ([+-])= ([\d.]+);" % tid, c):
                out.append({'stat': g, 'op': 'add', 'value': float(m.group(2)) * (1 if m.group(1) == '+' else -1)})
            for m in re.finditer(r"has\('%s'\)\s*\?\s*(-?[\d.]+)" % tid, c):
                out.append({'stat': g, 'op': 'set', 'value': float(m.group(1))})
        return out

    ctor, _ = fc.body_of(r'Character\(this\.professionId, Set<String> chosen, this\.createdAt\)\s*:\s*traits = \{[^}]*\}')
    if '_bump(' not in ctor:
        raise DartParseError('character.dart: Character constructor body not found')
    bumps = {}
    for m in re.finditer(r"if \(traits\.contains\('(\w+)'\)\)\s*(\{[^}]*\}|[^;]*;)", ctor):
        bumps[m.group(1)] = re.findall(r"_bump\('(\w+)'\)", m.group(2))

    # code references across lib/game
    refs = {}
    lib_root = os.path.dirname(lib_dir)
    for root, _dirs, files in sorted(os.walk(lib_root)):
        for fn in sorted(files):
            if not fn.endswith('.dart'):
                continue
            rel = os.path.relpath(os.path.join(root, fn), lib_root)
            with open(os.path.join(root, fn), encoding='utf-8') as fh:
                for ln, line in enumerate(fh, 1):
                    if rel != 'game/character.dart':
                        for m in re.finditer(r"\bhas\('(\w+)'\)", line):
                            if m.group(1) in tids:
                                refs.setdefault(m.group(1), []).append('%s:%d: %s' % (rel, ln, line.strip()[:200]))
                    for m in re.finditer(r"professionId == '(\w+)'", line):
                        refs.setdefault('prof:' + m.group(1), []).append('%s:%d: %s' % (rel, ln, line.strip()[:200]))

    by_id = {t['id']: t for t in traits}
    tout = []
    for t in traits:
        for c in t['conflicts']:
            if c not in tids:
                raise DartParseError('character.dart: trait %s conflicts with unknown %s' % (t['id'], c))
        d = dict(t)
        tr.add(d, 'name')
        tr.add(d, 'effect')
        d['positive'] = t['cost'] > 0
        d['effects'] = effects_of(t['id'])
        d['skill_bonus'] = bumps.get(t['id'], [])
        d['code_refs'] = refs.get(t['id'], [])
        d['conflict_names'] = [by_id[c]['name'] for c in t['conflicts']]
        d['granted_by_professions'] = [p['id'] for p in profs if t['id'] in p['freeTraits']]
        tout.append(d)
    pout = []
    for p in profs:
        d = dict(p)
        tr.add(d, 'name')
        tr.add(d, 'note')
        for tid in p['freeTraits']:
            if tid not in tids:
                raise DartParseError('character.dart: profession %s free trait unknown %s' % (p['id'], tid))
        d['free_trait_names'] = [by_id[x]['name'] for x in p['freeTraits']]
        d['free_traits_value'] = sum(by_id[x]['cost'] for x in p['freeTraits'])
        d['skill_names'] = {k: skill_names[k] for k in p['skills']}
        d['code_refs'] = refs.get('prof:' + p['id'], [])
        pout.append(d)

    xp_expr = rx(fc, r'int xpToNext\(int level\) => ([^;]+);', cast=str).strip()
    m = re.fullmatch(r'(\d+) \* \(level \+ (\d+)\)', xp_expr)
    if not m:
        raise DartParseError('character.dart: xpToNext formula changed: ' + xp_expr)
    a_, b_ = int(m.group(1)), int(m.group(2))
    skill_max = fc.const('skillMax')
    xp_to_next = [a_ * (lv + b_) for lv in range(skill_max)]
    cum = []
    s = 0
    for v in xp_to_next:
        s += v
        cum.append(s)
    book_skills = fsc.const('bookSkills')
    role_skills = fsc.const('roleSkills')
    role_names = fsc.const('roleNames')
    xp_sources = {}
    for m in re.finditer(r"_xp\('(\w+)', ([^)]+)\)", fsc.code):
        ln = fsc.line_of(m.start())
        xp_sources.setdefault(m.group(1), []).append({'amount': m.group(2).strip(), 'line': ln,
                                                      'code': fsc.lines[ln - 1].strip()[:200]})
    skills = []
    for sid, name in skill_names.items():
        d = {'id': sid, 'name': name}
        tr.add(d, 'name')
        eff = []
        for g, code in getters.items():
            c = ' '.join(code.split())
            for mm in re.finditer(r"([\d.]+) \* level\('%s'\)" % sid, c):
                eff.append({'stat': g, 'per_level': float(mm.group(1))})
        d['effects_per_level'] = eff
        d['books'] = [b for b, ss in book_skills.items() if sid in ss]
        d['group_roles'] = [r for r, ss in role_skills.items() if sid in ss]
        d['starting_from_professions'] = {p['id']: p['skills'][sid] for p in profs if sid in p['skills']}
        d['starting_from_traits'] = [t for t, ss in bumps.items() if sid in ss]
        d['xp_sources'] = xp_sources.get(sid, [])
        skills.append(d)
    xpmult = getters.get('xpMult', '')
    return {
        'professions': pout,
        'traits': tout,
        'skills': skills,
        'skill_max': skill_max,
        'xp_formula': 'xpToNext(level) = ' + xp_expr,
        'xp_to_next': xp_to_next,
        'xp_cumulative': cum,
        'xp_multipliers': {
            'traits': xpmult,
            'book': '+50% por 1 dia real na(s) habilidade(s) do livro',
            'group_role': '+25% nas habilidades do papel (traço Líder: dobro)',
        },
        'book_skills': book_skills,
        'group_roles': {r: {'name': role_names.get(r), 'skills': ss} for r, ss in role_skills.items()},
        'computed_stats': getters,
        'build_rules': {
            'validate': src_snippet(fc, r'String\? validateBuild\('),
            'points_left': src_snippet(fc, r'int pointsLeft\('),
        },
    }


# ---------------------------------------------------------------------------
# zombies
# ---------------------------------------------------------------------------

def build_zombies(F, tr, ctx):
    fz, fm, fi = F['zclass.dart'], F['models.dart'], F['interior.dart']
    classes = fz.enum_values('ZClass')
    loot_sw = fz.switch_after(r'get loot =>')
    statics = fz.static_consts('ZClass')
    sv = {s['name']: s for s in statics}
    by_place = sv['byPlace']['value']
    street = sv['streetWeights']['value']
    # field docs from the enum fields
    field_docs = {}
    for m in re.finditer(r'final (?:double|bool|String) (\w+);', fz.code):
        field_docs[m.group(1)] = trailing_comment(fz.lines[fz.line_of(m.start()) - 1])
    chefe_no_skin = rx(fz, r'special && this != ZClass\.(\w+) \? skinItem\(id\)', cast=str)
    out = []
    for name, c in classes.items():
        d = {'name': name}
        d.update(c)
        tr.add(d, 'label')
        d['special'] = name != 'comum'
        d['skin_item'] = ('roupa_' + c['id']) if d['special'] and name != chefe_no_skin else None
        if d['skin_item'] and d['skin_item'] not in ctx['items']:
            raise DartParseError('zclass.dart: skin item %s missing' % d['skin_item'])
        lt = loot_sw['cases'].get(name)
        if lt is None:
            raise DartParseError('zclass.dart: loot switch missing class %s' % name)
        d['loot'] = [{'item': i, 'chance': p, 'max': n, 'item_name': ctx['items'][i]['name']} for i, p, n in lt]
        d['places'] = sorted({p for p, lst in by_place.items() if name in lst})
        d['place_weight'] = {p: lst.count(name) / len(lst) for p, lst in by_place.items() if name in lst}
        d['street_weight'] = street.get(name)
        d['extra_backpack'] = name == 'mochileiro'
        out.append(d)
    mb = rx(fz, r'final n = (\d+) \+ rng\.nextInt\((\d+)\);\s*for \(var i = 0; i < n; i\+\+\) \{\s*got\.add\(pickWeighted\(rng\.nextDouble\(\) < ([\d.]+)', group=None)
    # map zombie states (models.dart doc comment)
    zdoc_pos = fm.code.index('enum ZType')
    states = {}
    for ln in doc_above(fm, zdoc_pos).split(' - ')[1:]:
        k, _, v = ln.partition(':')
        states[k.strip()] = v.strip()
    zt = list(fm.enum_values('ZType'))
    if set(states) != set(zt):
        raise DartParseError('models.dart: ZType docs %s != enum %s' % (sorted(states), zt))
    return {
        'classes': out,
        'field_docs': field_docs,
        'missing_fields_note': 'ZClass não tem multiplicador de dano nem de loot: só hp, speed, torso, head, '
                               'fireproof e windup (preparo do golpe; menor = ataca mais rápido).',
        'skin_drop': sv['skinDrop']['value'],
        'street_chance': sv['streetChance']['value'],
        'near_chance': sv['nearChance']['value'],
        'horde_militar': sv['hordeMilitar']['value'],
        'statics': statics,
        'by_place': by_place,
        'street_weights': street,
        'mochileiro_backpack': {'items': [int(mb.group(1)), int(mb.group(1)) + int(mb.group(2)) - 1],
                                'corpse_loot_chance': float(mb.group(3)),
                                'else': 'backpack_loot'},
        'pick_rules': src_snippet(fz, r'static ZClass pick\('),
        'map_states': [{'id': s, 'description': states[s]} for s in zt],
        'asleep_rule': 'dormente e caido começam adormecidos (asleep = type != errante)',
        'zombies_per_place_interior': {cid: fi.switch_after(r'zombieRange\(PoiCategory c\)')['cases'].get(
            cid, fi.switch_after(r'zombieRange\(PoiCategory c\)')['cases']['_default']) for cid in ctx['categories']},
        'guards_per_place': {cid: c['guards'] for cid, c in ctx['categories'].items()},
    }


# ---------------------------------------------------------------------------
# base
# ---------------------------------------------------------------------------

def build_base(F, tr, ctx):
    fb, fsc, fc = F['base.dart'], F['session_controller.dart'], F['combat.dart']
    fk = fb.const('furnitureKinds')
    furn_statics = {s['name']: s for s in fb.static_consts('Furniture')}
    open_statics = {s['name']: s for s in fb.static_consts('Opening')}
    base_statics = fb.static_consts('Base')
    outpost = fb.static_consts('Outpost')
    rearm = fsc.const('rearmCost')
    recipes_by_furn = {r['furniture']: r for r in ctx['recipes'] if r['furniture']}
    trap_uses = furn_statics['trapUses']['value']
    pieces = []
    for kid, k in fk.items():
        d = dict(k)
        tr.add(d, 'name')
        tr.add(d, 'use')
        r = recipes_by_furn.get(kid)
        d['recipe'] = r['id'] if r else None
        d['cost'] = r['inputs'] if r else None
        d['tools'] = r['tools'] if r else None
        d['needsBench'] = r['needsBench'] if r else None
        d['skill'] = r['skill'] if r else None
        d['minLevel'] = r['minLevel'] if r else None
        d['xp'] = r['xp'] if r else None
        d['trap'] = kid in furn_statics['trapKinds']['value']
        d['uses'] = trap_uses.get(kid)
        d['rearm_cost'] = rearm.get(kid)
        d['fire'] = kid in furn_statics['fireKinds']['value']
        if kid == 'bau':
            d['capacity_kg'] = furn_statics['chestCapacity']['value']
        if kid == 'barril':
            d['max_bottles'] = furn_statics['barrelMax']['value']
        pieces.append(d)
    for kid in recipes_by_furn:
        if kid not in fk:
            raise DartParseError('crafting.dart: recipe furniture %s has no FurnitureKind' % kid)
    up = rx(fsc, r"final n = max\(1, \(len / (\d+)\)\.ceil\(\)\);\s*return base\.tierOf\(i\) == 0 \? \{'chapa': n, 'pregos': (\d+) \* n\} : \{'cimento': n, 'agua': n\};", group=None)
    tier_names = fb.const('wallTierNames')
    tier_hp = fb.const('wallTierHp')
    per = int(up.group(1))
    mpb = [s['value'] for s in base_statics if s['name'] == 'metersPerBoard'][0]
    walls = [{'tier': 0, 'name': tier_names[0], 'hp': tier_hp[0],
              'cost': {'tabuas': '1 a cada %s m' % mpb, 'pregos': '1 a cada %s m' % mpb}}]
    walls.append({'tier': 1, 'name': tier_names[1], 'hp': tier_hp[1],
                  'upgrade_cost': {'chapa': '1 a cada %d m' % per, 'pregos': '%s a cada %d m' % (up.group(2), per)}})
    walls.append({'tier': 2, 'name': tier_names[2], 'hp': tier_hp[2],
                  'upgrade_cost': {'cimento': '1 a cada %d m' % per, 'agua': '1 a cada %d m' % per}})
    hp_m = rx(fb, r"hp = hp \?\? \(kind == 'janela' \? (\d+) : (\d+)\)", group=None)
    openings = []
    for k, w in open_statics['width']['value'].items():
        openings.append({'id': k, 'name': open_statics['names']['value'][k], 'width_m': w,
                         'cost': open_statics['cost']['value'][k],
                         'hp': int(hp_m.group(1)) if k == 'janela' else int(hp_m.group(2)),
                         'boards_hp_bonus': open_statics['boardsHp']['value'] if k == 'janela' else None})
        tr.add(openings[-1], 'name')
    return {
        'furniture': pieces,
        'walls': walls,
        'wall_upgrade_rule': 'reforço: 1 unidade a cada %d m (mínimo 1); madeira -> chapa -> concreto' % per,
        'openings': openings,
        'base_constants': base_statics,
        'furniture_constants': list(furn_statics.values()),
        'opening_constants': list(open_statics.values()),
        'outpost_constants': outpost,
        'window_boards': {
            'cost': {k: int(v) for k, v in re.findall(r"'(\w+)': (\d+)", rx(
                fsc, r"if \(o\.boards\) return 'Já tem tábuas\.';\s*const cost = (\{[^}]*\});", cast=str))},
            'xp_carpintaria': rx(fsc, r"o\.boards = true;\s*o\.hp = o\.maxHp;\s*_xp\('carpintaria', (\d+)\)", cast=int),
        },
        'trap_effects_in_combat': {
            'estacas': {'leg_damage': rx(fc, r'case CombatTerrain\.kEstacas:\s*z\.legDmg \+= (\d+);', cast=int),
                        'damage': rx(fc, r"_burnZombie\(z, (\d+), label: 'estacas!'\)", cast=int),
                        'cripples_when_leg_damage_over_maxhp_frac': rx(fc, r'z\.legDmg > z\.maxHp \* ([\d.]+)')},
            'buraco': {'down_time': rx(fc, r'case CombatTerrain\.kBuraco:\s*z\.down = ([^;]+);', cast=str)},
            'latas': 'alarme sonoro, não gasta',
            'zombie_cooldown_s': rx(fc, r'void _springTrap\(CZombie z, int i\) \{\s*z\.trapCd = (\d+);', cast=int),
        },
        'night_siege': {
            'trap_catches': '1 zumbi a cada 3 atacantes por armadilha (até os usos dela)',
            'warned_damage_mult': {
                'latas': rx(fsc, r'\(alarm \? ([\d.]+) : 1\.0\)'),
                'torre': rx(fsc, r'\(tower \? ([\d.]+) : 1\.0\)'),
                'holofote': rx(fsc, r'\(light \? ([\d.]+) : 1\.0\)'),
            },
            'holofote_extra_attackers': rx(fsc, r'if \(light\) attackers \+= (\d+);', cast=int),
            'damage_per_attacker': rx(fsc, r'var dmg = \((\d+ \+ _rng\.nextDouble\(\) \* \d+)\) \* warned;', cast=str),
            'defended_mult': rx(fsc, r'if \(defended\) dmg \*= ([\d.]+);'),
            'opening_target_chance': rx(fsc, r'ops\.isNotEmpty && _rng\.nextDouble\(\) < ([\d.]+)\)'),
            'attackers': rx(fsc, r'var attackers = horde > 0 \? horde : ([^;]+);', cast=str),
        },
        'trap_rearm_xp': rx(fsc, r"f\.uses = full;\s*_xp\('carpintaria', (\d+)\)", cast=int),
        'dismantleable_furniture': list(fsc.const('dismantleable')),
        'tear_tools': fsc.const('_tearTools'),
    }


# ---------------------------------------------------------------------------
# body / needs / mind
# ---------------------------------------------------------------------------

def build_body(F, tr, ctx):
    fb, fn, fm, fsc, fc = (F['body.dart'], F['needs.dart'], F['mind.dart'], F['session_controller.dart'],
                           F['combat.dart'])
    labels = fb.const('woundLabel')
    heal = fb.switch_after(r'Duration get healTime =>')['cases']
    canbleed = fb.switch_after(r'bool get canBleed =>')['cases']
    bleed = fb.switch_after(r'double get bleedSecondsPerHp \{')['cases']
    pain = fb.switch_after(r'double get pain \{')['cases']
    corte_bandaged = rx(fb, r'if \(type == WoundType\.corte && bandaged && !sutured\) return (\d+);', cast=float)
    needs_body, _ = fb.body_of(r'List<Treat> get needs')
    blocks = {}
    for m in re.finditer(r'(case WoundType\.(\w+):|default:)(.*?)(?=case WoundType|default:|\Z)', needs_body, re.S):
        key = m.group(2) or '_default'
        steps = [{'treat': t, 'when': c} for c, t in re.findall(r'if \((.*?)\) out\.add\(Treat\.(\w+)\)', m.group(3))]
        blocks[key] = steps
    roll = rx(fb, r'final type = t < ([\d.]+)\s*\? WoundType\.arranhao\s*: t < ([\d.]+)\s*\? \(rng\.nextDouble\(\) < ([\d.]+) \? WoundType\.hemorragia : WoundType\.laceracao\)', group=None)
    a_, b_, h_ = float(roll.group(1)), float(roll.group(2)), float(roll.group(3))
    heal_body, _ = fb.body_of(r'void heal\(DateTime now')
    common_inf = [{'when': c, 'chance_per_hour': float(v)} for c, v in re.findall(r'if \((.*?)\) p \+= ([\d.]+);', heal_body)]
    burn_inf = float(re.search(r'pow\(1 - ([\d.]+), hours\)\) \{\s*w\.infected = true;\s*w\.infectedAt = now;\s*\}\s*\}\s*if \(w\.treated\)', heal_body).group(1))
    wounds = []
    ch = F['character.dart']
    bite = rx(ch, r"return has\('imunidade_forte'\)\s*\? ([\d.]+)\s*: has\('imunidade_fraca'\)\s*\? ([\d.]+)\s*: ([\d.]+);", group=None)
    lac = rx(ch, r"return has\('imunidade_fraca'\) \? ([\d.]+) : 0;")
    for wt in fb.enum_values('WoundType'):
        d = {'id': wt, 'label': labels[wt]}
        tr.add(d, 'label')
        d['heal_time'] = heal[wt]
        d['heal_days'] = heal[wt]['total_seconds'] / 86400
        d['can_bleed'] = canbleed.get(wt, canbleed.get('_default'))
        d['bleed_seconds_per_hp'] = bleed.get(wt, bleed.get('_default'))
        if wt == 'corte':
            d['bleed_seconds_per_hp_bandaged_unsutured'] = corte_bandaged
        d['pain'] = pain[wt]
        steps = []
        for st in blocks.get(wt, blocks['_default']):
            cond = st['when']
            m_ = re.match(r'type == WoundType\.(\w+) && (.*)', cond)
            if m_:
                if m_.group(1) != wt:
                    continue
                cond = m_.group(2)
            elif 'WoundType' in cond:
                raise DartParseError('body.dart: unresolved wound condition %r' % cond)
            steps.append({'treat': st['treat'], 'when': cond})
        d['treatment_steps'] = steps
        d['zombie_infection_chance'] = ({'default': float(bite.group(3)), 'imunidade_forte': float(bite.group(1)),
                                          'imunidade_fraca': float(bite.group(2))} if wt == 'mordida' else
                                         {'default': 0, 'imunidade_fraca': lac} if wt == 'laceracao' else None)
        d['hit_roll_chance'] = round({'arranhao': a_, 'laceracao': (b_ - a_) * (1 - h_), 'hemorragia': (b_ - a_) * h_,
                                      'mordida': 1 - b_}.get(wt, 0), 6)
        wounds.append(d)
    treats = []
    ti, ts, tx, tl = fb.const('treatItems'), fb.const('treatSeconds'), fb.const('treatXp'), fb.const('treatLabel')
    tools = fb.const('treatTools')
    lvl_cut = rx(fsc, r'treatSeconds\[[^\]]+\]!? \* \(1 - ([\d.]+) \* ', cast=float, flags=re.S) if re.search(r'treatSeconds\[[^\]]+\]!? \* \(1 - ([\d.]+) \* ', fsc.code) else None
    if lvl_cut is None:
        m = re.search(r'Segundos de cada passo \(nivel 0; cada nivel de primeiros socorros tira (\d+)%\)', fb.src)
        if not m:
            raise DartParseError('body.dart: treatSeconds level reduction not found')
        lvl_cut = int(m.group(1)) / 100
    for t in fb.enum_values('Treat'):
        d = {'id': t, 'label': tl[t], 'items': ti[t], 'tools_not_consumed': [i for i in ti[t] if i in tools],
             'seconds': ts[t], 'xp': tx[t], 'skill': 'primeiros_socorros'}
        tr.add(d, 'label')
        d['item_names'] = [ctx['items'][i]['name'] for i in ti[t]]
        treats.append(d)
    phases = [{'phase': p, 'from_day': int(dd)} for dd, p in
              re.findall(r'if \(days >= (\d+)\) return InfectionPhase\.(\w+);', fb.code)]
    rx(fb, r'return InfectionPhase\.incubando;', group=None)
    phases = [{'phase': 'incubando', 'from_day': 0}] + sorted(phases, key=lambda x: x['from_day'])
    phase_doc = {m.group(1): m.group(2).strip() for m in re.finditer(
        r'return InfectionPhase\.(\w+); // (.*)', fb.src)}
    for ph in phases:
        ph['effect'] = phase_doc.get(ph['phase'], '')
    body_statics = fb.static_consts('Body')
    pk = rx(fb, r'painkillerUntil!\)\) p \*= ([\d.]+);')
    painlv = rx(fb, r'return p >= (\d+) \? 3 : \(p >= (\d+) \? 2 : \(p >= (\d+) \? 1 : 0\)\);', group=None)

    # moodles
    moodle_body = src_snippet(fsc, r'List<Moodle> get moodles')
    moodles = []
    for m in re.finditer(r"add\('(\w+)', \[([^\]]*)\]\[", moodle_body):
        labels_ = re.findall(r"'([^']*)'", m.group(2))
        moodles.append({'id': m.group(1), 'labels': labels_})
    for m in re.finditer(r"add\('(\w+)', '([^']*)'", moodle_body):
        moodles.append({'id': m.group(1), 'labels': [m.group(2)]})
    for m in re.finditer(r"add\('(\w+)', (\w+)\.\w+ \? '([^']*)' : '([^']*)'", moodle_body):
        moodles.append({'id': m.group(1), 'labels': [m.group(3), m.group(4)]})
    if re.search(r"add\('panico', panicLabels", moodle_body):
        moodles.append({'id': 'panico', 'labels': fc.const('panicLabels')})
    seen = {}
    for mo in moodles:
        if mo['id'] in seen:
            seen[mo['id']]['labels'] += [x for x in mo['labels'] if x not in seen[mo['id']]['labels']]
        else:
            seen[mo['id']] = mo
    moodles = list(seen.values())
    order = re.findall(r"add\('(\w+)'", moodle_body)
    moodles.sort(key=lambda m: order.index(m['id']))
    for mo in moodles:
        mo['labels_en'] = [tr.en.get(x) for x in mo['labels']]
        mo['labels_es'] = [tr.es.get(x) for x in mo['labels']]

    nl = rx(fn, r'static int level\(double frac\) => frac < damageLevel\s*\? 3\s*: frac < ([\d.]+)\s*\? 2\s*: frac < ([\d.]+)\s*\? 1', group=None)
    fat = rx(fn, r'fatigue >= (\d+)\s*\? 3\s*: fatigue >= (\d+)\s*\? 2\s*: fatigue >= (\d+)\s*\? 1', group=None)
    mind_cuts = {m.group(1): [num(x) for x in m.group(2).split(', ')]
                 for m in rx(fm, r'int get (\w+)Level => lvl\(\w+, const \[([\d, .]+)\]\);', all_=True)}
    pl = rx(fc, r'int panicLevel\(double p\) => p >= (\d+)\s*\? 4\s*: p >= (\d+)\s*\? 3\s*: p >= (\d+)\s*\? 2\s*: p >= (\d+)\s*\? 1', group=None)
    damage_level = [s for s in fn.static_consts('Needs') if s['name'] == 'damageLevel'][0]['value']
    thresholds = {
        'fome': {'unit': 'fração do estoque de kcal', 'level_1_below': float(nl.group(2)),
                 'level_2_below': float(nl.group(1)), 'level_3_below': damage_level},
        'sede': {'unit': 'fração da água', 'level_1_below': float(nl.group(2)),
                 'level_2_below': float(nl.group(1)), 'level_3_below': damage_level},
        'cansaco': {'unit': 'fadiga 0..100', 'level_1_from': int(fat.group(3)), 'level_2_from': int(fat.group(2)),
                    'level_3_from': int(fat.group(1))},
        'dor': {'unit': 'dor 0..100', 'level_1_from': int(painlv.group(3)), 'level_2_from': int(painlv.group(2)),
                'level_3_from': int(painlv.group(1))},
        'panico': {'unit': 'pânico 0..100', 'level_1_from': int(pl.group(4)), 'level_2_from': int(pl.group(3)),
                   'level_3_from': int(pl.group(2)), 'level_4_from': int(pl.group(1)),
                   'note': 'moodle mostra até nível 3'},
        'sangrando': {'unit': 'número de feridas sangrando', 'level': 'min(3, n)'},
    }
    for k, cuts in mind_cuts.items():
        key = {'stress': 'estresse', 'unhappy': 'tristeza', 'bored': 'tedio'}[k]
        thresholds[key] = {'unit': '0..100', 'level_1_from': cuts[0], 'level_2_from': cuts[1], 'level_3_from': cuts[2]}
    cold = rx(fsc, r'final need = f < (\d+) \? 2 : \(f < (\d+) \? 1 : 0\);', group=None)
    thresholds['frio'] = {'unit': 'sensação térmica °C (chuva sem capa -4, noite -2)',
                          'need_level_1_below': int(cold.group(2)), 'need_level_2_below': int(cold.group(1)),
                          'level': 'max(0, need - calor das roupas)', 'warmth_items': fsc.const('_warmth')}
    heat = rx(fsc, r'if \(t > (\d+)\) return max\(0, \(load > 0 \? 2 : 1\) - shade\);\s*if \(t > (\d+)\)', group=None)
    thresholds['calor'] = {'unit': 'temperatura °C (de dia)', 'hot_above': int(heat.group(2)),
                           'very_hot_above': int(heat.group(1)), 'heavy_items': fsc.const('_heavy'),
                           'bone_reduces': 1}
    for mo in moodles:
        mo['thresholds'] = thresholds.get(mo['id'])

    mind_getters = {}
    for name in ('panicMult', 'xpMult', 'regenMult', 'damageMult', 'spread', 'lootMult', 'tick', 'offline'):
        mind_getters[name] = src_snippet(fm, r'(?:double|void)(?: get)? %s\b' % name)

    return {
        'body_parts': fb.const('bodyParts'),
        'body_part_labels': fb.const('bodyPartLabel'),
        'hit_location_weights': fb.const('_partWeights'),
        'wounds': wounds,
        'hit_roll': {'arranhao_below': a_, 'laceracao_below': b_, 'hemorragia_share_of_laceracao': h_,
                     'mordida': 'resto', 'armor': 'chance da roupa bloquear = proteção da parte para o ataque'},
        'treatments': treats,
        'treatment_seconds_cut_per_level': lvl_cut,
        'zombie_infection': {
            'phases': phases,
            'lethal': [s for s in body_statics if s['name'] == 'infectionLethal'][0]['value'],
            'cure': 'nenhuma',
        },
        'common_infection': {
            'per_hour_chances': common_inf,
            'burn_without_ointment_per_hour': burn_inf,
            'cure': 'antibiotico',
            'hp_drain_after_hours': rx(fb, r"t\.difference\(ia\) > const Duration\(hours: (\d+)\)\) d \+= seconds / (\d+);", group=1, cast=int),
            'hp_drain_seconds_per_hp': rx(fb, r"t\.difference\(ia\) > const Duration\(hours: (\d+)\)\) d \+= seconds / (\d+);", group=2, cast=int),
        },
        'tourniquet': {
            'max': [s for s in body_statics if s['name'] == 'tourniquetMax'][0]['value'],
            'seconds_per_hp_after_max': rx(fb, r'> tourniquetMax\) d \+= seconds / (\d+);', cast=int),
        },
        'dressing_dirty_after_hours': {'normal': rx(fb, r'Duration\(hours: tape \? (\d+) : (\d+)\)', group=2, cast=int),
                                       'with_esparadrapo': rx(fb, r'Duration\(hours: tape \? (\d+) : (\d+)\)', group=1, cast=int)},
        'pain': {'painkiller_factor': pk, 'morphine': 'zera', 'levels_from': [int(painlv.group(3)), int(painlv.group(2)), int(painlv.group(1))]},
        'body_constants': body_statics,
        'moodles': moodles,
        'needs': {
            'constants': fn.static_consts('Needs'),
            'starvation_seconds_per_hp': {
                'hunger': rx(fn, r'if \(hungerFrac < damageLevel\) d \+= seconds / (\d+);', cast=int),
                'thirst': rx(fn, r'if \(thirstFrac < damageLevel\) d \+= seconds / (\d+);', cast=int),
            },
            'fatigue_per_km': {'walking': rx(fn, r'\(running \? ([\d.]+) : ([\d.]+)\) \* km', group=2),
                               'running': rx(fn, r'\(running \? ([\d.]+) : ([\d.]+)\) \* km', group=1)},
            'running_km_mult': rx(fn, r'meters / 1000 \* \(running \? ([\d.]+) : 1\.0\)'),
            'default_rest_rate_per_hour': rx(fn, r'double restRate = ([\d.]+)'),
            'rest_while_still_per_minute': rx(fn, r'fatigue - ([\d.]+) \* seconds / 60'),
            'offline_floor': 'fora da sessão a fome/sede param em damageLevel + 1% (ninguém morre offline)',
        },
        'mind': {
            'doc': doc_above(fm, fm.code.index('class Mind')),
            'levels': mind_cuts,
            'formulas': mind_getters,
        },
    }


# ---------------------------------------------------------------------------
# rules
# ---------------------------------------------------------------------------

def build_rules(F):
    fr = F['rules.dart']
    m = re.search(r'class Rules\s*\{', fr.code)
    a = m.end()
    b = fr.matching(m.end() - 1)
    consts = fr.static_consts('Rules')
    # section headers: standalone comment lines preceded by a blank line
    sections = []
    for ln in range(fr.line_of(a), fr.line_of(b) + 1):
        s = fr.lines[ln - 1].strip()
        if s.startswith('//') and not s.startswith('///') and fr.lines[ln - 2].strip() == '' or \
                (s.startswith('//') and not s.startswith('///') and fr.lines[ln - 2].strip().endswith('{')):
            sections.append((ln, s.lstrip('/').strip()))
    for c in consts:
        sec = [t for ln, t in sections if ln <= c['line']]
        c['section'] = sec[-1] if sec else ''
        c['comment'] = trailing_comment(fr.lines[c['line'] - 1])
        above = []
        k = c['line'] - 2
        while k >= 0 and fr.lines[k].strip().startswith('//'):
            above.insert(0, fr.lines[k].strip().lstrip('/').strip())
            k -= 1
        c['comment_above'] = ' '.join(above)
    funcs = []
    for m in re.finditer(r'\n  static (double|int|bool) (\w+)\(([^)]*)\)', fr.code[a:b]):
        funcs.append({'name': m.group(2), 'returns': m.group(1), 'params': m.group(3),
                      'doc': doc_above(fr, a + m.start() + 1),
                      'source': src_snippet(fr, r'static %s %s\(' % (m.group(1), m.group(2)))})
    return {'doc': doc_above(fr, fr.code.index('class Rules')), 'constants': consts, 'functions': funcs}


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def spot_check(F, items_data, recipes_data, chars):
    import random
    rnd = random.Random(7)
    fi, fc, fch = F['items.dart'], F['crafting.dart'], F['character.dart']
    print('\n=== spot-check: 5 items ===')
    items = items_data['items']
    picks = [i for i in items if i['id'] in ('pistola', 'escopeta', 'jaqueta', 'arroz_cozido', 'mochila_tatica')]
    for it in picks:
        ln = it['source_line']
        print('-- %s (items.dart:%d)' % (it['id'], ln))
        print('   SRC :', ' '.join(item_src(fi, it['id']).split()))
        show = {k: it[k] for k in ('name', 'kind', 'rarity', 'weight', 'kcal', 'ml', 'armor', 'pockets', 'bagKg',
                                    'shelfLife_days', 'note') if k in it}
        if it['weapon']:
            show['weapon'] = it['weapon']
        print('   JSON:', json.dumps(show, ensure_ascii=False))
        _check_item_against_source(fi, it)
    print('\n=== spot-check: 3 recipes ===')
    for rid in ('R10', 'E02', 'C05'):
        r = next(x for x in recipes_data['recipes'] if x['id'] == rid)
        m = re.search(r"Recipe\('%s'.*?\)\s*,\s*\n" % rid, fc.src, re.S)
        print('-- %s' % rid)
        print('   SRC :', ' '.join(m.group(0).split()))
        print('   JSON:', json.dumps({k: r[k] for k in ('name', 'output', 'qty', 'inputs', 'tools', 'station', 'skill',
                                                      'minLevel', 'xp', 'kind')}, ensure_ascii=False))
        for k, v in r['inputs'].items():
            if not re.search(r"'%s': %d\b" % (k, v), m.group(0)):
                raise AssertionError('recipe %s input %s:%d not in source' % (rid, k, v))
    print('\n=== spot-check: 3 traits ===')
    for tid in ('forte', 'sortudo', 'covarde'):
        t = next(x for x in chars['traits'] if x['id'] == tid)
        m = re.search(r"Trait\('%s'.*?\),\n" % tid, fch.src)
        print('-- %s' % tid)
        print('   SRC :', m.group(0).strip())
        print('   JSON:', json.dumps({k: t[k] for k in ('name', 'cost', 'effect', 'conflicts', 'effects')}, ensure_ascii=False))
        if "'%s', %d," % (t['name'], t['cost']) not in m.group(0):
            raise AssertionError('trait %s mismatch' % tid)


def item_src(fi, iid):
    """Original source text of one entry of the items map."""
    a = fi.src.index("'%s': ItemDef(" % iid)
    nxt = re.search(r"'\w+': ItemDef\(|\n\};", fi.src[a + 10:])
    return fi.src[a:a + 10 + nxt.start()].rstrip()


def _check_item_against_source(fi, it):
    """Cross-check numbers found in the item's source text with the JSON."""
    seg = item_src(fi, it['id'])
    for k in ('weight', 'kcal', 'ml', 'heal', 'pockets', 'bagKg'):
        m = re.search(r'\b%s: ([\d.]+)' % k, seg)
        if m and float(m.group(1)) != float(it[k]):
            raise AssertionError('%s.%s: source %s json %s' % (it['id'], k, m.group(1), it[k]))
    if it['weapon']:
        for k, v in it['weapon'].items():
            m = re.search(r'\b%s: ([\d.]+)' % k, seg)
            if m and float(m.group(1)) != float(v):
                raise AssertionError('%s.weapon.%s: source %s json %s' % (it['id'], k, m.group(1), v))
    print('   OK  : numbers match source')


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='/mnt/user-data/outputs/footfall')
    ap.add_argument('--out', default=os.path.join(HERE, 'data'))
    args = ap.parse_args()
    lib = os.path.join(args.src, 'lib/game')
    os.makedirs(args.out, exist_ok=True)

    reg = Registry()
    F = {}
    for fn in ('items.dart', 'armor.dart', 'appearance.dart', 'crafting.dart', 'loot.dart', 'poi.dart',
               'interior.dart', 'bunker_floors.dart', 'character.dart', 'zclass.dart', 'models.dart', 'base.dart',
               'body.dart', 'needs.dart', 'mind.dart', 'rules.dart', 'prices.dart', 'combat.dart',
               'session_controller.dart'):
        F[fn] = DartFile(os.path.join(lib, fn), reg)
    tr = I18n(args.src)
    ctx = {'item_ids': set(), 'lib_root': os.path.join(args.src, 'lib')}

    items_data = build_items(F, tr, ctx)
    recipes_data = build_recipes(F, tr, ctx)
    loot_data = build_loot(F, tr, ctx)
    chars = build_characters(F, tr, ctx, lib)
    zombies = build_zombies(F, tr, ctx)
    base = build_base(F, tr, ctx)
    body = build_body(F, tr, ctx)
    rules = build_rules(F)
    where = build_items_where(ctx, loot_data, zombies, recipes_data, items_data)

    meta = {'source': args.src, 'generator': 'extract.py'}
    outputs = [
        ('items.json', dict(items_data, _meta=meta), len(items_data['items'])),
        ('recipes.json', dict(recipes_data, _meta=meta), len(recipes_data['recipes'])),
        ('loot.json', dict(loot_data, _meta=meta), len(loot_data['categories'])),
        ('items_where.json', where, len(where)),
        ('characters.json', dict(chars, _meta=meta), None),
        ('zombies.json', dict(zombies, _meta=meta), len(zombies['classes'])),
        ('base.json', dict(base, _meta=meta), len(base['furniture'])),
        ('body.json', dict(body, _meta=meta), len(body['wounds'])),
        ('rules.json', dict(rules, _meta=meta), len(rules['constants'])),
    ]
    summary = {
        'items.json': lambda: '%d items, starter kit %d entries, %d skins' % (
            len(items_data['items']), len(items_data['starter_kit']), len(items_data['skins']['styles'])),
        'recipes.json': lambda: '%d recipes' % len(recipes_data['recipes']),
        'loot.json': lambda: '%d place categories, %d furniture kinds' % (
            len(loot_data['categories']), len(loot_data['furniture_kinds'])),
        'items_where.json': lambda: '%d items (%d with no known source)' % (
            len(where), sum(1 for w in where.values() if not w['obtainable'])),
        'characters.json': lambda: '%d professions, %d traits, %d skills' % (
            len(chars['professions']), len(chars['traits']), len(chars['skills'])),
        'zombies.json': lambda: '%d classes, %d map states' % (len(zombies['classes']), len(zombies['map_states'])),
        'base.json': lambda: '%d furniture pieces, %d wall tiers, %d openings' % (
            len(base['furniture']), len(base['walls']), len(base['openings'])),
        'body.json': lambda: '%d wound types, %d treatments, %d moodles, %d hit locations' % (
            len(body['wounds']), len(body['treatments']), len(body['moodles']), len(body['hit_location_weights'])),
        'rules.json': lambda: '%d constants, %d functions' % (len(rules['constants']), len(rules['functions'])),
    }
    print('=== written ===')
    for name, data, _n in outputs:
        p = write(args.out, name, data)
        print('%-18s %8d bytes  %s' % (name, os.path.getsize(p), summary[name]()))
    print('i18n: %d strings translated, %d without translation' % (tr.hits, tr.miss))
    skipped_path = os.path.join(args.out, '_skipped.txt')
    if SKIPPED:
        with open(skipped_path, 'w', encoding='utf-8') as fh:
            for what, why in SKIPPED:
                fh.write('%s\t%s\n' % (what, why))
        print('SKIPPED %d entries -> %s' % (len(SKIPPED), skipped_path))
    elif os.path.exists(skipped_path):
        os.remove(skipped_path)
    spot_check(F, items_data, recipes_data, chars)


if __name__ == '__main__':
    try:
        main()
    except DartParseError as e:
        print('PARSE ERROR: %s' % e, file=sys.stderr)
        sys.exit(2)
