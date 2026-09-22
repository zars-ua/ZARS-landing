"""Єдиний підвал для всіх сторінок макета (22.09.2026): теракотовий, як на сторінці девелопера,
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
