"""Gera a wiki do Footfall em <site>/wiki (pt), <site>/wiki/en e <site>/wiki/es
a partir de data/*.json e paginas*/*.html.
Uso: python3 build_wiki.py <pasta do site> [<pasta do jogo>]"""
import html, json, os, re, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1]
GAME = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/footfall'
ROOT = os.path.join(SITE, 'wiki')
LANGS = ['pt', 'en', 'es']
D = lambda n: json.load(open(os.path.join(HERE, 'data', n + '.json')))
ITEMS, WHERE, LOOT, RECIPES, ZOMB, BASE, BODY, CHARS = (D('items'), D('items_where'), D('loot'), D('recipes'),
                                                       D('zombies'), D('base'), D('body'), D('characters'))
IT = {i['id']: i for i in ITEMS['items']}
CATS = LOOT['categories']
for _z in ZOMB['classes']:
    _z['id'] = _z['id'] or _z['name']
ZC = {z['id']: z for z in ZOMB['classes']}
GAME_TR = {L: json.load(open(os.path.join(GAME, 'assets', 'i18n', L + '.json'))) for L in ('en', 'es')}
# Traduções do jogo que ficaram erradas (o jogo também precisa corrigir): o posto de gasolina
# virou "Outpost/Puesto" (confunde com o posto avançado) e o móvel "Depósito" virou "Vault".
CATS['posto']['label_en'], CATS['posto']['label_es'] = 'Gas station', 'Gasolinera'
GAME_TR['en']['Depósito'] = 'Storeroom'
GAME_TR['en']['Estante'] = 'Bookcase'
e = html.escape
LANG = 'pt'

