#!/usr/bin/env bash
#
# .rpm yig'ish (Fedora/RHEL/openSUSE yoki Debian'da `apt install rpm`):
#   bash linux/rpm/build-rpm.sh [versiya]     -> linux/dist/*.rpm
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
VER="${1:-2.0.0}"
TOP="$(mktemp -d)"
mkdir -p "$TOP"/{SOURCES,SPECS,BUILD,RPMS,SRPMS}

STAGE="$(mktemp -d)/uzbek-new-keyboard-layout-$VER"
mkdir -p "$STAGE"
cp -r "$REPO/linux" "$REPO/LICENSE" "$STAGE/"
rm -rf "$STAGE/linux/dist" "$STAGE/linux/__pycache__" "$STAGE/linux/lib/__pycache__"
tar -C "$(dirname "$STAGE")" -czf "$TOP/SOURCES/uzbek-new-keyboard-layout-$VER.tar.gz" "uzbek-new-keyboard-layout-$VER"

cp "$HERE/uzbek-new-keyboard-layout.spec" "$TOP/SPECS/"
rpmbuild -bb --define "_topdir $TOP" --define "pkgver $VER" "$TOP/SPECS/uzbek-new-keyboard-layout.spec"
mkdir -p "$REPO/linux/dist"
cp "$TOP"/RPMS/noarch/*.rpm "$REPO/linux/dist/"
ls -la "$REPO/linux/dist/"*.rpm
