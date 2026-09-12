#!/bin/bash
# Готує герой-відео для сторінки ФБ29Б з інтро-ролика.
# Перший кадр-план (0–2.29 с, захід сонця) розвертається «туди-назад»,
# щоб отримати безшовну петлю без стрибка на монтажному склейці.
set -e
SRC="/Users/manager/Desktop/ФБ29б/Интро (2).mp4"
OUT="$(dirname "$0")/../assets/video"
mkdir -p "$OUT"

# петля туди-назад із першого плану, без звуку
FILTER="[0:v]trim=0:2.28,setpts=PTS-STARTPTS,scale=1600:-2[a];\
[0:v]trim=0:2.28,setpts=PTS-STARTPTS,reverse,scale=1600:-2[b];\
[a][b]concat=n=2:v=1:a=0[v]"

ffmpeg -v error -y -i "$SRC" -filter_complex "$FILTER" -map "[v]" -an \
  -c:v libx264 -profile:v high -crf 26 -preset slow -pix_fmt yuv420p \
  -movflags +faststart "$OUT/fb29b-hero.mp4"

ffmpeg -v error -y -i "$SRC" -filter_complex "$FILTER" -map "[v]" -an \
  -c:v libvpx-vp9 -crf 36 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 \
  "$OUT/fb29b-hero.webm"

# постер — перший кадр
ffmpeg -v error -y -i "$SRC" -vf "select=eq(n\,0),scale=1600:-2" -frames:v 1 \
  -q:v 2 "$OUT/fb29b-hero-poster.jpg"
python3 - "$OUT/fb29b-hero-poster.jpg" <<'PY'
import sys
from PIL import Image
p=sys.argv[1]
Image.open(p).convert('RGB').save(p.replace('.jpg','.webp'),'WEBP',quality=82,method=6)
import os; os.remove(p)
PY

ls -la "$OUT"
