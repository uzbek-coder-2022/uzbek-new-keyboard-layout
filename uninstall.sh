#!/usr/bin/env bash
#
# Uzbek (yangi lotin, Q) klaviatura layoutini olib tashlash skripti.
# Foydalanish: chmod +x uninstall.sh && ./uninstall.sh

set -e

SYMBOLS_DEST="/usr/share/X11/xkb/symbols/uzq"
AUTOSTART_FILE="$HOME/.config/autostart/uz-keyboard.desktop"

if command -v gsettings >/dev/null 2>&1 && gsettings list-schemas | grep -q "org.gnome.desktop.input-sources"; then
    echo "==> GNOME input source ro'yxatidan olib tashlanmoqda..."
    CURRENT="$(gsettings get org.gnome.desktop.input-sources sources)"
    NEW="$(python3 - "$CURRENT" << 'PYEOF'
import ast, sys
current = ast.literal_eval(sys.argv[1])
current = [s for s in current if s != ('xkb', 'uzq+basic')]
print(current)
PYEOF
)"
    gsettings set org.gnome.desktop.input-sources sources "$NEW"
    echo "    -> Olib tashlandi."
else
    echo "==> Standart klaviatura layoutiga qaytarilmoqda..."
    setxkbmap us || true
fi

if [ -f "$AUTOSTART_FILE" ]; then
    rm -f "$AUTOSTART_FILE"
    echo "==> Autostart yozuvi o'chirildi."
fi

if [ -f "$SYMBOLS_DEST" ]; then
    echo "==> Symbols faylini o'chirish uchun sudo huquqi kerak bo'ladi."
    sudo rm -f "$SYMBOLS_DEST"
    echo "==> $SYMBOLS_DEST o'chirildi."
fi

echo ""
echo "Layout to'liq olib tashlandi."
