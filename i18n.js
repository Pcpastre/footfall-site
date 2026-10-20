/* Footfall — idioma do site (inglês é o padrão; o HTML já vem em inglês).
   Escolha: ?lang=pt|en|es na URL > a última escolha (localStorage) > inglês. */
(() => {
  'use strict';
  const LANGS = ['en', 'pt', 'es'];
  const HTML_LANG = { en: 'en', pt: 'pt-BR', es: 'es' };
  const T = {
    pt: {
      'title.index': 'Footfall — sobrevivência zumbi na sua cidade real',
      'title.privacy': 'Footfall — Política de privacidade',
      'title.delete': 'Footfall — Excluir conta',
      'desc.index': 'Footfall é um jogo de sobrevivência zumbi para Android, em pixel art gótico, jogado andando pela sua cidade real. Saqueie lugares de verdade, monte uma base com o seu grupo e aguente as noites.',
      'skip': 'Pular para o conteúdo',
      'lang': 'Idioma',
      'nav.game': 'O jogo', 'nav.images': 'Imagens', 'nav.support': 'Apoie', 'nav.download': 'Baixar',
      'nav.home': 'Início', 'nav.privacy': 'Privacidade',
      'hero.tag': 'Ande. O corvo está vendo.',
      'hero.sub': 'Sobrevivência zumbi para Android jogada andando de verdade. O mapa é a sua cidade, e ela está cheia de mortos.',
      'hero.download': 'Baixar', 'hero.more': 'Conhecer o jogo',
      'game.kicker': 'O jogo', 'game.title': 'Sua cidade. Os mortos. Você.',
      'game.p1': 'Footfall é um jogo de sobrevivência zumbi em pixel art gótico jogado andando pela sua cidade real. As ruas, as farmácias, os mercados e os postos são os de verdade, e estão tomados.',
      'game.p2': 'Ande para achar o que precisa. Saqueie lugares que enchem de novo toda semana, cuide de cada ferida, levante uma base com o seu grupo e aguente as noites. Quanto mais você anda, mais longe chega.',
      'game.quote': 'Quando você puser a primeira porta, um corvo pousa nela. Ele fica.',
      'alt.confront': 'Três sobreviventes sob a luz de uma lanterna diante de uma horda de zumbis',
      'f1.t': 'O mapa é a sua cidade', 'f1.p': 'Ruas e lugares reais pelo GPS. Você só vê o que está à sua frente; prédios tapam a visão e a noite encurta tudo.',
      'f2.t': 'Saque de verdade', 'f2.p': 'Pela porta é rápido; entrando tem mais coisa, e mais zumbi. Cada móvel faz barulho ao abrir. Tudo enche de novo toda semana.',
      'f3.t': 'Tela de ação', 'f3.p': 'Lute de perto: empurre, agache, mire, arremesse. Cada arma gasta e faz barulho. Quem estiver a até 120 m entra junto.',
      'f4.t': 'Corpo de verdade', 'f4.p': 'Feridas tratadas passo a passo. Fome, sede, cansaço e o clima real. Mordida infecta, e não tem cura.',
      'f5.t': 'Base do grupo', 'f5.p': 'Demarque na grade, levante paredes, ponha portas, baús, horta e armadilhas. Toda noite ela é atacada.',
      'f6.t': 'Mercado de selos', 'f6.p': 'Uma caixa de correio na base é o mercado de todo mundo. A moeda é o selo, e ninguém vê o que os outros negociam.',
      'f7.t': 'Pontos dominados', 'f7.p': 'Lugares grandes têm bandeira. Vença os guardas na arena e o ponto é do seu grupo, pagando selos todo dia.',
      'f8.t': 'Rádio Corvo', 'f8.p': 'Com um rádio, você ouve a horda da semana, as caixas de suprimento, pistas e missões.',
      'f9.t': 'Roupas raras', 'f9.p': 'Do comum ao lendário. Algumas só saem do corpo do zumbi do mesmo ofício: polícia, bombeiro, médico…',
      'img.kicker': 'Imagens', 'img.title': 'O que te espera lá fora',
      'alt.horde': 'Uma horda de zumbis com uniformes de polícia, bombeiro, médico e presidiário',
      'alt.outfits': 'Sobreviventes com roupas de raridades diferentes',
      'alt.arsenal': 'Armas, remédios e suprimentos do jogo em casas de inventário',
      'g1.t': 'A horda', 'g1.p': 'Zumbis de uniforme carregam o que usavam em vida.',
      'g2.t': 'Roupas', 'g2.p': 'Ache conjuntos no saque e troque no armário da base.',
      'g3.t': 'Arsenal', 'g3.p': 'Da faca ao fuzil, de bandagem a rádio.',
      'safe.kicker': 'Antes de sair', 'safe.title': 'Jogue de cabeça erguida',
      's1.t': 'Olhe o trânsito', 's1.p': 'Nunca jogue dirigindo. Ao atravessar a rua, o jogo pausa as ameaças: olhe a rua de verdade.',
      's2.t': 'Lugares são referência', 's2.p': 'Não entre em imóveis, terrenos ou áreas fechadas. O saque acontece no jogo.',
      's3.t': 'Ninguém vê você', 's3.p': 'Sua posição fica só no servidor. Outros jogadores não recebem onde você está.',
      'dl.kicker': 'Baixar e apoiar', 'dl.title': 'Entre no apocalipse',
      'dl.h': 'Baixe o Footfall', 'dl.p': 'Grátis, sem anúncios. Em breve na Google Play; siga as redes para entrar no teste.',
      'dl.apk': 'Baixar APK', 'dl.net': 'Internet',
      'sup.h': 'Apoie o Footfall', 'sup.p': 'Um jogo feito por uma pessoa só, sem anúncios e sem vender vantagem. O seu apoio mantém os servidores ligados e o corvo acordado.',
      'sup.btn': 'Apoie', 'sup.soon': 'em breve no Patreon',
      'soon': 'em breve', 'ok.playstore': 'Disponível', 'ok.apk': 'Versão de teste', 'ok.apoio': 'Patreon',
      'ft.privacy': 'Política de privacidade', 'ft.delete': 'Excluir conta', 'ft.home': 'Início',
      'ft.copy': '© 2026 Footfall · Feito no Brasil'
    },
    es: {
      'title.index': 'Footfall — supervivencia zombi en tu ciudad real',
      'title.privacy': 'Footfall — Política de privacidad',
      'title.delete': 'Footfall — Eliminar cuenta',
      'desc.index': 'Footfall es un juego de supervivencia zombi para Android, en pixel art gótico, que se juega caminando por tu ciudad real. Saquea lugares de verdad, arma una base con tu grupo y resiste las noches.',
      'skip': 'Ir al contenido',
      'lang': 'Idioma',
      'nav.game': 'El juego', 'nav.images': 'Imágenes', 'nav.support': 'Apoya', 'nav.download': 'Descargar',
      'nav.home': 'Inicio', 'nav.privacy': 'Privacidad',
      'hero.tag': 'Camina. El cuervo te está viendo.',
      'hero.sub': 'Supervivencia zombi para Android que se juega caminando de verdad. El mapa es tu ciudad, y está llena de muertos.',
      'hero.download': 'Descargar', 'hero.more': 'Conocer el juego',
      'game.kicker': 'El juego', 'game.title': 'Tu ciudad. Los muertos. Tú.',
      'game.p1': 'Footfall es un juego de supervivencia zombi en pixel art gótico que se juega caminando por tu ciudad real. Las calles, las farmacias, los supermercados y las gasolineras son los de verdad, y están tomados.',
      'game.p2': 'Camina para encontrar lo que necesitas. Saquea lugares que se reabastecen cada semana, cura cada herida, levanta una base con tu grupo y resiste las noches. Cuanto más caminas, más lejos llegas.',
      'game.quote': 'Cuando pongas tu primera puerta, un cuervo se posará en ella. Y se quedará.',
      'alt.confront': 'Tres sobrevivientes bajo la luz de una linterna frente a una horda de zombis',
      'f1.t': 'El mapa es tu ciudad', 'f1.p': 'Calles y lugares reales por GPS. Solo ves lo que tienes enfrente; los edificios tapan la vista y la noche lo acorta todo.',
      'f2.t': 'Saqueo de verdad', 'f2.p': 'Desde la puerta es rápido; adentro hay más cosas, y más zombis. Cada mueble hace ruido al abrirse. Todo se reabastece cada semana.',
      'f3.t': 'Pantalla de acción', 'f3.p': 'Pelea de cerca: empuja, agáchate, apunta, lanza. Cada arma se desgasta y hace ruido. Quien esté a menos de 120 m puede unirse.',
      'f4.t': 'Un cuerpo de verdad', 'f4.p': 'Heridas tratadas paso a paso. Hambre, sed, cansancio y el clima real. La mordida infecta, y no tiene cura.',
      'f5.t': 'Base del grupo', 'f5.p': 'Márcala en la cuadrícula, levanta muros, pon puertas, cofres, huerto y trampas. Cada noche la atacan.',
      'f6.t': 'Mercado de sellos', 'f6.p': 'Un buzón en la base es el mercado de todos. La moneda es el sello, y nadie ve lo que negocian los demás.',
      'f7.t': 'Puntos dominados', 'f7.p': 'Los lugares grandes tienen bandera. Vence a los guardias en la arena y el punto es de tu grupo, y paga sellos cada día.',
      'f8.t': 'Radio Cuervo', 'f8.p': 'Con una radio escuchas la horda de la semana, las cajas de suministros, pistas y misiones.',
      'f9.t': 'Ropa rara', 'f9.p': 'De común a legendaria. Algunas solo salen del cuerpo del zombi del mismo oficio: policía, bombero, médico…',
      'img.kicker': 'Imágenes', 'img.title': 'Lo que te espera allá afuera',
      'alt.horde': 'Una horda de zombis con uniformes de policía, bombero, médico y presidiario',
      'alt.outfits': 'Sobrevivientes con ropa de distintas rarezas',
      'alt.arsenal': 'Armas, medicinas y suministros del juego en casillas de inventario',
      'g1.t': 'La horda', 'g1.p': 'Los zombis con uniforme cargan lo que usaban en vida.',
      'g2.t': 'Ropa', 'g2.p': 'Encuentra conjuntos al saquear y cámbiate en el armario de la base.',
      'g3.t': 'Arsenal', 'g3.p': 'Del cuchillo al fusil, de la venda a la radio.',
      'safe.kicker': 'Antes de salir', 'safe.title': 'Juega con la cabeza en alto',
      's1.t': 'Mira el tráfico', 's1.p': 'Nunca juegues manejando. Al cruzar la calle, el juego pausa las amenazas: mira la calle de verdad.',
      's2.t': 'Los lugares son una referencia', 's2.p': 'No entres a inmuebles, terrenos ni áreas cerradas. El saqueo ocurre en el juego.',
      's3.t': 'Nadie te ve', 's3.p': 'Tu posición queda solo en el servidor. Los demás jugadores nunca reciben dónde estás.',
      'dl.kicker': 'Descargar y apoyar', 'dl.title': 'Entra al apocalipsis',
      'dl.h': 'Descarga Footfall', 'dl.p': 'Gratis, sin anuncios. Pronto en Google Play; síguenos para entrar a la prueba.',
      'dl.apk': 'Descargar APK', 'dl.net': 'Internet',
      'sup.h': 'Apoya Footfall', 'sup.p': 'Un juego hecho por una sola persona, sin anuncios y sin vender ventajas. Tu apoyo mantiene los servidores encendidos y al cuervo despierto.',
      'sup.btn': 'Apoya', 'sup.soon': 'pronto en Patreon',
      'soon': 'pronto', 'ok.playstore': 'Disponible', 'ok.apk': 'Versión de prueba', 'ok.apoio': 'Patreon',
      'ft.privacy': 'Política de privacidad', 'ft.delete': 'Eliminar cuenta', 'ft.home': 'Inicio',
      'ft.copy': '© 2026 Footfall · Hecho en Brasil'
    },
    en: {
      'title.privacy': 'Footfall — Privacy policy',
      'title.delete': 'Footfall — Delete account',
      'soon': 'coming soon', 'sup.soon': 'coming soon on Patreon',
      'ok.playstore': 'Available', 'ok.apk': 'Test version', 'ok.apoio': 'Patreon',
      'lang': 'Language'
    }
  };

  const store = {
    get() { try { return localStorage.getItem('lang'); } catch (_) { return null; } },
    set(v) { try { localStorage.setItem('lang', v); } catch (_) { /* sem armazenamento */ } }
  };
  const fromUrl = new URLSearchParams(location.search).get('lang');
  let lang = LANGS.includes(fromUrl) ? fromUrl : (LANGS.includes(store.get()) ? store.get() : 'en');

  // o inglês original fica guardado no próprio elemento
  const orig = (el, attr) => {
    const k = attr ? 'en' + attr : 'en';
    if (el.dataset[k] === undefined) el.dataset[k] = attr ? (el.getAttribute(attr) || '') : el.textContent;
    return el.dataset[k];
  };
  const t = (key, fallback) => (T[lang] && T[lang][key]) || (T.en[key]) || fallback;

  function apply() {
    document.documentElement.lang = HTML_LANG[lang];
    const page = document.documentElement.dataset.page || 'index';
    const title = document.querySelector('title');
    orig(title);
    document.title = lang === 'en' && page === 'index' ? title.dataset.en : t('title.' + page, title.dataset.en);
    const desc = document.querySelector('meta[name="description"]');
    if (desc && page === 'index') desc.setAttribute('content', lang === 'en' ? orig(desc, 'content') : t('desc.index', orig(desc, 'content')));
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const en = orig(el);
      el.textContent = lang === 'en' ? en : t(el.dataset.i18n, en);
    });
    document.querySelectorAll('[data-i18n-alt]').forEach((el) => {
      const en = orig(el, 'alt');
      el.setAttribute('alt', lang === 'en' ? en : t(el.dataset.i18nAlt, en));
    });
    document.querySelectorAll('[data-lang]').forEach((el) => { el.hidden = el.dataset.lang !== lang; });
    document.querySelectorAll('.flag').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.set === lang)));
    document.querySelectorAll('.langs').forEach((g) => g.setAttribute('aria-label', t('lang', 'Language')));
    window.dispatchEvent(new CustomEvent('ff:lang', { detail: lang }));
  }

  window.FF = { get lang() { return lang; }, t: (k, f) => t(k, f) };
  document.addEventListener('click', (e) => {
    const b = e.target.closest('.flag');
    if (!b || b.dataset.set === lang) return;
    lang = b.dataset.set;
    store.set(lang);
    if (fromUrl) history.replaceState(null, '', location.pathname + location.hash);
    apply();
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply); else apply();
})();
