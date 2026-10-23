#!/usr/bin/env bash
#
# Uzbek-Keyboard-Setup.exe ni yig'adi (Linux/WSL, Mono kerak):
#   sudo apt install mono-mcs libmono-system-windows-forms4.0-cil binutils-mingw-w64
#   bash windows/installer/build-exe.sh
#
# Oldin DLL'lar yig'ilgan bo'lishi kerak: bash windows/tools/build.sh
set -e
cd "$(dirname "$0")/.."          # windows/
for f in Setup.ps1 bin/x64/kbduzq.dll bin/x64/kbduzcw.dll bin/x86/kbduzq.dll bin/x86/kbduzcw.dll; do
    [ -f "$f" ] || { echo "Topilmadi: $f (avval tools/build.sh ni ishga tushiring)"; exit 1; }
done
# UAC (administrator) manifesti: mcs -win32manifest'ni qo'llamaydi, shuning uchun .res yasaymiz
echo '1 24 "installer/app.manifest"' > installer/manifest.rc
x86_64-w64-mingw32-windres -O res -i installer/manifest.rc -o installer/manifest.res

mcs -nologo -target:winexe -platform:anycpu -optimize+ \
    -win32res:installer/manifest.res \
    -reference:System.Windows.Forms.dll \
    -resource:Setup.ps1,Setup.ps1 \
    -resource:bin/x64/kbduzq.dll,bin/x64/kbduzq.dll \
    -resource:bin/x64/kbduzcw.dll,bin/x64/kbduzcw.dll \
    -resource:bin/x86/kbduzq.dll,bin/x86/kbduzq.dll \
    -resource:bin/x86/kbduzcw.dll,bin/x86/kbduzcw.dll \
    -out:Uzbek-Keyboard-Setup.exe installer/Setup.cs
rm -f installer/manifest.rc installer/manifest.res
echo "yig'ildi: windows/Uzbek-Keyboard-Setup.exe"
