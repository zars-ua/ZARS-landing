#!/usr/bin/env python3
"""Готує зображення для сайту ЗАРС: обрізає під потрібне співвідношення,
робить WebP у кількох ширинах і крихітний LQIP-плейсхолдер у base64.

Запуск:  python3 tools/build_images.py
Джерела лежать поза репозиторієм (папки з фірмовим стилем на Desktop).
"""
import base64, io, json, os, sys
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FB29  = '/Users/manager/Desktop/ФБ29а/Избранные фото ФБ29 2'
SRC_FB29B = '/Users/manager/Desktop/ФБ29б/ Новые визы 2'

# name, source file, aspect (w/h) or None to keep, focal point (0..1 vertical)
JOBS = [
    # ---------- Французький бульвар, 29 (зданий) ----------
    ('fb29/hero',        SRC_FB29,  '800_7751-NEF.jpg_',                    21/9,  0.50),
    ('fb29/dusk-wide',   SRC_FB29,  '800_7763_00001.jpg_',                  16/9,  0.45),
    ('fb29/sea',         SRC_FB29,  '8002213-NEF_DxO_DeepPRIMEXD (1).jpg_', 16/9,  0.45),
    ('fb29/treeline',    SRC_FB29,  '800_4613 (1).jpg',                     4/3,   0.50),
    ('fb29/facade',      SRC_FB29,  '800_1981.jpg',                         3/4,   0.45),
    ('fb29/curve',       SRC_FB29,  '8008547.JPG_',                         1/1,   0.45),
    ('fb29/entrance',    SRC_FB29,  '800_7461.jpg',                         3/4,   0.50),
    ('fb29/fountain',    SRC_FB29,  '800_5796.jpg',                         3/4,   0.50),
    ('fb29/water',       SRC_FB29,  '800_5811.jpg',                         1/1,   0.50),
    ('fb29/dusk-park',   SRC_FB29,  '800_5837.jpg',                         16/9,  0.50),
    ('fb29/lobby',       SRC_FB29,  '800_8423_15.jpg_',                     3/2,   0.50),
    ('fb29/canopy',      SRC_FB29,  'DSC_5505.jpg',                         3/4,   0.50),
    ('fb29/garden',      SRC_FB29,  '800_5863.jpg',                         16/9,  0.50),
    ('fb29/porch',       SRC_FB29,  '8008743.JPG_',                         3/2,   0.50),
    ('fb29/aerial',      SRC_FB29,  '2 (4).jpg',                            4/3,   0.45),

    # ---------- Французький бульвар, 29Б (будується) ----------
    ('fb29b/hero',       SRC_FB29B, '2.jpg',                                21/9,  0.50),
    ('fb29b/street',     SRC_FB29B, '1.jpg',                                16/9,  0.50),
    ('fb29b/among',      SRC_FB29B, '5.jpg',                                4/3,   0.50),
    ('fb29b/terrace',    SRC_FB29B, '9.jpg',                                3/2,   0.50),
    ('fb29b/terraces',   SRC_FB29B, '6.jpg',                                4/3,   0.50),
    ('fb29b/commerce',   SRC_FB29B, '10.jpg',                               3/2,   0.50),
    ('fb29b/court',      SRC_FB29B, '12.jpg',                               16/9,  0.50),
    ('fb29b/sunset',     SRC_FB29B, '3.jpg',                                16/9,  0.50),
    ('fb29b/promenade',  SRC_FB29B, '4.jpg',                                3/2,   0.50),
]

WIDTHS = [480, 960, 1440, 1920, 2560]
QUALITY = 80


def crop_to(im, aspect, focal):
    w, h = im.size
    if aspect is None:
        return im
    target = aspect
    cur = w / h
    if abs(cur - target) < 0.01:
        return im
    if cur > target:                      # надто широке → ріжемо по боках
        nw = int(round(h * target))
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(round(w / target))           # надто високе → ріжемо по вертикалі до фокуса
    y = int(round((h - nh) * focal))
    y = max(0, min(h - nh, y))
    return im.crop((0, y, w, y + nh))


def lqip(im):
    t = im.copy()
    t.thumbnail((20, 20))
    t = t.filter(ImageFilter.GaussianBlur(0.6))
    buf = io.BytesIO()
    t.save(buf, 'WEBP', quality=42)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def main():
    manifest = {}
    total = 0
    for name, src_dir, fname, aspect, focal in JOBS:
        path = os.path.join(src_dir, fname)
        if not os.path.exists(path):
            print(f'  ПРОПУЩЕНО (немає файлу): {path}', file=sys.stderr)
            continue
        im = Image.open(path)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im = crop_to(im, aspect, focal)
        out_dir = os.path.join(ROOT, 'assets/img', os.path.dirname(name))
        os.makedirs(out_dir, exist_ok=True)
        base = os.path.basename(name)
        made = []
        for w in WIDTHS:
            if w > im.width * 1.02:
                continue
            r = im.resize((w, max(1, round(w * im.height / im.width))), Image.LANCZOS)
            out = os.path.join(out_dir, f'{base}-{w}.webp')
            r.save(out, 'WEBP', quality=QUALITY, method=6)
            made.append(w)
            total += os.path.getsize(out)
        manifest[name] = {
            'widths': made,
            'ratio': round(im.width / im.height, 4),
            'lqip': lqip(im),
        }
        print(f'{name:20} {im.width}x{im.height}  ->  {made}')
    with open(os.path.join(ROOT, 'assets/img/manifest.json'), 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f'\nВсього: {len(manifest)} зображень, {total/1e6:.1f} MB')


if __name__ == '__main__':
    main()
