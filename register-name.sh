#!/usr/bin/env bash
#
# GNOME Settings ro'yxatida "uzq+basic" o'rniga o'qilishi qulay nom
# ko'rinishi uchun XKB reestrini yangilaydi. Amaliy ishni xkb_register.py
# bajaradi (shu papkada, shu skript bilan birga bo'lishi kerak).
#
# Foydalanish:
#   chmod +x register-name.sh
#   ./register-name.sh
#   ./register-name.sh "Boshqa nom"

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_HELPER="$SCRIPT_DIR/xkb_register.py"

if [ -z "$1" ]; then
    DESC="New Uzbek (Latin)"
else
    DESC="$1"
fi

echo "==> Korsatiladigan nom: $DESC"

if [ ! -f "$PY_HELPER" ]; then
    echo "Xato: xkb_register.py topilmadi. Uni register-name.sh bilan bir papkada saqlang."
    exit 1
fi

FILES="/usr/share/X11/xkb/rules/evdev.xml /usr/share/X11/xkb/rules/base.xml"

for f in $FILES; do
    if [ ! -e "$f" ]; then
        continue
    fi

    echo "==> $f faylini yangilash uchun sudo huquqi kerak boladi."
    sudo cp "$f" "$f.bak"
    sudo python3 "$PY_HELPER" "$f" "$DESC"
done

echo ""
echo "Tayyor. Ozgarish korinishi uchun seansdan chiqib qayta kiring."
echo "Agar muammo bolsa, zaxiradan tiklash mumkin:"
echo "  sudo cp /usr/share/X11/xkb/rules/evdev.xml.bak /usr/share/X11/xkb/rules/evdev.xml"
echo "  sudo cp /usr/share/X11/xkb/rules/base.xml.bak /usr/share/X11/xkb/rules/base.xml"
