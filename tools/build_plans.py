#!/usr/bin/env python3
"""Витягує поверхові плани з буклетів як растрові WebP без втрат.

Підписи всередині планів («2К 110,2 м²», розміри) мовно-нейтральні,
тож вони лишаються як є. Російські підписи сторінок («2 этаж», «Море»,
«Французский бульвар») лежать поза кадром плану і в кроп не потрапляють.

Запуск:  python3 tools/build_plans.py
"""
import io, json, os, sys
import fitz
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/plans')
WIDTHS = [1200, 2400]   # креслення без втрат: 2400 px вистачає для зуму

BOOK_B = '/Users/manager/Desktop/ФБ29б/ФБ, 29б - электронная презентация (1).pdf'
BOOK_A = '/Users/manager/Desktop/ФБ29а/fr29 (1) (1).pdf'

# (файл, сторінка, половина L/R, id, підпис укр., підзаголовок)
PLATES = [
    # ---- Французький бульвар, 29Б ----
    (BOOK_B, 34, 'R', 'fb29b-f1',  '1 поверх',      None),
    (BOOK_B, 35, 'L', 'fb29b-f2',  '2 поверх',      None),
    (BOOK_B, 35, 'R', 'fb29b-f3',  '3 поверх',      None),
    (BOOK_B, 36, 'L', 'fb29b-f47', '4–7 поверхи',   None),
    (BOOK_B, 36, 'R', 'fb29b-f8',  '8 поверх',      None),
    (BOOK_B, 37, 'L', 'fb29b-f9',  '9 поверх',      None),
    (BOOK_B, 37, 'R', 'fb29b-f10', '10 поверх',     None),
    (BOOK_B, 38, 'L', 'fb29b-ph',  'Пентхаус',      None),
    # ---- Французький бульвар, 29 (три секції) ----
    (BOOK_A, 33, 'R', 'fb29-s1-f1',  '1 поверх',           'I секція'),
    (BOOK_A, 34, 'L', 'fb29-s1-f2',  '2 поверх',           'I секція'),
    (BOOK_A, 34, 'R', 'fb29-s1-ft',  'Типовий поверх',     'I секція'),
    (BOOK_A, 35, 'L', 'fb29-s1-p1',  'Пентхаус, рівень 1', 'I секція'),
    (BOOK_A, 35, 'R', 'fb29-s1-p2',  'Пентхаус, рівень 2', 'I секція'),
    (BOOK_A, 36, 'R', 'fb29-s2-f1',  '1 поверх',           'II секція'),
    (BOOK_A, 37, 'L', 'fb29-s2-f2',  '2 поверх',           'II секція'),
    (BOOK_A, 37, 'R', 'fb29-s2-ft',  'Типовий поверх',     'II секція'),
    (BOOK_A, 38, 'L', 'fb29-s2-p1',  'Пентхаус, рівень 1', 'II секція'),
    (BOOK_A, 38, 'R', 'fb29-s2-p2',  'Пентхаус, рівень 2', 'II секція'),
    (BOOK_A, 39, 'R', 'fb29-s3-f1',  '1 поверх',           'III секція'),
    (BOOK_A, 40, 'L', 'fb29-s3-f2',  '2 поверх',           'III секція'),
    (BOOK_A, 40, 'R', 'fb29-s3-ft',  'Типовий поверх',     'III секція'),
    (BOOK_A, 41, 'L', 'fb29-s3-p1',  'Пентхаус, рівень 1', 'III секція'),
    (BOOK_A, 41, 'R', 'fb29-s3-p2',  'Пентхаус, рівень 2', 'III секція'),
]

DARK = 205          # поріг «це лінія плану», а не фонова хвиля
BAND = (55, 575)    # щедра смуга пошуку по вертикалі, пункти
DILATE = 7          # розширення маски, px: зшиває тонкі лінії плану, не дістає до підпису
FOOT = 0.86         # нижня смуга кадру, де стоять російські підписи й міні-схема секції
MARGIN = 10         # поля навколо плану, пункти


def _runs(mask_row):
    """Горизонтальні відрізки чорнила в рядку: [(початок, кінець), ...]."""
    out, start = [], None
    for x, v in enumerate(mask_row):
        if v and start is None:
            start = x
        elif not v and start is not None:
            out.append((start, x - 1))
            start = None
    if start is not None:
        out.append((start, len(mask_row) - 1))
    return out


def _components(mask):
    """Зв'язні області через RLE та union-find.

    Повертає список (площа, x0, y0, x1, y1), відсортований за площею.
    Креслення — одна суцільна область; російський підпис і міні-схема
    секції — окремі, бо відділені білим полем.
    """
    h, w = mask.shape
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    prev, prev_lab, labels, nxt = [], [], [], 0
    for y in range(h):
        cur = _runs(mask[y])
        cur_lab = []
        for (s0, e0) in cur:
            hit = [lab for (s1, e1), lab in zip(prev, prev_lab)
                   if not (e1 < s0 - 1 or s1 > e0 + 1)]
            if hit:
                lab = hit[0]
                for other in hit[1:]:
                    union(lab, other)
            else:
                lab = nxt
                parent[lab] = lab
                nxt += 1
            cur_lab.append(lab)
            labels.append((lab, s0, e0, y))
        prev, prev_lab = cur, cur_lab

    agg = {}
    for lab, s0, e0, y in labels:
        r = find(lab)
        a = agg.get(r)
        n = e0 - s0 + 1
        if a is None:
            agg[r] = [n, s0, y, e0, y]
        else:
            a[0] += n
            a[1] = min(a[1], s0); a[2] = min(a[2], y)
            a[3] = max(a[3], e0); a[4] = max(a[4], y)
    return sorted(([v[0], v[1], v[2], v[3], v[4]] for v in agg.values()),
                  key=lambda c: -c[0])


