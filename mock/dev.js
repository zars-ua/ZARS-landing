/* Сторінка девелопера: рух (17.09.2026).
   Сценарні блоки (інтро, переваги, логотип у підвалі) працюють на всіх системах:
   ними керує прокрутка самого відвідувача. Якщо в системі вимкнено анімації
   (prefers-reduced-motion), вимикаються лише плавна прокрутка й безкінечний цикл підказки.
   Галерея будинків — звичайна горизонтальна стрічка: сторінка гортається повз неї вільно.
   Без GSAP сторінка показує все стовпчиком. */
(() => {
  const html = document.documentElement;
  if (!window.gsap || !window.ScrollTrigger) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = () => matchMedia('(max-width: 900px)').matches;
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });
  html.classList.add('motion');
  if (reduce) html.classList.add('reduce');

  /* Lenis — лише на ПК. На мобільній вона віртуалізує тач-скрол через RAF/lerp, що на слабших
     телефонах дає ривки; нативний інерційний скрол там і плавніший, і дешевший. */
  let lenis = null;
  if (window.Lenis && !reduce && !isMobile()) {
    lenis = new Lenis({ lerp: 0.1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const scrollToY = (y) => (lenis ? lenis.scrollTo(y, { duration: 1.2 }) : window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }));
  const bar = document.querySelector('.bar');

  /* 1. Інтро: літери ЗАРС як вікно у відео; логотип і гасло з'являються самі після розкриття */
  const intro = document.querySelector('[data-intro]');
  if (intro) {
    const svg = intro.querySelector('.d-intro__veil');
    const letters = svg.querySelector('.d-intro__letters');
    const use = letters.querySelector('use');
    const media = intro.querySelector('.d-intro__media');
    const cue = intro.querySelector('.d-intro__cue');
    const mark = intro.querySelector('.lockup__mark');
    const motto = intro.querySelector('.lockup__motto');
    const VB = { x: 32, y: 32, w: 5120, h: 756 };
    const STEM = { x: 2844, y: 420 };
    const layout = () => {
      const W = intro.clientWidth, H = intro.clientHeight;
      const lw = Math.min(W * (W < 700 ? 0.84 : 0.62), 1100), lh = lw * VB.h / VB.w;
      const x = (W - lw) / 2, y = (H - lh) / 2;
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      use.setAttribute('x', x); use.setAttribute('y', y);
      use.setAttribute('width', lw); use.setAttribute('height', lh);
      gsap.set(letters, { svgOrigin: `${x + (STEM.x - VB.x) / VB.w * lw} ${y + (STEM.y - VB.y) / VB.h * lh}` });
    };
    layout();
    const lockup = gsap.timeline({ paused: true })
      .fromTo(mark, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1.1, ease: 'expo.out' })
      .fromTo(motto, { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out' }, 0.18);
    let shown = false;
    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: intro, start: 'top top', pin: true, invalidateOnRefresh: true,
        end: () => '+=' + (isMobile() ? intro.clientHeight * 0.85 : innerHeight * 1.05),
        scrub: isMobile() ? true : 0.45,
        onRefresh: layout,
        onUpdate: (st) => {
          bar && bar.toggleAttribute('data-on-veil', st.progress < 0.5);
          cue.classList.toggle('is-gone', st.progress > 0.02);
          if (st.progress > 0.74 && !shown) { shown = true; lockup.play(); }
          if (st.progress < 0.5 && shown) { shown = false; lockup.reverse(); }
        },
      },
    });
    tl.to(letters, { scale: 30, duration: 0.72, ease: 'power2.in' }, 0)
      .to(svg, { autoAlpha: 0, duration: 0.24, ease: 'power1.in' }, 0.48)
      .fromTo(media, { scale: 1.14 }, { scale: 1, duration: 0.8, ease: 'power2.out' }, 0)
      .to({}, { duration: 0.28 }, 0.72);
    bar && bar.setAttribute('data-on-veil', '');
  }

  /* Шапка стає суцільною, щойно інтро пішло */
  if (bar) {
    ScrollTrigger.create({
      trigger: '.d-claim', start: 'top top+=72',
      onEnter: () => bar.setAttribute('data-stuck', ''), onLeaveBack: () => bar.removeAttribute('data-stuck'),
    });
  }

  /* Прості проявлення */
  gsap.utils.toArray('[data-rise]').forEach((el) => {
    gsap.fromTo(el, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
  });
  gsap.utils.toArray('[data-lines]').forEach((el) => {
    gsap.fromTo(el.querySelectorAll('.line > span'), { yPercent: 110 }, { yPercent: 0, duration: 1.3, stagger: 0.14, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 80%', once: true } });
  });
  gsap.utils.toArray('[data-words]').forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach((w, i) => { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; el.append(s, i < words.length - 1 ? ' ' : ''); });
    gsap.fromTo(el.querySelectorAll('.w'), { opacity: 0.18 }, { opacity: 1, stagger: 0.05, ease: 'none', scrollTrigger: { trigger: el, start: 'top 88%', end: 'bottom 55%', scrub: true } });
  });

  /* 30 років */
  const claim = document.querySelector('.d-claim');
  if (claim) {
    gsap.timeline({ scrollTrigger: { trigger: claim, start: 'top 82%', once: true } })
      .fromTo(claim.querySelector('.d-claim__num'), { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 1.3, ease: 'expo.out' })
      .fromTo(claim.querySelector('.d-claim__unit'), { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out' }, 0.15)
      .fromTo(claim.querySelectorAll('.d-claim__text span'), { autoAlpha: 0, y: 34 }, { autoAlpha: 1, y: 0, duration: 1.1, stagger: 0.12, ease: 'expo.out' }, 0.2);
  }

  /* Паралакс фото: холдинг, маніфест, Відчуття дому */
  const drift = (frame, img, amount) => gsap.fromTo(img, { yPercent: -amount }, { yPercent: amount, ease: 'none', scrollTrigger: { trigger: frame, start: 'top bottom', end: 'bottom top', scrub: true } });
  document.querySelectorAll('.d-holding__photo').forEach((f) => drift(f, f.querySelector('img'), 8));
  document.querySelectorAll('.d-photo__frame').forEach((f) => drift(f, f.querySelector('img'), 14));

  /* Засновник: поява й власний паралакс поверх фото */
  const founder = document.querySelector('.d-founder');
  if (founder) {
    const media = founder.closest('.d-holding__media');
    gsap.fromTo(founder, { yPercent: 22 }, { yPercent: -22, ease: 'none', scrollTrigger: { trigger: media, start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.timeline({ scrollTrigger: { trigger: media, start: 'top 70%', once: true } })
      .fromTo(founder, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.4 })
      .fromTo(founder.querySelector('.d-founder__frame'), { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, ease: 'expo.inOut' }, 0)
      .fromTo(founder.querySelector('.d-founder__frame img'), { scale: 1.25 }, { scale: 1, duration: 1.8, ease: 'expo.out' }, 0.2)
      .fromTo(founder.querySelector('figcaption'), { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: 0.9, ease: 'expo.out' }, 0.8);
  }

  /* Галерея будинків: компактна картка, перемикається ЛИШЕ кнопками (ПК) або
     свайпом/кнопками (мобільна). Прокрутка сторінки на неї НЕ впливає — жодного
     піна й жодної прив'язки до скролу. Перехід — той самий кроссфейд-вайп «зправа»,
     що був у попередній версії (клієнт попросив повернути). Паралакс фото — власний
     повільний цикл, контур кадру завжди в межах overflow:hidden (фото на 12% більше кадру). */
  const gal = document.querySelector('[data-gal]');
  if (gal) {
    const track = gal.querySelector('.d-gal__track');
    const slides = [...gal.querySelectorAll('.d-gal__slide')];
    const imgs = slides.map((s) => s.querySelector('.d-gal__figure img'));
    const ticks = [...gal.querySelectorAll('.d-gal__tick')];
    const curEl = gal.querySelector('.d-gal__cur');
    const prevBtn = gal.querySelector('[data-prev]');
    const nextBtn = gal.querySelector('[data-next]');
    const n = slides.length;
    let idx = 0, z = n, idle = null;

    gsap.set(slides, { zIndex: (k) => k + 1, clipPath: 'inset(0% 0% 0% 0%)' });
    gsap.set(slides.slice(1), { clipPath: 'inset(0% 0% 0% 100%)' });
    gsap.set(imgs.slice(1), { xPercent: 14 });
    const drift = (img) => gsap.to(img, { yPercent: 4, duration: 8, ease: 'sine.inOut', yoyo: true, repeat: -1, overwrite: 'auto' });
    idle = drift(imgs[0]);

    const paint = () => {
      curEl.textContent = String(idx + 1).padStart(2, '0');
      ticks.forEach((t, k) => t.setAttribute('aria-current', String(k === idx)));
      prevBtn.disabled = idx <= 0;
      nextBtn.disabled = idx >= n - 1;
    };
    paint();

    const go = (i) => {
      i = gsap.utils.clamp(0, n - 1, i);
      if (i === idx) return;
      const prev = idx; idx = i;
      gsap.set(slides[idx], { zIndex: ++z });
      gsap.fromTo(slides[idx], { clipPath: 'inset(0% 0% 0% 100%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'power2.inOut', overwrite: 'auto' });
      gsap.fromTo(imgs[idx], { xPercent: 14 }, { xPercent: 0, duration: 1, ease: 'power2.out', overwrite: 'auto' });
      gsap.to(imgs[prev], { xPercent: -10, duration: 1, ease: 'power2.in', overwrite: 'auto' });
      idle && idle.kill();
      gsap.set(imgs[idx], { yPercent: 0 });
      idle = drift(imgs[idx]);
      paint();
    };
    prevBtn.addEventListener('click', () => go(idx - 1));
    nextBtn.addEventListener('click', () => go(idx + 1));
    ticks.forEach((t, i) => t.addEventListener('click', () => go(i)));

    /* Свайп на мобільній — лише горизонтальний жест на самій картці, вертикальну
       прокрутку сторінки не чіпає (passive-слухачі, без preventDefault). */
    let sx = 0, sy = 0, tracking = false;
    track.addEventListener('touchstart', (e) => {
      const t = e.touches[0]; sx = t.clientX; sy = t.clientY; tracking = true;
    }, { passive: true });
    track.addEventListener('touchend', (e) => {
      if (!tracking) return;
      tracking = false;
      const t = e.changedTouches[0];
      const dx = t.clientX - sx, dy = t.clientY - sy;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) go(idx + (dx < 0 ? 1 : -1));
    }, { passive: true });

    gsap.fromTo(gal.querySelector('.d-gal__bar'), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: gal, start: 'top 85%', once: true } });
  }

  /* Переваги: компактна sticky-картка (CSS position:sticky, без GSAP pin/snap — саме так
     зроблено на rolex.com/watches/new-watches: перевірено в цій сесії через CDP,
     .e14gephn0 = position:sticky, висота обгортки = n×100vh, ніякого пін-спейсера й снепу
     не було, тому й нема «стрибків» скролбару). Перехід — та сама «стара» анімація: вертикальний
     clip-path-вайп + зум фото (1.22→1.02), текст іде послідовно (спершу згасає старий, потім
     з'являється новий — ніколи одночасно, тому в паузі просто немає накладення). Усе — ЧИСТА
     функція self.progress (scrub:true, без пін і без кроків/дебаунсу): завжди синхронно зі
     скролом, назад-вперед теж працює. На кадр торкаємось лише 2 сусідніх слайдів, не всіх 8 —
     дешевше на слабших телефонах. */
  const adv = document.querySelector('[data-adv]');
  if (adv) {
    const figs = [...adv.querySelectorAll('.d-adv__media figure')];
    const imgs = figs.map((f) => f.querySelector('img'));
    const texts = [...adv.querySelectorAll('.d-adv__text')];
    const navs = [...adv.querySelectorAll('.d-adv__nav button')];
    const n = figs.length;
    const TRANS = 0.3;

    let lastI = -1, lastActive = -1;
    const setNav = (activeIdx) => {
      if (activeIdx === lastActive) return;
      lastActive = activeIdx;
      navs.forEach((b, k) => b.setAttribute('aria-current', String(k === activeIdx)));
    };
    const resetLayer = (i) => {
      figs.forEach((f, k) => {
        if (k === i) gsap.set(f, { autoAlpha: 1, zIndex: 2, clipPath: 'inset(0% 0% 0% 0%)' });
        else if (k === i + 1) gsap.set(f, { autoAlpha: 1, zIndex: 3, clipPath: 'inset(100% 0% 0% 0%)' });
        else gsap.set(f, { autoAlpha: 0, zIndex: 1 });
      });
      imgs.forEach((im, k) => { if (k === i || k === i + 1) gsap.set(im, { scale: k === i ? 1.02 : 1.22 }); });
      texts.forEach((el, k) => gsap.set(el, { autoAlpha: k === i ? 1 : 0, y: 0 }));
    };
    resetLayer(0);
    setNav(0);

    const apply = (progress) => {
      const pos = gsap.utils.clamp(0, n - 0.0001, progress * n);
      const i = Math.floor(pos);
      const localT = pos - i;
      if (i !== lastI) { lastI = i; resetLayer(i); }
      if (i >= n - 1) { setNav(i); return; }
      const t = localT > 1 - TRANS ? (localT - (1 - TRANS)) / TRANS : 0;
      gsap.set(figs[i + 1], { clipPath: `inset(${(1 - t) * 100}% 0% 0% 0%)` });
      gsap.set(imgs[i + 1], { scale: 1.22 - 0.2 * t });
      if (t < 0.5) {
        const t1 = t / 0.5;
        gsap.set(texts[i], { autoAlpha: 1 - t1, y: -20 * t1 });
      } else {
        const t2 = (t - 0.5) / 0.5;
        gsap.set(texts[i], { autoAlpha: 0 });
        gsap.set(texts[i + 1], { autoAlpha: t2, y: 24 * (1 - t2) });
      }
      setNav(t >= 0.5 ? i + 1 : i);
    };

    const st = ScrollTrigger.create({
      trigger: adv, start: 'top top', end: 'bottom bottom', scrub: true,
      onUpdate: (self) => apply(self.progress),
    });
    navs.forEach((b, i) => b.addEventListener('click', () => scrollToY(st.start + (st.end - st.start) * ((i + 0.02) / n))));

    /* Легкий паралакс активного фото — власний цикл, не прив'язаний до scrub */
    let idleIdx = -1, idle = null;
    ScrollTrigger.create({
      trigger: adv, start: 'top top', end: 'bottom bottom',
      onUpdate: (self) => {
        const i = Math.min(n - 1, Math.floor(self.progress * n));
        if (i === idleIdx) return;
        idleIdx = i;
        idle && idle.kill();
        gsap.set(imgs[i], { yPercent: 0 });
        idle = gsap.to(imgs[i], { yPercent: 6, duration: 7, ease: 'sine.inOut', yoyo: true, repeat: -1, overwrite: 'auto' });
      },
    });
  }

  /* Логотип у підвалі виїжджає знизу, коли сторінку докручено */
  const footMark = document.querySelector('.d-foot__mark');
  if (footMark) {
    gsap.fromTo(footMark.querySelector('svg'), { yPercent: 100 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: footMark, start: 'top bottom', end: 'bottom bottom', scrub: true } });
  }

  addEventListener('load', () => ScrollTrigger.refresh());
})();
