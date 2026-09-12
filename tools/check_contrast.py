#!/usr/bin/env python3
"""Звіряє контраст кожної пари «текст на тлі» у всіх трьох виданнях карти.

Фірмові кольори гайдлайну не проходять WCAG AA на темних ґрунтах, тому
для тексту використано освітлені варіанти. Цей скрипт стежить, щоб
хтось не «повернув як було» і не зламав читабельність.

Запуск:  python3 tools/check_contrast.py    (код виходу 1, якщо є провал)
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSET_INK = {'holding': '#9C4618', 'fb29b': '#8A3512'}   # чорнило на паперовій вставці
INSET_BG = '#ECE6DB'
AA = 4.5


def luminance(hex_colour):
    h = hex_colour.lstrip('#')
    ch = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        ch.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    css = open(os.path.join(ROOT, 'css/zars.css'), encoding='utf-8').read()
    fails = []
    for m in re.finditer(r"\[data-chart='(\w+)'\]\s*\{(.*?)\n\}", css, re.S):
        ed = m.group(1)
        tok = dict(re.findall(r'--([\w-]+):\s*(#[0-9A-Fa-f]{6})', m.group(2)))
        if 'ground' not in tok:
            continue
        print(f'\n— {ed}')
        pairs = []
        for gname, g in (('ґрунт', tok['ground']), ('другий ґрунт', tok['ground-2'])):
            for tname in ('text', 'text-dim', 'ink', 'warn'):
                if tok.get(tname):
                    pairs.append((f'{tname} на {gname}', tok[tname], g))
        pairs.append(('текст кнопки на чорнилі', tok['on-ink'], tok['ink']))
        if ed in INSET_INK:
            pairs += [('вставка: текст', '#1C2433', INSET_BG),
                      ('вставка: тьмяний', '#5A6478', INSET_BG),
                      ('вставка: чорнило', INSET_INK[ed], INSET_BG)]
        for label, fg, bg in pairs:
            r = ratio(fg, bg)
            ok = r >= AA
            if not ok:
                fails.append(f'{ed}: {label} ({fg} на {bg}) = {r:.2f}')
            print(f'   {label:28} {r:5.2f} {"✓" if ok else "✗ ПРОВАЛ"}')

    if fails:
        print('\nПРОВАЛИ:')
        for f in fails:
            print('  ', f)
        sys.exit(1)
    print('\nУсі пари проходять WCAG AA (≥ 4,5:1).')


if __name__ == '__main__':
    main()
