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

  let lenis = null;
  if (window.Lenis && !reduce) {
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

  /* Галерея будинків: горизонтальна стрічка зі стрілками, точками й перетягуванням.
     Вертикальну прокрутку сторінки не перехоплює. */
  const gal = document.querySelector('[data-gal]');
  if (gal) {
    const vp = gal.querySelector('.d-gal__viewport');
    const track = gal.querySelector('.d-gal__track');
    const slides = [...gal.querySelectorAll('.d-gal__slide')];
    const ticks = [...gal.querySelectorAll('.d-gal__tick')];
    const cur = gal.querySelector('.d-gal__cur');
    const prev = gal.querySelector('[data-prev]');
    const next = gal.querySelector('[data-next]');
    const n = slides.length;
    let idx = 0, raf = 0;
    const left = (i) => slides[i].offsetLeft - track.offsetLeft;
    const nearest = () => {
      const x = vp.scrollLeft;
      let best = 0, d = Infinity;
      slides.forEach((s, i) => { const dd = Math.abs(left(i) - x); if (dd < d) { d = dd; best = i; } });
      return best;
    };
    const paint = () => {
      idx = nearest();
      cur.textContent = String(idx + 1).padStart(2, '0');
      ticks.forEach((t, k) => t.setAttribute('aria-current', String(k === idx)));
      prev.disabled = vp.scrollLeft <= 2;
      next.disabled = vp.scrollLeft >= vp.scrollWidth - vp.clientWidth - 2;
      const mid = vp.scrollLeft + vp.clientWidth / 2;
      slides.forEach((s, i) => {
        const c = left(i) + s.offsetWidth / 2;
        gsap.set(s.querySelector('img'), { xPercent: gsap.utils.clamp(-5, 5, ((c - mid) / vp.clientWidth) * -5) });
      });
    };
    const go = (i) => vp.scrollTo({ left: left(gsap.utils.clamp(0, n - 1, i)), behavior: reduce ? 'auto' : 'smooth' });
    vp.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(paint); }, { passive: true });
    prev.addEventListener('click', () => go(idx - 1));
    next.addEventListener('click', () => go(idx + 1));
    ticks.forEach((t, i) => t.addEventListener('click', () => go(i)));
    vp.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
    });
    let down = false, sx = 0, sl = 0, moved = false;
    vp.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = vp.scrollLeft; vp.classList.add('is-drag'); });
    addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; vp.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; vp.classList.remove('is-drag'); go(nearest()); });
    vp.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    gsap.fromTo(gal.querySelector('.d-gal__bar'), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: gal, start: 'top 75%', once: true } });
    paint();
    addEventListener('resize', paint);
  }

  /* Переваги: одна картка, кадри й тексти змінюються за прокруткою */
  const adv = document.querySelector('[data-adv]');
  if (adv) {
    const figs = [...adv.querySelectorAll('.d-adv__media figure')];
    const texts = [...adv.querySelectorAll('.d-adv__text')];
    const navs = [...adv.querySelectorAll('.d-adv__nav button')];
    const prog = adv.querySelector('.d-adv__progress i');
    const n = figs.length;
    html.classList.add('adv-on');
    let z = 1, cur = -1;
    gsap.set(texts, { autoAlpha: 0 });
    const show = (i) => {
      if (i === cur) return;
      const prev = cur;
      cur = i;
      navs.forEach((b, k) => b.setAttribute('aria-current', String(k === i)));
      gsap.set(figs[i], { zIndex: ++z });
      if (prev < 0) { gsap.set(texts[i], { autoAlpha: 1 }); return; }
      const down = i > prev;
      gsap.fromTo(figs[i], { clipPath: down ? 'inset(100% 0% 0% 0%)' : 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'expo.inOut', overwrite: 'auto' });
      gsap.fromTo(figs[i].querySelector('img'), { scale: 1.22 }, { scale: 1.02, duration: 1.6, ease: 'expo.out', overwrite: 'auto' });
      gsap.to(texts[prev], { autoAlpha: 0, y: down ? -30 : 30, duration: 0.35, ease: 'power2.in', overwrite: 'auto' });
      gsap.set(texts[i], { autoAlpha: 1, y: 0 });
      gsap.fromTo(texts[i].children, { autoAlpha: 0, y: down ? 44 : -44 }, { autoAlpha: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.08, delay: 0.25, overwrite: 'auto' });
    };
    show(0);
    const st = ScrollTrigger.create({
      trigger: adv, start: 'top top', pin: true, invalidateOnRefresh: true, anticipatePin: 1,
      end: () => '+=' + innerHeight * (isMobile() ? 0.55 : 0.65) * n,
      onUpdate: (self) => {
        const pos = Math.min(n - 0.001, self.progress * n);
        const i = Math.floor(pos);
        show(i);
        prog.style.transform = `scaleX(${(i + 1) / n})`;
        gsap.set(figs[i].querySelector('img'), { yPercent: -7 + 14 * (pos - i) });
      },
    });
    navs.forEach((b, i) => b.addEventListener('click', () => scrollToY(st.start + (st.end - st.start) * ((i + 0.5) / n))));
  }

  /* Логотип у підвалі виїжджає знизу, коли сторінку докручено */
  const footMark = document.querySelector('.d-foot__mark');
  if (footMark) {
    gsap.fromTo(footMark.querySelector('svg'), { yPercent: 100 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: footMark, start: 'top bottom', end: 'bottom bottom', scrub: true } });
  }

  addEventListener('load', () => ScrollTrigger.refresh());
})();
