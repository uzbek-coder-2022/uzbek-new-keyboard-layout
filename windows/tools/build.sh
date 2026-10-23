#!/usr/bin/env bash
#
# Windows layout DLL'larini mingw-w64 bilan yig'adi (Linux yoki WSL'da).
#   sudo apt install gcc-mingw-w64-x86-64 gcc-mingw-w64-i686 binutils-mingw-w64
#   bash tools/build.sh
#
# Natija: bin/x64/kbd*.dll va bin/x86/kbd*.dll

set -e
cd "$(dirname "$0")/.."

python3 tools/generate.py

for id in uzq uzcw; do
    for arch in x64 x86; do
        if [ "$arch" = "x64" ]; then CC=x86_64-w64-mingw32-gcc; EXTRA="-Wl,--disable-high-entropy-va"; else CC=i686-w64-mingw32-gcc; EXTRA=""; fi
        mkdir -p "bin/$arch"
        # -nostdlib: hech qanday importsiz toza DLL (kernel rejimida win32k yuklaydi)
        # --subsystem native, --entry=0: MSKLC DLL'lari kabi kirish nuqtasisiz
        $CC -O2 -s -shared -nostdlib -nostartfiles -ffreestanding -Wall -Isrc \
            -Wl,--subsystem,native \
            -Wl,--entry=0 \
            $EXTRA \
            -Wl,--file-alignment,0x200 -Wl,--section-alignment,0x1000 \
            -o "bin/$arch/kbd$id.dll" "src/kbd$id.c" "src/kbd$id.def"
        echo "yig'ildi: bin/$arch/kbd$id.dll"
    done
done

python3 tools/pe_checksum.py bin/x64/*.dll bin/x86/*.dll