# --- textos do gerador, por idioma (pt é a chave) ------------------------------------------------
TR = {
 'en': {
  'Armas': 'Weapons', 'Médico': 'Medical', 'Comida e bebida': 'Food and drink', 'Materiais': 'Materials', 'Ferramentas': 'Tools',
  'Roupas e equipamento': 'Clothing and gear', 'Arma': 'Weapon', 'Comida/bebida': 'Food/drink', 'Material': 'Material',
  'Ferramenta': 'Tool', 'Roupa/equipamento': 'Clothing/gear', 'Comum': 'Common', 'Incomum': 'Uncommon', 'Raro': 'Rare',
  'Lendário': 'Legendary', 'Cabeça': 'Head', 'Tronco': 'Torso', 'Braços': 'Arms', 'Mãos': 'Hands', 'Pernas': 'Legs', 'Pés': 'Feet',
  'Mordida': 'Bite', 'Arranhão': 'Scratch', 'Golpe': 'Hit', 'Tiro': 'Shot',
  'Índices': 'Indexes', 'Todos os itens': 'All items', 'Lugares': 'Places', 'Tipos de zumbi': 'Zombie types', 'As memórias': 'The memories',
  'Wiki do Footfall': 'Footfall Wiki', 'Buscar na wiki': 'Search the wiki', 'Seções': 'Sections', 'Seções da wiki': 'Wiki sections',
  'Site': 'Site', 'Guias': 'Guides', 'Política de privacidade': 'Privacy policy', 'Rodapé': 'Footer',
  'Wiki gerada a partir do código do jogo. Valores podem mudar entre versões.': 'Wiki generated from the game code. Values may change between versions.',
  ' (móvel)': ' (furniture)', 'Fogo': 'Fire', 'Bancada': 'Workbench', 'Tipo': 'Type', 'Raridade': 'Rarity', 'Peso': 'Weight',
  'Onde vai': 'Slot', 'Preço de referência': 'Reference price', 'selos': 'stamps', 'Dano por tiro': 'Damage per shot', 'chumbos': 'pellets',
  'Alcance': 'Range', 'Pente': 'Magazine', 'Recarga': 'Reload', 'Intervalo entre tiros': 'Time between shots', 'Rajada': 'Burst',
  'tiros': 'shots', 'Munição': 'Ammo', 'Barulho no mapa': 'Noise on the map', 'raio de tiro (150 m)': 'gunshot radius (150 m)',
  'Dano': 'Damage', 'Intervalo': 'Swing time', 'Arco do golpe': 'Swing arc', 'Alvos por golpe': 'Targets per swing',
  'Durabilidade': 'Durability', 'não gasta': 'does not wear', 'Dano por segundo (teórico)': 'Damage per second (theoretical)',
  'Atributo': 'Attribute', 'Valor': 'Value', 'Calorias': 'Calories', 'Água': 'Water', 'Validade': 'Shelf life', 'dias': 'days',
  'não estraga': 'does not spoil', 'Alimento': 'Food', 'Cura': 'Heals', 'de vida': 'health', 'Serve para enfaixar': 'Works as a dressing',
  'sim': 'yes', 'Usado em': 'Used in', 'Veja': 'See', 'Tratamento': 'Treatment', 'Feridas': 'Wounds', 'e': 'and', 'Bolsos': 'Pockets',
  'Capacidade': 'Capacity', 'Calor': 'Warmth', 'Roupa pesada (calor)': 'Heavy clothing (heat)', 'Desgaste por mordida': 'Wear per bite',
  'Equipamento': 'Gear', 'Mochila e peso': 'Backpack and weight', 'Costura e roupas': 'Sewing and clothing', 'Parte': 'Part', 'rasgada': 'ripped',
  'Proteção': 'Protection', 'Chance de a roupa segurar cada tipo de ataque na parte que cobre.': 'Chance the clothing stops each kind of attack on the part it covers.',
  'Lugar': 'Place', 'Chance na raridade': 'Chance within rarity', 'Móveis': 'Furniture',
  'Chance mostrada: a parte que este item ocupa entre os itens da mesma raridade naquele tipo de lugar.': 'Chance shown: this item\'s share among items of the same rarity in that kind of place.',
  'Em zumbis': 'On zombies', 'Zumbi': 'Zombie', 'Chance': 'Chance', 'Máx.': 'Max.',
  'corpos de zumbi (bolsos)': 'zombie corpses (pockets)', 'mochila de zumbi mochileiro': 'backpacker zombie\'s backpack',
  'móveis especiais de alguns cômodos': 'special furniture in some rooms', 'receita': 'recipe', 'kit inicial': 'starter kit',
  'achado raríssimo ao entrar nos lugares': 'very rare find when going inside places', 'caixa de resgate / sinalizador': 'rescue box / flare',
  'conjunto de roupa raro': 'rare outfit set', 'Também': 'Also', 'Fabricado por receita (veja abaixo).': 'Made by a recipe (see below).',
  'Onde achar': 'Where to find', 'Memórias': 'Memories', 'Como fazer': 'How to make', 'Usado como ingrediente': 'Used as an ingredient',
  'Usado como ferramenta': 'Used as a tool', 'Receita': 'Recipe', 'Ingredientes': 'Ingredients', 'Onde': 'Where', 'Habilidade': 'Skill',
  'Resultado': 'Result', 'Receitas': 'Recipes', 'Código': 'Code',
  'Todos os itens do jogo, com os valores do código. Toque no nome para ver a ficha completa.': 'Every item in the game, with the values from the code. Tap a name to see its full page.',
  'Filtrar itens': 'Filter items', 'Item': 'Item', 'kcal': 'kcal', 'ml': 'ml', 'Validade (dias)': 'Shelf life (days)', 'Lugar no corpo': 'Body slot',
  'Carga': 'Carry', 'mochila': 'backpack', 'Nota': 'Note', 'fogo': 'firearm', 'arco': 'bow', 'branca': 'melee',
  'Lugares de verdade do mapa (OpenStreetMap) que o jogo trata como': 'Real places on the map (OpenStreetMap) that the game treats as',
  'Veja também': 'See also', 'Saque': 'Looting', 'Guardas no máximo (pontos dominados)': 'Max guards (strongholds)', 'Zumbis dentro': 'Zombies inside',
  'a': 'to', 'Tamanho típico': 'Typical size', 'Pela porta': 'From the door', 'Móveis da entrada, rápidos e sem itens raros.': 'Furniture by the entrance: quick, and no rare items.',
  'Móvel': 'Furniture', 'Tempo': 'Time', 'Barulho': 'Noise', 'trancado': 'locked', 'Entrando': 'Going inside',
  'Cômodos e móveis que dá para vasculhar dentro do prédio. Dentro, os raros têm mais chance.': 'Rooms and furniture you can search inside the building. Inside, rare items are more likely.',
  'Cômodo': 'Room', 'O que sai daqui': 'What you find here',
  'Cada item sorteado primeiro tira a raridade e depois um item daquela raridade; a coluna mostra a parte do item dentro da raridade.': 'Each roll first picks a rarity and then an item of that rarity; the column shows the item\'s share within its rarity.',
  'Zumbis especiais por perto': 'Special zombies nearby', 'Zumbis': 'Zombies', 'Memória': 'Memory',
  'Um livro de memória pode aparecer nos móveis de dentro: veja': 'A memory book can turn up in the furniture inside: see', 'a memória': 'the memory',
  'Cada lugar do mapa cai numa categoria, e a categoria decide os móveis, o saque e os zumbis.': 'Every place on the map falls into a category, and the category decides the furniture, the loot and the zombies.',
  'Categoria': 'Category', 'Guardas (máx.)': 'Guards (max.)', 'Itens possíveis': 'Possible items',
  'Multiplicadores sobre o zumbi comum. Cabeça e tronco: quanto do dano entra naquela parte (menor = mais protegido).': 'Multipliers over the common zombie. Head and torso: how much damage gets through on that part (lower = better protected).',
  'Vida': 'Health', 'Velocidade': 'Speed', 'Dano na cabeça': 'Head damage', 'Dano no tronco': 'Torso damage', 'Não pega fogo': 'Fireproof',
  'As histórias jogáveis da estante do depósito do rádio. Sem spoilers: só onde achar, desafio e recompensa.': 'The playable stories on the radio vault shelf. No spoilers: only where to find them, the challenge and the reward.',
  'itens': 'items', 'tipos de lugar': 'place types', 'tipos de zumbi': 'zombie types', 'receitas': 'recipes', 'traços': 'traits',
  'A enciclopédia do Footfall: cada mecânica, item, lugar e zumbi, com os números tirados direto do código do jogo.': 'The Footfall encyclopedia: every mechanic, item, place and zombie, with the numbers taken straight from the game code.',
  'Começando agora? Leia os': 'Just starting? Read the', 'guias': 'guides', 'primeiro.': 'first.', 'Lugar ': 'Place', 'Itens': 'Items',
  'Buscar': 'Search', 'Os tipos de lugar do mapa.': 'The kinds of place on the map.', 'Todos os tipos de zumbi e os multiplicadores.': 'Every zombie type and its multipliers.',
  'As histórias jogáveis.': 'The playable stories.', 'itens do jogo.': 'items in the game.', 'Os': 'The', 'Combate': 'Combat',
  'Idioma': 'Language',
 },
 'es': {
  'Armas': 'Armas', 'Médico': 'Médico', 'Comida e bebida': 'Comida y bebida', 'Materiais': 'Materiales', 'Ferramentas': 'Herramientas',
  'Roupas e equipamento': 'Ropa y equipo', 'Arma': 'Arma', 'Comida/bebida': 'Comida/bebida', 'Material': 'Material',
  'Ferramenta': 'Herramienta', 'Roupa/equipamento': 'Ropa/equipo', 'Comum': 'Común', 'Incomum': 'Poco común', 'Raro': 'Raro',
  'Lendário': 'Legendario', 'Cabeça': 'Cabeza', 'Tronco': 'Torso', 'Braços': 'Brazos', 'Mãos': 'Manos', 'Pernas': 'Piernas', 'Pés': 'Pies',
  'Mordida': 'Mordida', 'Arranhão': 'Arañazo', 'Golpe': 'Golpe', 'Tiro': 'Disparo',
  'Índices': 'Índices', 'Todos os itens': 'Todos los objetos', 'Lugares': 'Lugares', 'Tipos de zumbi': 'Tipos de zombi', 'As memórias': 'Las memorias',
  'Wiki do Footfall': 'Wiki de Footfall', 'Buscar na wiki': 'Buscar en la wiki', 'Seções': 'Secciones', 'Seções da wiki': 'Secciones de la wiki',
  'Site': 'Sitio', 'Guias': 'Guías', 'Política de privacidade': 'Política de privacidad', 'Rodapé': 'Pie de página',
  'Wiki gerada a partir do código do jogo. Valores podem mudar entre versões.': 'Wiki generada a partir del código del juego. Los valores pueden cambiar entre versiones.',
  ' (móvel)': ' (mueble)', 'Fogo': 'Fuego', 'Bancada': 'Banco de trabajo', 'Tipo': 'Tipo', 'Raridade': 'Rareza', 'Peso': 'Peso',
  'Onde vai': 'Ranura', 'Preço de referência': 'Precio de referencia', 'selos': 'sellos', 'Dano por tiro': 'Daño por disparo', 'chumbos': 'perdigones',
  'Alcance': 'Alcance', 'Pente': 'Cargador', 'Recarga': 'Recarga', 'Intervalo entre tiros': 'Tiempo entre disparos', 'Rajada': 'Ráfaga',
  'tiros': 'disparos', 'Munição': 'Munición', 'Barulho no mapa': 'Ruido en el mapa', 'raio de tiro (150 m)': 'radio de disparo (150 m)',
  'Dano': 'Daño', 'Intervalo': 'Intervalo', 'Arco do golpe': 'Arco del golpe', 'Alvos por golpe': 'Objetivos por golpe',
  'Durabilidade': 'Durabilidad', 'não gasta': 'no se gasta', 'Dano por segundo (teórico)': 'Daño por segundo (teórico)',
  'Atributo': 'Atributo', 'Valor': 'Valor', 'Calorias': 'Calorías', 'Água': 'Agua', 'Validade': 'Caducidad', 'dias': 'días',
  'não estraga': 'no se echa a perder', 'Alimento': 'Alimento', 'Cura': 'Cura', 'de vida': 'de vida', 'Serve para enfaixar': 'Sirve para vendar',
  'sim': 'sí', 'Usado em': 'Se usa en', 'Veja': 'Mira', 'Tratamento': 'Tratamiento', 'Feridas': 'Heridas', 'e': 'y', 'Bolsos': 'Bolsillos',
  'Capacidade': 'Capacidad', 'Calor': 'Abrigo', 'Roupa pesada (calor)': 'Ropa pesada (calor)', 'Desgaste por mordida': 'Desgaste por mordida',
  'Equipamento': 'Equipo', 'Mochila e peso': 'Mochila y peso', 'Costura e roupas': 'Costura y ropa', 'Parte': 'Parte', 'rasgada': 'rota',
  'Proteção': 'Protección', 'Chance de a roupa segurar cada tipo de ataque na parte que cobre.': 'Probabilidad de que la ropa detenga cada tipo de ataque en la parte que cubre.',
  'Lugar': 'Lugar', 'Chance na raridade': 'Probabilidad en la rareza', 'Móveis': 'Muebles',
  'Chance mostrada: a parte que este item ocupa entre os itens da mesma raridade naquele tipo de lugar.': 'Probabilidad mostrada: la parte que ocupa este objeto entre los objetos de la misma rareza en ese tipo de lugar.',
  'Em zumbis': 'En zombis', 'Zumbi': 'Zombi', 'Chance': 'Probabilidad', 'Máx.': 'Máx.',
  'corpos de zumbi (bolsos)': 'cuerpos de zombi (bolsillos)', 'mochila de zumbi mochileiro': 'mochila del zombi mochilero',
  'móveis especiais de alguns cômodos': 'muebles especiales de algunas habitaciones', 'receita': 'receta', 'kit inicial': 'kit inicial',
  'achado raríssimo ao entrar nos lugares': 'hallazgo rarísimo al entrar en los lugares', 'caixa de resgate / sinalizador': 'caja de rescate / bengala',
  'conjunto de roupa raro': 'conjunto de ropa raro', 'Também': 'También', 'Fabricado por receita (veja abaixo).': 'Se fabrica con una receta (mira abajo).',
  'Onde achar': 'Dónde encontrarlo', 'Memórias': 'Memorias', 'Como fazer': 'Cómo hacerlo', 'Usado como ingrediente': 'Se usa como ingrediente',
  'Usado como ferramenta': 'Se usa como herramienta', 'Receita': 'Receta', 'Ingredientes': 'Ingredientes', 'Onde': 'Dónde', 'Habilidade': 'Habilidad',
  'Resultado': 'Resultado', 'Receitas': 'Recetas', 'Código': 'Código',
  'Todos os itens do jogo, com os valores do código. Toque no nome para ver a ficha completa.': 'Todos los objetos del juego, con los valores del código. Toca el nombre para ver la ficha completa.',
  'Filtrar itens': 'Filtrar objetos', 'Item': 'Objeto', 'kcal': 'kcal', 'ml': 'ml', 'Validade (dias)': 'Caducidad (días)', 'Lugar no corpo': 'Lugar en el cuerpo',
  'Carga': 'Carga', 'mochila': 'mochila', 'Nota': 'Nota', 'fogo': 'de fuego', 'arco': 'arco', 'branca': 'blanca',
  'Lugares de verdade do mapa (OpenStreetMap) que o jogo trata como': 'Lugares reales del mapa (OpenStreetMap) que el juego trata como',
  'Veja também': 'Mira también', 'Saque': 'Saqueo', 'Guardas no máximo (pontos dominados)': 'Guardias máximos (bastiones)', 'Zumbis dentro': 'Zombis dentro',
  'a': 'a', 'Tamanho típico': 'Tamaño típico', 'Pela porta': 'Desde la puerta', 'Móveis da entrada, rápidos e sem itens raros.': 'Muebles de la entrada: rápidos y sin objetos raros.',
  'Móvel': 'Mueble', 'Tempo': 'Tiempo', 'Barulho': 'Ruido', 'trancado': 'cerrado con llave', 'Entrando': 'Entrando',
  'Cômodos e móveis que dá para vasculhar dentro do prédio. Dentro, os raros têm mais chance.': 'Habitaciones y muebles que puedes registrar dentro del edificio. Dentro, los raros tienen más probabilidad.',
  'Cômodo': 'Habitación', 'O que sai daqui': 'Qué sale de aquí',
  'Cada item sorteado primeiro tira a raridade e depois um item daquela raridade; a coluna mostra a parte do item dentro da raridade.': 'Cada sorteo elige primero la rareza y luego un objeto de esa rareza; la columna muestra la parte del objeto dentro de su rareza.',
  'Zumbis especiais por perto': 'Zombis especiales cerca', 'Zumbis': 'Zombis', 'Memória': 'Memoria',
  'Um livro de memória pode aparecer nos móveis de dentro: veja': 'Un libro de memoria puede aparecer en los muebles de dentro: mira', 'a memória': 'la memoria',
  'Cada lugar do mapa cai numa categoria, e a categoria decide os móveis, o saque e os zumbis.': 'Cada lugar del mapa cae en una categoría, y la categoría decide los muebles, el botín y los zombis.',
  'Categoria': 'Categoría', 'Guardas (máx.)': 'Guardias (máx.)', 'Itens possíveis': 'Objetos posibles',
  'Multiplicadores sobre o zumbi comum. Cabeça e tronco: quanto do dano entra naquela parte (menor = mais protegido).': 'Multiplicadores sobre el zombi común. Cabeza y torso: cuánto daño entra en esa parte (menor = más protegido).',
  'Vida': 'Vida', 'Velocidade': 'Velocidad', 'Dano na cabeça': 'Daño en la cabeza', 'Dano no tronco': 'Daño en el torso', 'Não pega fogo': 'Ignífugo',
  'As histórias jogáveis da estante do depósito do rádio. Sem spoilers: só onde achar, desafio e recompensa.': 'Las historias jugables de la estantería del depósito de la radio. Sin spoilers: solo dónde encontrarlas, el desafío y la recompensa.',
  'itens': 'objetos', 'tipos de lugar': 'tipos de lugar', 'tipos de zumbi': 'tipos de zombi', 'receitas': 'recetas', 'traços': 'rasgos',
  'A enciclopédia do Footfall: cada mecânica, item, lugar e zumbi, com os números tirados direto do código do jogo.': 'La enciclopedia de Footfall: cada mecánica, objeto, lugar y zombi, con los números sacados directamente del código del juego.',
  'Começando agora? Leia os': '¿Recién empiezas? Lee primero las', 'guias': 'guías', 'primeiro.': '.', 'Lugar ': 'Lugar', 'Itens': 'Objetos',
  'Buscar': 'Buscar', 'Os tipos de lugar do mapa.': 'Los tipos de lugar del mapa.', 'Todos os tipos de zumbi e os multiplicadores.': 'Todos los tipos de zombi y sus multiplicadores.',
  'As histórias jogáveis.': 'Las historias jugables.', 'itens do jogo.': 'objetos del juego.', 'Os': 'Los', 'Combate': 'Combate',
  'Idioma': 'Idioma',
 },
}
SLOT = {'en': {'cabeca': 'head', 'tronco': 'torso', 'bracos': 'arms', 'maos': 'hands', 'pernas': 'legs', 'pes': 'feet', 'calca': 'pants',
               'cinto': 'belt', 'colete': 'vest', 'costas': 'back', 'mochila': 'backpack', 'pochete': 'waist pack', 'bolsa_braco': 'arm pouch',
               'bolsa_perna': 'thigh bag', 'couro': 'leather', 'jeans': 'denim', 'tecido': 'cloth', 'rigido': 'rigid', 'balistico': 'ballistic'},
        'es': {'cabeca': 'cabeza', 'tronco': 'torso', 'bracos': 'brazos', 'maos': 'manos', 'pernas': 'piernas', 'pes': 'pies', 'calca': 'pantalón',
               'cinto': 'cinturón', 'colete': 'chaleco', 'costas': 'espalda', 'mochila': 'mochila', 'pochete': 'riñonera', 'bolsa_braco': 'bolsa de brazo',
               'bolsa_perna': 'bolsa de muslo', 'couro': 'cuero', 'jeans': 'mezclilla', 'tecido': 'tela', 'rigido': 'rígido', 'balistico': 'balístico'},
        'pt': {'bolsa_braco': 'bolsa de braço', 'bolsa_perna': 'bolsa de coxa', 'cabeca': 'cabeça', 'bracos': 'braços', 'maos': 'mãos', 'pes': 'pés',
               'calca': 'calça', 'rigido': 'rígido', 'balistico': 'balístico'}}
