/* Поведінка сторінок будинків: вибір планування, лайтбокс, форма. Без залежностей.
   Без JS: усі планування видно списком, фото — звичайні зображення, форма веде на телефон. */
(() => {
  const PHONE = '+380 (67) 160 88 77';

  /* ---------- Планування ---------- */
  document.querySelectorAll('[data-plans]').forEach((root) => {
    const tabs = [...root.querySelectorAll('.plans__tab')];
    const stage = root.querySelector('.plans__stage');
    const imgs = [...stage.querySelectorAll('img')];
    const area = root.querySelector('.plans__area');
    const info = root.querySelector('.plans__info');
    const select = (i, focus) => {
      tabs.forEach((t, k) => {
        t.setAttribute('aria-selected', String(k === i));
        t.tabIndex = k === i ? 0 : -1;
      });
      if (imgs[i].hidden) {
        stage.setAttribute('data-loading', '');
        const show = () => {
          imgs.forEach((im, k) => { im.hidden = k !== i; });
          stage.removeAttribute('data-loading');
        };
        imgs[i].complete ? show() : imgs[i].addEventListener('load', show, { once: true });
        imgs[i].loading = 'eager';
      }
      area.textContent = tabs[i].dataset.area;
      info.textContent = tabs[i].dataset.info;
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); select((i + d + tabs.length) % tabs.length, true); }
      });
    });
    imgs.forEach((im, k) => { im.hidden = k !== 0; });
    select(0);
    root.querySelector('.zoom')?.addEventListener('click', () => {
      const cur = imgs.find((im) => !im.hidden);
      openLightbox([{ src: cur.dataset.full || cur.currentSrc || cur.src, alt: cur.alt }], 0, true);
    });
  });

  /* ---------- Лайтбокс ---------- */
  let dlg, dlgImg, dlgCap, list = [], idx = 0, opener = null;
  const build = () => {
    dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.setAttribute('aria-label', 'Перегляд зображення');
    const close = document.createElement('button');
    close.className = 'lightbox__close'; close.type = 'button'; close.textContent = 'Закрити';
    dlgImg = document.createElement('img');
    dlgCap = document.createElement('p'); dlgCap.className = 'lightbox__cap';
    const nav = document.createElement('div'); nav.className = 'lightbox__nav';
    const prev = document.createElement('button'); prev.type = 'button'; prev.textContent = '←'; prev.setAttribute('aria-label', 'Попереднє');
    const next = document.createElement('button'); next.type = 'button'; next.textContent = '→'; next.setAttribute('aria-label', 'Наступне');
    nav.append(prev, next);
    dlg.append(close, dlgImg, dlgCap, nav);
    document.body.append(dlg);
    close.addEventListener('click', () => dlg.close());
    prev.addEventListener('click', () => show(idx - 1));
    next.addEventListener('click', () => show(idx + 1));
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
    dlg.addEventListener('close', () => { document.documentElement.style.overflow = ''; opener?.focus(); });
    dlg._nav = nav;
  };
  const show = (i) => {
    idx = (i + list.length) % list.length;
    dlgImg.src = list[idx].src; dlgImg.alt = list[idx].alt || '';
    dlgCap.textContent = list[idx].alt || '';
  };
  function openLightbox(items, i, plan) {
    if (!dlg) build();
    opener = document.activeElement;
    list = items; dlg.classList.toggle('lightbox--plan', !!plan);
    dlg._nav.hidden = items.length < 2;
    show(i);
    document.documentElement.style.overflow = 'hidden';
    dlg.showModal();
  }
  document.querySelectorAll('[data-gallery]').forEach((g) => {
    const figs = [...g.querySelectorAll('figure')];
    const items = figs.map((f) => {
      const im = f.querySelector('img');
      return { src: im.dataset.full || im.currentSrc || im.src, alt: im.alt };
    });
    figs.forEach((f, i) => {
      f.tabIndex = 0;
      f.setAttribute('role', 'button');
      const open = () => {
        const im = f.querySelector('img');
        items[i].src = im.dataset.full || im.currentSrc || im.src;
        openLightbox(items, i);
      };
      f.addEventListener('click', open);
      f.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
  });

  /* ---------- Форма: чесний стан, поки не підключено приймач заявок ---------- */
  document.querySelectorAll('[data-enquiry]').forEach((form) => {
    const msg = form.querySelector('.form__msg');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const phone = form.querySelector('input[type="tel"]');
      if (!phone.value.replace(/\D/g, '').match(/^\d{9,13}$/)) {
        msg.textContent = 'Вкажіть номер телефону, щоб ми могли Вам передзвонити.';
        phone.focus();
        return;
      }
      msg.textContent = `Онлайн-заявки ще не підключено. Будь ласка, зателефонуйте: ${PHONE}.`;
    });
  });
})();

/* ---------- Карусель Будинків Каркашадзе ----------
   Нативна прокрутка зі scroll-snap (свайп, трекпад, клавіатура), стрілки,
   лічильник і лінія прогресу. Без JS — звичайна горизонтальна стрічка. */
(() => {
  document.querySelectorAll('[data-houses]').forEach((root) => {
    const track = root.querySelector('.houses__track');
    const slides = [...track.children];
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    const cur = root.querySelector('.houses__cur');
    const bar = root.querySelector('.houses__bar i');
    const pad = (n) => String(n).padStart(2, '0');
    let idx = 0, raf = 0;

    const nearest = () => {
      const x = track.scrollLeft + track.clientWidth * 0.08;
      let best = 0, d = Infinity;
      slides.forEach((s, i) => { const dd = Math.abs(s.offsetLeft - track.offsetLeft - x); if (dd < d) { d = dd; best = i; } });
      return best;
    };
    const paint = () => {
      idx = nearest();
      cur.textContent = pad(idx + 1);
      bar.style.transform = `scaleX(${(idx + 1) / slides.length})`;
      slides.forEach((s, i) => s.toggleAttribute('data-active', i === idx));
      prev.disabled = idx === 0;
      next.disabled = idx === slides.length - 1;
    };
    const go = (i) => {
      const t = slides[Math.max(0, Math.min(slides.length - 1, i))];
      track.scrollTo({ left: t.offsetLeft - track.offsetLeft, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    };
    track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(paint); }, { passive: true });
    prev.addEventListener('click', () => go(idx - 1));
    next.addEventListener('click', () => go(idx + 1));
    root.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
    });
    // перетягування мишею на десктопі
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = track.scrollLeft; track.classList.add('is-drag'); });
    window.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; track.scrollLeft = sl - dx; });
    window.addEventListener('pointerup', () => { if (!down) return; down = false; track.classList.remove('is-drag'); go(nearest()); });
    track.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    root.classList.add('houses--ready');
    paint();
  });
})();
