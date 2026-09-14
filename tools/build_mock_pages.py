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

def pan(key, title, text, sizes='100vw'):
    return f'''<figure class="pan">{pic(key, title, sizes)}
    <figcaption class="pan__cap"><h3 class="pan__title">{title}</h3><p class="pan__text">{text}</p></figcaption></figure>'''

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
    <button class="act" type="submit">Запросити приватну презентацію</button>
    <p class="form__msg" role="status" aria-live="polite"></p>
  </form>
</section>'''

FOOT = '''<footer class="foot" id="contacts">
  <div><a class="foot__logo" href="index.html" aria-label="ЗАРС">{logo}</a></div>
  <div><h4>Проєкти</h4><ul><li><a href="fb29.html">Французький бульвар, 29</a></li><li><a href="fb29b.html">Французький бульвар, 29Б</a></li><li><a href="index.html">Девелопер</a></li></ul></div>
  <div><h4>Контакти</h4><ul><li><a href="tel:+380671608877">+380 (67) 160 88 77</a></li><li><a href="mailto:estate@zars.ua">estate@zars.ua</a></li><li>Одеса, Французький бульвар, 2</li></ul></div>
  <p class="foot__copy">© 1996-2026 ЗАРС. Якість. Естетика. Традиції.</p>
</footer>'''

SCRIPTS = '''<script src="../assets/vendor/gsap.min.js" defer></script>
<script src="../assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="../assets/vendor/lenis.min.js" defer></script>
<script src="motion.js" defer></script>
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
</section>

<section class="pans pans--split" aria-label="Концепція">
  {pan('fb29/path', 'Приватність', 'Лише три квартири на поверсі. На території комплексу немає торговельно-офісних приміщень і сторонньої інфраструктури.', '(max-width: 900px) 100vw, 60vw')}
  {pan('fb29/rise', 'Комфорт', 'Концепція будинку на Французькому бульварі, 29 передбачає комфорт та абсолютну приватність мешканців.', '(max-width: 900px) 100vw, 40vw')}
</section>

<section class="air" aria-labelledby="s29-loc">
  <span class="label" id="s29-loc">Розташування</span>
  <div class="two">
    <div>
      <p class="big-dist"><b>400</b><span>метрів до моря</span></p>
      <p class="lead">Скільки існує Одеса, стільки Французький бульвар вважається кращим місцем для життя тут. Поєднання чистого морського та «лісового» повітря створює найкращі екологічні умови для життя.</p>
    </div>
    {dist([('Траса здоров’я', '200 м'), ('Яхт-клуб', '400 м'), ('Одеська кіностудія', '420 м'), ('Театр музичної комедії', '900 м'), ('Театр опери та балету', '3,9 км'), ('Аркадія', '4,4 км'), ('Аеропорт', '9,4 км')])}
  </div>
</section>
<section class="pans" aria-label="Море">{pan('fb29/sea', 'Чорне море', 'Вид на море та місто з верхніх поверхів.')}</section>

<section class="air" aria-labelledby="s29-adv">
  <h2 class="title-lg" id="s29-adv">Переваги</h2>
</section>
<section class="pans" aria-label="Переваги">
  {pan('fb29/lobby', 'Виправдана розкіш', 'Оздоблення місць загального користування мармуром, деревом, оніксом.')}
  <div class="pans pans--split" style="padding-inline:0">
    {pan('fb29/garden', 'Благоустрій', 'Фонтани, площадки для відпочинку дітей та дорослих.', '(max-width: 900px) 100vw, 60vw')}
    {pan('fb29/parking', 'Паркінг', 'Підземний паркінг на 149 місць.', '(max-width: 900px) 100vw, 40vw')}
  </div>
</section>
<section class="air">
  {facts([('Кращий девелопер міста', '30 років будівництва нерухомості преміум-класу.'), ('Панорамні вікна', 'Алюміній та натуральне дерево (Євробрус).'), ('Автономність', 'Автономне теплопостачання, дизель-генератор.'), ('Безпека', 'Територія, що цілодобово охороняється, відеоспостереження.'), ('Розташування', 'Французький бульвар, 400 метрів до моря.'), ('Три квартири на поверсі', 'Абсолютна приватність мешканців.')])}
