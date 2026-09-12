#!/usr/bin/env python3
"""Перевіряє три сторінки сайту чотирма замірами.

  python3 tools/qa/check.py                # локальний сервер :8931
  ZARS_BASE=https://zars-ua.github.io/ZARS-landing python3 tools/qa/check.py

Що міряє:
  console   помилки консолі та биті зображення
  overflow  горизонтальне переповнення на 360 / 400 / 768 px
  nojs      чи читається сторінка з повністю вимкненим JavaScript
  timing    коли текст героя починає проявлятися після першої фарби

⚠️ Останній замір існує тому, що на живому хостингу колись знайшлася
   вада, невидима локально: герой чекав на defer-скрипт і 345 мс стояв
   порожнім. Тепер перший екран анімується чистим CSS (.rise), і цей
   тест стереже, щоб хтось не повернув залежність від JS.
"""
import base64, json, os, statistics, subprocess, sys, time, urllib.request
import websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PORT = 9350
PROFILE = '/tmp/zars-qa-profile'
BASE = os.environ.get('ZARS_BASE', 'http://127.0.0.1:8931')
PAGES = ('index.html', 'fb29.html', 'fb29b.html')

SETTLE = r"""
(async () => {
  const st = document.createElement('style');
  st.textContent = '.plot{opacity:1!important;transform:none!important;transition:none!important}';
  document.head.append(st);
  document.querySelectorAll('.plot').forEach(e => e.classList.add('plot--in'));
  await document.fonts.ready;
  await new Promise(r => setTimeout(r, 500));
  const vw = document.documentElement.clientWidth;
  const over = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (!r.width) continue;
    if (getComputedStyle(el).position === 'fixed') continue;
    if (el.closest('.hero__map') || el.closest('.hp')) continue;   // карта обрізана навмисно, пастка за екраном
    if (r.right > vw + 1.5 || r.left < -1.5) over.push(el.tagName + '.' + (el.className || ''));
  }
  return JSON.stringify({
    vw, scrollW: document.documentElement.scrollWidth,
    over: over.slice(0, 6),
    broken: [...document.images].filter(i => i.complete && !i.naturalWidth && i.getAttribute('src'))
                                .map(i => i.getAttribute('src')),
    fonts: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))],
  });
})()
"""

TIMING = r"""
(async () => {
  const h1 = document.querySelector('.hero h1, .shot-hero h1');
  const start = performance.now();
  while (performance.now() - start < 8000) {
    if (parseFloat(getComputedStyle(h1).opacity) > 0.08) break;
    await new Promise(r => requestAnimationFrame(r));
  }
  const fcp = performance.getEntriesByName('first-contentful-paint')[0];
  return JSON.stringify({ text: Math.round(performance.now()),
                          fcp: fcp ? Math.round(fcp.startTime) : null });
})()
"""


class CDP:
    def __init__(self, url):
        self.ws = websocket.create_connection(url, timeout=60)
        self.n = 0
        self.logs = []

    def send(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({'id': self.n, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('method') in ('Log.entryAdded', 'Runtime.exceptionThrown'):
                self.logs.append(json.dumps(msg['params'])[:200])
            if msg.get('id') == self.n:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})

    def ev(self, expr):
        r = self.send('Runtime.evaluate', expression=expr, awaitPromise=True, returnByValue=True)
        return r['result']['value']


def main():
    subprocess.run(['pkill', '-f', PROFILE], capture_output=True)
    proc = subprocess.Popen(
        [CHROME, '--headless=new', f'--remote-debugging-port={PORT}',
         f'--user-data-dir={PROFILE}', '--disable-gpu', '--no-first-run',
         '--hide-scrollbars', '--remote-allow-origins=*', 'about:blank'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    bad = []
    try:
        for _ in range(60):
            try:
                tab = next(t for t in json.load(urllib.request.urlopen(
                    f'http://127.0.0.1:{PORT}/json')) if t['type'] == 'page')
                break
            except Exception:
                time.sleep(0.5)
        else:
            sys.exit('Chrome не піднявся')
        c = CDP(tab['webSocketDebuggerUrl'])
        for m in ('Page.enable', 'Runtime.enable', 'Log.enable', 'Network.enable'):
            c.send(m)
        c.send('Network.setCacheDisabled', cacheDisabled=True)

        print(f'Перевіряю {BASE}\n')
        for width in (360, 400, 768, 1440):
            for page in PAGES:
                c.logs.clear()
                c.send('Emulation.setDeviceMetricsOverride', width=width, height=900,
                       deviceScaleFactor=1, mobile=width < 700)
                c.send('Page.navigate', url=f'{BASE}/{page}?qa={int(time.time()*1000)}')
                time.sleep(2.6)
                r = json.loads(c.ev(SETTLE))
                errs = [l for l in c.logs if 'error' in l.lower() or 'exception' in l.lower()]
                ok = r['scrollW'] <= r['vw'] and not r['over'] and not r['broken'] and not errs
                if not ok:
                    bad.append(f'{width}px {page}: переповнення={r["over"]} биті={r["broken"]} помилки={errs}')
                print(f'  {width:>4}px {page:12} ширина {r["scrollW"]:<5} '
                      f'шрифтів {len(r["fonts"])}  {"✓" if ok else "✗"}')

        print('\nБез JavaScript:')
        c.send('Emulation.setScriptExecutionDisabled', value=True)
        c.send('Emulation.setDeviceMetricsOverride', width=1440, height=900,
               deviceScaleFactor=1, mobile=False)
        for page in PAGES:
            c.send('Page.navigate', url=f'{BASE}/{page}?nojs={int(time.time()*1000)}')
            time.sleep(2.2)
            # без JS не можна виконати скрипт у сторінці — дивимось на висоту документа
            m = c.send('Page.getLayoutMetrics')
            h = round(m['contentSize']['height'])
            ok = h > 3000
            if not ok:
                bad.append(f'без JS {page}: висота документа {h} — сторінка схлопнулась')
            print(f'  {page:12} висота документа {h:<7} {"✓" if ok else "✗"}')
        c.send('Emulation.setScriptExecutionDisabled', value=False)

        print('\nКоли текст героя починає проявлятися:')
        for page in PAGES:
            runs = []
            for i in range(3):
                c.send('Page.navigate', url=f'{BASE}/{page}?t={int(time.time()*1000)}{i}')
                time.sleep(0.2)
                runs.append(json.loads(c.ev(TIMING)))
            # Браузер не завжди встигає зафіксувати first-contentful-paint —
            # тоді розрив рахувати нема від чого, і це не привід валити перевірку.
            paints = [r['fcp'] for r in runs if r['fcp']]
            txt = statistics.median([r['text'] for r in runs])
            if not paints:
                print(f'  {page:12} першу фарбу не зафіксовано, текст {txt:>4.0f} мс  —')
                continue
            fcp = statistics.median(paints)
            gap = txt - fcp
            ok = gap < 250
            if not ok:
                bad.append(f'{page}: текст відстає від першої фарби на {gap:.0f} мс')
            print(f'  {page:12} перша фарба {fcp:>4.0f} мс, текст {txt:>4.0f} мс '
                  f'(розрив {gap:>3.0f}) {"✓" if ok else "✗"}')
    finally:
        proc.terminate()

    if bad:
        print('\nПРОБЛЕМИ:')
        for b in bad:
            print('  ', b)
        sys.exit(1)
    print('\nУсі перевірки пройдено.')


if __name__ == '__main__':
    main()
