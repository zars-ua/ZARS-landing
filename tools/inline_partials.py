#!/usr/bin/env python3
"""Один раз вставляє спільні шматки у сторінки замість маркерів.

Сайт лишається без кроку збірки: після цієї вставки .html самодостатні,
і текст у них правиться напряму. Скрипт потрібен лише тоді, коли
змінюється логотип, карта або форма — тоді маркери повертають вручну.

Маркери:  <!--LOGO-->  <!--COAST-->  <!--FORM-->
Запуск:   python3 tools/inline_partials.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARTS = {
    'LOGO':  'assets/logo/zars.svg',
    'COAST': 'assets/map/coast.svg',
    'FORM':  'tools/partials/form.html',
    'PLATE-FB29':  'tools/partials/plate-fb29.html',
    'PLATE-FB29B': 'tools/partials/plate-fb29b.html',
}
PAGES = ['index.html', 'fb29.html', 'fb29b.html']


def main():
    parts = {k: open(os.path.join(ROOT, v), encoding='utf-8').read().strip()
             for k, v in PARTS.items()}
    for page in PAGES:
        path = os.path.join(ROOT, page)
        if not os.path.exists(path):
            print(f'  пропущено (ще немає): {page}', file=sys.stderr)
            continue
        html = open(path, encoding='utf-8').read()
        used = []
        for key, body in parts.items():
            marker = f'<!--{key}-->'
            if marker in html:
                html = html.replace(marker, body)
                used.append(key)
        open(path, 'w', encoding='utf-8').write(html)
        print(f'{page}: вставлено {", ".join(used) if used else "нічого"}')


if __name__ == '__main__':
    main()
