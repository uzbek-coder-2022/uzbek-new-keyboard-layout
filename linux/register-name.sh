#!/usr/bin/env bash
#
# GNOME Settings ro'yxatida "uzq+basic" / "uzq+cw" o'rniga o'qilishi qulay nom
# ko'rinishi uchun XKB reestrini (evdev.xml, base.xml) yangilaydi.
#
#   ./register-name.sh                  -> "New Uzbek (Latin)" va "... - C/W"
#   ./register-name.sh "Boshqa nom"     -> asosiy nomni o'zgartirish

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/lib/common.sh"
PY_HELPER="$DIR/lib/xkb_register.py"
DESC="${1:-New Uzbek (Latin)}"

[ -f "$PY_HELPER" ] || { echo "Xato: lib/xkb_register.py topilmadi."; exit 1; }
echo "==> Ko'rsatiladigan nom: $DESC"

for f in /usr/share/X11/xkb/rules/evdev.xml /usr/share/X11/xkb/rules/base.xml; do
    [ -e "$f" ] || continue
    echo "==> $f yangilanmoqda..."
    as_root cp "$f" "$f.bak"
    as_root python3 "$PY_HELPER" "$f" "$DESC"
done
echo "Tayyor. O'zgarish ko'rinishi uchun seansdan chiqib qayta kiring."
echo "Tiklash: sudo cp <fayl>.bak <fayl>  (evdev.xml, base.xml)"
