#!/usr/bin/env bash
#
# uzbek-new-keyboard-layout_<versiya>_all.deb ni yig'adi.
#   bash linux/deb/build-deb.sh [versiya]        (standart: 2.0.0)
# Talab: dpkg-deb (Debian/Ubuntu'da bor)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
LIN="$(dirname "$HERE")"
VER="${1:-2.0.0}"
PKG="uzbek-new-keyboard-layout"
OUT="$LIN/dist"
ROOT="$(mktemp -d)/$PKG"

install -d "$ROOT/DEBIAN" "$ROOT/usr/bin" "$ROOT/usr/share/uzbek-keyboard" \
           "$ROOT/usr/share/X11/xkb/symbols" "$ROOT/usr/share/applications" \
           "$ROOT/usr/share/doc/$PKG"

install -m 0644 "$LIN/xkb/symbols/uzq"        "$ROOT/usr/share/X11/xkb/symbols/uzq"
install -m 0755 "$HERE/uzbek-keyboard"        "$ROOT/usr/bin/uzbek-keyboard"
printf '#!/bin/sh\nexec uzbek-keyboard gui "$@"\n' > "$ROOT/usr/bin/uzbek-keyboard-gui"; chmod 0755 "$ROOT/usr/bin/uzbek-keyboard-gui"
install -m 0644 "$LIN/lib/xkb_register.py"    "$ROOT/usr/share/uzbek-keyboard/xkb_register.py"
install -m 0755 "$LIN/uz-keyboard-gui.py"     "$ROOT/usr/share/uzbek-keyboard/uz-keyboard-gui.py"
install -m 0644 "$HERE/uzbek-keyboard.desktop" "$ROOT/usr/share/applications/uzbek-keyboard.desktop"
install -m 0644 "$LIN/../LICENSE"             "$ROOT/usr/share/doc/$PKG/copyright"

install -m 0644 "$HERE/templates" "$ROOT/DEBIAN/templates"
install -m 0755 "$HERE/postinst" "$HERE/prerm" "$HERE/postrm" "$ROOT/DEBIAN/"
echo "interest-noawait /usr/share/X11/xkb/rules" > "$ROOT/DEBIAN/triggers"

SIZE="$(du -sk --exclude=DEBIAN "$ROOT" | cut -f1)"
cat > "$ROOT/DEBIAN/control" << CTL
Package: $PKG
Version: $VER
Section: utils
Priority: optional
Architecture: all
Installed-Size: $SIZE
Depends: debconf (>= 1.5), python3, xkb-data
Recommends: python3-gi, gir1.2-gtk-3.0, x11-xkb-utils
Maintainer: Uzbek keyboard layout <noreply@example.com>
Homepage: https://github.com/
Description: New Uzbek (Latin) keyboard layouts (Ö Ğ Ş Ç ʼ)
 Two XKB layout variants for the new Uzbek Latin alphabet:
 "basic" (Q layout: [ ] ; ' -> ö ğ ş ç) and "cw" (c w ; , -> ç ş ö ğ).
 The old characters stay available via AltGr. The variants to enable are
 chosen at install time and can be changed later with "uzbek-keyboard" or
 its GTK window.
CTL

( cd "$ROOT" && find . -type f ! -path './DEBIAN/*' -printf '%P\0' | xargs -0 md5sum > DEBIAN/md5sums )
mkdir -p "$OUT"
dpkg-deb --root-owner-group --build "$ROOT" "$OUT/${PKG}_${VER}_all.deb"
