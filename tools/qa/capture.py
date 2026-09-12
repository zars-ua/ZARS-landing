#!/usr/bin/env python3
"""Знімає вісім оглядових кадрів сайту через Chrome DevTools Protocol.

Три сторінки на 1440 і 400 px плюс два кадри вибору поверху в активному
стані. Анімації появи гасяться, шрифти й зображення дочікуються, тож у
кадр не потрапляє елемент посеред переходу.

  python3 tools/qa/capture.py                     # локальний сервер :8931
  ZARS_BASE=https://zars-ua.github.io/ZARS-landing python3 tools/qa/capture.py

⚠️ Висоту в\'юпорта не міняти: герой на 100svh розтягнеться на всю
   сторінку й кадр вийде вдвічі вищим. Тільки captureBeyondViewport.
"""
import base64, json, os, subprocess, sys, time, urllib.request
import websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PORT = 9333
OUT = os.environ.get('ZARS_OUT',
       os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    '.impeccable/review'))
BASE = os.environ.get('ZARS_BASE', 'http://127.0.0.1:8931')
PROFILE = '/tmp/zars-cdp-profile'

SETTLE = r"""
(async () => {
  const st = document.createElement('style');
  st.textContent = `.plot{opacity:1!important;transform:none!important;transition:none!important}
    .wall__bar,.bar__fill{transform:scaleX(1)!important;transition:none!important}
    .coast__line path,.coast__street path{stroke-dashoffset:0!important;transition:none!important}
    .mark--live .mark__halo{animation:none!important}
    html{scroll-behavior:auto!important}
    *,*::before,*::after{animation-play-state:paused!important}
    .rise{animation:none!important;opacity:1!important;transform:none!important}`;
  document.head.append(st);
  document.querySelectorAll('.plot').forEach(e => e.classList.add('plot--in'));
  document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
  await document.fonts.ready;
  const imgs = [...document.images].filter(i => !i.complete);
  await Promise.all(imgs.map(i => new Promise(r => { i.onload = i.onerror = r; })));
  await new Promise(r => setTimeout(r, 400));
  return JSON.stringify({
    h: document.documentElement.scrollHeight,
    w: document.documentElement.scrollWidth,
    broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0)
                                .map(i => i.getAttribute('src')).slice(0, 5),
  });
})()
"""

JOBS = [
    ('desktop',            'index.html',  1440, None),
    ('mobile',             'index.html',   400, None),
    ('fb29-desktop',       'fb29.html',   1440, None),
    ('fb29-mobile',        'fb29.html',    400, None),
    ('fb29b-desktop',      'fb29b.html',  1440, None),
    ('fb29b-mobile',       'fb29b.html',   400, None),
    ('fb29-floorplate-active',  'fb29.html',  1440,
     "document.querySelectorAll('[data-group]')[1].click();"
     "document.querySelectorAll('[data-level]')[3].click();"),
    ('fb29b-floorplate-active', 'fb29b.html', 1440,
     "document.querySelectorAll('[data-level]')[7].click();"),
]


class CDP:
    def __init__(self, url):
        self.ws = websocket.create_connection(url, timeout=60)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({'id': self.i, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.i:
                if 'error' in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get('result', {})

    def eval(self, expr, await_promise=True):
        r = self.send('Runtime.evaluate', expression=expr,
                      awaitPromise=await_promise, returnByValue=True)
        return r.get('result', {}).get('value')


def main():
    os.makedirs(OUT, exist_ok=True)
    proc = subprocess.Popen(
        [CHROME, '--headless=new', f'--remote-debugging-port={PORT}',
         f'--user-data-dir={PROFILE}', '--hide-scrollbars',
         '--disable-gpu', '--no-first-run', '--force-device-scale-factor=1',
         '--remote-allow-origins=*',
         'about:blank'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
                target = next(t for t in tabs if t['type'] == 'page')
                break
            except Exception:
                time.sleep(0.5)
        else:
            sys.exit('Chrome не піднявся')

        c = CDP(target['webSocketDebuggerUrl'])
        c.send('Page.enable')
        c.send('Runtime.enable')

        for name, page, width, extra in JOBS:
            c.send('Emulation.setDeviceMetricsOverride', width=width, height=900,
                   deviceScaleFactor=1, mobile=width < 700)
            c.send('Page.navigate', url=f'{BASE}/{page}?cap={int(time.time()*1000)}')
            time.sleep(3.0)
            info = json.loads(c.eval(SETTLE))
            if extra:
                c.eval(extra, await_promise=False)
                time.sleep(1.2)
                info = json.loads(c.eval(SETTLE))
                # знімок самого блока планувань, а не всієї сторінки
                c.eval("document.querySelector('.plate')"
                       ".scrollIntoView({block:'start',behavior:'instant'});"
                       "window.scrollBy(0,-70)", await_promise=False)
                time.sleep(0.6)
                shot = c.send('Page.captureScreenshot', format='png')
            else:
                # висоту в'юпорта НЕ чіпаємо: інакше герой на 100svh
                # розтягнеться на всю сторінку й кадр буде вдвічі вищим
                c.eval("window.scrollTo(0,0)", await_promise=False)
                time.sleep(0.3)
                shot = c.send('Page.captureScreenshot', format='png',
                              captureBeyondViewport=True)
            path = os.path.join(OUT, f'{name}.png')
            open(path, 'wb').write(base64.b64decode(shot['data']))
            kb = os.path.getsize(path) // 1024
            print(f'{name:26} {width}px  висота {info["h"]:>6}  {kb:>6} KB'
                  f'{"  БИТІ: " + str(info["broken"]) if info["broken"] else ""}')
    finally:
        proc.terminate()


if __name__ == '__main__':
    main()