</section>

<section class="air" id="plans" aria-labelledby="s29-plans">
  <span class="label">Планування</span>
  <h2 class="title-lg" id="s29-plans" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Трикімнатна квартира, 164,5 м²</h2>
  {plans([('fb29/plan-164-a', 'Варіант А', '164,5 м²', '11 поверх · вид на море та місто'), ('fb29/plan-164-b', 'Варіант Б', '164,5 м²', '11 поверх · вид на море та місто')], 'Площа проєктна. Детальні характеристики й наявність покажемо під час приватної презентації.')}
</section>

<section class="air awards" aria-labelledby="s29-awards">
  <div>
    <h2 class="title-lg" id="s29-awards">Відзнака проєкту</h2>
    <p class="lead">У 2021 році в Лондоні Будинок Каркашадзе Французький бульвар, 29 був відзначений міжнародною премією International Property Awards у 4 номінаціях.</p>
  </div>
  <div class="awards__ribbons">''' + ''.join(
    f'<figure><img src="../assets/awards/ipa-{s}-960.webp" srcset="../assets/awards/ipa-{s}-480.webp 1x, ../assets/awards/ipa-{s}-960.webp 2x" width="113" height="480" alt="European Property Awards 2021-2022: {t}" loading="lazy"><figcaption>{t}</figcaption></figure>'
    for s, t in [('high-rise-development', 'Residential High Rise Development'), ('high-rise-architecture', 'Residential High Rise Architecture'), ('architecture-multiple-residence', 'Architecture Multiple Residence'), ('residential-development', 'Residential Development')]) + f'''</div>
</section>

<section class="air" aria-labelledby="s29-photo">
  <h2 class="title-lg" id="s29-photo" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Фото</h2>
  {gallery([('fb29/tower-green', 'Будинок над зеленню парку', 'e-7'), ('fb29/canopy', 'Біонічні навіси і фасад будинку', 'e-5'), ('fb29/autumn', 'Будинок на тлі осіннього парку', 'e-12'), ('fb29/dusk', 'Будинок у парку з моря', 'e-6'), ('fb29/garden', 'Прибудинкова територія', 'e-6')])}
</section>

{enquiry('Французький бульвар, 29')}
{FOOT.format(logo=LOGO)}
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

<section class="pans" aria-label="Будинок">{pan('fb29b/tower', 'Одеська класика', 'Естетика, натхненна архітектурою одеської класики.')}</section>

<section class="air" aria-labelledby="s29b-loc">
  <span class="label" id="s29b-loc">Розташування</span>
  <div class="two">
    <div>
      <p class="big-dist"><b>500</b><span>метрів до моря</span></p>
      <p class="lead">Ви немов живете за містом, однак залишаєтеся в безпосередній близькості до його ділового та культурно-розважального життя. До значущих місць Одеси можна дістатися пішки або за кілька хвилин автомобілем.</p>
    </div>
    {dist([('Траса здоров’я', '350 м'), ('Одеська кіностудія', '350 м'), ('Яхт-клуб', '450 м'), ('Театр музкомедії', '900 м'), ('Оперний театр', '3,9 км'), ('Аркадія', '4,4 км'), ('Аеропорт', '9,4 км')])}
  </div>
</section>
<section class="pans" aria-label="Вид">{pan('fb29b/view-sea', 'Тихе місце', 'Непроїздний провулок біля моря і паркової зони.')}</section>

<section class="air" aria-labelledby="s29b-adv">
  <h2 class="title-lg" id="s29b-adv">Переваги</h2>
