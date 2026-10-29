/* BarkodPRO — site behaviour */
(() => {
  const WA = '994516782878';
  const $ = (s, p = document) => p.querySelector(s);
  const $$ = (s, p = document) => [...p.querySelectorAll(s)];
  const D = window.BP_I18N || { az: {}, ru: {} };
  let lang = 'az';
  try { lang = localStorage.getItem('bp_lang') === 'ru' ? 'ru' : 'az'; } catch (e) {}
  const t = (k) => (D[lang] && D[lang][k] !== undefined ? D[lang][k] : (D.az[k] !== undefined ? D.az[k] : k));
  const page = document.documentElement.dataset.page;

  /* ---------- language ---------- */
  function applyLang() {
    document.documentElement.lang = lang;
    $$('[data-i18n]').forEach(el => { const v = t(el.dataset.i18n); if (v !== undefined) el.innerHTML = v; });
    $$('[data-i18n-ph]').forEach(el => el.setAttribute('placeholder', t(el.dataset.i18nPh)));
    $$('[data-i18n-alt]').forEach(el => el.setAttribute('alt', t(el.dataset.i18nAlt)));
    if (page && D.az[page + '.title']) {
      document.title = t(page + '.title');
      const m = $('meta[name="description"]'); if (m) m.setAttribute('content', t(page + '.desc'));
    }
    $$('.lang button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    setToday();
    if (typeof renderMap === 'function') renderMap();
    if (typeof renderQuote === 'function') renderQuote();
  }
  $$('.lang button').forEach(b => b.addEventListener('click', () => {
    lang = b.dataset.lang;
    try { localStorage.setItem('bp_lang', lang); } catch (e) {}
    applyLang();
  }));

  function setToday() {
    const d = new Date();
    const s = String(d.getDate()).padStart(2, '0') + '.' + String(d.getMonth() + 1).padStart(2, '0') + '.' + d.getFullYear();
    $$('[data-today]').forEach(el => el.textContent = s);
    $$('[data-year]').forEach(el => el.textContent = d.getFullYear());
  }

  /* ---------- header, drawer ---------- */
  const head = $('.site-head'), menuBtn = $('.menu-btn'), drawer = $('#drawer');
  const onScroll = () => head && head.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  menuBtn && menuBtn.addEventListener('click', () => {
    const open = drawer.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });
  $$('#drawer a').forEach(a => a.addEventListener('click', () => { drawer.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }));
  addEventListener('keydown', e => { if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) { drawer.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.focus(); } });

  /* ---------- toast ---------- */
  const toastEl = $('.toast');
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove('show'), 2600);
  }
  const openWA = (text) => window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener');

  /* ---------- service filters ---------- */
  $$('.filters button').forEach(b => b.addEventListener('click', () => {
    const f = b.dataset.filter;
    $$('.filters button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    $$('.svc').forEach(li => { li.hidden = !(f === 'all' || li.dataset.cat === f); });
  }));

  /* ---------- system map ---------- */
  let mapNode = 'kassa';
  var renderMap = function () {
    if (!$('.map')) return;
    $$('.map-node').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.node === mapNode)));
    $$('.wire').forEach(w => w.classList.toggle('on', w.dataset.wire === mapNode));
    $('#mapKind').textContent = t('map.' + mapNode + '.k');
    $('#mapTitle').textContent = t('map.' + mapNode + '.t');
    $('#mapDesc').textContent = t('map.' + mapNode + '.d');
    $('#mapFlow').innerHTML = [0, 1, 2].map(i => '<li><span>0' + (i + 1) + '</span><span>' + t('map.' + mapNode + '.f' + i) + '</span></li>').join('');
    $('#mapLink').hidden = mapNode !== 'tsd';
  };
  $$('.map-node').forEach(b => b.addEventListener('click', () => { mapNode = b.dataset.node; renderMap(); }));

  /* ---------- quote builder ---------- */
  const qf = $('#quoteForm');
  function quoteData() {
    const biz = $('input[name="biz"]:checked', qf);
    const has = $('input[name="has1c"]:checked', qf);
    return {
      biz: biz ? t('q.biz.' + biz.value) : '—',
      needs: $$('input[name="need"]:checked', qf).map(i => t('q.need.' + i.value)),
      kassa: $('#qKassa').value || '0',
      tsd: $('#qTsd').value || '0',
      has: has ? t('q.has1c.' + has.value) : '—',
      name: $('#qName').value.trim(),
      phone: $('#qPhone').value.trim(),
      note: $('#qNote').value.trim()
    };
  }
  var renderQuote = function () {
    if (!qf) return;
    const d = quoteData();
    $('#rcBiz').textContent = d.biz;
    $('#rcNeeds').innerHTML = d.needs.length
      ? d.needs.map(n => '<li><span></span><span>[OK]</span></li>').join('')
      : '<li class="rc-empty"></li>';
    const lis = $$('#rcNeeds li');
    if (d.needs.length) d.needs.forEach((n, i) => lis[i].firstChild.textContent = n);
    else lis[0].textContent = t('js.none');
    $('#rcKassa').textContent = d.kassa; $('#rcTsd').textContent = d.tsd; $('#rcHas').textContent = d.has;
    $('#rcName').textContent = d.name || '—';
  };
  function quoteText() {
    const d = quoteData();
    const L = [t('js.q.head'), '', t('js.q.biz') + ': ' + d.biz,
      t('js.q.needs') + ': ' + (d.needs.length ? d.needs.join(', ') : '—'),
      t('js.q.kassa') + ': ' + d.kassa, t('js.q.tsd') + ': ' + d.tsd, t('js.q.has') + ': ' + d.has];
    if (d.name) L.push(t('js.q.name') + ': ' + d.name);
    if (d.phone) L.push(t('js.q.phone') + ': ' + d.phone);
    if (d.note) L.push(t('js.q.note') + ': ' + d.note);
    return L.join('\n');
  }
  if (qf) {
    qf.addEventListener('input', renderQuote);
    qf.addEventListener('change', renderQuote);
    $$('[data-step]', qf).forEach(b => b.addEventListener('click', () => {
      const inp = document.getElementById(b.dataset.for);
      const v = Math.max(0, Math.min(99, (parseInt(inp.value, 10) || 0) + parseInt(b.dataset.step, 10)));
      inp.value = v; renderQuote();
    }));
    qf.addEventListener('submit', e => { e.preventDefault(); openWA(quoteText()); toast(t('js.sent')); });
    $('#quoteCopy').addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(quoteText()); toast(t('js.copied')); } catch (err) { openWA(quoteText()); }
    });
  }

  /* ---------- contact form ---------- */
  const cf = $('#contactForm');
  cf && cf.addEventListener('submit', e => {
    e.preventDefault();
    const n = $('#cName').value.trim(), p = $('#cPhone').value.trim(), m = $('#cMsg').value.trim();
    let s = t('js.c.head');
    if (n) s += '\n' + t('js.q.name') + ': ' + n;
    if (p) s += '\n' + t('js.q.phone') + ': ' + p;
    if (m) s += '\n' + t('js.c.msg') + ': ' + m;
    openWA(s); toast(t('js.sent'));
  });

  /* ---------- lightbox ---------- */
  const lb = $('#lightbox');
  if (lb && lb.showModal) {
    const img = $('img', lb);
    $$('[data-zoom]').forEach(b => b.addEventListener('click', () => {
      const src = $('img', b); img.src = b.dataset.zoom; img.alt = src ? src.alt : ''; lb.showModal();
    }));
    $('button', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
  }

  /* ---------- login (demo) ---------- */
  const lf = $('#loginForm');
  lf && lf.addEventListener('submit', e => {
    e.preventDefault();
    const user = $('#lgUser').value.trim() || 'Müştəri';
    const btn = $('#lgBtn'); btn.disabled = true; btn.textContent = t('js.lg.wait');
    try { sessionStorage.setItem('barkodpro_demo_user', user); } catch (err) {}
    setTimeout(() => { location.href = 'dashboard.html'; }, 600);
  });

  applyLang();
})();
