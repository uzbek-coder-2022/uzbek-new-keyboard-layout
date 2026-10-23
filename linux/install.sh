#!/usr/bin/env bash
#
# Uzbek (yangi lotin) klaviatura layoutlarini o'rnatish.
#
#   ./install.sh            -> menyu (terminalda) yoki "basic" (terminalsiz)
#   ./install.sh basic      -> Q joylashuvi:  [ ] ; '  -> ö ğ ş ç
#   ./install.sh cw         -> C/W joylashuvi: c w ; ,  -> ç ş ö ğ
#   ./install.sh all        -> ikkalasi (GNOME'da)
#
# GNOME (Wayland yoki Xorg) va sof Xorg/boshqa DE muhitlarini avtomatik aniqlaydi.

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/lib/common.sh"
SYMBOLS_SRC="$DIR/xkb/symbols/uzq"

[ -f "$SYMBOLS_SRC" ] || { echo "Xato: $SYMBOLS_SRC topilmadi."; exit 1; }

CHOICE="$1"
if [ -z "$CHOICE" ]; then
    if [ -t 0 ]; then
        echo "Qaysi layoutni o'rnatamiz?"
        echo "  1) basic  - [ ] ; '  tugmalari  -> ö ğ ş ç   (joriy layout)"
        echo "  2) cw     - c w ; ,  tugmalari  -> ç ş ö ğ   (yangi)"
        echo "  3) ikkalasi"
        read -r -p "Tanlang [1-3, standart 1]: " n
        case "$n" in 2) CHOICE=cw ;; 3) CHOICE=all ;; *) CHOICE=basic ;; esac
    else
        CHOICE=basic
    fi
fi
valid_variant "$CHOICE" || { echo "Xato: noma'lum variant \"$CHOICE\" (basic | cw | all)"; exit 1; }

echo "==> XKB symbols faylini nusxalash (root huquqi kerak)..."
as_root cp "$SYMBOLS_SRC" "$SYMBOLS_DEST"
echo "    -> $SYMBOLS_DEST"

if is_gnome; then
    echo "==> GNOME aniqlandi. Input source ro'yxatiga qo'shilmoqda..."
    for v in $(variants_of "$CHOICE"); do
        ID="$(src_id "$v")"
        CURRENT="$(gsettings get org.gnome.desktop.input-sources sources)"
        if echo "$CURRENT" | grep -qF "$ID"; then
            echo "    -> $ID allaqachon qo'shilgan."
            continue
        fi
        NEW="$(python3 - "$CURRENT" "$ID" << "PYEOF"
import ast, sys
cur = ast.literal_eval(sys.argv[1])
cur.append(("xkb", sys.argv[2]))
print(cur)
PYEOF
)"
        gsettings set org.gnome.desktop.input-sources sources "$NEW"
        echo "    -> $ID qo'shildi."
    done
    echo ""
    echo "Tayyor! Layoutlarni Super+Space bilan almashtiring."
    echo "Ro'yxatda ko'rinmasa, seansdan chiqib qayta kiring."
else
    [ "$CHOICE" = "all" ] && { echo "Xato: GNOME bo'lmagan muhitda bir vaqtda faqat bitta variant yoqiladi (basic yoki cw)."; exit 1; }
    echo "==> GNOME aniqlanmadi. Xorg 'setxkbmap' usuli ishlatilmoqda..."
    setxkbmap -symbols "pc+us+uzq($CHOICE)"
    mkdir -p "$(dirname "$AUTOSTART_FILE")"
    cat > "$AUTOSTART_FILE" << DESK
[Desktop Entry]
Type=Application
Exec=setxkbmap -symbols "pc+us+uzq($CHOICE)"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Uzbek Keyboard Layout ($CHOICE)
Comment=Yangi o'zbek lotin alifbosi (Ö Ğ Ş Ç) klaviatura layouti
DESK
    echo "    -> Faollashtirildi, autostart yozuvi: $AUTOSTART_FILE"
fi
echo "Olib tashlash uchun: ./uninstall.sh [basic|cw|all]"
