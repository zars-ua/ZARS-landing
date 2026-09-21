/* Мобільне меню (21.09.2026): кнопка «Меню» у шапці (видима до 1200 px) відкриває повноекранну
   панель з переходами на сторінки проєктів. Панель будується з уже наявних посилань шапки,
   тож список сторінок живе в одному місці. Без JS кнопка нічого не робить, а переходи є в підвалі. */
(() => {
  const bar = document.querySelector('.bar');
  const btn = bar && bar.querySelector('.bar__menu');
  if (!btn) return;
  const here = location.pathname.split('/').pop() || 'index.html';
  const links = [['index.html', 'Девелопер ЗАРС'], ...[...bar.querySelectorAll('.bar__nav a')].map((a) => [a.getAttribute('href'), a.textContent.trim()])];
  const cta = bar.querySelector('.bar__cta');

  const panel = document.createElement('div');
  panel.className = 'menu';
  panel.id = 'site-menu';
  panel.hidden = true;
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'true');
  panel.setAttribute('aria-label', 'Меню');
  panel.innerHTML = `<nav class="menu__nav" aria-label="Сторінки">${links.map(([href, t]) =>
      `<a href="${href}"${href === here ? ' aria-current="page"' : ''}>${t}</a>`).join('')}</nav>
    <div class="menu__foot">${cta ? `<a class="act" href="${cta.getAttribute('href')}">${cta.textContent.trim()}</a>` : ''}
      <a class="menu__tel" href="tel:+380671608877">+380 (67) 160 88 77</a></div>`;
  bar.after(panel);

  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', panel.id);
  const label = btn.textContent;
  let open = false;
  const set = (v) => {
    if (v === open) return;
    open = v;
    btn.setAttribute('aria-expanded', String(v));
    btn.textContent = v ? 'Закрити' : label;
    bar.toggleAttribute('data-menu', v);
    document.documentElement.classList.toggle('menu-open', v);
    if (v) {
      panel.hidden = false;
      requestAnimationFrame(() => { panel.classList.add('is-open'); panel.querySelector('a')?.focus({ preventScroll: true }); });
    } else {
      panel.classList.remove('is-open');
      setTimeout(() => { if (!open) panel.hidden = true; }, 450);
    }
  };
  btn.addEventListener('click', () => set(!open));
  panel.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
  addEventListener('keydown', (e) => {
    if (!open) return;
    if (e.key === 'Escape') { set(false); btn.focus(); }
    if (e.key === 'Tab') {
      const f = [btn, ...panel.querySelectorAll('a')];
      const i = f.indexOf(document.activeElement);
      const n = e.shiftKey ? (i <= 0 ? f.length - 1 : i - 1) : (i === f.length - 1 ? 0 : i + 1);
      e.preventDefault(); f[n].focus();
    }
  });
  matchMedia('(min-width: 1201px)').addEventListener('change', (m) => m.matches && set(false));
})();
