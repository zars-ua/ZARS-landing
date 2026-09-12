#!/usr/bin/env python3
"""Будує SVG берега Одеської затоки з реальних даних OpenStreetMap.

Геометрія на карті — це твердження про місцевість, тому вона не малюється
від руки: берегова лінія і Французький бульвар беруться з OSM
(assets/map/osm-raw.json, запит Overpass лежить у tools/overpass.txt),
координати будинків — з геокодера Nominatim.

Запуск:  python3 tools/build_map.py
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'assets/map/osm-raw.json')
OUT = os.path.join(ROOT, 'assets/map/coast.svg')

# Рамка карти: обидва будинки плюс смуга моря.
# Рамку задають довготи й формат кадру; широти рахуються від середини між
# будинками, щоб масштаб по обох осях був однаковий і відстані лишалися чесними.
# Кадр підібрано під композицію першого екрана: мітки лягають приблизно
# на 62 % ширини — праворуч від тексту, — а море лишається смугою біля
# правого краю. Ширина кадру ≈ 2000 м.
LON0, LON1 = 30.740390, 30.766470
W, H = 1600, 1000
CENTRE_LAT = 46.46125

M_PER_DEG = 111320.0
_K = math.cos(math.radians(CENTRE_LAT))
_SCALE = W / ((LON1 - LON0) * _K * M_PER_DEG)
_HALF_LAT = (H / _SCALE) / M_PER_DEG / 2
LAT0, LAT1 = CENTRE_LAT - _HALF_LAT, CENTRE_LAT + _HALF_LAT

MARKS = [
    ('fb29',  46.4614137, 30.7562069, 'Французький бульвар, 29'),
    ('fb29b', 46.4610972, 30.7569145, 'Французький бульвар, 29Б'),
]


def project(lat, lon):
    """Метрична проєкція: однаковий масштаб по обох осях, тож відстані чесні."""
    x = (lon - LON0) * _K * M_PER_DEG * _SCALE
    y = H - (lat - LAT0) * M_PER_DEG * _SCALE
    return x, y


def clip(pts):
    """Лишає лише відрізки всередині рамки, розриваючи лінію на виході за межі."""
    runs, cur = [], []
    for la, lo in pts:
        if LAT0 - 0.004 <= la <= LAT1 + 0.004 and LON0 - 0.004 <= lo <= LON1 + 0.004:
            cur.append(project(la, lo))
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) > 1]


def to_path(run):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in run)


def path_len(run):
    return sum(math.dist(run[i], run[i + 1]) for i in range(len(run) - 1))


def metres_per_unit():
    """Скільки метрів в одній одиниці SVG — щоб малювати кола дальності."""
    return 1.0 / _SCALE


def main():
    data = json.load(open(RAW))
    coast, boulevard = [], []
    for el in data['elements']:
        geom = [(p['lat'], p['lon']) for p in el.get('geometry', [])]
        if not geom:
            continue
        tags = el.get('tags', {})
        target = coast if tags.get('natural') == 'coastline' else boulevard
        target.extend(clip(geom))

    mpu = metres_per_unit()
    parts = [
        f'<svg class="coast" viewBox="0 0 {W} {H}" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
        f'preserveAspectRatio="xMidYMid slice">',
        '<g class="coast__sea">',
    ]

    # Поле моря: берегова лінія, замкнена по правому краю рамки.
    sea = max(coast, key=path_len) if coast else []
    if sea:
        d = to_path(sea) + f' L{W} {sea[-1][1]:.1f} L{W} {sea[0][1]:.1f} Z'
        parts.append(f'<path d="{d}"/>')
    parts.append('</g>')

    # Смуга мілководдя вздовж берега — так на картах відділяють воду від суші.
    if sea:
        parts.append('<g class="coast__shoal">')
        parts.append(f'<path d="{to_path(sea)}"/>')
        parts.append('</g>')

    # Кола дальності від будинків. Міра на карті має бути названа,
    # інакше це просто кола: кожне коло підписане по верхньому краю.
    cx, cy = project(46.46125, 30.75656)
    parts.append('<g class="coast__rings">')
    for m in (250, 500):
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{m / mpu:.1f}" '
                     f'data-m="{m}"/>')
    parts.append('</g>')
    parts.append('<g class="coast__ringlabels">')
    for m, label in ((250, '250 м'), (500, '500 м')):
        r = m / mpu
        parts.append(f'<text x="{cx:.1f}" y="{cy - r + 8:.1f}" '
                     f'text-anchor="middle">{label}</text>')
    parts.append('</g>')

    parts.append('<g class="coast__street">')
    for run in boulevard:
        parts.append(f'<path d="{to_path(run)}" style="--len:{path_len(run):.0f}"/>')
    parts.append('</g>')

    parts.append('<g class="coast__line">')
    for run in coast:
        parts.append(f'<path d="{to_path(run)}" style="--len:{path_len(run):.0f}"/>')
    parts.append('</g>')

    parts.append('<g class="coast__marks">')
    for mid, la, lo, title in MARKS:
        x, y = project(la, lo)
        parts.append(
            f'<g class="mark" data-mark="{mid}" transform="translate({x:.1f} {y:.1f})">'
            f'<circle class="mark__halo" r="34"/>'
            f'<circle class="mark__dot" r="7"/>'
            f'<title>{title}</title></g>')
    parts.append('</g></svg>')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write('\n'.join(parts))
    print(f'{OUT}: берегова лінія {len(coast)} відрізків, '
          f'бульвар {len(boulevard)}, масштаб {mpu:.2f} м / од.')
    print('позиції міток:', {m[0]: tuple(round(v) for v in project(m[1], m[2])) for m in MARKS})


if __name__ == '__main__':
    main()
