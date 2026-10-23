#!/usr/bin/env bash
#
# Hamma distrolar uchun tar.gz:  bash linux/build-tarball.sh [versiya]  -> linux/dist/*.tar.gz
# Foydalanuvchi:  tar xzf ...; cd uzbek-new-keyboard-layout-*; sudo make -C linux install
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(dirname "$HERE")"
VER="${1:-2.0.0}"
NAME="uzbek-new-keyboard-layout-$VER"
STAGE="$(mktemp -d)/$NAME"
mkdir -p "$STAGE"
cp -r "$REPO/linux" "$REPO/LICENSE" "$STAGE/"
rm -rf "$STAGE/linux/dist" "$STAGE/linux/__pycache__" "$STAGE/linux/lib/__pycache__"
mkdir -p "$HERE/dist"
tar -C "$(dirname "$STAGE")" -czf "$HERE/dist/$NAME-linux.tar.gz" "$NAME"
ls -la "$HERE/dist/$NAME-linux.tar.gz"
