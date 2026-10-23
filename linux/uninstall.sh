#!/usr/bin/env bash
#
# Uzbek klaviatura layoutlarini olib tashlash.
#   ./uninstall.sh          -> hammasi (all)
#   ./uninstall.sh basic    -> faqat Q joylashuvi
#   ./uninstall.sh cw       -> faqat C/W joylashuvi
#
# Symbols fayli faqat ikkala layout ham ishlatilmay qolganda o'chiriladi.

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/lib/common.sh"

CHOICE="${1:-all}"
valid_variant "$CHOICE" || { echo "Xato: noma'lum variant \"$CHOICE\" (basic | cw | all)"; exit 1; }

if is_gnome; then
    echo "==> GNOME input source ro'yxatidan olib tashlanmoqda..."
    for v in $(variants_of "$CHOICE"); do
        CURRENT="$(gsettings get org.gnome.desktop.input-sources sources)"
        NEW="$(python3 - "$CURRENT" "$(src_id "$v")" << "PYEOF"
import ast, sys
cur = ast.literal_eval(sys.argv[1])
print([s for s in cur if s != ("xkb", sys.argv[2])])
PYEOF
)"
        # ro'yxat bo'sh qolmasligi uchun (GNOME buzilmasin) kamida "us" qoldiramiz
        [ "$NEW" = "[]" ] && NEW="[(\"xkb\", \"us\")]"
        gsettings set org.gnome.desktop.input-sources sources "$NEW"
        echo "    -> $(src_id "$v") olib tashlandi."
    done
    STILL="$(gsettings get org.gnome.desktop.input-sources sources)"
    if echo "$STILL" | grep -qE "uzq\+(basic|cw)"; then
        echo "==> Boshqa uzq layouti hali ishlatilmoqda — symbols fayli saqlab qolindi."
        exit 0
    fi
else
    echo "==> Standart layoutga qaytarilmoqda..."
    setxkbmap us || true
    rm -f "$AUTOSTART_FILE" && echo "==> Autostart yozuvi o'chirildi."
fi

if [ -f "$SYMBOLS_DEST" ]; then
    echo "==> Symbols faylini o'chirish (root huquqi kerak)..."
    as_root rm -f "$SYMBOLS_DEST"
fi
echo "Layout olib tashlandi."
