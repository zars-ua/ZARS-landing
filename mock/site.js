/* Поведінка сторінок будинків: вибір планування, лайтбокс, форма. Без залежностей.
   Без JS: усі планування видно списком, фото — звичайні зображення, форма веде на телефон. */
(() => {
  const PHONE = '+380 (67) 160 88 77';

  /* ---------- Планування ---------- */
  document.querySelectorAll('[data-plans]').forEach((root) => {
    const tabs = [...root.querySelectorAll('.plans__tab')];
    const stage = root.querySelector('.plans__stage');
    /* слайд — або <img>, або .planvid з відео (23.09.2026) */
    const slides = [...stage.children];
    const imgs = slides.map((el) => (el.tagName === 'IMG' ? el : el.querySelector('img')));
    const area = root.querySelector('.plans__area');
    const info = root.querySelector('.plans__info');
    const desc = root.querySelector('.plans__desc');
    const select = (i, focus) => {
      tabs.forEach((t, k) => {
        t.setAttribute('aria-selected', String(k === i));
        t.tabIndex = k === i ? 0 : -1;
      });
      if (slides[i].hidden) {
        slides.forEach((el, k) => { if (k !== i) stopPlanVideo(el); });
        const im = imgs[i];
        if (im && !im.complete) {
          stage.setAttribute('data-loading', '');
          im.loading = 'eager';
          im.addEventListener('load', () => {
            slides.forEach((el, k) => { el.hidden = k !== i; });
            stage.removeAttribute('data-loading');
          }, { once: true });
        } else {
          slides.forEach((el, k) => { el.hidden = k !== i; });
          stage.removeAttribute('data-loading');
        }
      }
      area.textContent = tabs[i].dataset.area;
      info.textContent = tabs[i].dataset.info;
      if (desc) { desc.textContent = tabs[i].dataset.desc || ''; desc.hidden = !tabs[i].dataset.desc; }
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', (e) => {
        const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); select((i + d + tabs.length) % tabs.length, true); }
      });
    });
    slides.forEach((el, k) => { el.hidden = k !== 0; });
    select(0);
    root.querySelector('.zoom')?.addEventListener('click', () => {
      const cur = slides.find((el) => !el.hidden);
      const im = cur.tagName === 'IMG' ? cur : null;
      openLightbox([{ src: cur.dataset.full || (im && (im.dataset.full || im.currentSrc || im.src)), alt: cur.dataset.alt || (im && im.alt) || '' }], 0, true);
    });
  });

  /* ---------- Анімація планування: запускає відвідувач, без автоплею ---------- */
  const stopPlanVideo = (el) => {
    const v = el && el.querySelector && el.querySelector('video');
    if (!v) return;
    v.pause(); v.currentTime = 0; el.removeAttribute('data-playing');
  };
  document.querySelectorAll('.planvid').forEach((box) => {
    const v = box.querySelector('video');
    const btn = box.querySelector('.planvid__play');
    const toggle = () => {
      if (v.paused) { box.setAttribute('data-playing', ''); v.play().catch(() => box.removeAttribute('data-playing')); }
      else { v.pause(); box.removeAttribute('data-playing'); }
    };
    btn.addEventListener('click', toggle);
    v.addEventListener('click', toggle);
    v.addEventListener('ended', () => { v.currentTime = 0; box.removeAttribute('data-playing'); });
    v.addEventListener('pause', () => box.removeAttribute('data-playing'));
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
    dlg.addEventListener('close', () => { document.documentElement.style.overflow = ''; window.__lenis?.start(); opener?.focus(); });
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
    window.__lenis?.stop();
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


/* ---------- Розділи про будинки: активний розділ міняє кадр ---------- */
(() => {
  document.querySelectorAll('[data-chapters]').forEach((root) => {
    const figs = [...root.querySelectorAll('.chapters__media figure')];
    const arts = [...root.querySelectorAll('.chapter')];
    let cur = -1;
    const show = (i) => {
      if (i === cur) return;
      figs.forEach((f, k) => { f.toggleAttribute('data-was', k === cur); f.toggleAttribute('data-active', k === i); });
      arts.forEach((a, k) => a.toggleAttribute('data-active', k === i));
      cur = i;
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) show(arts.indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    arts.forEach((a) => io.observe(a));
    show(0);
  });
})();

/* ---------- Карусель переваг ФБ29Б (21.09.2026) ----------
   Нативний горизонтальний скрол зі scroll-snap: свайп, трекпад, клавіатура; стрілки гортають
   на одну картку, смуга показує видиму частину стрічки. Без JS — звичайна стрічка зі свайпом. */
(() => {
  document.querySelectorAll('[data-perks]').forEach((root) => {
    const track = root.querySelector('.perks__track');
    const cards = [...track.children];
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    const fill = root.querySelector('.perks__bar i');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const step = () => (cards[1] ? cards[1].offsetLeft - cards[0].offsetLeft : track.clientWidth);
    let raf = 0;
    const paint = () => {
      const max = track.scrollWidth - track.clientWidth;
      const vis = track.clientWidth / track.scrollWidth;
      const p = max > 0 ? track.scrollLeft / max : 0;
      fill.style.width = `${vis * 100}%`;
      fill.style.transform = `translateX(${(p * (1 - vis) / vis) * 100}%)`;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max - 2;
    };
    const by = (d) => track.scrollBy({ left: d * step(), behavior: reduce ? 'auto' : 'smooth' });
    prev.addEventListener('click', () => by(-1));
    next.addEventListener('click', () => by(1));
    track.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); by(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); by(-1); }
    });
    track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(paint); }, { passive: true });
    addEventListener('resize', paint);
    // перетягування мишею на ПК; після відпускання — доводка до найближчої картки
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = track.scrollLeft; });
    addEventListener('pointermove', (e) => {
      if (!down) return;
      const dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 4) { moved = true; track.classList.add('is-drag'); }
      if (moved) track.scrollLeft = sl - dx;
    });
    addEventListener('pointerup', () => {
      if (!down) return;
      down = false;
      if (!moved) return;
      const s = step(), i = Math.round(track.scrollLeft / s);
      track.classList.remove('is-drag');
      track.scrollTo({ left: i * s, behavior: reduce ? 'auto' : 'smooth' });
    });
    track.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    paint();
  });
})();
