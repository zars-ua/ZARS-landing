#!/usr/bin/env python3
"""Збирає mock/fb29.html і mock/fb29b.html зі спільної шапки, героя й даних лендингів.
Зображення беруться з assets/wix/manifest.json і assets/img/manifest.json."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, 'assets/wix/manifest.json')))
M_OLD = json.load(open(os.path.join(ROOT, 'assets/img/manifest.json')))
PHONE, TEL = '+380 (67) 160 88 77', '+380671608877'

def pic(key, alt, sizes='100vw', eager=False, cls=''):
    if key in M:
        base, widths = f'../assets/wix/{key}', M[key]['widths']
    else:
        base, widths = f'../assets/img/{key}', [w for w in M_OLD[key]['widths'] if w <= 2400]
    ss = ', '.join(f'{base}-{w}.webp {w}w' for w in widths)
    src = f'{base}-{max(w for w in widths if w <= 1600) if min(widths) <= 1600 else widths[0]}.webp'
    full = f'{base}-{widths[-1]}.webp'
    load = 'eager' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}" srcset="{ss}" sizes="{sizes}" data-full="{full}" alt="{alt}" loading="{load}" decoding="async">'

def pan(key, title, text, sizes='100vw', cls=''):
    body = f'<p class="pan__text">{text}</p>' if text else ''
    return f'''<figure class="pan{' ' + cls if cls else ''}">{pic(key, re.sub(r'<[^>]+>', ' ', title), sizes)}
    <figcaption class="pan__cap"><h3 class="pan__title">{title}</h3>{body}</figcaption></figure>'''

def loc_schema():
    """Схема розташування ФБ29Б — та сама картинка й підписи, що на zars.ua/objects/fr29b (21.09.2026)."""
    items = [('street1', 'Французький бульвар', 1), ('street2', 'пров. Спортивний', 1), ('opera', 'Оперний театр <br>3,9 км', 0),
             ('muz', 'Театр музкомедії <br>900 м', 0), ('b29', 'Французький <br>бульвар, 29Б', 0), ('club', 'Яхт-клуб <br>450 м', 0),
             ('health', 'Траса здоров’я <br>350 м', 0), ('kino', 'Одеська кіностудія <br>350 м', 0), ('arcadia', 'Аркадія <br>4,4 км', 0),
             ('airport', 'Аеропорт <br>9,4 км', 0)]
    labels = ''.join(f'<div class="loc__item loc__{k}"><span class="{"loc__street" if st else "loc__label"}">{t}</span></div>' for k, t, st in items)
    return f'''<div class="loc__schema" data-loc aria-label="Схема: відстані від будинку до значущих місць Одеси" role="img">
    <div class="loc__item loc__bg"><img src="../assets/map/fr29b-map.svg" alt="" width="1556" height="1636" loading="lazy" decoding="async"></div>
    {labels}
  </div>'''

def stage_grid():
    """Стадія будівництва ФБ29Б: чотири вертикальні кадри в ряд, розкриття й паралакс (21.09.2026)."""
    shots = [('fb29b/build-1', 'Фасад будинку на стадії будівництва'), ('fb29b/build-2', 'Будинок і будівельний кран'),
             ('fb29b/build-3', 'Балкони фасаду'), ('fb29b/build-4', 'Тераса на стадії будівництва')]
    return '<div class="stage__grid" data-gallery data-stage>' + ''.join(
        f'<figure class="stage__frame">{pic(k, alt, "(max-width: 900px) 50vw, 26vw")}</figure>' for k, alt in shots) + '</div>'

def perks(items, site='fb29b'):
    """Горизонтальна карусель переваг з іконками (21.09.2026)."""
    icon = lambda i: ('<span class="perk__icon perk__icon--logo"><svg viewBox="32.0 32.0 5120.0 756.0" aria-hidden="true"><use href="#zars"/></svg></span>' if i == 'zars-logo'
                      else f'<img class="perk__icon" src="../assets/icons/{site}/{i}.svg" alt="" loading="lazy">')
    cards = ''.join(f'<li class="perk">{icon(i)}<h3 class="perk__title">{t}</h3><p class="perk__text">{d}</p></li>' for i, t, d in items)
    arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
    return f'''<section class="perks" data-perks aria-roledescription="карусель" aria-label="Переваги будинку">
  <ul class="perks__track" tabindex="0">{cards}</ul>
  <div class="perks__nav"><button type="button" data-prev aria-label="Попередні переваги">{arrow}</button><span class="perks__bar"><i></i></span><button type="button" data-next aria-label="Наступні переваги">{arrow}</button></div>
</section>'''

def facts(items):
    return '<dl class="facts">' + ''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in items) + '</dl>'

def dist(items):
    return '<ul class="dist">' + ''.join(f'<li><span class="dist__name">{n}</span><span class="dist__val">{v}</span></li>' for n, v in items) + '</ul>'

def plans(items, note=''):
    tabs = ''.join(
        f'<li><button class="plans__tab" type="button" role="tab" aria-selected="{str(i == 0).lower()}" data-area="{a}" data-info="{inf}"><b>{t}</b><span>{a} · {inf}</span></button></li>'
        for i, (k, t, a, inf) in enumerate(items))
    imgs = ''.join(pic(k, f'Планування: {t}, {a}', '(max-width: 900px) 100vw, 60vw', eager=(i == 0)) for i, (k, t, a, inf) in enumerate(items))
    return f'''<div class="plans" data-plans>
    <ul class="plans__list" role="tablist" aria-label="Планування">{tabs}</ul>
    <div>
      <figure class="plans__stage">{imgs}</figure>
      <div class="plans__meta"><div><span class="plans__area">{items[0][2]}</span> <span class="plans__info">{items[0][3]}</span></div>
        <button class="zoom" type="button"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6.5 1a5.5 5.5 0 0 1 4.38 8.82l4.15 4.15-1.06 1.06-4.15-4.15A5.5 5.5 0 1 1 6.5 1Zm0 1.5a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM5.75 4h1.5v1.75H9v1.5H7.25V9h-1.5V7.25H4v-1.5h1.75Z" fill="currentColor"/></svg>Збільшити</button></div>
      {f'<p class="note">{note}</p>' if note else ''}
    </div></div>'''

def gallery(items):
    return '<div class="editorial" data-gallery>' + ''.join(
        f'<figure class="{cls}">{pic(k, alt, "(max-width: 900px) 100vw, 60vw")}</figure>' for k, alt, cls in items) + '</div>'

def enquiry(project):
    opts = ''.join(f'<option{" selected" if p == project else ""}>{p}</option>' for p in ['Французький бульвар, 29', 'Французький бульвар, 29Б'])
    return f'''<section class="enquiry" id="presentation" aria-labelledby="enq-title">
  <div>
    <h2 class="title-lg" id="enq-title">Приватна презентація</h2>
    <p class="lead">Покажемо будинок і квартири особисто, у зручний для Вас час.</p>
    <a class="enquiry__phone" href="tel:{TEL}">{PHONE}</a>
  </div>
  <form class="form" data-enquiry novalidate>
    <label class="field"><span>Ім'я</span><input name="name" autocomplete="name" required></label>
    <label class="field"><span>Телефон</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
    <div class="form__row">
      <label class="field"><span>Проєкт</span><select name="project">{opts}</select></label>
      <label class="field"><span>Зручний час</span><select name="time"><option>Будь-коли</option><option>Зранку</option><option>Вдень</option><option>Увечері</option></select></label>
    </div>
    <button class="act" type="submit">Надіслати запит</button>
    <p class="form__msg" role="status" aria-live="polite"></p>
  </form>
</section>'''

from site_footer import footer as _footer

SCRIPTS = '''<script src="../assets/vendor/gsap.min.js" defer></script>
<script src="../assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="motion.js" defer></script>
<script src="menu.js" defer></script>
<script src="site.js" defer></script>'''

def shell(fname, body_sections):
    s = open(os.path.join(ROOT, 'mock', fname)).read()
    m = re.search(r'<section class="hero[^"]*"[^>]*>.*?</section>', s, re.S)
    head = s[:m.start()]
    # нормалізувати відкривальний тег, щоб повторна збірка давала той самий результат
    hero = re.sub(r'^<section class="hero[^"]*"[^>]*>', '<section class="hero">', m.group(0))
    sym = re.search(r'<svg width="0" height="0".*?</svg>', s, re.S).group(0)
    return head, hero, sym

def logo_use(sym):
    vb = re.search(r'<symbol id="zars" viewBox="([^"]+)"', sym).group(1)
    return f'<svg viewBox="{vb}" aria-hidden="true"><use href="#zars"/></svg>'

# ------------------------------------------------------------------ ФБ29
head, hero, sym = shell('fb29.html', None)
LOGO = logo_use(sym)
hero = hero.replace('<section class="hero">', '<section class="hero hero--ken" data-stick-after>')
fb29 = head + hero + f'''
<section class="air" aria-labelledby="s29-offer">
  <p class="statement" id="s29-offer" data-reveal-lines>
    <span class="line"><span>Унікальні пропозиції</span></span>
    <span class="line"><span>з видом на море</span></span>
  </p>
  <div class="two" style="margin-top:clamp(3rem,8vh,6rem)">
    <p class="words" data-reveal-words style="margin:0;text-align:left">Будинки Каркашадзе — це унікальний приклад висотного цегляного будівництва, якість якого не має аналогів в Одесі.</p>
    <p class="lead">Більше того, у світі взагалі не так багато висотних будівель, побудованих повністю з цегли.</p>
  </div>
  <dl class="stats" data-stats>
    <div><dt>10</dt><dd>поверхів</dd></div>
    <div><dt>3</dt><dd>секції</dd></div>
    <div><dt>120</dt><dd>місць<br>у підземному паркінгу</dd></div>
    <div><dt>0,7</dt><dd>га загальної площі<br>території комплексу</dd></div>
  </dl>
</section>

<section class="air loc loc--29" aria-labelledby="s29-loc">
  <div class="loc__text">
    <h2 class="label" id="s29-loc">Розташування</h2>
    <p class="big-dist"><b>400</b><span>метрів<br>до моря</span></p>
    <p class="lead">Будинок розташований усього у 400 метрах від моря та у 40 метрах від парку «Ювілейний». Поєднання чистого морського та «лісового» повітря створює найкращі екологічні умови для життя.</p>
    <a class="act act--quiet loc__map" href="https://www.google.com/maps/search/?api=1&amp;query=46.4614137%2C30.7562069" target="_blank" rel="noopener">Дивитися на карті</a>
  </div>
  <div class="map29" data-map29 role="img" aria-label="Схема: відстані від будинку до моря, Траси здоров’я, яхт-клубу, театрів, Аркадії та аеропорту">
    <img class="map29__base" src="../assets/map/fb29/road-and-sea.webp" alt="" width="1303" height="980" loading="lazy" decoding="async">
    <img class="map29__building" src="../assets/map/fb29/building.webp" alt="" loading="lazy">
    <img class="map29__attr" src="../assets/map/fb29/attraction.webp" alt="" loading="lazy">
    <img class="map29__lines" src="../assets/map/fb29/lines.webp" alt="" loading="lazy">
  </div>
</section>

<section class="award" aria-labelledby="s29-awards">
  <figure class="award__media">{pic('fb29/dusk-wide', 'Будинок на Французькому бульварі, 29 увечері', '(max-width: 900px) 200vw, min(125vw, 1520px)')}</figure>
  <div class="award__body">
    <div class="award__text">
      <h2 class="award__title" id="s29-awards">Відзнака проєкту</h2>
      <p>У 2021 році в Лондоні Будинок Каркашадзе Французький бульвар, 29 був відзначений міжнародною премією International Property Awards у 4 номінаціях.</p>
    </div>
    <div class="award__ribbons">''' + ''.join(
    f'<figure><img src="../assets/awards/ipa-{s}-960.webp" srcset="../assets/awards/ipa-{s}-480.webp 1x, ../assets/awards/ipa-{s}-960.webp 2x" width="113" height="480" alt="European Property Awards 2021-2022: {t}" loading="lazy"></figure>'
    for s, t in [('high-rise-development', 'Residential High Rise Development'), ('high-rise-architecture', 'Residential High Rise Architecture'), ('architecture-multiple-residence', 'Architecture Multiple Residence'), ('residential-development', 'Residential Development')]) + f'''</div>
  </div>
</section>

<section class="pans pans--adv" aria-label="Переваги">
  {pan('fb29/sea', 'Захоплюючий вид на море', '', '(max-width: 900px) 200vw, min(125vw, 1520px)')}
  {pan('fb29/lobby', 'Виправдана розкіш', 'Оздоблення місць загального користування мармуром, деревом, оніксом.', '(max-width: 900px) 200vw, min(125vw, 1520px)')}
  <div class="pans pans--split pans--split-rev" style="padding-inline:0">
    {pan('fb29/path', 'Приватність', 'Лише три квартири на поверсі. На території комплексу немає торговельно-офісних приміщень і сторонньої інфраструктури.', '(max-width: 900px) 200vw, 52vw')}
    {pan('fb29/rise', 'Комфорт', 'Концепція будинку на Французькому бульварі, 29 передбачає комфорт та абсолютну приватність мешканців.', '(max-width: 900px) 200vw, 72vw')}
  </div>
  <div class="pans pans--split" style="padding-inline:0">
    {pan('fb29/landscaping', 'Благоустрій', 'Фонтани, площадки для відпочинку дітей та дорослих.', '(max-width: 900px) 200vw, 72vw')}
    {pan('fb29/parking', 'Паркінг', 'Підземний паркінг на 120 місць.', '(max-width: 900px) 200vw, 52vw')}
  </div>
</section>
{perks([('zars-logo', 'Кращий девелопер міста', '30 років будівництва нерухомості преміум-класу.'), ('three-per-floor', 'Три квартири на поверсі', 'Абсолютна приватність мешканців.'), ('walls', 'Найкращий будівельний матеріал', 'Усі стіни з червоної ефективної керамічної цегли. Зовнішні 640 мм, внутрішні 510 мм та 380 мм, перегородки 120 мм.'), ('windows', 'Панорамні вікна', 'Алюміній та натуральне дерево (Євробрус).'), ('ceiling', 'Висота приміщень', '3,15 м.'), ('autonomy', 'Автономність', 'Автономне теплопостачання, дизель-генератор.'), ('power', 'Електропостачання', 'Трансформаторна підстанція. Дизель-генератор.'), ('security', 'Безпека', 'Територія, що цілодобово охороняється, відеоспостереження.')], 'fb29')}

<section class="air" id="plans" aria-labelledby="s29-plans">
  <span class="label">Планування</span>
  <h2 class="title-lg" id="s29-plans" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Трикімнатна квартира, 164,5 м²</h2>
  {plans([('fb29/plan-164-a', 'Варіант А', '164,5 м²', '11 поверх · вид на море та місто'), ('fb29/plan-164-b', 'Варіант Б', '164,5 м²', '11 поверх · вид на море та місто')], 'Площа проєктна. Детальні характеристики й наявність покажемо під час приватної презентації.')}
</section>

{enquiry('Французький бульвар, 29')}
{_footer(LOGO)}
{sym}
{SCRIPTS}
</body>
</html>
'''
open(os.path.join(ROOT, 'mock/fb29.html'), 'w').write(fb29)

# ------------------------------------------------------------------ ФБ29Б
head, hero, sym = shell('fb29b.html', None)
hero = hero.replace('<section class="hero">', '<section class="hero" data-stick-after>')
fb29b = head + hero + f'''
<section class="air" aria-labelledby="s29b-about">
  <span class="label" id="s29b-about">Про будинок</span>
  <p class="statement" data-reveal-lines>
    <span class="line"><span>Колекція</span></span>
    <span class="line"><span>48 квартир</span></span>
  </p>
  <div class="two" style="margin-top:clamp(3rem,8vh,6rem)">
    <p class="words" data-reveal-words style="margin:0;text-align:left">У ньому поєднуються естетика, натхненна архітектурою одеської класики, традиційна якість Будинків Каркашадзе, прекрасне місце розташування й паркова прибудинкова територія.</p>
    <p class="lead">Щоб зробити Ваше проживання ще більш комфортним і спокійним, ми передбачили всього 48 квартир у будинку. Скління квартир більше за рахунок панорамних вікон з алюмінієвих вітражів. Хол просторий, його дизайн архітектори продумали до дрібниць. Технічне оснащення: обладнання останнього покоління від кращих європейських виробників.</p>
  </div>
</section>

<section class="air loc" aria-labelledby="s29b-loc">
  <div class="loc__text">
    <h2 class="label" id="s29b-loc">Розташування</h2>
    <p class="big-dist"><b>500</b><span>метрів<br>до моря</span></p>
    <p class="lead">Ви немов живете за містом, однак залишаєтеся в безпосередній близькості до його ділового та культурно-розважального життя. До значущих місць Одеси можна дістатися пішки або за кілька хвилин автомобілем.</p>
    <a class="act act--quiet loc__map" href="https://www.google.com/maps/search/?api=1&amp;query=46.4610972%2C30.7569145" target="_blank" rel="noopener">Дивитися на карті</a>
  </div>
  {loc_schema()}
</section>
<section class="pans" aria-label="Вид">{pan('fb29b/view-sea', 'Захоплюючі краєвиди <br>на море та місто', '', '(max-width: 900px) 200vw, min(125vw, 1520px)', cls='pan--top')}</section>

<section class="pans pans--adv" aria-label="Переваги">
  {pan('fb29b/terrace', 'Тераси або балкони', 'В кожній квартирі. Ми будуємо дім в одному з найзеленіших і мальовничих районів міста, щоб Ви завжди могли насолоджуватися краєвидами і свіжим повітрям.', '(max-width: 900px) 200vw, min(125vw, 1520px)')}
  <div class="pans pans--split pans--split-rev" style="padding-inline:0">
    {pan('fb29b/privacy-facade', 'Приватність', 'Всього 48 квартир у будинку.', '(max-width: 900px) 200vw, 52vw')}
    {pan('fb29b/lobby-hall', 'Стиль і розкіш', 'Інтер’єр холу й місць загального користування оздоблені преміальними матеріалами — мармур, ліпнина, натуральне дерево.', '(max-width: 900px) 200vw, 72vw')}
  </div>
  <div class="pans pans--split" style="padding-inline:0">
    {pan('fb29b/yard-family', 'Прибудинкова територія', 'Зручні лавки, яскраві клумби, ексклюзивний фонтан і стильні ліхтарі формують унікальний ландшафт благоустрою в стилі класицизму з сучасними елементами.', '(max-width: 900px) 200vw, 72vw')}
    {pan('fb29b/parking', 'Підземний паркінг', 'Високі стелі та просторі паркомісця.', '(max-width: 900px) 200vw, 52vw')}
  </div>
</section>
{perks([('zars-logo', 'Кращий девелопер міста', '30 років будівництва нерухомості преміум-класу.'), ('quiet-place', 'Тихе місце', 'Непроїздний провулок біля моря і паркової зони.'), ('panoramic', 'Вікна Schüco', 'Панорамні вікна з алюмінієвих вітражів.'), ('master-bedroom', 'Майстер-спальня', 'Планування кожної квартири передбачає майстер-спальню.'), ('energy', 'Енергоефективність', 'Утеплення стін, енергозберігаючі вікна, сучасна котельня.'), ('lifts', 'Ліфти', 'Ексклюзивні, просторі, швидкісні, безшумні, останнього покоління.'), ('autonomy', 'Автономність', 'Автономне водопостачання, дизель-генератор.'), ('security', 'Безпека', 'Територія, що цілодобово охороняється. Відеоспостереження, система контролю доступу.'), ('windows', 'Вікна', 'Енергозберігаючі — з алюмінію і натурального дерева (Євробрус).')])}

<section class="air" id="plans" aria-labelledby="s29b-plans">
  <span class="label">Планування квартир</span>
  <h2 class="title-lg" id="s29b-plans" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Оберіть квартиру</h2>
  {plans([('fb29b/plan-1k-54', '1-кімнатна квартира', '54,31 м²', '8 поверх'), ('fb29b/plan-3k-131', '3-кімнатна квартира', '131,32 м²', '8 поверх'), ('fb29b/plan-3k-119', '3-кімнатна квартира', '119,38 м²', '9 поверх'), ('fb29b/plan-ph-208', 'Пентхаус', '208 м²', 'верхній рівень')], 'Площі проєктні. За дозвільною документацією квартири є житловими приміщеннями, а пентхаус є технічним приміщенням.')}
</section>

<section class="air stage" aria-labelledby="s29b-build">
  <div class="stage__head">
    <h2 class="stage__title" id="s29b-build">Актуальна стадія будівництва</h2>
    <p class="stage__lead">Будується. Плановий строк здачі: IV квартал 2026.</p>
  </div>
  {stage_grid()}
</section>

{enquiry('Французький бульвар, 29Б')}
<p class="legal">«Французький бульвар, 29Б» є адресою, що використовується в рекламних цілях. Будівельна адреса: пров. Спортивний, 4 та бульвар Французький, 29-Б, м. Одеса. Квартири за дозвільною документацією є житловими приміщеннями, пентхаус є технічним приміщенням. Візуалізації та площі проєктні.</p>
{_footer(LOGO)}
{sym}
{SCRIPTS}
</body>
</html>
'''
open(os.path.join(ROOT, 'mock/fb29b.html'), 'w').write(fb29b)
print('fb29', len(fb29), 'fb29b', len(fb29b))
