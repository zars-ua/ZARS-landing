#!/usr/bin/env python3
"""Фото 11 зданих Будинків Каркашадзе для каруселі на сторінці девелопера.

Джерело: карусель https://zars.ua/objects/ (slider scale-slider), файли з
zars.ua/wp-content/uploads/2020/05/ у найбільшому доступному розмірі.
Завантажені в /tmp/zars-objects/img/<slug>.<ext> (slug = частина URL об'єкта).

  python3 tools/build_houses.py [тека_з_фото]
"""
import json, os, sys
from PIL import Image, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/zars-objects/img'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'houses')

# порядок і підписи — як у каруселі zars.ua/objects (від новішого до старшого)
HOUSES = [
    ('f29',  'Французький бульвар, 29',  '2017–2020'),
    ('f2',   'Французький бульвар, 2',   '2012–2016'),
    ('k9',   'Провулок Каркашадзе, 9',   '2008–2011'),
    ('k7',   'Провулок Каркашадзе, 7',   '2003–2007'),
    ('d4a',  'Вулиця Довженка, 4А',      '2003–2007'),
    ('d4',   'Вулиця Довженка, 4',       '2003–2006'),
    ('k3',   'Провулок Каркашадзе, 3/1', '2003–2006'),
    ('f35',  'Французький бульвар, 35',  '2001–2003'),
    ('d2',   'Вулиця Довженка, 2',       '1999–2002'),
    ('d6a',  'Вулиця Довженка, 6А',      '1997–2000'),
    ('d6',   'Вулиця Довженка, 6',       '1996–1999'),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for slug, name, years in HOUSES:
        path = next(os.path.join(SRC, f) for f in os.listdir(SRC) if os.path.splitext(f)[0] == slug)
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
        widths = sorted(set([min(960, im.width), min(1600, im.width), im.width]))
        for w in widths:
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(
                os.path.join(OUT, f'{slug}-{w}.webp'), 'WEBP', quality=82, method=6)
        manifest.append({'slug': slug, 'name': name, 'years': years, 'widths': widths,
                         'ratio': round(im.width / im.height, 4),
                         'source': f'https://zars.ua/objects/{slug}/ · {os.path.basename(path)}'})
        print(slug, widths, round(im.width / im.height, 2))
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
