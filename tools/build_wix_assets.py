#!/usr/bin/env python3
"""Готує зображення з двох Wix-лендингів замовника для сторінок ФБ29 і ФБ29Б.

Джерела (медіа завантажено з static.wixstatic.com у /tmp/zars-wix/media):
  https://marketing89613.wixsite.com/website-1       — ФБ29Б
  https://marketing89613.wixsite.com/penthouse_fb29  — ФБ29, пентхаус

Результат: assets/wix/<проєкт>/<ім'я>-<ширина>.webp + assets/wix/manifest.json
(ширини, пропорція, походження). Плани квартир — одна-дві ширини, без втрат якості.

  python3 tools/build_wix_assets.py [теку_з_медіа]
"""
import json, os, sys
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/zars-wix/media'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'wix')

W1 = 'https://marketing89613.wixsite.com/website-1'
W2 = 'https://marketing89613.wixsite.com/penthouse_fb29'

PHOTOS = [
    # (проєкт, ім'я, wix id, лендинг)
    ('fb29b', 'view-sea',   'dbdfe3_c2c983369a8b44199434b38269e9b3de~mv2.jpg', W1),
    ('fb29b', 'tower',      'dbdfe3_4b7bbdca5b6f46c992f8e2b80126a295~mv2.jpg', W1),
    ('fb29b', 'terrace',    'dbdfe3_7366f0a6b858407ca04ec92e998235ee~mv2.jpg', W1),
    ('fb29b', 'yard',       'dbdfe3_0043c44898dc420ca4c34f2f63160a5b~mv2.jpg', W1),
    ('fb29b', 'parking',    '3cf61b_e55a583ab11146cfb10d1d3426146018~mv2.webp', W1),
    ('fb29b', 'lane',       'dbdfe3_005a9e3e2617447e8d708b804aaf0e72~mv2.jpg', W1),
    ('fb29b', 'courtyard',  'dbdfe3_1621d088f70e4f7f9c08ceac08ebafae~mv2.jpg', W1),
    ('fb29b', 'tower-park', 'dbdfe3_b506650edd774ebd95877c94c136e620~mv2.jpg', W1),
    ('fb29b', 'street',     'dbdfe3_ba1fe23a35ab49849c9fb1f880609e26~mv2.jpg', W1),
    ('fb29b', 'build-1',    'dbdfe3_ebba2d0b6d6b4694aeab0a2b91ef277f~mv2.jpg', W1),
    ('fb29b', 'build-2',    'dbdfe3_7de4fd6b24de455cb9e893b2bc3fd96f~mv2.jpg', W1),
    ('fb29b', 'build-3',    'dbdfe3_5d914b9fe10342e39d985212d8f75162~mv2.jpg', W1),
    ('fb29b', 'build-4',    'dbdfe3_3bf2dc763e1b460db6af9d029610d9c7~mv2.jpg', W1),
    ('zars',  'office',     '3cf61b_3994e954fde641a1a93a00950acaa72e~mv2.webp', W1),
    ('fb29',  'path',       '18e4f2_8414f8147ba645d99e746ee2ab047820~mv2.jpg', W2),
    ('fb29',  'rise',       '18e4f2_dab4fef0baeb44959536bdf073843676~mv2.jpg', W2),
    ('fb29',  'tower-green','18e4f2_dfa483581da340949a65426f2b54e6d0~mv2.jpg', W2),
    ('fb29',  'autumn',     '18e4f2_61571b7a9aa34a4b90a18498f661236e~mv2.jpg', W2),
    ('fb29',  'garden',     '18e4f2_fda35ed91a684b769888f16afbf4dac9~mv2.png', W2),
    ('fb29',  'lobby',      '18e4f2_bf7eb4f325ca48619621e2bcc8db9db4~mv2.jpg', W2),
    ('fb29',  'parking',    '18e4f2_150669bcdd7540dba57bbe9f09b593eb~mv2.jpg', W2),
    ('fb29',  'sea',        '18e4f2_e729173819aa4793b12ed2c13bc70be4~mv2.jpg', W2),
    ('fb29',  'dusk',       '18e4f2_6c2c967b17f7420f855fa493102e6ba3~mv2.jpg', W2),
    ('fb29',  'entrance',   '18e4f2_d34a599db8934127850436d781a9e595~mv2.jpg', W2),
]
PLANS = [
    ('fb29b', 'plan-3k-131', 'dbdfe3_79416a3ed6d44647a01027e02590d9fb~mv2.png', W1),
    ('fb29b', 'plan-3k-119', 'dbdfe3_ab095dd6f57441d8971946911694ce1d~mv2.png', W1),
    ('fb29b', 'plan-1k-54',  'dbdfe3_0dde9967bada42ebbecfae36be2165e7~mv2.png', W1),
    ('fb29b', 'plan-ph-208', 'dbdfe3_e03125af313c4a1eb36df21c65283802~mv2.png', W1),
    ('fb29',  'plan-164-a',  'dbdfe3_cdad5bec0c424ae8a6462459041684fc~mv2.jpg', W2),
    ('fb29',  'plan-164-b',  'dbdfe3_4fee9a30105240f48905dd43b17b5eaa~mv2.jpg', W2),
]


def save(im, path, **kw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, 'WEBP', method=6, **kw)


def main():
    manifest = {}
    for proj, name, wid, page in PHOTOS:
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, wid))).convert('RGB')
        widths = [w for w in (960, 1600, 2400) if w < im.width] + ([] if im.width >= 2400 else [im.width])
        widths = sorted(set(min(w, im.width) for w in widths))
        for w in widths:
            save(im.resize((w, round(im.height * w / im.width)), Image.LANCZOS),
                 os.path.join(OUT, proj, f'{name}-{w}.webp'), quality=80)
        manifest[f'{proj}/{name}'] = {'widths': widths, 'ratio': round(im.width / im.height, 4),
                                      'source': f'{page} · static.wixstatic.com/media/{wid}'}
    for proj, name, wid, page in PLANS:
        im = Image.open(os.path.join(SRC, wid)).convert('RGB')
        # обрізати білі поля навколо креслення
        bbox = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 18 else 0).getbbox()
        if bbox:
            pad = 24
            im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                          min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
        widths = sorted(set(min(w, im.width) for w in (1200, 2400)))
        for w in widths:
            save(im.resize((w, round(im.height * w / im.width)), Image.LANCZOS),
                 os.path.join(OUT, proj, f'{name}-{w}.webp'), quality=92)
        manifest[f'{proj}/{name}'] = {'widths': widths, 'ratio': round(im.width / im.height, 4),
                                      'source': f'{page} · static.wixstatic.com/media/{wid}'}
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    for k, v in manifest.items():
        print(k, v['widths'], v['ratio'])


if __name__ == '__main__':
    main()