</section>
<section class="pans" aria-label="Переваги">
  {pan('fb29b/terrace', 'Тераси або балкони', 'В кожній квартирі. Ми будуємо дім в одному з найзеленіших і мальовничих районів міста, щоб Ви завжди могли насолоджуватися краєвидами і свіжим повітрям.')}
  <div class="pans pans--split" style="padding-inline:0">
    {pan('fb29b/yard', 'Прибудинкова територія', 'Паркова територія, що цілодобово охороняється.', '(max-width: 900px) 100vw, 60vw')}
    {pan('fb29b/parking', 'Підземний паркінг', 'Місця для автомобілів мешканців під будинком.', '(max-width: 900px) 100vw, 40vw')}
  </div>
</section>
<section class="air">
  {facts([('Кращий девелопер міста', '30 років будівництва нерухомості преміум-класу.'), ('Камерність і приватність', 'Менше 50 квартир у будинку.'), ('Майстер-спальня', 'Планування кожної квартири передбачає майстер-спальню.'), ('Стиль і розкіш', 'Інтер’єр холу й місць загального користування оздоблені преміальними матеріалами — мармур, ліпнина, натуральне дерево.'), ('Енергоефективність', 'Утеплення стін, енергозберігаючі вікна, сучасна котельня.'), ('Автономність', 'Автономне водопостачання, дизель-генератор.'), ('Вікна Schüco', 'Панорамні вікна з алюмінієвих вітражів.'), ('Безпека', 'Територія, що цілодобово охороняється. Відеоспостереження, система контролю доступу.')])}
</section>

<section class="air" id="plans" aria-labelledby="s29b-plans">
  <span class="label">Планування квартир</span>
  <h2 class="title-lg" id="s29b-plans" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Оберіть квартиру</h2>
  {plans([('fb29b/plan-1k-54', '1-кімнатна квартира', '54,31 м²', '8 поверх'), ('fb29b/plan-3k-131', '3-кімнатна квартира', '131,32 м²', '8 поверх'), ('fb29b/plan-3k-119', '3-кімнатна квартира', '119,38 м²', '9 поверх'), ('fb29b/plan-ph-208', 'Пентхаус', '208 м²', 'верхній рівень')], 'Площі проєктні. За дозвільною документацією квартири є житловими приміщеннями, а пентхаус є технічним приміщенням.')}
</section>

<section class="air" aria-labelledby="s29b-build">
  <div style="margin-bottom:clamp(2.5rem,6vh,4rem)">
    <h2 class="title-lg" id="s29b-build">Актуальна стадія будівництва</h2>
    <p class="lead">Будується. Плановий строк здачі: IV квартал 2026.</p>
  </div>
  {gallery([('fb29b/build-1', 'Фасад будинку на стадії будівництва', 'e-4'), ('fb29b/build-2', 'Будинок і будівельний кран', 'e-8'), ('fb29b/build-3', 'Балкони фасаду', 'e-5 e-low'), ('fb29b/build-4', 'Тераса на стадії будівництва', 'e-7')])}
</section>

<section class="air" aria-labelledby="s29b-gal">
  <h2 class="title-lg" id="s29b-gal" style="margin-bottom:clamp(2.5rem,6vh,4rem)">Галерея</h2>
  {gallery([('fb29b/tower-park', 'Будинок серед парку', 'e-12'), ('fb29b/lane', 'Провулок біля будинку', 'e-7'), ('fb29b/courtyard', 'Двір і дитячий майданчик', 'e-5'), ('fb29b/street', 'Фасад з боку вулиці', 'e-12')])}
</section>

{enquiry('Французький бульвар, 29Б')}
<p class="legal">«Французький бульвар, 29Б» є адресою, що використовується в рекламних цілях. Будівельна адреса: пров. Спортивний, 4 та бульвар Французький, 29-Б, м. Одеса. Квартири за дозвільною документацією є житловими приміщеннями, пентхаус є технічним приміщенням. Візуалізації та площі проєктні.</p>
{FOOT.format(logo=LOGO)}
{sym}
{SCRIPTS}
</body>
</html>
'''
open(os.path.join(ROOT, 'mock/fb29b.html'), 'w').write(fb29b)
print('fb29', len(fb29), 'fb29b', len(fb29b))
