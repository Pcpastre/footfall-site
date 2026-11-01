// Wiki do Footfall: busca, filtro de tabela e menu do celular
(() => {
  'use strict';
  let idx = null;
  const load = () => idx ? Promise.resolve(idx) : fetch('busca.json').then(r => r.json()).then(j => (idx = j));
  const norm = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function find(q) {
    const n = norm(q).trim();
    if (!n) return [];
    const words = n.split(/\s+/);
    return idx.map(p => {
      const t = norm(p.t), all = t + ' ' + norm(p.r) + ' ' + norm(p.c), body = norm(p.x);
      const inHead = words.every(w => all.includes(w));
      if (!inHead && !words.every(w => all.includes(w) || body.includes(w))) return null;
      let s = t === n ? 100 : t.startsWith(n) ? 60 : t.includes(n) ? 40 : inHead ? 20 : 5;
      if (!p.i) s += 5;
      return [s, p];
    }).filter(Boolean).sort((a, b) => b[0] - a[0]).map(x => x[1]);
  }
  const A = document.body.dataset.a || '';
  const row = p => `<a href="${p.u}">${p.i ? `<img class="px" src="${A}img/itens/${p.i}.png" alt="" width="24" height="24" style="display:inline;vertical-align:-6px;margin-right:6px">` : ''}${esc(p.t)}<small>${esc(p.c)}${p.r ? ' · ' + esc(p.r) : ''}</small></a>`;
  const form = document.querySelector('.busca');
  if (form) {
    const inp = form.querySelector('input'), sug = form.querySelector('.sug');
    let sel = -1;
    inp.addEventListener('input', () => load().then(() => {
      const r = find(inp.value).slice(0, 8);
      sel = -1;
      sug.innerHTML = r.map(row).join('');
      sug.hidden = !r.length;
    }));
    inp.addEventListener('keydown', ev => {
      const as = [...sug.querySelectorAll('a')];
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault();
        sel = Math.max(0, Math.min(as.length - 1, sel + (ev.key === 'ArrowDown' ? 1 : -1)));
        as.forEach((a, i) => a.classList.toggle('on', i === sel));
      } else if (ev.key === 'Enter' && sel >= 0 && as[sel]) {
        ev.preventDefault();
        location.href = as[sel].getAttribute('href');
      } else if (ev.key === 'Escape') sug.hidden = true;
    });
    document.addEventListener('click', ev => { if (!form.contains(ev.target)) sug.hidden = true; });
  }
  const res = document.getElementById('resultados');
  if (res) {
    const q = new URLSearchParams(location.search).get('q') || '';
    const inp = document.querySelector('.busca input');
    if (inp) inp.value = q;
    load().then(() => {
      const r = find(q);
      res.className = 'res';
      res.innerHTML = q ? `<p>${r.length} resultado(s) para “${esc(q)}”.</p>` + r.map(row).join('') : '<p>Digite algo na busca.</p>';
    });
  }
  document.querySelectorAll('[data-filtro]').forEach(inp => inp.addEventListener('input', () => {
    const n = norm(inp.value);
    document.querySelectorAll('table.filt tbody tr').forEach(tr => { tr.hidden = n && !norm(tr.textContent).includes(n); });
  }));
  const btn = document.querySelector('.menu'), side = document.getElementById('side');
  if (btn && side) btn.addEventListener('click', () => {
    const o = side.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(o));
  });
})();