ROOM = {
 'pt': {'almoxarifado': 'almoxarifado', 'arsenal': 'arsenal', 'balcao': 'balcão', 'banheiro': 'banheiro', 'camara': 'câmara fria', 'celas': 'celas',
        'consultorio': 'consultório', 'conveniencia': 'conveniência', 'cozinha': 'cozinha', 'deposito': 'depósito', 'escritorio': 'escritório',
        'estoque': 'estoque', 'garagem': 'garagem', 'loja': 'loja', 'quarto': 'quarto', 'recepcao': 'recepção', 'remedios': 'farmácia (remédios)',
        'sala': 'sala', 'sala_estar': 'sala de estar', 'salao': 'salão', 'salao_mesas': 'salão (mesas)', 'secretaria': 'secretaria', 'vestiario': 'vestiário'},
 'en': {'almoxarifado': 'storeroom', 'arsenal': 'armory', 'balcao': 'counter', 'banheiro': 'bathroom', 'camara': 'cold room', 'celas': 'cells',
        'consultorio': 'exam room', 'conveniencia': 'convenience store', 'cozinha': 'kitchen', 'deposito': 'storage', 'escritorio': 'office',
        'estoque': 'stockroom', 'garagem': 'garage', 'loja': 'shop floor', 'quarto': 'bedroom', 'recepcao': 'reception', 'remedios': 'pharmacy (medicine)',
        'sala': 'room', 'sala_estar': 'living room', 'salao': 'hall', 'salao_mesas': 'dining hall', 'secretaria': 'school office', 'vestiario': 'locker room'},
 'es': {'almoxarifado': 'almacén', 'arsenal': 'arsenal', 'balcao': 'mostrador', 'banheiro': 'baño', 'camara': 'cámara fría', 'celas': 'celdas',
        'consultorio': 'consultorio', 'conveniencia': 'tienda de conveniencia', 'cozinha': 'cocina', 'deposito': 'depósito', 'escritorio': 'oficina',
        'estoque': 'bodega', 'garagem': 'garaje', 'loja': 'tienda', 'quarto': 'dormitorio', 'recepcao': 'recepción', 'remedios': 'farmacia (medicinas)',
        'sala': 'sala', 'sala_estar': 'sala de estar', 'salao': 'salón', 'salao_mesas': 'salón (mesas)', 'secretaria': 'secretaría', 'vestiario': 'vestuario'}}
