# 25.10.2026: растрова копія схеми ФБ29Б (assets/map/fr29b-map.svg → WebP 1200/2000/3000).
# Навіщо: анімація «опускання» схеми (scale+rotation) змушувала Chrome растрювати складну SVG
# на кадрах — на телефоні кадри до 380 мс. Запуск з кореня репо при живому http.server :8931:
#   python3 tools/build_fb29b_map_raster.py
import sys,base64,io,time; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent / '.impeccable/qa-0921')); from cdp import C
from PIL import Image
out=sys.argv[1] if len(sys.argv)>1 else 'assets/map'; c=C(9571)
try:
  for w in [1200,2000,3000]:
    h=round(w*1635.87/1556.15)
    c.cmd('Emulation.setDeviceMetricsOverride',width=w,height=h,deviceScaleFactor=1,mobile=False)
    c.cmd('Emulation.setDefaultBackgroundColorOverride',color={'r':0,'g':0,'b':0,'a':0})
    c.go('http://127.0.0.1:8931/assets/map/fr29b-map.svg',2)
    c.ev("document.documentElement.setAttribute('width','%d');document.documentElement.setAttribute('height','%d');1"%(w,h)); time.sleep(0.5)
    d=c.cmd('Page.captureScreenshot',format='png',clip={'x':0,'y':0,'width':w,'height':h,'scale':1})['data']
    im=Image.open(io.BytesIO(base64.b64decode(d))).convert('RGBA')
    p=f'{out}/fr29b-map-{w}.webp'; im.save(p,'WEBP',quality=82,method=6)
    import os; print(w,h,im.size,os.path.getsize(p)//1024,'KB', 'alpha range',im.getchannel('A').getextrema())
finally: c.close()
