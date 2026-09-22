/* Рух макета: GSAP + ScrollTrigger (прокрутка нативна). Без JS сторінка
   показує кінцевий стан (весь текст, фото без вуалі). */
(() => {
  const bar = document.querySelector('.bar');

  // Шапка: суцільна, щойно перший екран пішов
  const stickAfter = document.querySelector('[data-stick-after]') || document.querySelector('.hero, .intro');
  if (bar && stickAfter) {
    new IntersectionObserver(([e]) => {
      bar.toggleAttribute('data-stuck', !e.isIntersecting);
    }, { rootMargin: `-${bar.offsetHeight}px 0px 0px 0px` }).observe(stickAfter);
  }

  /* Як і на сторінці девелопера: сценарні ефекти (паралакс, проявлення) працюють і з prefers-reduced-motion —
     саме так виглядає Windows із вимкненими «ефектами анімації», і клієнт бачив там сторінку без паралаксу. */
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('motion');

  /* Прокрутка — нативна браузерна (21.09.2026), як на arccagroup.us (еталон клієнта):
     Lenis прибрано — він рухав сторінку з головного потоку й смикався на слабших Windows-ПК. */

  /* 1. Літери ЗАРС як вікно. Світла вуаль кольору сторінки з вирізаними літерами;
        прокрутка збільшує знак довкола точки всередині ніжки «Р», доки проріз не заповнить екран. */
  const intro = document.querySelector('[data-intro]');
  if (intro) {
    const svg = intro.querySelector('.intro__veil');
    const letters = svg.querySelector('.intro__letters');
    const use = letters.querySelector('use');
    const VB = { x: 32, y: 32, w: 5120, h: 756 };       // viewBox знака
    const STEM = { x: 2844, y: 420 };                     // ніжка «Р» у координатах знака
    const layout = () => {
      const W = innerWidth, H = innerHeight;
      const lw = Math.min(W * (W < 700 ? 0.86 : 0.7), 1180), lh = lw * VB.h / VB.w;
      const x = (W - lw) / 2, y = (H - lh) / 2 - H * 0.04;
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      use.setAttribute('x', x); use.setAttribute('y', y);
      use.setAttribute('width', lw); use.setAttribute('height', lh);
      return { ox: x + (STEM.x - VB.x) / VB.w * lw, oy: y + (STEM.y - VB.y) / VB.h * lh };
    };
    let o = layout();
    gsap.set(letters, { svgOrigin: `${o.ox} ${o.oy}`, scale: 1 });
    const body = intro.querySelector('.hero__body');
    const hint = intro.querySelector('.intro__hint');
    gsap.set(body, { autoAlpha: 0, y: 30 });
    bar && bar.setAttribute('data-on-veil', '');

    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: intro, start: 'top top', end: '+=160%', scrub: 0.8, pin: true, anticipatePin: 1,
        invalidateOnRefresh: true,
        onRefresh: () => { o = layout(); gsap.set(letters, { svgOrigin: `${o.ox} ${o.oy}`, smoothOrigin: false, x: 0, y: 0 }); },
        onUpdate: (st) => bar && bar.toggleAttribute('data-on-veil', st.progress < 0.42),
      },
    });
    tl.to(hint, { autoAlpha: 0, duration: 0.08 }, 0)
      .to(letters, { scale: 90, duration: 0.62, ease: 'power3.in' }, 0)
      .to(svg, { autoAlpha: 0, duration: 0.08 }, 0.56)
      .fromTo(intro.querySelector('.hero__media'), { scale: 1.12 }, { scale: 1, duration: 0.7, ease: 'power2.out' }, 0)
      .to(body, { autoAlpha: 1, y: 0, duration: 0.24, ease: 'power2.out' }, 0.7);
  }

  /* 2. Текст, що проявляється словами за прокруткою (з сірого в чорнило) */
  document.querySelectorAll('[data-reveal-words]').forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach((w, i) => {
      const s = document.createElement('span');
      s.className = 'w';
      s.textContent = w;
      el.append(s, i < words.length - 1 ? ' ' : '');
    });
    gsap.fromTo(el.querySelectorAll('.w'), { opacity: 0.16 }, {
      opacity: 1, stagger: 0.06, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 45%', scrub: true },
    });
  });

  /* 3. Рядки, що виходять із-під маски по черзі */
  document.querySelectorAll('[data-reveal-lines]').forEach((el) => {
    const lines = el.querySelectorAll('.line > span');
    gsap.fromTo(lines, { yPercent: 110 }, {
      yPercent: 0, duration: 1.4, stagger: 0.18, ease: 'expo.out',
      scrollTrigger: { trigger: el, start: 'top 75%', once: true },
    });
  });

  /* 4. Панелі в дусі Rolex: фото тече всередині рамки, підпис проявляється і гасне */
  document.querySelectorAll('.pan').forEach((pan) => {
    const img = pan.querySelector('img');
    const cap = pan.querySelector('.pan__cap');
    /* .pan--top кадровано до верхнього краю — фото тільки підіймається, верх кадру видно на вході */
    const top = pan.classList.contains('pan--top');
    /* ФБ29Б: запас фото 12% (а не 24%), тож і хід паралаксу менший — інакше край фото вилазить у кадр */
    const amp = ['fb29b', 'fb29'].includes(document.documentElement.dataset.site) ? 8 : 9;
    /* scrub 0,5 — невелике згладження: без Lenis коліщатко на Windows іде кроками по 100px, і без нього паралакс «стрибав» */
    gsap.fromTo(img, { yPercent: top ? 0 : -amp }, {
      yPercent: top ? -amp * 2 : amp, ease: 'none',
      scrollTrigger: { trigger: pan, start: 'top bottom', end: 'bottom top', scrub: 0.5 },
    });
    if (!cap) return;
    gsap.timeline({ scrollTrigger: { trigger: pan, start: 'top 85%', end: 'bottom 15%', scrub: true } })
      .fromTo(cap, { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, ease: 'power2.out', duration: 0.35 })
      .to(cap, { autoAlpha: 1, y: -10, duration: 0.4, ease: 'none' })
      .to(cap, { autoAlpha: 0, y: -40, duration: 0.25, ease: 'power1.in' });
  });


  /* 5б. Схема розташування ФБ29Б — та сама анімація, що на zars.ua/objects/fr29b (їхній script.js):
         схема «опускається» з повороту й збільшення, потім підписи по черзі виїжджають справа. */
  document.querySelectorAll('[data-loc]').forEach((schema) => {
    gsap.timeline({ scrollTrigger: { trigger: schema.closest('.loc') || schema, start: 'top center', once: true } })
      .from(schema, { y: -100, autoAlpha: 0, scale: 1.4, rotation: 16, duration: 1.4, ease: 'power1.out' })
      .from(schema.querySelectorAll('.loc__label'), { autoAlpha: 0, x: 100, duration: 0.6, stagger: 0.2, ease: 'power1.out' });
  });

  /* 5в. Стадія будівництва ФБ29Б: кадри розкриваються знизу по черзі, фото всередині «сідає» зі збільшення;
         далі за прокруткою парні кадри йдуть повільніше за непарні, а фото тече всередині рамки. */
  document.querySelectorAll('[data-stage]').forEach((grid) => {
    const frames = [...grid.querySelectorAll('.stage__frame')];
    const imgs = frames.map((f) => f.querySelector('img'));
    gsap.timeline({ scrollTrigger: { trigger: grid, start: 'top 82%', once: true } })
      .fromTo(frames, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, stagger: 0.14, ease: 'expo.inOut' })
      .fromTo(imgs, { scale: 1.3 }, { scale: 1, duration: 1.9, stagger: 0.14, ease: 'expo.out' }, 0.25);
    frames.forEach((f, i) => {
      gsap.fromTo(f, { y: i % 2 ? 50 : 0 }, { y: i % 2 ? -30 : 0, ease: 'none', scrollTrigger: { trigger: grid, start: 'top bottom', end: 'bottom top', scrub: true } });
      gsap.fromTo(imgs[i], { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: f, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  });

  /* Знак ЗАРС у підвалі виїжджає знизу, коли сторінку докручено (як на сторінці девелопера) */
  const footMark = document.querySelector('.d-foot__mark svg');
  footMark && gsap.fromTo(footMark, { yPercent: 100 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: footMark.parentElement, start: 'top bottom', end: 'bottom bottom', scrub: true } });

  /* 5г. Схема ФБ29 — як на zars.ua/objects/f29 (їхній main.js): поверх підкладки по черзі проявляються
         будинок, пам'ятки й лінії, по 0,5 с. Додано легкий «наплив» знизу. */
  document.querySelectorAll('[data-map29]').forEach((m) => {
    const layers = ['.map29__building', '.map29__attr', '.map29__lines'].map((q) => m.querySelector(q));
    gsap.timeline({ scrollTrigger: { trigger: m, start: 'top 70%', once: true } })
      .from(m.querySelector('.map29__base'), { autoAlpha: 0, y: 40, duration: 1, ease: 'power2.out' })
      .from(layers, { autoAlpha: 0, y: 14, duration: 0.5, stagger: 0.5, ease: 'power1.out' }, 0.5);
  });
  /* Відзнака ФБ29: паралакс фото, стрічки «спускаються» по черзі */
  document.querySelectorAll('.award').forEach((aw) => {
    const img = aw.querySelector('.award__media img');
    img && gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: aw, start: 'top bottom', end: 'bottom top', scrub: 0.5 } });
    gsap.timeline({ scrollTrigger: { trigger: aw, start: 'top 65%', once: true } })
      .from(aw.querySelectorAll('.award__text > *'), { autoAlpha: 0, y: 30, duration: 1, stagger: 0.12, ease: 'expo.out' })
      .from(aw.querySelectorAll('.award__ribbons figure'), { yPercent: -30, autoAlpha: 0, duration: 1.1, stagger: 0.14, ease: 'expo.out' }, 0.2);
  });

  /* 6. Будинки Каркашадзе: кадри змінюються вбік за прокруткою (Rolex, горизонтально) */
  document.querySelectorAll('[data-dk]').forEach((dk) => {
    const slides = [...dk.querySelectorAll('.dk__slide')];
    const n = slides.length;
    if (n < 2) return;
    const ticks = [...dk.querySelectorAll('.dk__tick')];
    const cur = dk.querySelector('.dk__cur');
    const span = dk.querySelector('.dk__span');
    const fill = dk.querySelector('.dk__fill');
    const imgs = slides.map((s) => s.querySelector('img'));
    const caps = slides.map((s) => s.querySelector('.dk__cap'));
    let active = -1;
    const setActive = (i) => {
      if (i === active) return;
      active = i;
      cur.textContent = String(i + 1).padStart(2, '0');
      span.textContent = slides[i].dataset.years;
      ticks.forEach((t, k) => t.setAttribute('aria-current', String(k === i)));
    };
    gsap.set(slides, { zIndex: (k) => k + 1 });
    gsap.set(slides.slice(1), { clipPath: 'inset(0% 0% 0% 100%)' });
    gsap.set(imgs.slice(1), { xPercent: 18 });
    gsap.set(caps.slice(1), { autoAlpha: 0, x: 80 });
    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: dk, start: 'top top', end: () => '+=' + innerHeight * (n - 1) * 0.85,
        pin: true, scrub: 0.7, invalidateOnRefresh: true, anticipatePin: 1,
        snap: { snapTo: 1 / (n - 1), duration: { min: 0.3, max: 0.8 }, delay: 0.08, ease: 'power2.inOut' },
        onUpdate: (st) => { fill.style.transform = `scaleX(${st.progress})`; setActive(Math.round(st.progress * (n - 1))); },
      },
    });
    for (let i = 1; i < n; i++) {
      const t = i - 1;
      tl.to(slides[i], { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'power1.inOut' }, t)
        .to(imgs[i], { xPercent: 0, duration: 1, ease: 'power1.out' }, t)
        .to(imgs[i - 1], { xPercent: -12, duration: 1, ease: 'power1.in' }, t)
        .to(caps[i - 1], { autoAlpha: 0, x: -60, duration: 0.35 }, t)
        .to(caps[i], { autoAlpha: 1, x: 0, duration: 0.45, ease: 'power2.out' }, t + 0.55);
    }
    setActive(0);
    ticks.forEach((tk, i) => tk.addEventListener('click', () => {
      const st = tl.scrollTrigger;
      const y = st.start + (st.end - st.start) * (i / (n - 1));
      window.scrollTo({ top: y, behavior: 'smooth' });
    }));
  });

  /* 7. Фото маніфесту і матеріалів течуть усередині рамки */
  document.querySelectorAll('.manifest, .holding__photo, .material__frame').forEach((frame) => {
    const img = frame.querySelector('img');
    img && gsap.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none',
      scrollTrigger: { trigger: frame, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  document.querySelectorAll('.holding__photo, .founder__frame').forEach((frame) => {
    gsap.fromTo(frame, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.6, ease: 'expo.inOut',
      scrollTrigger: { trigger: frame, start: 'top 82%', once: true } });
  });

  /* 5. Проєкти розкриваються з арки (силует куполів ФБ29) у повний кадр */
  document.querySelectorAll('[data-arch]').forEach((el) => {
    const s = { side: 30, top: 14, r: 50 };
    const apply = () => {
      el.style.clipPath = `inset(${s.top}% ${s.side}% 0% ${s.side}% round ${s.r}vw ${s.r}vw 0 0)`;
    };
    apply();
    gsap.to(s, {
      side: 0, top: 0, r: 0, ease: 'power2.inOut', onUpdate: apply,
      scrollTrigger: { trigger: el, start: 'top 90%', end: 'top 15%', scrub: true },
    });
    const img = el.querySelector('img');
    img && gsap.fromTo(img, { scale: 1.25 }, {
      scale: 1, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true },
    });
  });
})();

/* Якірні посилання (#presentation, #contacts) — плавно, нативним скролом, з відступом під шапку.
   CSS scroll-behavior:smooth не вмикаємо: він ламає ScrollTrigger.refresh (той сам прокручує сторінку). */
document.addEventListener('click', (e) => {
  const a = e.target.closest('a[href^="#"]');
  if (!a || a.getAttribute('href').length < 2) return;
  const t = document.querySelector(a.getAttribute('href'));
  if (!t) return;
  e.preventDefault();
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top: t.getBoundingClientRect().top + scrollY, behavior: reduce ? 'auto' : 'smooth' });
  history.replaceState(null, '', a.getAttribute('href'));
});
