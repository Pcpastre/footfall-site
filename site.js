/* Footfall — capa com a tempestade da tela inicial do jogo e links vindos do Supabase. */
(() => {
  'use strict';
  const SB = 'https://vcrdzdjjhksistodqmzb.supabase.co';
  const KEY = 'sb_publishable_EX_TlcGojTgx9llsuTkjJA_SvUsWNoE'; // chave pública (só lê links)
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Links (Instagram/TikTok na tabela links; download e apoio em site_links) ---------- */
  const ICON = { instagram: 'ig', tiktok: 'tt', youtube: 'play', patreon: 'pt' };
  const https = (u) => typeof u === 'string' && /^https:\/\/[^\s]+$/.test(u);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function socials(list) {
    const html = list.map((l) => {
      const ic = `<svg aria-hidden="true"><use href="#i-${ICON[l.key] || 'heart'}"/></svg>`;
      return https(l.url)
        ? `<a class="soc bevel" href="${esc(l.url)}" target="_blank" rel="noopener">${ic}${esc(l.label)}</a>`
        : `<span class="soc off bevel">${ic}${esc(l.label)} <em>em breve</em></span>`;
    }).join('');
    document.querySelectorAll('[data-socials]').forEach((el) => { el.innerHTML = html; });
  }
  const base = [{ key: 'instagram', label: 'Instagram', url: '' }, { key: 'tiktok', label: 'TikTok', url: '' }];
  socials(base);

  const SMALL = { playstore: 'Disponível', apk: 'Versão de teste', apoio: 'Patreon' };
  function siteLinks(list) {
    for (const l of list) {
      if (!https(l.url)) continue;
      document.querySelectorAll(`[data-site="${CSS.escape(l.key)}"]`).forEach((a) => {
        a.href = l.url;
        a.classList.remove('off');
        a.removeAttribute('aria-disabled');
        if (l.key !== 'apk') { a.target = '_blank'; a.rel = 'noopener'; }
        const s = a.querySelector('small');
        if (s) s.textContent = SMALL[l.key] || '';
      });
    }
  }
  document.querySelectorAll('[data-site]').forEach((a) => a.addEventListener('click', (e) => {
    if (a.classList.contains('off')) e.preventDefault();
  }));

  async function get(table) {
    const r = await fetch(`${SB}/rest/v1/${table}?select=key,label,url,sort&active=eq.true&order=sort`, { headers: { apikey: KEY } });
    if (!r.ok) throw new Error(String(r.status));
    return r.json();
  }
  get('links').then((rows) => {
    const merged = base.map((b) => ({ ...b, ...(rows.find((r) => r.key === b.key) || {}) }));
    for (const r of rows) if (!merged.some((m) => m.key === r.key) && https(r.url)) merged.push(r);
    socials(merged);
  }).catch(() => {});
  get('site_links').then(siteLinks).catch(() => {});

  /* ---------- A tempestade (porta gótica, corvo, raios e chuva), igual à tela inicial ---------- */
  const cv = document.getElementById('storm');
  if (!cv) return;
  const hero = cv.parentElement;
  const stage = document.getElementById('stage');
  const ctx = cv.getContext('2d');
  const off = document.createElement('canvas');
  const octx = off.getContext('2d');
  const load = (src) => { const i = new Image(); i.src = src; return i; };
  const crow = load('img/corvo.png');
  const eye = load('img/corvo_olho.png');
  const surv = load('img/andar/sobrevivente_parado.png');
  const zs = ['zumbi1', 'zumbi3', 'zumbi2', 'zumbi4'].map((n) => load(`img/andar/${n}.png`));

  // gerador com semente (o jogo usa Random(seed) para nuvens e chuva)
  const seeded = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const clouds = (() => { const r = seeded(21); return Array.from({ length: 9 }, () => ({ w: r(), h: r(), x: r(), v: r(), y: r() })); })();
  const drops = Array.from({ length: 90 }, (_, i) => { const r = seeded(500 + i); return [r(), r()]; });

  let W = 0, H = 0, dpr = 1, k = 4, ground = 0;
  const bump = (t, c, w) => Math.max(0, 1 - Math.abs(t - c) / w);
  const lerp = (a, b, f) => a + (b - a) * f;

  function layout() {
    W = hero.clientWidth;
    k = Math.max(3, Math.min(6, Math.floor(Math.min(W, 480) / 80)));
    hero.style.setProperty('--stage', `${52 * k + 8}px`);
    H = hero.clientHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    for (const c of [cv, off]) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); }
    const hr = hero.getBoundingClientRect(), sr = stage.getBoundingClientRect();
    ground = Math.round(sr.bottom - hr.top - 8);
  }

  function draw(now) {
    const T = 11000, t = (now % T) / T, cycle = Math.floor(now / T);
    const f = reduce ? 0 : Math.max(bump(t, 0.18, 0.012), bump(t, 0.205, 0.022), bump(t, 0.64, 0.014) * 0.7);
    const w = W, h = H;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
    // céu
    let g = ctx.createLinearGradient(0, 0, 0, ground);
    g.addColorStop(0, '#07050a'); g.addColorStop(0.6, '#140f18'); g.addColorStop(1, '#1a1420');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    // nuvens
    const cr = Math.round(lerp(0x1e, 0x5a, f * 0.6)), cg = Math.round(lerp(0x18, 0x70, f * 0.6)), cb = Math.round(lerp(0x26, 0x88, f * 0.6));
    ctx.fillStyle = `rgba(${cr},${cg},${cb},.75)`;
    for (const c of clouds) {
      const cw = w * (0.4 + c.w * 0.5), ch = ground * (0.06 + c.h * 0.07);
      const x = ((c.x * w * 1.6 + t * w * (0.08 + c.v * 0.06)) % (w * 1.6)) - w * 0.3;
      const y = ground * (0.02 + c.y * 0.42);
      ctx.beginPath(); ctx.ellipse(x + cw / 2, y + ch / 2, cw / 2, ch / 2, 0, 0, Math.PI * 2); ctx.fill();
    }
    if (f > 0) { ctx.fillStyle = `rgba(138,164,184,${0.28 * f})`; ctx.fillRect(0, 0, w, h); }

    // porta
    const cx = Math.floor(w / 2 / k) * k, b = Math.floor(ground / k) * k;
    const dw = 14 * k, dh = 26 * k;
    // raio
    if (f > 0.08) {
      const r = seeded(cycle * 7 + (t > 0.5 ? 3 : 0));
      let x = w * (0.62 + r() * 0.3), y = 0;
      ctx.beginPath(); ctx.moveTo(x, y);
      while (y < b - dh - 10 * k) { x += (r() - 0.5) * w * 0.12; y += ground * (0.04 + r() * 0.06); ctx.lineTo(Math.round(x), Math.round(y)); }
      ctx.lineJoin = 'miter';
      ctx.strokeStyle = `rgba(138,164,184,${0.35 * f})`; ctx.lineWidth = 7; ctx.shadowColor = 'rgba(138,164,184,.8)'; ctx.shadowBlur = 12; ctx.stroke();
      ctx.shadowBlur = 0; ctx.strokeStyle = `rgba(240,230,208,${f})`; ctx.lineWidth = 2.5; ctx.stroke();
    }
    // chão
    ctx.fillStyle = '#0b0710'; ctx.fillRect(0, ground, w, h - ground);
    const inner = new Path2D();
    inner.moveTo(cx - dw / 2, b); inner.lineTo(cx - dw / 2, b - dh * 0.68); inner.lineTo(cx, b - dh);
    inner.lineTo(cx + dw / 2, b - dh * 0.68); inner.lineTo(cx + dw / 2, b); inner.closePath();
    const fr = Math.round(lerp(0x0b, 0x5a, f * 0.8)), fg = Math.round(lerp(0x07, 0x42, f * 0.8)), fb = Math.round(lerp(0x10, 0x50, f * 0.8));
    const outer = new Path2D();
    outer.moveTo(cx - dw / 2 - 3 * k, b); outer.lineTo(cx - dw / 2 - 3 * k, b - dh * 0.68); outer.lineTo(cx, b - dh - 5 * k);
    outer.lineTo(cx + dw / 2 + 3 * k, b - dh * 0.68); outer.lineTo(cx + dw / 2 + 3 * k, b); outer.closePath();
    ctx.fillStyle = `rgb(${fr},${fg},${fb})`; ctx.fill(outer);
    g = ctx.createRadialGradient(cx, b - dh * 0.35, 0, cx, b - dh * 0.35, dh * 0.6);
    g.addColorStop(0, 'rgba(224,160,64,.55)'); g.addColorStop(1, 'rgba(58,36,24,.9)');
    ctx.fillStyle = '#0b0710'; ctx.fill(inner);
    ctx.fillStyle = g; ctx.fill(inner);
    ctx.fillStyle = `rgb(${fr},${fg},${fb})`;
    ctx.fillRect(cx - 6 * k, b - dh - 6 * k, 12 * k, 2 * k);
    // luz da porta no chão
    ctx.fillStyle = 'rgba(224,160,64,.12)';
    ctx.beginPath(); ctx.ellipse(cx, b + 2 * k, dw * 1.1, 3 * k, 0, 0, Math.PI * 2); ctx.fill();

    // personagens e o corvo numa camada escurecida (silhueta), acesa no raio
    octx.setTransform(dpr, 0, 0, dpr, 0, 0);
    octx.imageSmoothingEnabled = false;
    octx.clearRect(0, 0, w, h);
    const s = Math.max(2, Math.round(k * 0.5));
    const shadow = (x, y) => { octx.fillStyle = 'rgba(0,0,0,.45)'; octx.beginPath(); octx.ellipse(x, y, 11 * s, 4 * s, 0, 0, Math.PI * 2); octx.fill(); };
    const put = (img, sx, x, y) => { if (!img.complete || !img.naturalWidth) return; shadow(x, y); octx.drawImage(img, sx * 64, 0, 64, 64, Math.round(x - 32 * s), Math.round(y - 52 * s), 64 * s, 64 * s); };
    const step = reduce ? 0 : Math.floor(now / 170);
    zs.forEach((img, i) => {
      const x = cx - dw / 2 - 12 * k - i * 13 * k;
      if (x < -20 * s) return;
      put(img, (step + i * 3) % 4, x, b + (i % 2 ? 4 : 10) * k * 0.5);
    });
    put(surv, 0, cx + dw / 2 + 11 * k, b + 6 * k * 0.5);
    // corvo pousado na pedra do topo
    const sc = k * 0.9, at = [cx, b - dh - 6 * k + 1];
    const caw = !reduce && t > 0.205 && t < 0.3;
    if (crow.complete && crow.naturalWidth) {
      octx.drawImage(crow, caw ? 88 : 0, 0, 88, 88, Math.round(at[0] - 44 * sc), Math.round(at[1] - 44 * sc), 88 * sc, 88 * sc);
    }
    octx.globalCompositeOperation = 'source-atop';
    octx.fillStyle = `rgba(${Math.round(lerp(7, 138, f))},${Math.round(lerp(5, 164, f))},${Math.round(lerp(10, 184, f))},${lerp(0.82, 0.25, f)})`;
    octx.fillRect(0, 0, w, h);
    octx.globalCompositeOperation = 'source-over';
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.drawImage(off, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
    // olho aceso
    if (eye.complete && eye.naturalWidth) {
      ctx.shadowColor = 'rgba(255,216,128,.9)'; ctx.shadowBlur = 8;
      ctx.drawImage(eye, caw ? 88 : 0, 0, 88, 88, Math.round(at[0] - 44 * sc), Math.round(at[1] - 44 * sc), 88 * sc, 88 * sc);
      ctx.shadowBlur = 0;
    }
    // chuva
    if (!reduce) {
      ctx.strokeStyle = 'rgba(184,172,156,.25)'; ctx.lineWidth = 1; ctx.beginPath();
      for (const [rx, ry] of drops) {
        const x = (rx * w + t * 11 * 40) % w, y = (ry * h + t * 11 * 520) % h;
        ctx.moveTo(x, y); ctx.lineTo(x - 3, y + 11);
      }
      ctx.stroke();
    }
    // neblina rente ao chão e vinheta
    g = ctx.createLinearGradient(0, ground - h * 0.05, 0, ground + h * 0.07);
    g.addColorStop(0, 'rgba(26,20,32,0)'); g.addColorStop(0.5, 'rgba(26,20,32,.4)'); g.addColorStop(1, 'rgba(26,20,32,0)');
    ctx.fillStyle = g; ctx.fillRect(0, ground - h * 0.05, w, h * 0.12);
    g = ctx.createRadialGradient(w / 2, h * 0.45, 0, w / 2, h * 0.45, Math.max(w, h) * 0.75);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(7,5,10,.93)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }

  let visible = true, raf = 0;
  const loop = (now) => { draw(now); raf = visible && !reduce ? requestAnimationFrame(loop) : 0; };
  const start = () => { if (!raf) raf = requestAnimationFrame(loop); };
  layout();
  window.addEventListener('resize', () => { layout(); if (reduce) draw(1500); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => { visible = e.isIntersecting && !document.hidden; if (visible) start(); }).observe(hero);
  }
  document.addEventListener('visibilitychange', () => { visible = !document.hidden; if (visible) start(); });
  const ready = [crow, eye, surv, ...zs].map((i) => i.decode ? i.decode().catch(() => {}) : Promise.resolve());
  Promise.all(ready).then(() => { if (reduce) draw(1500); });
  if (reduce) draw(1500); else start();
})();
