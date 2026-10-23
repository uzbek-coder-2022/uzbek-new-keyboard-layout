#!/usr/bin/env bash
# Umumiy yordamchi funksiyalar (install.sh, uninstall.sh, register-name.sh uchun).

SYMBOLS_DEST="/usr/share/X11/xkb/symbols/uzq"
AUTOSTART_FILE="$HOME/.config/autostart/uz-keyboard.desktop"

# variant -> GNOME input source identifikatori
src_id() { echo "uzq+$1"; }

# root huquqi bilan buyruq bajarish: root bo'lsa to'g'ridan-to'g'ri, terminal bo'lsa sudo,
# aks holda (GUI) pkexec.
as_root() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    elif [ -t 0 ] || ! command -v pkexec >/dev/null 2>&1; then
        sudo "$@"
    else
        pkexec "$@"
    fi
}

is_gnome() {
    command -v gsettings >/dev/null 2>&1 \
        && gsettings list-schemas 2>/dev/null | grep -q "org.gnome.desktop.input-sources"
}

# variant nomini tekshirish: basic | cw | all
valid_variant() {
    case "$1" in basic|cw|all) return 0 ;; *) return 1 ;; esac
}

variants_of() {
    if [ "$1" = "all" ]; then echo "basic cw"; else echo "$1"; fi
}
