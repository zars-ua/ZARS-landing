#!/usr/bin/env python3
"""Збирає HTML-блоки вибору поверху з assets/plans/plans.json.

Пишемо їх у tools/partials/, звідки inline_partials.py вставляє у сторінки.
Запуск:  python3 tools/build_plate_html.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANS = json.load(open(os.path.join(ROOT, 'assets/plans/plans.json'), encoding='utf-8'))
BY_ID = {p['id']: p for p in PLANS}

LEVELS_FB29 = [('f1', '1 поверх'), ('f2', '2 поверх'), ('ft', 'Типовий поверх'),
               ('p1', 'Пентхаус, рівень 1'), ('p2', 'Пентхаус, рівень 2')]
SECTIONS = [('fb29-s1', 'I секція'), ('fb29-s2', 'II секція'), ('fb29-s3', 'III секція')]
LEVELS_FB29B = [('fb29b-f1', '1 поверх'), ('fb29b-f2', '2 поверх'), ('fb29b-f3', '3 поверх'),
                ('fb29b-f47', '4–7 поверхи'), ('fb29b-f8', '8 поверх'), ('fb29b-f9', '9 поверх'),
                ('fb29b-f10', '10 поверх'), ('fb29b-ph', 'Пентхаус')]


def buttons(items, attr):
    return '\n'.join(
        f'          <button type="button" {attr}="{key}" aria-pressed="false">{label}</button>'
        for key, label in items)


def data_blob(ids, house):
    out = {}
    for pid in ids:
        p = BY_ID[pid]
        name = f"{p['label']}{', ' + p['section'] if p['section'] else ''}"
        out[pid] = {
            'ratio': p['ratio'],
            'cap': f"{name} — {house}",
            'alt': f"Поверховий план: {name}, {house}",
        }
    return json.dumps(out, ensure_ascii=False, indent=1)


def plate(house, group_items, level_items, ids, note):
    groups = ''
    if group_items:
        groups = (
            '      <div class="plate__ctrl" role="group" aria-label="Секція">\n'
            f'{buttons(group_items, "data-group")}\n'
            '      </div>\n')
    return f'''<div class="plate" data-plate>
      <script type="application/json" data-plate-data>
{data_blob(ids, house)}
      </script>
{groups}      <div class="plate__ctrl" role="group" aria-label="Рівень">
{buttons(level_items, "data-level")}
      </div>
      <figure class="plate__view">
        <img data-plate-img src="" alt="" width="1200" height="800"
             sizes="(max-width: 900px) 92vw, 62vw" loading="lazy" decoding="async">
        <figcaption data-plate-cap></figcaption>
      </figure>
      <p class="plate__note">{note}</p>
    </div>'''


def main():
    os.makedirs(os.path.join(ROOT, 'tools/partials'), exist_ok=True)

    ids29 = [f'{s}-{l}' for s, _ in SECTIONS for l, _ in LEVELS_FB29 if f'{s}-{l}' in BY_ID]
    html29 = plate(
        'Французький бульвар, 29', SECTIONS, LEVELS_FB29, ids29,
        'Усі стіни — червона ефективна керамічна цегла: зовнішні 640 мм, '
        'міжквартирні 510 і 380 мм, перегородки 120 мм. Холи й коридори оздоблені мармуром. '
        'Планування конкретного поверху уточнюйте у відділі продажу.')
    open(os.path.join(ROOT, 'tools/partials/plate-fb29.html'), 'w', encoding='utf-8').write(html29)

    ids29b = [i for i, _ in LEVELS_FB29B if i in BY_ID]
    html29b = plate(
        'Французький бульвар, 29Б', None, LEVELS_FB29B, ids29b,
        'Усі стіни — червона ефективна керамічна цегла: зовнішні 510 мм, '
        'міжквартирні 380 мм, перегородки 120 мм. Можливе індивідуальне планування. '
        'Планування конкретного поверху уточнюйте у відділі продажу.')
    open(os.path.join(ROOT, 'tools/partials/plate-fb29b.html'), 'w', encoding='utf-8').write(html29b)

    print(f'plate-fb29.html  — {len(ids29)} планів, {len(SECTIONS)} секції')
    print(f'plate-fb29b.html — {len(ids29b)} планів')


if __name__ == '__main__':
    main()
