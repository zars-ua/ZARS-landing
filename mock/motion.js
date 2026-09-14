/* Рух макета: GSAP + ScrollTrigger + Lenis. Без JS і з prefers-reduced-motion сторінка
   показує кінцевий стан (весь текст, фото без вуалі). */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const bar = document.querySelector('.bar');

  // Шапка: суцільна, щойно перший екран пішов
  const stickAfter = document.querySelector('[data-stick-after]') || document.querySelector('.hero, .intro');
  if (bar && stickAfter) {
    new IntersectionObserver(([e]) => {
      bar.toggleAttribute('data-stuck', !e.isIntersecting);
    }, { rootMargin: `-${bar.offsetHeight}px 0px 0px 0px` }).observe(stickAfter);
  }

  if (reduce || !window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('motion');

  // Плавна прокрутка
  if (window.Lenis) {
    const lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 0.9 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

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
        onRefresh: () => { o = layout(); gsap.set(letters, { svgOrigin: `${o.ox} ${o.oy}` }); },
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
    gsap.fromTo(img, { yPercent: -9 }, {
      yPercent: 9, ease: 'none',
      scrollTrigger: { trigger: pan, start: 'top bottom', end: 'bottom top', scrub: true },
    });
    if (!cap) return;
    gsap.timeline({ scrollTrigger: { trigger: pan, start: 'top 85%', end: 'bottom 15%', scrub: true } })
      .fromTo(cap, { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, ease: 'power2.out', duration: 0.35 })
      .to(cap, { autoAlpha: 1, y: -10, duration: 0.4, ease: 'none' })
      .to(cap, { autoAlpha: 0, y: -40, duration: 0.25, ease: 'power1.in' });
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