CAT_ORDER = {'pt': ['Começo', 'Personagem', 'Saúde', 'Mundo', 'Saque', 'Combate', 'Base', 'Social', 'Corvo e rádio', 'Memórias'],
             'en': ['Getting started', 'Character', 'Health', 'World', 'Looting', 'Combat', 'Base', 'Social', 'Crow and radio', 'Memories'],
             'es': ['Comienzo', 'Personaje', 'Salud', 'Mundo', 'Saqueo', 'Combate', 'Base', 'Social', 'Cuervo y radio', 'Memorias']}
HTML_LANG = {'pt': 'pt-BR', 'en': 'en', 'es': 'es'}
LANG_NAME = {'pt': 'Português', 'en': 'English', 'es': 'Español'}


def _(s):
    return s if LANG == 'pt' else TR[LANG].get(s, s)


def G(s):
    """Texto que o próprio jogo traduz (móveis, tratamentos, habilidades...)."""
    return s if LANG == 'pt' or not s else GAME_TR[LANG].get(s, s)


def F(obj, key):
    """Campo traduzido de um registro dos JSON (name/name_en, label/label_en...)."""
    if LANG != 'pt' and obj.get(f'{key}_{LANG}'):
        return obj[f'{key}_{LANG}']
    return obj.get(key) or ''


def slot(s):
    return SLOT[LANG].get(s, s)


def num(v, d=2):
    if v is None:
        return '∞'
    if isinstance(v, float):
        s = f'{v:.{d}f}'.rstrip('0').rstrip('.')
        return s if LANG == 'en' else s.replace('.', ',')
    return str(v)


def pct(v):
    return num(round(v * 100, 1), 1) + '%'


KIND = {'arma': 'Armas', 'medico': 'Médico', 'comida': 'Comida e bebida', 'material': 'Materiais',
        'ferramenta': 'Ferramentas', 'roupa': 'Roupas e equipamento'}
KIND1 = {'arma': 'Arma', 'medico': 'Médico', 'comida': 'Comida/bebida', 'material': 'Material',
         'ferramenta': 'Ferramenta', 'roupa': 'Roupa/equipamento'}
RAR = {'comum': 'Comum', 'incomum': 'Incomum', 'raro': 'Raro', 'lendario': 'Lendário'}
PART = {'cabeca': 'Cabeça', 'tronco': 'Tronco', 'bracos': 'Braços', 'maos': 'Mãos', 'pernas': 'Pernas', 'pes': 'Pés'}
ATK = {'mordida': 'Mordida', 'arranhao': 'Arranhão', 'golpe': 'Golpe', 'tiro': 'Tiro'}


def A():
    """Prefixo até a pasta de recursos da wiki (img/itens, wiki.css)."""
    return '' if LANG == 'pt' else '../'


def R():
    """Prefixo até a raiz do site."""
    return '../' if LANG == 'pt' else '../../'


def ilink(iid, icon=True):
    it = IT.get(iid)
    if not it:
        return e(iid)
    img = f'<img class="ic px" src="{A()}img/itens/{iid}.png" alt="" width="24" height="24">' if icon else ''
    return f'<a class="il" href="item-{iid}.html">{img}{e(F(it, "name"))}</a>'


def clink(cat):
    c = CATS.get(cat)
    return f'<a href="lugar-{cat}.html">{e(F(c, "label")) if c else e(cat)}</a>'


def zlabel(z):
    return F(z, 'label')


