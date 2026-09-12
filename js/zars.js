/* =============================================================
   ЗАРС — поведінка сайту. Без залежностей.
   ============================================================= */
(() => {
  'use strict';

  /* ---------------------------------------------------------
     КУДИ ЙДУТЬ ЗАЯВКИ

     Вставте сюди адресу веб-застосунку Google Apps Script, який
     пересилає заявку в Telegram-канал. Токен бота лишається на
     боці скрипта і ніколи не потрапляє в код сайту.

     Поки рядок порожній, форма чесно каже відвідувачеві
     зателефонувати і не вдає, що заявку надіслано.
     --------------------------------------------------------- */
  const LEAD_ENDPOINT = '';

  const SALES_PHONE = '+380 48 788-77-77';
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Шапка: фон з'являється, щойно сторінка зрушила ---------- */
  const top = document.getElementById('top');
  if (top) {
    const sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px';
    document.body.prepend(sentinel);
    new IntersectionObserver(
      ([e]) => top.toggleAttribute('data-stuck', !e.isIntersecting),
      { threshold: 0 }
    ).observe(sentinel);
  }

  /* ---------- Нанесення на карту: секції з'являються при прокрутці ---------- */
  const plots = document.querySelectorAll('.plot');
  if (calm) {
    plots.forEach((el) => el.classList.add('plot--in'));
  } else {
    // Те, що вже у першому екрані, показуємо негайно: чекати на
    // спостерігача означало б тримати героя порожнім зайві частки секунди.
    const fold = innerHeight;
    plots.forEach((el) => {
      if (el.getBoundingClientRect().top < fold) el.classList.add('plot--in');
    });
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add('plot--in');
        io.unobserve(e.target);
      }),
      { rootMargin: '0px 0px -12% 0px', threshold: 0.08 }
    );
    plots.forEach((el) => {
      if (!el.classList.contains('plot--in')) io.observe(el);
    });
  }

  /* ---------- Берег: лінія наноситься, орієнтир пульсує ---------- */
  const map = document.querySelector('[data-map]');
  if (map) {
    const lines = map.querySelectorAll('.coast__line path, .coast__street path');
    if (!calm) {
      lines.forEach((p) => {
        const len = p.getTotalLength();
        p.style.strokeDasharray = len;
        p.style.strokeDashoffset = len;
        p.style.transition = 'stroke-dashoffset 2600ms cubic-bezier(0.16,1,0.3,1)';
      });
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          lines.forEach((p) => { p.style.strokeDashoffset = '0'; });
        });
      });
    }
    // орієнтир будинку, чия сторінка зараз відкрита, — живий
    const here = document.documentElement.dataset.chart;
    const live = map.querySelector(`[data-mark="${here}"]`);
    if (live && !calm) live.classList.add('mark--live');
    // на головній оживає той, на який навели в легенді
    document.querySelectorAll('[data-legend]').forEach((link) => {
      const dot = map.querySelector(`[data-mark="${link.dataset.legend}"]`);
      if (!dot) return;
      const on = () => dot.classList.add('mark--live');
      const off = () => dot.classList.remove('mark--live');
      link.addEventListener('pointerenter', on);
      link.addEventListener('focus', on);
      link.addEventListener('pointerleave', off);
      link.addEventListener('blur', off);
    });
  }

  /* ---------- Планування: вибір секції та поверху ---------- */
  document.querySelectorAll('[data-plate]').forEach((root) => {
    const data = JSON.parse(root.querySelector('[data-plate-data]').textContent);
    const img = root.querySelector('[data-plate-img]');
    const cap = root.querySelector('[data-plate-cap]');
    const groupBtns = [...root.querySelectorAll('[data-group]')];
    const levelBtns = [...root.querySelectorAll('[data-level]')];
    let group = groupBtns.length ? groupBtns[0].dataset.group : '';
    let level = levelBtns.length ? levelBtns[0].dataset.level : '';

    const show = () => {
      const id = group ? `${group}-${level}` : level;
      const plan = data[id];
      if (!plan) return;
      const want = `assets/plans/${id}-1200.webp`;
      cap.textContent = plan.cap;
      img.dataset.shot = `assets/plans/${id}-2400.webp`;
      groupBtns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.group === group)));
      levelBtns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.level === level)));
      if (img.getAttribute('src') === want) return;   // цей план уже на екрані

      // Попередній план лишається видимим, поки новий не завантажиться, —
      // плита ніколи не блимає порожнечею.
      img.dataset.loading = '1';
      const next = new Image();
      next.onload = next.onerror = () => {
        img.style.aspectRatio = String(plan.ratio);
        img.src = want;
        img.srcset = next.srcset;
        img.alt = plan.alt;
        delete img.dataset.loading;
      };
      next.srcset = `assets/plans/${id}-1200.webp 1200w, assets/plans/${id}-2400.webp 2400w`;
      next.sizes = img.sizes || '(max-width: 900px) 92vw, 62vw';
      next.src = want;
    };

    groupBtns.forEach((b) => b.addEventListener('click', () => { group = b.dataset.group; show(); }));
    levelBtns.forEach((b) => b.addEventListener('click', () => { level = b.dataset.level; show(); }));
    show();
  });

  /* ---------- Заявка ---------- */
  document.querySelectorAll('[data-lead-form]').forEach((form) => {
    const note = form.querySelector('[data-note]');
    const button = form.querySelector('button[type="submit"]');

    const say = (text, state) => {
      note.textContent = text;
      if (state) note.setAttribute('data-state', state);
      else note.removeAttribute('data-state');
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (form.querySelector('.hp input').value) return;   // пастка для ботів

      const phone = form.elements.phone.value.trim();
      if (phone.replace(/\D/g, '').length < 9) {
        say('Перевірте, будь ласка, номер телефону.', 'err');
        form.elements.phone.focus();
        return;
      }

      if (!LEAD_ENDPOINT) {
        say(`Форма ще не підключена. Зателефонуйте, будь ласка: ${SALES_PHONE}`, 'err');
        return;
      }

      button.disabled = true;
      say('Надсилаємо…');
      try {
        await fetch(LEAD_ENDPOINT, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify({
            name: form.elements.name.value.trim(),
            phone,
            object: form.elements.object ? form.elements.object.value : '',
            comment: form.elements.comment.value.trim(),
            page: location.pathname,
            at: new Date().toISOString(),
          }),
        });
        form.reset();
        say('Дякуємо. Консультант зателефонує найближчим часом.');
      } catch (err) {
        say(`Не вдалося надіслати. Зателефонуйте, будь ласка: ${SALES_PHONE}`, 'err');
      } finally {
        button.disabled = false;
      }
    });
  });

  /* ---------- Галерея: перегляд на весь екран ---------- */
  const shots = document.querySelectorAll('[data-shot]');
  if (shots.length) {
    const box = document.createElement('div');
    box.className = 'lightbox';
    box.hidden = true;
    box.innerHTML =
      '<button class="lightbox__close" type="button" aria-label="Закрити">✕</button>' +
      '<img alt="">';
    document.body.append(box);
    const big = box.querySelector('img');
    let opener = null;

    const close = () => {
      box.hidden = true;
      document.documentElement.style.overflow = '';
      if (opener) opener.focus();
    };
    shots.forEach((s) => s.addEventListener('click', () => {
      const pic = s.tagName === 'IMG' ? s : s.querySelector('img');
      big.src = s.dataset.shot || pic.currentSrc || pic.src;
      big.alt = pic.alt;
      opener = s;
      box.hidden = false;
      document.documentElement.style.overflow = 'hidden';
      box.querySelector('.lightbox__close').focus();
    }));
    box.addEventListener('click', (e) => {
      if (e.target === box || e.target.closest('.lightbox__close')) close();
    });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && !box.hidden) close(); });
  }
})();
