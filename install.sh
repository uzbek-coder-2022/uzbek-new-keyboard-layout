#!/usr/bin/env bash
#
# Uzbek (yangi lotin, Q) klaviatura layoutini o'rnatish skripti.
# GNOME (Wayland yoki Xorg) va sof Xorg/boshqa DE muhitlarini avtomatik
# aniqlab, mos usulni tanlaydi.
#
# Foydalanish: chmod +x install.sh && ./install.sh

set -e

SYMBOLS_SRC="$(dirname "$0")/uzq"
SYMBOLS_DEST="/usr/share/X11/xkb/symbols/uzq"
AUTOSTART_DIR="$HOME/.config/autostart"
AUTOSTART_FILE="$AUTOSTART_DIR/uz-keyboard.desktop"

if [ ! -f "$SYMBOLS_SRC" ]; then
    echo "Xato: 'uzq' fayli topilmadi. Skriptni loyiha papkasi ichida ishga tushiring."
    exit 1
fi

echo "==> XKB symbols faylini nusxalash uchun sudo huquqi kerak bo'ladi."
sudo cp "$SYMBOLS_SRC" "$SYMBOLS_DEST"
echo "    -> $SYMBOLS_DEST ga nusxalandi."

if command -v gsettings >/dev/null 2>&1 && gsettings list-schemas | grep -q "org.gnome.desktop.input-sources"; then
    echo "==> GNOME aniqlandi (Wayland yoki Xorg). Input source ro'yxatiga qo'shilmoqda..."

    CURRENT="$(gsettings get org.gnome.desktop.input-sources sources)"

    if echo "$CURRENT" | grep -q "uzq+basic"; then
        echo "    -> Layout allaqachon qo'shilgan, o'tkazib yuborilmoqda."
    else
        NEW="$(python3 - "$CURRENT" << 'PYEOF'
import ast, sys
current = ast.literal_eval(sys.argv[1])
current.append(('xkb', 'uzq+basic'))
print(current)
PYEOF
)"
        gsettings set org.gnome.desktop.input-sources sources "$NEW"
        echo "    -> Qo'shildi."
    fi

    echo ""
    echo "Tayyor! Layoutlar orasida almashish uchun Super+Space (yoki tepadagi"
    echo "panelda til belgisini bosing) tugmalaridan foydalaning."
    echo "Agar darhol ko'rinmasa, seansdan chiqib qayta kiring."
else
    echo "==> GNOME/gsettings aniqlanmadi. Xorg 'setxkbmap' usuli ishlatilmoqda..."
    setxkbmap -symbols "pc+us+uzq(basic)"
    echo "    -> Faollashtirildi. Sinab ko'ring: [ ] ; ' tugmalari."

    echo "==> Har login'da avtomatik ishga tushishi uchun autostart yozuvi qo'shilmoqda..."
    mkdir -p "$AUTOSTART_DIR"
    cat > "$AUTOSTART_FILE" << 'EOF'
[Desktop Entry]
Type=Application
Exec=setxkbmap -symbols "pc+us+uzq(basic)"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Uzbek Q Keyboard Layout
Comment=Yangi o'zbek lotin alifbosi (Ö Ğ Ş Ç) uchun klaviatura layoutini yoqadi
EOF
    echo "    -> $AUTOSTART_FILE yaratildi."
    echo ""
    echo "Tayyor! Kompyuterni qayta ishga tushirganingizdan keyin ham layout avtomatik yoqiladi."
fi

echo "Olib tashlash uchun: ./uninstall.sh"