def tbl(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


# --- paginas de texto ----------------------------------------------------------------------------
def load_pages(lang):
    pages = {}
    base = os.path.join(HERE, 'paginas')
    loc = os.path.join(HERE, 'paginas' if lang == 'pt' else f'paginas_{lang}')
    for fn in sorted(os.listdir(base)):
        if not fn.endswith('.html'):
            continue
        path = os.path.join(loc, fn)
        fallback = not os.path.exists(path)
        src = open(os.path.join(base if fallback else loc, fn)).read()
        m = re.match(r'\s*<!--(.*?)-->', src, re.S)
        meta = {}
        if m:
            for part in m.group(1).split('|'):
                if ':' in part:
                    k, v = part.split(':', 1)
                    meta[k.strip()] = v.strip()
            src = src[m.end():]
        cat = meta.get('categoria', 'Mundo')
        if fallback and lang != 'pt':
            cat = CAT_ORDER[lang][CAT_ORDER['pt'].index(cat)] if cat in CAT_ORDER['pt'] else cat
        pages[fn[:-5]] = {'titulo': meta.get('titulo', fn[:-5]), 'categoria': cat, 'resumo': meta.get('resumo', ''),
                          'corpo': src.strip(), 'fallback': fallback and lang != 'pt'}
    return pages


PAGES = {}


def nav_side(active):
    groups = {}
    for slug, p in PAGES.items():
        if slug.startswith(('zumbi-', 'memoria-')):
            continue
        groups.setdefault(p['categoria'], []).append((slug, p['titulo']))
    out = []
    order = CAT_ORDER[LANG]
    for cat in order + sorted(set(groups) - set(order)):
        if cat not in groups:
            continue
        items = ''.join(f'<li><a href="{s}.html"{" aria-current=page" if s == active else ""}>{e(t)}</a></li>'
                        for s, t in sorted(groups[cat], key=lambda x: x[1]))
        out.append(f'<details open><summary>{e(cat)}</summary><ul>{items}</ul></details>')
    extra = ''.join(f'<li><a href="{s}.html"{" aria-current=page" if s == active else ""}>{_(t)}</a></li>'
                    for s, t in [('itens', 'Todos os itens'), ('lugares', 'Lugares'), ('zumbis-lista', 'Tipos de zumbi'),
                                 ('memorias-lista', 'As memórias')])
    return f'<details open><summary>{_("Índices")}</summary><ul>{extra}</ul></details>' + ''.join(out)


def lang_links(slug):
    out = []
    for L in LANGS:
        if L == LANG:
            href = f'{slug}.html'
        elif L == 'pt':
            href = f'../{slug}.html'
        elif LANG == 'pt':
            href = f'{L}/{slug}.html'
        else:
            href = f'../{L}/{slug}.html'
        cur = ' aria-current="true"' if L == LANG else ''
        out.append(f'<a class="flag" href="{href}" hreflang="{HTML_LANG[L]}" title="{LANG_NAME[L]}"{cur}>'
                   f'<img class="px" src="{R()}img/flags/{L}.png" alt="{LANG_NAME[L]}" width="18" height="12"></a>')
    return f'<div class="langs" role="group" aria-label="{_("Idioma")}">' + ''.join(out) + '</div>'


GUIDES_HREF = {'pt': 'guias.html?lang=pt', 'en': 'guias.html?lang=en', 'es': 'guias.html?lang=es'}


def page(slug, title, body, summary='', crumbs=None, cat=None):
    crumbs = crumbs or ([('index.html', 'Wiki')] + ([(None, cat)] if cat else []))
    cr = ' / '.join(f'<a href="{h}">{e(t)}</a>' if h else e(t) for h, t in crumbs)
    alts = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG[L]}" href="https://footfall.pcpastre.com/wiki/{"" if L == "pt" else L + "/"}{slug}.html">'
                   for L in LANGS)
    note = ''
    if PAGES.get(slug, {}).get('fallback'):
        note = {'en': '<p class="tip">This page has not been translated yet: showing the Portuguese text.</p>',
                'es': '<p class="tip">Esta página aún no está traducida: se muestra el texto en portugués.</p>'}[LANG]
    return f'''<!doctype html>
<html lang="{HTML_LANG[LANG]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)} — {_('Wiki do Footfall')}</title>
<meta name="description" content="{e(summary or title)}">
<meta name="theme-color" content="#0b0a10">
{alts}
<link rel="icon" type="image/png" href="{R()}img/icone.png">
<link rel="stylesheet" href="{R()}estilo.css">
<link rel="stylesheet" href="{A()}wiki.css">
</head>
<body class="wiki" data-a="{A()}">
<header class="top">
  <div class="wrap">
    <a class="brand" href="{R()}index.html?lang={LANG}" aria-label="Footfall"><img class="px" src="{R()}img/logo.png" alt="Footfall" width="148" height="58"></a>
    <a class="wk" href="index.html">Wiki</a>
    <form class="busca" role="search" action="busca.html"><input type="search" name="q" placeholder="{_('Buscar na wiki')}" aria-label="{_('Buscar na wiki')}" autocomplete="off"><div class="sug" hidden></div></form>
    {lang_links(slug)}
    <button type="button" class="menu" aria-expanded="false" aria-controls="side">{_('Seções')}</button>
  </div>
</header>
<div class="wiki-wrap">
<nav class="side" id="side" aria-label="{_('Seções da wiki')}">{nav_side(slug)}</nav>
<main class="doc wdoc">
<p class="crumbs">{cr}</p>
<h1>{e(title)}</h1>
{f'<p class="sub">{e(summary)}</p>' if summary else ''}
{note}
{body}
</main>
</div>
<footer class="foot">
  <div class="wrap">
    <img class="px" src="{R()}img/logo.png" alt="Footfall" width="148" height="58">
    <nav aria-label="{_('Rodapé')}">
      <a href="{R()}index.html?lang={LANG}">{_('Site')}</a>
      <a href="{R()}{GUIDES_HREF[LANG]}">{_('Guias')}</a>
      <a href="index.html">Wiki</a>
      <a href="{R()}privacidade.html?lang={LANG}">{_('Política de privacidade')}</a>
      <a href="mailto:contato@footfall.pcpastre.com">contato@footfall.pcpastre.com</a>
    </nav>
  </div>
  <div class="wrap" style="margin-top:14px">{_('Wiki gerada a partir do código do jogo. Valores podem mudar entre versões.')}</div>
</footer>
<script src="{A()}wiki.js" defer></script>
</body>
</html>
'''


OUT = ROOT


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


def recipe_row(r):
    ins = ', '.join(f'{ilink(k)} ×{v}' for k, v in r.get('inputs', {}).items()) or '—'
    tools = ', '.join(ilink(k) for k in r.get('tools', [])) or '—'
    name = F(r, 'name')
    if r.get('output'):
        out = f'{ilink(r["output"])} ×{r.get("qty", 1)}'
    elif r.get('furniture'):
        out = e(name) + _(' (móvel)')
    else:
        out = e(name)
    st = {'fogo': _('Fogo'), 'bancada': _('Bancada'), 'nenhuma': '—'}.get(r.get('station'), e(str(r.get('station'))))
    sk = f'{e(G(r.get("skill_name") or ""))} {r.get("minLevel") or ""}'.strip() or '—'
    return [f'<b>{e(name)}</b>', ins, tools, st, sk, out]


TREAT_ITEMS = {}
for t in BODY.get('treatments', []):
    for k in (t.get('items') or []) + (t.get('tools_not_consumed') or []):
        TREAT_ITEMS.setdefault(k, []).append(t['label'])


def infobox(it):
    rows = [(_('Tipo'), _(KIND1.get(it['kind'], it['kind']))),
            (_('Raridade'), f'<span class="r-{it["rarity"]}">{_(RAR.get(it["rarity"], it["rarity"]))}</span>'),
            (_('Peso'), num(it['weight']) + ' kg')]
    d = it.get('derived', {})
    if d.get('slot'):
        rows.append((_('Onde vai'), e(slot(str(d['slot'])))))
    if d.get('ref_price'):
        rows.append((_('Preço de referência'), f'{d["ref_price"]} {_("selos")}'))
    others = [L for L in LANGS if L != LANG]
    nm = {'pt': it['name'], 'en': it.get('name_en'), 'es': it.get('name_es')}
    names = '<p class="alt">' + '<br>'.join(f'{L}: {e(nm[L] or "—")}' for L in others) + '</p>'
    trs = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows)
    return (f'<aside class="infobox"><img class="px" src="{A()}img/itens/{it["id"]}.png" alt="" width="96" height="96">'
            f'<b>{e(F(it, "name"))}</b>{names}<table>{trs}</table></aside>')


