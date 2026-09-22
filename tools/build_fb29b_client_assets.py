#!/usr/bin/env python3
"""Матеріали клієнта для ФБ29Б від 21.09.2026 → assets.
Джерело (поза репо): ~/Desktop/ФБ29б/Від клієнта 21.09.2026/
  - 3 рендери для карток переваг → assets/wix/fb29b/<ім'я>-<ширина>.webp + запис у assets/wix/manifest.json
  - схема розташування з zars.ua/objects/fr29b (zars_map.svg) → assets/map/fr29b-map.svg,
    перефарбована в палітру сторінки: іконки #8c3b19 → фірмовий #913814, блакитні хвилі моря → сірий.
Іконки переваг (assets/icons/fb29b/*.svg) обведено з PNG клієнта potrace-ом окремо, тут не генеруються."""
import json, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.expanduser('~/Desktop/ФБ29б/Від клієнта 21.09.2026')
MAN = os.path.join(ROOT, 'assets/wix/manifest.json')
IMAGES = [('yard-family', 'прибудинкова-територія.png'), ('privacy-facade', 'приватність-фасад.png'), ('lobby-hall', 'стиль-і-розкіш-хол.png')]

m = json.load(open(MAN))
for name, fn in IMAGES:
    im = Image.open(os.path.join(SRC, fn)).convert('RGB')
    widths = [w for w in (960, 1600, 1920) if w < im.width] + [im.width if im.width <= 2000 else 1920]
    widths = sorted(set(widths))
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(ROOT, f'assets/wix/fb29b/{name}-{w}.webp'), quality=82, method=6)
    m[f'fb29b/{name}'] = {'widths': widths, 'ratio': round(im.width / im.height, 4), 'source': f'клієнт, 21.09.2026 · {fn}'}
    print(name, widths)
json.dump(m, open(MAN, 'w'), ensure_ascii=False, indent=1)

svg = open(os.path.join(SRC, 'zars_map-оригінал-zars-ua.svg')).read()
svg = svg.replace('#8c3b19', '#913814').replace('#aebadb', '#BFC3C4')
open(os.path.join(ROOT, 'assets/map/fr29b-map.svg'), 'w').write(svg)
print('map', len(svg))

# ФБ29 (22.09.2026): фото благоустрою від клієнта — ~/Desktop/WEBP/Благоустройство.webp
src29 = os.path.expanduser('~/Desktop/WEBP/Благоустройство.webp')
im = Image.open(src29).convert('RGB')
widths = [960, 1600, im.width]
for w in widths:
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(ROOT, f'assets/wix/fb29/landscaping-{w}.webp'), quality=82, method=6)
m = json.load(open(MAN))
m['fb29/landscaping'] = {'widths': widths, 'ratio': round(im.width / im.height, 4), 'source': 'клієнт, 22.09.2026 · ~/Desktop/WEBP/Благоустройство.webp'}
json.dump(m, open(MAN, 'w'), ensure_ascii=False, indent=1)
print('fb29/landscaping', widths)
