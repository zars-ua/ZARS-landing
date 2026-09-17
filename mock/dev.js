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

  /* Галерея будинків.
     ПК: пінена стрічка «Rolex» — прокрутка/трекпад-свайп вниз перемикає слайд ДИСКРЕТНО
     (снеп до найближчого кадру + невеличкий дебаунс не дають перемкнути кілька слайдів
     за один різкий рух), плюс кнопки-стрілки. Паралакс фото — власний повільний цикл,
     не прив'язаний до прокрутки, щоб сама прокрутка не «тягала» картинку замість перемикання.
     Мобільна: горизонтальна стрічка — гортається вбік свайпом чи перетягуванням,
     сторінку не пінить, вертикальну прокрутку не перехоплює. */
  const gal = document.querySelector('[data-gal]');
  if (gal) {
    const vp = gal.querySelector('.d-gal__viewport');
    const track = gal.querySelector('.d-gal__track');
    const slides = [...gal.querySelectorAll('.d-gal__slide')];
    const imgs = slides.map((s) => s.querySelector('.d-gal__figure img'));
    const ticks = [...gal.querySelectorAll('.d-gal__tick')];
    const curEl = gal.querySelector('.d-gal__cur');
    const prevBtn = gal.querySelector('[data-prev]');
    const nextBtn = gal.querySelector('[data-next]');
    const n = slides.length;
    let nav = null;

    const paint = (idx) => {
      curEl.textContent = String(idx + 1).padStart(2, '0');
      ticks.forEach((t, k) => t.setAttribute('aria-current', String(k === idx)));
      prevBtn.disabled = idx <= 0;
      nextBtn.disabled = idx >= n - 1;
    };
    ticks.forEach((t, i) => t.addEventListener('click', () => nav && nav.go(i)));
    prevBtn.addEventListener('click', () => nav && nav.go(nav.idx() - 1));
    nextBtn.addEventListener('click', () => nav && nav.go(nav.idx() + 1));
    gsap.fromTo(gal.querySelector('.d-gal__bar'), { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: gal, start: 'top 75%', once: true } });

    ScrollTrigger.matchMedia({
      '(min-width: 901px)': function () {
        html.classList.add('gal-on');
        gsap.set(slides, { zIndex: (k) => k + 1, clipPath: 'inset(0% 0% 0% 0%)' });
        gsap.set(slides.slice(1), { clipPath: 'inset(0% 0% 0% 100%)' });
        gsap.set(imgs.slice(1), { xPercent: 14 });
        let z = n, cur = 0, idle = null;
        const drift = (img) => gsap.to(img, { yPercent: 5, duration: 7, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 1.2, overwrite: 'auto' });
        idle = drift(imgs[0]);
        const show = (i) => {
          if (i === cur) return;
          const prev = cur; cur = i; paint(i);
          gsap.set(slides[i], { zIndex: ++z });
          idle && idle.kill();
          gsap.set(imgs[cur], { yPercent: 0 });
          idle = drift(imgs[cur]);
          gsap.fromTo(slides[i], { clipPath: 'inset(0% 0% 0% 100%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'power2.inOut', overwrite: 'auto' });
          gsap.fromTo(imgs[i], { xPercent: 14 }, { xPercent: 0, duration: 1, ease: 'power2.out', overwrite: 'auto' });
          gsap.to(imgs[prev], { xPercent: -10, duration: 1, ease: 'power2.in', overwrite: 'auto' });
        };
        paint(0);
        /* Дискретний крок: навіть якщо прокрутка різко пройшла кілька сегментів (інерція
           трекпада), перемикаємось по одному кадру за раз — жоден слайд не «проскакує» непоміченим. */
        let pending = 0, settleId = null, stepping = false;
        const step = () => {
          if (cur === pending) { stepping = false; return; }
          stepping = true;
          show(cur + (pending > cur ? 1 : -1));
          setTimeout(step, 1080);
        };
        const commit = () => { if (!stepping) step(); };
        const st = ScrollTrigger.create({
          trigger: gal, start: 'top top', pin: true, invalidateOnRefresh: true, anticipatePin: 1,
          end: () => '+=' + innerHeight * 0.6 * (n - 1),
          snap: { snapTo: 1 / (n - 1), duration: 0.5, delay: 0.04, ease: 'power1.inOut' },
          onUpdate: (self) => {
            pending = Math.round(self.progress * (n - 1));
            clearTimeout(settleId);
            settleId = setTimeout(commit, 70);
          },
        });
        nav = { idx: () => cur, go: (i) => scrollToY(st.start + (st.end - st.start) * (gsap.utils.clamp(0, n - 1, i) / (n - 1))) };
        return () => { html.classList.remove('gal-on'); idle && idle.kill(); nav = null; };
      },
      '(max-width: 900px)': function () {
        let idx = 0, raf = 0;
        const left = (i) => slides[i].offsetLeft - track.offsetLeft;
        const nearest = () => {
          const x = vp.scrollLeft;
          let best = 0, d = Infinity;
          slides.forEach((s, i) => { const dd = Math.abs(left(i) - x); if (dd < d) { d = dd; best = i; } });
          return best;
        };
        const onScroll = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(paintMobile); };
        const paintMobile = () => {
          idx = nearest();
          paint(idx);
          prevBtn.disabled = vp.scrollLeft <= 2;
          nextBtn.disabled = vp.scrollLeft >= vp.scrollWidth - vp.clientWidth - 2;
          const mid = vp.scrollLeft + vp.clientWidth / 2;
          slides.forEach((s, i) => {
            const c = left(i) + s.offsetWidth / 2;
            gsap.set(s.querySelector('img'), { xPercent: gsap.utils.clamp(-5, 5, ((c - mid) / vp.clientWidth) * -5) });
          });
        };
        const go = (i) => vp.scrollTo({ left: left(gsap.utils.clamp(0, n - 1, i)), behavior: reduce ? 'auto' : 'smooth' });
        nav = { idx: () => idx, go };
        vp.addEventListener('scroll', onScroll, { passive: true });
        const onKeydown = (e) => {
          if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
          if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1); }
        };
        vp.addEventListener('keydown', onKeydown);
        let down = false, sx = 0, sl = 0, moved = false;
        const onDown = (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = vp.scrollLeft; vp.classList.add('is-drag'); };
        const onMove = (e) => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; vp.scrollLeft = sl - dx; };
        const onUp = () => { if (!down) return; down = false; vp.classList.remove('is-drag'); go(nearest()); };
        const onClick = (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } };
        vp.addEventListener('pointerdown', onDown);
        addEventListener('pointermove', onMove);
        addEventListener('pointerup', onUp);
        vp.addEventListener('click', onClick, true);
        addEventListener('resize', paintMobile);
        paintMobile();
        return () => {
          vp.removeEventListener('scroll', onScroll);
          vp.removeEventListener('keydown', onKeydown);
          vp.removeEventListener('pointerdown', onDown);
          removeEventListener('pointermove', onMove);
          removeEventListener('pointerup', onUp);
          vp.removeEventListener('click', onClick, true);
          removeEventListener('resize', paintMobile);
          nav = null;
        };
      },
    });
  }

  /* Переваги: одна компактна картка, кадри й тексти перемикаються ДИСКРЕТНО за прокруткою вниз
     (снеп + дебаунс — як у галереї, щоб не перемикалось відразу кілька слайдів). Висота картки
     задається фото (--adv-media-h), а стовпець тексту центрується по висоті найвищого варіанта
     тексту (--adv-text-h, виміряно нижче), без порожнього хвоста знизу. Паралакс фото — власний
     повільний цикл, не прив'язаний до прокрутки. */
  const adv = document.querySelector('[data-adv]');
  if (adv) {
    const figs = [...adv.querySelectorAll('.d-adv__media figure')];
    const texts = [...adv.querySelectorAll('.d-adv__text')];
    const textsBox = adv.querySelector('.d-adv__texts');
    const navs = [...adv.querySelectorAll('.d-adv__nav button')];
    const n = figs.length;
    html.classList.add('adv-on');

    const measure = () => {
      const maxText = Math.max(...texts.map((t) => t.offsetHeight));
      textsBox.style.setProperty('--adv-text-h', maxText + 'px');
      const navH = adv.querySelector('.d-adv__nav').offsetHeight;
      adv.style.setProperty('--adv-media-h', Math.round(navH + 22 + maxText + 80) + 'px');
    };
    measure();
    addEventListener('resize', measure);
    document.fonts && document.fonts.ready.then(measure);

    let z = 1, cur = -1, idle = null;
    gsap.set(texts, { autoAlpha: 0 });
    const drift = (img) => gsap.to(img, { yPercent: 6, duration: 7, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 1.4, overwrite: 'auto' });
    const show = (i) => {
      if (i === cur) return;
      const prev = cur;
      cur = i;
      navs.forEach((b, k) => b.setAttribute('aria-current', String(k === i)));
      gsap.set(figs[i], { zIndex: ++z });
      idle && idle.kill();
      gsap.set(figs[i].querySelector('img'), { yPercent: 0 });
      idle = drift(figs[i].querySelector('img'));
      if (prev < 0) { gsap.set(texts[i], { autoAlpha: 1 }); return; }
      const down = i > prev;
      gsap.fromTo(figs[i], { clipPath: down ? 'inset(100% 0% 0% 0%)' : 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'expo.inOut', overwrite: 'auto' });
      gsap.fromTo(figs[i].querySelector('img'), { scale: 1.22 }, { scale: 1.02, duration: 1.6, ease: 'expo.out', overwrite: 'auto' });
      gsap.to(texts[prev], { autoAlpha: 0, y: down ? -30 : 30, duration: 0.35, ease: 'power2.in', overwrite: 'auto' });
      gsap.set(texts[i], { autoAlpha: 1, y: 0 });
      gsap.fromTo(texts[i].children, { autoAlpha: 0, y: down ? 44 : -44 }, { autoAlpha: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.08, delay: 0.25, overwrite: 'auto' });
    };
    show(0);
    /* Дискретний крок: навіть при різкій інерційній прокрутці перемикаємось по одному
       кадру за раз, жоден слайд не проскакує непоміченим. */
    let pending = 0, settleId = null, stepping = false;
    const step = () => {
      if (cur === pending) { stepping = false; return; }
      stepping = true;
      show(cur + (pending > cur ? 1 : -1));
      setTimeout(step, 1300);
    };
    const commit = () => { if (!stepping) step(); };
    const st = ScrollTrigger.create({
      trigger: adv, start: 'top top', pin: true, invalidateOnRefresh: true, anticipatePin: 1,
      end: () => '+=' + innerHeight * (isMobile() ? 0.55 : 0.65) * n,
      snap: { snapTo: 1 / (n - 1), duration: 0.5, delay: 0.04, ease: 'power1.inOut' },
      onUpdate: (self) => {
        pending = Math.round(self.progress * (n - 1));
        clearTimeout(settleId);
        settleId = setTimeout(commit, 70);
      },
    });
    navs.forEach((b, i) => b.addEventListener('click', () => scrollToY(st.start + (st.end - st.start) * (i / (n - 1)))));
  }

  /* Логотип у підвалі виїжджає знизу, коли сторінку докручено */
  const footMark = document.querySelector('.d-foot__mark');
  if (footMark) {
    gsap.fromTo(footMark.querySelector('svg'), { yPercent: 100 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: footMark, start: 'top bottom', end: 'bottom bottom', scrub: true } });
  }

  addEventListener('load', () => ScrollTrigger.refresh());
})();