def item_body(it):
    d = it.get('derived', {})
    parts = [infobox(it)]
    note = F(it, 'note')
    if note:
        parts.append(f'<p class="lead2">{e(note)}</p>')
    w = it.get('weapon')
    if w:
        rows = []
        if d.get('firearm') or d.get('bow') or w.get('ranged'):
            rows += [(_('Dano por tiro'), num(w['damage']) + (f' × {w["pellets"]} {_("chumbos")}' if (w.get('pellets') or 1) > 1 else '')),
                     (_('Alcance'), num(w['reach']) + ' m'), (_('Pente'), num(w.get('mag'))), (_('Recarga'), num(w.get('reload')) + ' s'),
                     (_('Intervalo entre tiros'), num(w.get('cooldown')) + ' s')]
            if d.get('burst', 1) > 1:
                rows.append((_('Rajada'), f'{d["burst"]} {_("tiros")}'))
            if w.get('ammo'):
                rows.append((_('Munição'), ilink(w['ammo'])))
            nz = w.get('noise')
            rows.append((_('Barulho no mapa'), _('raio de tiro (150 m)') if nz == 999 else (num(nz) + ' m' if nz else '—')))
        else:
            rows += [(_('Dano'), num(w['damage'])), (_('Alcance'), num(w['reach']) + ' m'), (_('Intervalo'), num(w.get('cooldown')) + ' s'),
                     (_('Arco do golpe'), num(w.get('arcDeg')) + '°'), (_('Alvos por golpe'), num(w.get('maxTargets'))),
                     (_('Durabilidade'), _('não gasta') if d.get('infinite_durability') else num(w.get('durability')))]
        if d.get('damage_per_second'):
            rows.append((_('Dano por segundo (teórico)'), num(d['damage_per_second'], 1)))
        parts.append(f'<h2>{_("Arma")}</h2>' + tbl([_('Atributo'), _('Valor')], rows, 'kv'))
    food = []
    if it.get('kcal'):
        food.append((_('Calorias'), f'{it["kcal"]} kcal'))
    if it.get('ml'):
        food.append((_('Água'), f'{it["ml"]} ml'))
    if it.get('shelfLife_days'):
        food.append((_('Validade'), num(it['shelfLife_days'], 1) + ' ' + _('dias')))
    elif it.get('edible') and not it.get('perishable'):
        food.append((_('Validade'), _('não estraga')))
    if food:
        parts.append(f'<h2>{_("Alimento")}</h2>' + tbl([_('Atributo'), _('Valor')], food, 'kv'))
    med = []
    if it.get('heal'):
        med.append((_('Cura'), f'{it["heal"]} {_("de vida")}'))
    if it.get('bandage'):
        med.append((_('Serve para enfaixar'), _('sim')))
    if it['id'] in TREAT_ITEMS:
        med.append((_('Usado em'), ', '.join(e(G(x)) for x in TREAT_ITEMS[it['id']])))
    if med:
        parts.append(f'<h2>{_("Médico")}</h2>' + tbl([_('Atributo'), _('Valor')], med, 'kv') +
                     f'<p>{_("Veja")} <a href="tratamento.html">{_("Tratamento")}</a> {_("e")} <a href="feridas.html">{_("Feridas")}</a>.</p>')
    gear = []
    if it.get('pockets'):
        gear.append((_('Bolsos'), f'+{num(it["pockets"])} kg'))
    if it.get('bagKg'):
        gear.append((_('Capacidade'), f'{num(it["bagKg"])} kg'))
    if d.get('warmth') is not None and it['kind'] == 'roupa':
        gear.append((_('Calor'), num(d['warmth'])))
    if d.get('heavy'):
        gear.append((_('Roupa pesada (calor)'), _('sim')))
    if d.get('armor_material'):
        gear.append((_('Material'), e(slot(d['armor_material']))))
    if d.get('armor_wear_per_bite'):
        gear.append((_('Desgaste por mordida'), num(d['armor_wear_per_bite'])))
    if gear:
        parts.append(f'<h2>{_("Equipamento")}</h2>' + tbl([_('Atributo'), _('Valor')], gear, 'kv') +
                     f'<p>{_("Veja")} <a href="mochila-e-peso.html">{_("Mochila e peso")}</a> {_("e")} <a href="costura-e-roupas.html">{_("Costura e roupas")}</a>.</p>')
    if d.get('armor_block'):
        heads = [_('Parte')] + [_(ATK[a]) for a in ATK]
        rows = []
        for part_, by in d['armor_block'].items():
            rip = d.get('armor_block_ripped', {}).get(part_, {})
            rows.append([_(PART.get(part_, part_))] + [f'{pct(by.get(a, 0))} <small>({_("rasgada")} {pct(rip.get(a, 0))})</small>' for a in ATK])
        parts.append(f'<h2>{_("Proteção")}</h2><p>{_("Chance de a roupa segurar cada tipo de ataque na parte que cobre.")}</p>' + tbl(heads, rows))
    wh = WHERE.get(it['id'], {})
    where = []
    pools = wh.get('pools', [])
    if pools:
        rows = []
        for p in sorted(pools, key=lambda x: -x['tier_share']):
            furn = ', '.join(e(G(f)) for f in (wh.get('furniture', {}).get(p['category'], {}) or {}))
            rows.append([clink(p['category']), pct(p['tier_share']), furn or '—'])
        where.append(f'<p>{_("Chance mostrada: a parte que este item ocupa entre os itens da mesma raridade naquele tipo de lugar.")}</p>' +
                     tbl([_('Lugar'), _('Chance na raridade'), _('Móveis')], rows))
    if wh.get('zombies'):
        where.append(f'<h3>{_("Em zumbis")}</h3>' + tbl([_('Zumbi'), _('Chance'), _('Máx.')],
                     [[f'<a href="zumbi-{z["class"]}.html">{e(zlabel(ZC.get(z["class"], {"label": z["class"]})))}</a>', pct(z['chance']), num(z['max'])] for z in wh['zombies']]))
    other = wh.get('other') or []
    OTH = {'corpse': 'corpos de zumbi (bolsos)', 'backpack': 'mochila de zumbi mochileiro', 'special_pool': 'móveis especiais de alguns cômodos',
           'recipe': 'receita', 'starter_kit': 'kit inicial', 'very_rare': 'achado raríssimo ao entrar nos lugares', 'flare': 'caixa de resgate / sinalizador',
           'skin': 'conjunto de roupa raro'}
    if other:
        kinds = {o if isinstance(o, str) else o.get('kind', '') for o in other}
        txt = ', '.join(sorted(_(OTH.get(k, k)) for k in kinds))
        where.append(f'<p>{_("Também")}: {e(txt)}.</p>')
    if it['id'] in REC_OUT:
        where.append(f'<p>{_("Fabricado por receita (veja abaixo).")}</p>')
    if where:
        parts.append(f'<h2>{_("Onde achar")}</h2>' + ''.join(where))
    elif it['id'].startswith('memoria_'):
        parts.append(f'<h2>{_("Onde achar")}</h2><p>{_("Veja")} <a href="memorias.html">{_("Memórias")}</a>.</p>')
    rs = []
    for title, src in [('Como fazer', REC_OUT), ('Usado como ingrediente', REC_IN), ('Usado como ferramenta', REC_TOOL)]:
        lst = src.get(it['id'])
        if lst:
            rs.append(f'<h3>{_(title)}</h3>' + tbl([_('Receita'), _('Ingredientes'), _('Ferramentas'), _('Onde'), _('Habilidade'), _('Resultado')],
                                                  [recipe_row(r) for r in lst]))
    if rs:
        parts.append(f'<h2>{_("Receitas")}</h2>' + ''.join(rs))
    parts.append(f'<p class="code">{_("Código")}: <code>{e(it["id"])}</code></p>')
    return '\n'.join(parts)


