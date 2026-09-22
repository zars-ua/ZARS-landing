/* Плавна прокрутка коліщатком миші (22.09.2026) — на всіх сторінках, лише для пристроїв з мишею/трекпадом
   (hover + pointer:fine); на телефонах і планшетах — нативний тач-скрол.
   Вмикається НЕЗАЛЕЖНО від prefers-reduced-motion: у Windows із вимкненими «Ефектами анімації» Chrome віддає
   reduce і водночас сам вимикає згладжування коліщатка — прокрутка йшла ривками по 100 px (скарга клієнта).
   Раніше Lenis саме в цьому режимі й не вмикався. Вкладені прокрутки (каруселі, меню, лайтбокс) — нативні. */
(() => {
  if (!window.Lenis || !window.gsap) return;
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const lenis = new Lenis({
    lerp: 0.1,
    smoothWheel: true,
    syncTouch: false,
    allowNestedScroll: true,
    prevent: (node) => !!(node && node.closest && node.closest('dialog, .menu')),
  });
  window.__lenis = lenis;
  if (window.ScrollTrigger) lenis.on('scroll', () => ScrollTrigger.update());
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
})();
