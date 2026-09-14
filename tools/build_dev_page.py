#!/usr/bin/env python3
"""Збирає mock/index.html — сторінку девелопера (16.09.2026).
Шапку й символ логотипа бере з поточного mock/index.html; зображення — з assets/zars/manifest.json."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cur = open(os.path.join(ROOT, 'mock/index.html')).read()
M = json.load(open(os.path.join(ROOT, 'assets/zars/manifest.json')))
Z = M['zars']
head = cur[:cur.index('<body')]
head = re.sub(r'<link rel="stylesheet" href="mock\.css">', '<link rel="stylesheet" href="mock.css">\n<link rel="stylesheet" href="dev.css">', head) if 'dev.css' not in head else head
header = re.search(r'<header class="bar">.*?</header>', cur, re.S).group(0)
header = header.replace('href="#presentation"', 'href="fb29b.html#presentation"')
sym = re.search(r'<svg width="0" height="0".*?</svg>', cur, re.S).group(0)
VB = re.search(r'<symbol id="zars" viewBox="([^"]+)"', sym).group(1)
motto = re.search(r'<svg class="lockup__motto".*?</svg>', cur, re.S).group(0)
LOGO = f'<svg viewBox="{VB}" aria-hidden="true"><use href="#zars"/></svg>'


def ss(base, ws):
    return ', '.join(f'{base}-{w}.webp {w}w' for w in ws)


def img(name, alt, sizes, eager=False):
    ws = Z[name]['w']; b = f'../assets/zars/{name}'
    mid = max([w for w in ws if w <= 1600] or ws[:1])
    return f'<img src="{b}-{mid}.webp" srcset="{ss(b, ws)}" sizes="{sizes}" alt="{alt}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def pic(name, mob, alt, sizes='100vw'):
    return f'<picture><source media="(max-width: 700px)" srcset="{ss("../assets/zars/" + mob, Z[mob]["w"])}" sizes="100vw">{img(name, alt, sizes)}</picture>'


houses = [dict(h, years=h['years'].replace('–', '-')) for h in reversed(M['houses'])]  # від новіших до старших; роки через дефіс
slides = []
for i, h in enumerate(houses):
    b = f'../assets/dk/{h["slug"]}'
    slides.append(f'''    <figure class="d-gal__slide" data-name="{h["name"]}" data-years="{h["years"]}">
      <picture><source media="(max-width: 700px)" srcset="{ss(b + '-p', h['tall'])}" sizes="100vw"><img src="{b}-1920.webp" srcset="{ss(b, h['wide'])}" sizes="100vw" alt="{h["name"]}" loading="{'eager' if i < 2 else 'lazy'}" decoding="async"></picture>
      <figcaption><b>{h["name"]}</b>{h["years"]}</figcaption>
    </figure>''')
ticks = ''.join(f'<li><button class="d-gal__tick" type="button" aria-current="{str(i == 0).lower()}" aria-label="{h["name"]}, {h["years"]}"><span>{h["years"][:4]}</span></button></li>' for i, h in enumerate(houses))

ADV = [
    ('arch', 'Архітектура', 'Архітектурний фрагмент Будинку Каркашадзе', ['Будинки Каркашадзе завжди мають унікальні для свого місця архітектурні рішення, що зберігають цінність і розвивають потенціал території, на якій вони побудовані.', 'Кожен наш новий будинок прагне доповнювати та підкреслювати унікальний архітектурний літопис Одеси.']),
    ('brick', 'Цегла', 'Червона керамічна цегла', ['Скільки б з часом не з’являлося матеріалів для будівництва, цегла залишатиметься найкращим з них. Міцна. Зносостійка. Вологостійка. Морозостійка. Практично вічна. Ми подбали, щоб наш головний будівельний матеріал був якнайкращим.', 'Цегла підходить для висотного будівництва за характеристиками міцності, а за шумо- і теплоізоляційними властивостями — для будівництва житла найвищого класу.']),
    ('landscape', 'Благоустрій', 'Прибудинкова територія з ландшафтним дизайном', ['Як сам будинок, так і територія навколо нього — це гармонія вишуканості й функційності.', 'Індивідуальний, спеціально розроблений ландшафтний дизайн чудово доповнює загальну концепцію кожного Будинку Каркашадзе. А цілодобова охорона й відеоспостереження гарантує безпеку та дозволить відчути себе захищено й комфортно.']),
    ('interiors', 'Інтер’єри', 'Хол Будинку Каркашадзе із зеленою стіною', ['Ми хочемо, щоб відчуття дому виникало, коли відчиняються двері в хол Будинку Каркашадзе, та не залишало Вас до самої квартири.', 'Атмосфера м’якої розкоші — цього відчуття ми завжди прагнемо досягти, проєктуючи інтер’єри. Її атрибути — італійські меблі в м’якому світлі люстр і бра довершують цей ефект.']),
    ('marble', 'Мармур', 'Мармурові сходи в холі', ['Тисячі років мармурові підлоги шляхетно приглушують звуки кроків власників хороших будинків. Тому коли справа стосується вибору матеріалів для холів і коридорів у Будинках Каркашадзе, ми завжди віддаємо перевагу класиці — мармуру високої якості.']),
    ('ergonomics', 'Ергономіка', 'Тераса квартири з видом на море', ['Передбачаючи Ваші побажання до формування комфортного житлового простору, наші експерти з ергономіки створюють продумані планування.', 'При цьому ми завжди залишаємо можливість індивідуально підійти до кожного проєкту для того, щоб втілити в реальність ваші уявлення про ідеальний будинок.']),
    ('windows', 'Вікна', 'Панорамне вікно з видом на море', ['Делікатність натурального дерева й технологічність алюмінію. Для оснащення вікон Будинків Каркашадзе ми використовуємо принцип з’єднання найкращих традиційних матеріалів і сучасних технічних вирішень.']),
    ('parking', 'Паркінг', 'Підземний паркінг Будинку Каркашадзе', ['Обов’язковий елемент комфорту Будинків Каркашадзе. Підземний паркінг з окремою системою вентиляції і димовидалення, спроєктований з урахуванням експлуатації автомобілів S Class.']),
]
adv_media = ''.join(f'<figure>{img(k, alt, "(max-width: 900px) 100vw, 58vw")}</figure>' for k, t, alt, ps in ADV)
adv_nav = ''.join(f'<li><button type="button" aria-current="{str(i == 0).lower()}">{t}</button></li>' for i, (k, t, alt, ps) in enumerate(ADV))
adv_texts = ''.join(f'<article class="d-adv__text"><h3 class="d-adv__title">{t}</h3>{"".join(f"<p>{p}</p>" for p in ps)}</article>' for k, t, alt, ps in ADV)

page = head + f'''<body class="h-zars">
<!-- Сторінка девелопера. Генерується tools/build_dev_page.py; стилі mock/dev.css, рух mock/dev.js. -->
{header}

<section class="d-intro" data-intro aria-label="ЗАРС">
  <div class="d-intro__media">
    <video muted playsinline loop autoplay preload="auto" poster="../assets/video/zars-intro-poster.webp">
      <source src="../assets/video/zars-intro-854.mp4" type="video/mp4" media="(max-width: 800px)">
      <source src="../assets/video/zars-intro-1600.mp4" type="video/mp4">
    </video>
  </div>
  <svg class="d-intro__veil" aria-hidden="true" preserveAspectRatio="none">
    <defs><mask id="d-intro-mask" maskUnits="userSpaceOnUse" x="-50%" y="-50%" width="200%" height="200%">
      <rect x="-50%" y="-50%" width="200%" height="200%" fill="#fff"/>
      <g class="d-intro__letters"><use href="#zars" style="color:#000"/></g>
    </mask></defs>
    <rect class="veil" x="-50%" y="-50%" width="200%" height="200%" mask="url(#d-intro-mask)"/>
  </svg>
  <div class="d-intro__cue" aria-hidden="true"></div>
  <div class="d-intro__body">
    <div class="lockup">
      <h1 class="lockup__mark" aria-label="ЗАРС">{LOGO}</h1>
      {motto}
    </div>
  </div>
</section>

<section class="d-claim gut" aria-label="30 років">
  <p class="d-claim__years"><span class="d-claim__num">30</span><span class="d-claim__unit">років</span></p>
  <p class="d-claim__text">створюємо унікальні проєкти поза часом</p>
</section>

<section class="d-holding gut" aria-labelledby="holding-title">
  <div class="d-holding__media">
    <figure class="d-holding__photo">{pic('office', 'office-m', 'Фасад офісу холдингу ЗАРС на Французькому бульварі', '(max-width: 900px) 100vw, 58vw')}</figure>
    <figure class="d-founder">
      <div class="d-founder__frame">{img('founder', 'Гіві Сілованович Каркашадзе, засновник ЗАРС', '(max-width: 900px) 46vw, 16vw')}</div>
      <figcaption><b>Гіві Сілованович Каркашадзе</b><span>Засновник ЗАРС, 1930-2006</span></figcaption>
    </figure>
  </div>
  <div class="d-holding__text" data-rise>
    <h2 class="d-holding__title" id="holding-title">Холдинг ЗАРС</h2>
    <p>Компанія ЗАРС заснована 14 жовтня 1996 року Гіві Сіловановичем Каркашадзе (1930-2006).</p>
    <p>Холдинг ЗАРС здійснює повний інвестиційно-будівельний цикл власних проєктів, від девелопменту та будівництва до введення в експлуатацію та управління.</p>
    <p>ЗАРС — це злагоджена команда професіоналів зі спільними цінностями та баченням. Розуміючи потреби наших клієнтів та враховуючи сучасні тенденції, наша компанія створює найкращі проєкти.</p>
  </div>
</section>

<section class="d-photo gut" aria-label="Принципи ЗАРС">
  <div class="d-photo__frame">
    {pic('manifest', 'manifest-p', 'Хвилясті балкони Будинку Каркашадзе на тлі неба')}
    <div class="d-photo__body"><p class="d-photo__text" data-words>Відмовившись від масового будівництва, ЗАРС створює унікальні проєкти поза часом, в яких естетика, якість і комфорт є основними принципами.</p></div>
  </div>
</section>

<section class="d-kk gut" aria-labelledby="kk-title">
  <h2 class="d-kk__title" id="kk-title" data-lines><span class="line"><span>Будинки</span></span><span class="line"><span>Каркашадзе</span></span></h2>
  <p class="d-kk__story" data-rise>Історія Будинків Каркашадзе почалася з мрії її засновника побудувати ідеальний будинок для життя. Ось уже 30 років компанія ЗАРС робить її реальністю і зберігає головні принципи, завдяки яким Будинки Каркашадзе стають мрією для інших людей. Мрією, яку вони зможуть передати вже як свою спадщину.</p>
</section>

<section class="d-gal gut" data-gal aria-roledescription="галерея" aria-label="Будинки Каркашадзе, від новіших до перших">
  <div class="d-gal__stage">
{chr(10).join(slides)}
    <div class="d-gal__overlay">
      <div class="d-gal__cap" aria-live="polite"><h3 class="d-gal__name">{houses[0]["name"]}</h3><p class="d-gal__years">{houses[0]["years"]}</p></div>
      <div class="d-gal__bar">
        <span class="d-gal__count"><b class="d-gal__cur" style="font-weight:400">01</b> / {len(houses):02d}</span>
        <div class="d-gal__track"><span class="d-gal__line"></span><span class="d-gal__fill"></span><ol class="d-gal__ticks">{ticks}</ol></div>
        <button class="d-gal__skip" type="button">Пропустити</button>
      </div>
    </div>
  </div>
</section>

<section class="d-photo gut" aria-labelledby="feel-title">
  <div class="d-photo__frame">
    {pic('feel', 'feel-p', 'Будинок на Французькому бульварі, 29 у вечірньому підсвічуванні')}
    <div class="d-photo__body"><h2 class="d-photo__title" id="feel-title">Відчуття дому</h2><p class="d-photo__text" data-words>Найцінніше, що створюють Будинки Каркашадзе для своїх мешканців, — це неповторне відчуття дому. Ось чому Будинки Каркашадзе — це найкращий вибір для тих, хто хоче знайти справжній дім для своєї родини.</p></div>
  </div>
</section>

<section class="d-adv gut" data-adv aria-label="Переваги Будинків Каркашадзе">
  <div class="d-adv__card">
    <div class="d-adv__media" aria-hidden="true">{adv_media}</div>
    <div class="d-adv__body">
      <ul class="d-adv__nav">{adv_nav}</ul>
      <div class="d-adv__texts">{adv_texts}</div>
      <div class="d-adv__progress" aria-hidden="true"><i></i></div>
    </div>
  </div>
</section>

<footer class="d-foot" id="contacts">
  <div class="d-foot__grid">
    <div><h2>Контакти</h2><ul><li><a href="tel:+380671608877">+380 (67) 160 88 77</a></li><li><a href="mailto:estate@zars.ua">estate@zars.ua</a></li><li>Одеса, Французький бульвар, 2</li></ul></div>
    <div><h2>Соціальні мережі</h2><ul><li><a href="https://www.instagram.com/zars.ua/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.facebook.com/www.zars.ua/" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    <p class="d-foot__copy">© 1996-2026 ЗАРС</p>
  </div>
  <div class="d-foot__mark" aria-hidden="true">{LOGO}</div>
</footer>
{sym}
<script src="../assets/vendor/gsap.min.js" defer></script>
<script src="../assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="../assets/vendor/lenis.min.js" defer></script>
<script src="dev.js" defer></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'mock/index.html'), 'w').write(page)
print('ok', len(page), 'slides', page.count('d-gal__slide"'), 'adv', page.count('d-adv__text"'))