def iname(i):
    return F(i, 'name')


def items_index():
    out = [f'<p>{_("Todos os itens do jogo, com os valores do código. Toque no nome para ver a ficha completa.")}</p>',
           f'<p class="filtro"><input type="search" placeholder="{_("Filtrar itens")}" aria-label="{_("Filtrar itens")}" data-filtro></p>']
    for kind, label in KIND.items():
        lst = sorted([i for i in ITEMS['items'] if i['kind'] == kind], key=iname)
        rar = lambda i: _(RAR[i['rarity']])
        if kind == 'arma':
            rows = [[ilink(i['id']), rar(i), num(i['weight']), num(i['weapon']['damage']) if i.get('weapon') else '—',
                     (num(i['weapon']['reach']) + ' m') if i.get('weapon') else '—',
                     (_('fogo') if i.get('derived', {}).get('firearm') else _('arco') if i.get('derived', {}).get('bow') else _('branca') if i.get('weapon') else '—')] for i in lst]
            head = [_('Item'), _('Raridade'), _('Peso'), _('Dano'), _('Alcance'), _('Tipo')]
        elif kind == 'comida':
            rows = [[ilink(i['id']), rar(i), num(i['weight']), i.get('kcal') or '—', i.get('ml') or '—',
                     num(i.get('shelfLife_days'), 1) if i.get('shelfLife_days') else '—'] for i in lst]
            head = [_('Item'), _('Raridade'), _('Peso'), 'kcal', 'ml', _('Validade (dias)')]
        elif kind == 'roupa':
            rows = [[ilink(i['id']), rar(i), num(i['weight']), e(slot(str(i.get('derived', {}).get('slot') or '—'))),
                     ('+' + num(i['pockets']) + ' kg') if i.get('pockets') else (_('mochila') + ' ' + num(i['bagKg']) + ' kg' if i.get('bagKg') else '—')] for i in lst]
            head = [_('Item'), _('Raridade'), _('Peso'), _('Lugar no corpo'), _('Carga')]
        else:
            rows = [[ilink(i['id']), rar(i), num(i['weight']), e(F(i, 'note'))[:110]] for i in lst]
            head = [_('Item'), _('Raridade'), _('Peso'), _('Nota')]
        out.append(f'<h2 id="{kind}">{_(label)} <small>({len(lst)})</small></h2>' + tbl(head, rows, 'filt'))
    return '\n'.join(out)


def noise_label(s):
    return G(s)


def place_body(cid):
    c = CATS[cid]
    parts = [f'<p>{_("Lugares de verdade do mapa (OpenStreetMap) que o jogo trata como")} <b>{e(F(c, "label"))}</b>. '
             f'{_("Veja também")} <a href="saque.html">{_("Saque")}</a>.</p>']
    rows = [(_('Guardas no máximo (pontos dominados)'), num(c.get('guards')))]
    it = c.get('interior') or {}
    if it.get('zombies'):
        rows.append((_('Zumbis dentro'), f'{it["zombies"][0]} {_("a")} {it["zombies"][1]}'))
    if it.get('typical_size_m'):
        rows.append((_('Tamanho típico'), f'{it["typical_size_m"][0]} {_("a")} {it["typical_size_m"][1]} m'))
    parts.append(tbl([_('Atributo'), _('Valor')], rows, 'kv'))
    qf = c.get('quick_loot_furniture') or []
    if qf:
        parts.append(f'<h2>{_("Pela porta")}</h2><p>{_("Móveis da entrada, rápidos e sem itens raros.")}</p>' +
                     tbl([_('Móvel'), _('Tempo'), _('Barulho')], [[e(G(f['name'])), num(f['seconds']) + ' s', f'{e(noise_label(f["noise_label"]))} (~{num(f["noise_radius_m"], 0)} m)'] for f in qf]))
    floors = (it.get('ground_floor') or []) + (it.get('upper_floors') or [])
    if floors:
        rows = []
        fk = LOOT['furniture_kinds']
        for fl in floors:
            for room in fl.get('rooms', []):
                furn = [f for f in room.get('furniture', []) if f.get('lootable')]
                if not furn:
                    continue
                rows.append([e(ROOM[LANG].get(room['room'], room['room'])) + (f' <small>({_("trancado")})</small>' if room.get('locked') else ''),
                             '<br>'.join(e(G(f['name'])) + (f' <small>{num(fk[f["name"]]["seconds"])} s, {e(noise_label(fk[f["name"]]["noise_label"]))}</small>' if f['name'] in fk else '') for f in furn)])
        if rows:
            parts.append(f'<h2>{_("Entrando")}</h2><p>{_("Cômodos e móveis que dá para vasculhar dentro do prédio. Dentro, os raros têm mais chance.")}</p>' +
                         tbl([_('Cômodo'), _('Móveis')], rows))
    ls = c.get('loot_stats') or {}
    if ls:
        order = ['comum', 'incomum', 'raro', 'lendario']
        rows = [[ilink(iid), _(RAR.get(s['rarity'], s['rarity'])), pct(s['tier_share'])]
                for iid, s in sorted(ls.items(), key=lambda kv: (order.index(kv[1]['rarity']) if kv[1]['rarity'] in order else 9, -kv[1]['tier_share']))]
        parts.append(f'<h2>{_("O que sai daqui")}</h2><p>{_("Cada item sorteado primeiro tira a raridade e depois um item daquela raridade; a coluna mostra a parte do item dentro da raridade.")}</p>' +
                     tbl([_('Item'), _('Raridade'), _('Chance na raridade')], rows))
    zs = ZOMB.get('by_place', {}).get(cid)
    if zs:
        parts.append(f'<h2>{_("Zumbis especiais por perto")}</h2><p>' + ', '.join(sorted({f'<a href="zumbi-{z}.html">{e(zlabel(ZC[z]))}</a>' for z in zs if z in ZC})) +
                     f'. {_("Veja")} <a href="zumbis.html">{_("Zumbis")}</a>.</p>')
    mem = {'saude': 'plantao', 'casa': 'jorge', 'eletronicos': 'voz', 'policia': 'quinta', 'bunker': 'cofre'}.get(cid)
    if mem:
        parts.append(f'<div class="tip"><b>{_("Memória")}</b>{_("Um livro de memória pode aparecer nos móveis de dentro: veja")} <a href="memoria-{mem}.html">{_("a memória")}</a>.</div>')
    return '\n'.join(parts)


def places_index():
    rows = [[f'<a href="lugar-{k}.html">{e(F(c, "label"))}</a>', num(c.get('guards')), len(c.get('loot_stats') or {})] for k, c in CATS.items()]
    return f'<p>{_("Cada lugar do mapa cai numa categoria, e a categoria decide os móveis, o saque e os zumbis.")}</p>' + \
        tbl([_('Categoria'), _('Guardas (máx.)'), _('Itens possíveis')], rows)


