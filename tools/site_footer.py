"""Спільні блоки всіх сторінок: форма «Приватна презентація» (22.09.2026 — і на сторінці девелопера) та
єдиний підвал для всіх сторінок макета (22.09.2026): теракотовий, як на сторінці девелопера,
з колонками «Проєкти», «Контакти», «Адреса», «Соціальні мережі» і великим знаком ЗАРС унизу.
Стилі — mock.css (.d-foot), поява знака — dev.js / motion.js."""

def footer(logo_svg):
    return f'''<footer class="d-foot" id="contacts">
  <div class="d-foot__grid">
    <div><h2>Проєкти</h2><ul><li><a href="fb29.html">Французький бульвар, 29</a></li><li><a href="fb29b.html">Французький бульвар, 29Б</a></li></ul></div>
    <div><h2>Контакти</h2><ul><li><a href="tel:+380671608877">+380 (67) 160 88 77</a></li><li><a href="mailto:estate@zars.ua">estate@zars.ua</a></li></ul></div>
    <div><h2>Адреса</h2><ul><li>Одеса,<br>Французький бульвар, 2</li></ul></div>
    <div><h2>Соціальні мережі</h2><ul><li><a href="https://www.instagram.com/zars.ua/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.facebook.com/www.zars.ua/" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    <p class="d-foot__copy">© 1996-2026 ЗАРС</p>
  </div>
  <div class="d-foot__mark" aria-hidden="true">{logo_svg}</div>
</footer>'''


PHONE, TEL = '+380 (67) 160 88 77', '+380671608877'

def enquiry(project):
    opts = ''.join(f'<option{" selected" if p == project else ""}>{p}</option>' for p in ['Французький бульвар, 29', 'Французький бульвар, 29Б'] + (['Ще не визначились'] if project == 'Ще не визначились' else []))
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