def ink_bbox(page, half, dpi=110):
    """Рамка креслення: найбільша зв'язна область темних пікселів у половині.

    Розширення на DILATE зшиває тонкі виносні лінії плану в одне ціле,
    але не дотягується до підпису під ним — тому підпис лишається зовні.
    """
    import numpy as np
    from PIL import ImageFilter

    pm = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
    im = Image.open(io.BytesIO(pm.tobytes('png'))).convert('L')
    sc = dpi / 72.0
    W = page.rect.width
    x_lo = 0 if half == 'L' else W / 2
    x_hi = W / 2 if half == 'L' else W
    box = (int(x_lo * sc), int(BAND[0] * sc), int(x_hi * sc), int(BAND[1] * sc))
    dark = im.crop(box).point(lambda v: 255 if v < DARK else 0)
    grown = dark.filter(ImageFilter.MaxFilter(DILATE))
    mask = (np.asarray(grown) > 0)

    comps = _components(mask)
    if not comps:
        return None
    area, cx0, cy0, cx1, cy1 = comps[0]
    pad = (DILATE - 1) // 2          # прибрати розширення назад
    cx0 += pad; cy0 += pad; cx1 -= pad; cy1 -= pad
    return fitz.Rect(
        x_lo + cx0 / sc - MARGIN, BAND[0] + cy0 / sc - MARGIN,
        x_lo + cx1 / sc + MARGIN, BAND[0] + cy1 / sc + MARGIN,
    )


def erase_captions(im):
    """Стирає з кадру все, що не є самим кресленням.

    Російські підписи («Пентхаус, уровень 1») і міні-схема секції лежать
    у порожньому куті всередині рамки плану, тож кроп їх не прибирає.
    Вони — окремі зв'язні області в нижній смузі кадру: їх і зафарбовуємо
    кольором паперу.
    """
    import numpy as np
    from PIL import ImageFilter

    g = im.convert('L')
    dark = g.point(lambda v: 255 if v < DARK else 0)
    grown = dark.filter(ImageFilter.MaxFilter(DILATE))
    mask = np.asarray(grown) > 0
    comps = _components(mask)
    if len(comps) < 2:
        return im
    H, W = mask.shape
    paper = im.getpixel((1, 1))
    arr = np.array(im)
    lum = np.asarray(g)
    wiped = 0
    for area, x0, y0, x1, y1 in comps[1:]:
        if y1 < FOOT * H:
            continue                       # це частина креслення, не підпис
        # стираємо все, що не папір: разом зі згладженими краями літер
        sub = lum[y0:y1 + 1, x0:x1 + 1] < 250
        region = arr[y0:y1 + 1, x0:x1 + 1]
        region[sub] = paper
        arr[y0:y1 + 1, x0:x1 + 1] = region
        wiped += 1
    return Image.fromarray(arr) if wiped else im


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    docs = {}
    for src, idx, half, pid, label, sub in PLATES:
        if src not in docs:
            docs[src] = fitz.open(src)
        d = fitz.open(src)               # свіжа копія: set_cropbox незворотній
        p = d[idx]
        r = ink_bbox(p, half)
        if r is None:
            print(f'  {pid}: креслення не знайдено', file=sys.stderr)
            continue
        r = r & p.rect                   # не виходити за межі сторінки
        p.set_cropbox(r)
        big = max(WIDTHS)
        z = big / r.width
        pm = p.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
        master = erase_captions(
            Image.open(io.BytesIO(pm.tobytes('png'))).convert('RGB'))
        made, size = [], 0
        for w in WIDTHS:
            im = master if w == big else master.resize(
                (w, round(w * master.height / master.width)), Image.LANCZOS)
            path = os.path.join(OUT, f'{pid}-{w}.webp')
            im.save(path, 'WEBP', lossless=True, method=6)
            made.append(w)
            size += os.path.getsize(path)
        manifest.append({
            'id': pid, 'label': label, 'section': sub,
            'widths': made, 'ratio': round(r.width / r.height, 4),
            'bytes': size,
        })
        print(f'{pid:14} {label:20} {sub or "":11} '
              f'{r.width:5.0f}×{r.height:<5.0f}pt  {size//1024:4} KB')
    with open(os.path.join(OUT, 'plans.json'), 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    tot = sum(m['bytes'] for m in manifest)
    print(f'\n{len(manifest)} планів, {tot/1024:.0f} KB разом')


if __name__ == '__main__':
    main()