def zombies_index():
    rows = [[f'<a href="zumbi-{z["id"]}.html">{e(zlabel(z))}</a>', '×' + num(z['hp']), '×' + num(z['speed']), '×' + num(z['head']),
             '×' + num(z['torso']), _('sim') if z.get('fireproof') else '—'] for z in ZOMB['classes']]
    return (f'<p>{_("Multiplicadores sobre o zumbi comum. Cabeça e tronco: quanto do dano entra naquela parte (menor = mais protegido).")} '
            f'{_("Veja")} <a href="zumbis.html">{_("Zumbis")}</a>.</p>' +
            tbl([_('Tipo'), _('Vida'), _('Velocidade'), _('Dano na cabeça'), _('Dano no tronco'), _('Não pega fogo')], rows))


def memories_index():
    lst = [s for s in PAGES if s.startswith('memoria-')]
    return (f'<p>{_("As histórias jogáveis da estante do depósito do rádio. Sem spoilers: só onde achar, desafio e recompensa.")} '
            f'{_("Veja")} <a href="memorias.html">{_("Memórias")}</a>.</p><ul>' +
            ''.join(f'<li><a href="{s}.html">{e(PAGES[s]["titulo"])}</a> — {e(PAGES[s]["resumo"])}</li>' for s in sorted(lst)) + '</ul>')


def home():
    groups = {}
    for slug, p in PAGES.items():
        if slug.startswith(('zumbi-', 'memoria-')):
            continue
        groups.setdefault(p['categoria'], []).append((slug, p))
    cards = []
    for cat in CAT_ORDER[LANG]:
        if cat not in groups:
            continue
        li = ''.join(f'<li><a href="{s}.html">{e(p["titulo"])}</a></li>' for s, p in sorted(groups[cat], key=lambda x: x[1]['titulo']))
        cards.append(f'<section class="wcat bevel"><h2>{e(cat)}</h2><ul>{li}</ul></section>')
    idx = (f'<div class="wstats"><a class="bevel" href="itens.html"><b>{len(ITEMS["items"])}</b>{_("itens")}</a>'
           f'<a class="bevel" href="lugares.html"><b>{len(CATS)}</b>{_("tipos de lugar")}</a>'
           f'<a class="bevel" href="zumbis-lista.html"><b>{len(ZOMB["classes"])}</b>{_("tipos de zumbi")}</a>'
           f'<a class="bevel" href="receitas.html"><b>{len(RECIPES["recipes"])}</b>{_("receitas")}</a>'
           f'<a class="bevel" href="tracos.html"><b>{len(CHARS["traits"])}</b>{_("traços")}</a></div>')
    return (f'<p class="lead">{_("A enciclopédia do Footfall: cada mecânica, item, lugar e zumbi, com os números tirados direto do código do jogo.")} '
            f'{_("Começando agora? Leia os")} <a href="{R()}{GUIDES_HREF[LANG]}">{_("guias")}</a> {_("primeiro.")}</p>' + idx +
            '<div class="wcats">' + ''.join(cards) + '</div>')


def search_index():
    idx = []
    for s, p in PAGES.items():
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', p['corpo']))).strip()
        idx.append({'t': p['titulo'], 'u': s + '.html', 'c': p['categoria'], 'r': p['resumo'], 'x': txt[:4000]})
    for i in ITEMS['items']:
        idx.append({'t': iname(i), 'u': f'item-{i["id"]}.html', 'c': _('Item') + ' · ' + _(KIND1.get(i['kind'], '')),
                    'r': F(i, 'note')[:120], 'i': i['id']})
    for k, c in CATS.items():
        idx.append({'t': F(c, 'label'), 'u': f'lugar-{k}.html', 'c': _('Lugar'), 'r': ''})
    return idx


def build_lang(lang):
    global LANG, PAGES, OUT
    LANG = lang
    OUT = ROOT if lang == 'pt' else os.path.join(ROOT, lang)
    os.makedirs(OUT, exist_ok=True)
    PAGES = load_pages(lang)
    for s, p in PAGES.items():
        if s.startswith('zumbi-'):
            cat, crumbs = _('Combate'), [('index.html', 'Wiki'), ('zumbis-lista.html', _('Tipos de zumbi'))]
        elif s.startswith('memoria-'):
            cat, crumbs = _('Memórias'), [('index.html', 'Wiki'), ('memorias-lista.html', _('Memórias'))]
        else:
            cat, crumbs = p['categoria'], None
        write(s, page(s, p['titulo'], p['corpo'], p['resumo'], crumbs, cat))
    for it in ITEMS['items']:
        write('item-' + it['id'], page('item-' + it['id'], iname(it), item_body(it), '',
                                       [('index.html', 'Wiki'), ('itens.html', _('Itens')), (f'itens.html#{it["kind"]}', _(KIND[it['kind']]))]))
    for k in CATS:
        write('lugar-' + k, page('lugar-' + k, F(CATS[k], 'label'), place_body(k), '', [('index.html', 'Wiki'), ('lugares.html', _('Lugares'))]))
    write('itens', page('itens', _('Itens'), items_index(), f'{_("Os")} {len(ITEMS["items"])} {_("itens do jogo.")}'))
    write('lugares', page('lugares', _('Lugares'), places_index(), _('Os tipos de lugar do mapa.')))
    write('zumbis-lista', page('zumbis-lista', _('Tipos de zumbi'), zombies_index(), _('Todos os tipos de zumbi e os multiplicadores.')))
    write('memorias-lista', page('memorias-lista', _('As memórias'), memories_index(), _('As histórias jogáveis.')))
    write('busca', page('busca', _('Buscar'), '<div id="resultados" aria-live="polite"></div>'))
    write('index', page('index', _('Wiki do Footfall'), home(), '', [(f'{R()}index.html?lang={LANG}', 'Footfall')]))
    with open(os.path.join(OUT, 'busca.json'), 'w') as f:
        json.dump(search_index(), f, ensure_ascii=False, separators=(',', ':'))
    names = set(os.listdir(OUT))
    bad = {}
    for fn in names:
        if fn.endswith('.html'):
            for h in re.findall(r'href="([^"#?:]+\.html)', open(os.path.join(OUT, fn)).read()):
                if h.startswith('../') or h.startswith(('en/', 'es/')):
                    continue
                if h not in names:
                    bad.setdefault(h, set()).add(fn)
    fb = sum(1 for p in PAGES.values() if p['fallback'])
    print(f'{lang}: {len([n for n in names if n.endswith(".html")])} paginas' + (f', {fb} sem traducao (texto em pt)' if fb else ''))
    for h, srcs in sorted(bad.items()):
        print('  LINK QUEBRADO', h, '<-', ', '.join(sorted(srcs))[:200])
    if lang != 'pt':
        missing = sorted({s for s in re.findall(r'_\(\'([^\']+)\'\)', open(__file__).read()) if s not in TR[lang]})
        if missing:
            print('  textos do gerador sem traducao:', missing[:20])


def build():
    os.makedirs(os.path.join(ROOT, 'img', 'itens'), exist_ok=True)
    sp = os.path.join(GAME, 'assets', 'sprites')
    atlas = json.load(open(os.path.join(sp, 'itens.json')))
    im = Image.open(os.path.join(sp, 'itens.png')).convert('RGBA')
    c = atlas['cell']
    for iid, (x, y) in atlas['items'].items():
        im.crop((x, y, x + c, y + c)).save(os.path.join(ROOT, 'img', 'itens', iid + '.png'), optimize=True)
    shutil.copy(os.path.join(HERE, 'wiki.css'), ROOT)
    shutil.copy(os.path.join(HERE, 'wiki.js'), ROOT)
    for L in LANGS:
        build_lang(L)


build()
