#!/usr/bin/env python3
"""Зображення сторінки девелопера (15.09.2026).

  Будинки Каркашадзе:  ~/Desktop/Обработанные фото ДК/*.jpg  → assets/dk/<slug>-{1280,1920,2560}.webp
                                                               + портретний кадр <slug>-p-{720,1080}.webp
  Фото для сайту:      ~/Desktop/Фото для сайта/               → assets/zars/{office,founder,manifest}
  Блоки про будинки:   zars.ua/objects (wp-content/uploads)     → assets/zars/<ім'я>-<w>.webp
"""
import json, os, unicodedata
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DK = os.path.expanduser('~/Desktop/Обработанные фото ДК')
PH = os.path.expanduser('~/Desktop/Фото для сайта')
ZB = '/tmp/zars-objects/blockimg'
N = lambda s: unicodedata.normalize('NFC', s)

# хронологічно — від першого будинку до ФБ29; (slug, файл, назва, роки, фокус x для портрета)
HOUSES = [
    ('d6',  'Довженко, 6.jpg',               'Вулиця Довженка, 6',       '1996–1999', 0.5),
    ('d6a', 'Довженко, 6А.jpg',              'Вулиця Довженка, 6А',      '1997–2000', 0.47),
    ('d2',  'Довженко, 2.jpg',               'Вулиця Довженка, 2',       '1999–2002', 0.55),
    ('f35', 'Французкий бульвар, 35.jpg',    'Французький бульвар, 35',  '2001–2003', 0.5),
    ('k3',  'Каркашадзе 3_1.jpg',            'Провулок Каркашадзе, 3/1', '2003–2006', 0.5),
    ('d4',  'Довженко, 4.jpg',               'Вулиця Довженка, 4',       '2003–2006', 0.5),
    ('d4a', 'Довженко, 4А.jpg',              'Вулиця Довженка, 4А',      '2003–2007', 0.5),
    ('k7',  'Каркашадзе 7.jpg',              'Провулок Каркашадзе, 7',   '2003–2007', 0.5),
    ('k9',  'Каркашадзе 9.jpg',              'Провулок Каркашадзе, 9',   '2008–2011', 0.5),
    ('f2',  'Французкий бульвар, 2.jpg',     'Французький бульвар, 2',   '2012–2016', 0.45),
    ('f29', 'Французкий бульвар, 29.jpg',    'Французький бульвар, 29',  '2017–2020', 0.42),
]


def find(folder, name):
    for f in os.listdir(folder):
        if N(f) == N(name):
            return os.path.join(folder, f)
    raise FileNotFoundError(name)


def crop(im, ratio, fx=0.5, fy=0.5):
    W, H = im.size
    if W / H > ratio:
        cw, ch = int(H * ratio), H
    else:
        cw, ch = W, int(W / ratio)
    x = int(min(max(W * fx - cw / 2, 0), W - cw)); y = int(min(max(H * fy - ch / 2, 0), H - ch))
    return im.crop((x, y, x + cw, y + ch))


def out(im, path, widths, q=80):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    done = []
    for w in widths:
        w = min(w, im.width)
        if w in done: continue
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f'{path}-{w}.webp', 'WEBP', quality=q, method=6)
        done.append(w)
    return done


def main():
    man = {'houses': [], 'zars': {}}
    for slug, fn, name, years, fx in HOUSES:
        im = ImageOps.exif_transpose(Image.open(find(DK, fn))).convert('RGB')
        wide = out(crop(im, 16 / 9, fx), f'{ROOT}/assets/dk/{slug}', [1280, 1920, 2560], 78)
        tall = out(crop(im, 3 / 4, fx), f'{ROOT}/assets/dk/{slug}-p', [720, 1080], 78)
        man['houses'].append({'slug': slug, 'name': name, 'years': years, 'wide': wide, 'tall': tall,
                              'source': f'~/Desktop/Обработанные фото ДК/{fn}'})
        print(slug, wide, tall)
    office = ImageOps.exif_transpose(Image.open(find(PH, '8.-Офис-ЗАРС-_фасад_-_1_.webp'))).convert('RGB')
    man['zars']['office'] = {'w': out(crop(office, 16 / 10, 0.52), f'{ROOT}/assets/zars/office', [960, 1600, 2400]), 'ratio': '16/10'}
    man['zars']['office-m'] = {'w': out(crop(office, 4 / 5, 0.55), f'{ROOT}/assets/zars/office-m', [720, 1080]), 'ratio': '4/5'}
    founder = ImageOps.exif_transpose(Image.open(find(PH, 'Гиви Силованович (2).jpg'))).convert('L').convert('RGB')
    man['zars']['founder'] = {'w': out(founder, f'{ROOT}/assets/zars/founder', [600, 1206], 84), 'ratio': f'{founder.width}/{founder.height}'}
    mf = ImageOps.exif_transpose(Image.open(find(PH, '_8008546.jpg'))).convert('RGB')
    man['zars']['manifest'] = {'w': out(crop(mf, 16 / 9, 0.5, 0.45), f'{ROOT}/assets/zars/manifest', [1280, 1920, 2560])}
    man['zars']['manifest-p'] = {'w': out(crop(mf, 3 / 4, 0.62), f'{ROOT}/assets/zars/manifest-p', [720, 1080])}
    blocks = {'arch': 'architect.jpg', 'landscape': 'blagoustiry.jpg', 'interiors': '800_8423_16.jpg', 'ergonomics': 'ergonomika-1.jpg',
              'parking': 'parking.jpg', 'brick': 'kirpich.jpg', 'marble': 'mramur-16.jpg', 'windows': 'okna.png',
              'kids': 'playgrounds_fb29-1.png', 'security': 'bezpeka.jpg', 'service': 'service_sl3.png', 'art': '800_8423_8-2.jpg'}
    for name, fn in blocks.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(ZB, fn))).convert('RGB')
        man['zars'][name] = {'w': out(im, f'{ROOT}/assets/zars/{name}', [960, 1600]), 'ratio': round(im.width / im.height, 3),
                             'source': f'https://zars.ua/objects/ · {fn}'}
    json.dump(man, open(f'{ROOT}/assets/zars/manifest.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(man['zars'], ensure_ascii=False))


if __name__ == '__main__':
    main()
