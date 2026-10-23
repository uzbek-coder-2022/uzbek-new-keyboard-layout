# O'zbek klaviatura layouti (yangi lotin alifbosi) — Linux va Windows

2026-yilgi o'zbek lotin alifbosi islohotidagi yangi harflar — **Ö, Ğ, Ş, Ç** va tutuq
belgisi **ʼ** — uchun tayyor klaviatura layoutlari. Ikkita variant bor, ikkalasi ham
**Linux (XKB)** va **Windows** uchun:

| Eski yozuv | Yangi harf |
|---|---|
| Sh, sh | Ş, ş |
| Ch, ch | Ç, ç |
| Oʻ, oʻ | Ö, ö |
| Gʻ, gʻ | Ğ, ğ |

## Ikki variant

Ikkalasi ham standart inglizcha QWERTY asosida; faqat ko'rsatilgan tugmalar o'zgargan.
Almashtirilgan tugmaning **eski belgisi o'ng Alt (AltGr)** bilan chiqadi.

### 1) Q joylashuvi — `basic` (Linux) / `uzq` (Windows)  ← joriy layout, o'zgarmagan

| Tugma | Oddiy | Shift | AltGr (eski belgi) |
|---|---|---|---|
| `[` | ö | Ö | `[` / `{` |
| `]` | ğ | Ğ | `]` / `}` |
| `;` | ş | Ş | `;` / `:` |
| `'` | ç | Ç | `'` / `"` |
| `` ` `` | ʼ | ~ | `` ` `` |

### 2) C/W joylashuvi — `cw` (Linux) / `uzcw` (Windows)  ← yangi

| Tugma | Oddiy | Shift | AltGr (eski belgi) |
|---|---|---|---|
| `c` | ç | Ç | `c` / `C` |
| `w` | ş | Ş | `w` / `W` |
| `;` | ö | Ö | `;` / `:` |
| `,` | ğ | Ğ | `,` / `<` |
| `` ` `` | ʼ | ~ | `` ` `` |

> Ikkala variantda ham tutuq belgisi (ʼ, U+02BC) `` ` `` tugmasida. Qolgan barcha tugmalar
> odatdagi inglizcha klaviatura kabi. CapsLock harflarga (ç ş ö ğ) ta'sir qiladi, `ʼ` ga yo'q.

## Fayl tuzilmasi

```
uzbek-new-keyboard-layout/
├── README.md
├── LICENSE
├── linux/
│   ├── xkb/symbols/uzq          # XKB fayli: ikkala variant (basic, cw)
│   ├── install.sh               # o'rnatish   (basic | cw | all)
│   ├── uninstall.sh             # o'chirish   (basic | cw | all)
│   ├── register-name.sh         # GNOME Settings'da chiroyli nom
│   ├── uz-keyboard-gui.py       # o'rnatish/o'chirish oynasi (GTK3)
│   ├── deb/                     # .deb paket manbalari (build-deb.sh, postinst, templates ...)
│   └── lib/
│       ├── common.sh
│       └── xkb_register.py
└── windows/
    ├── Uzbek-Keyboard-Setup.exe # ← YAGONA FAYL: ikki marta bosing (DLL'lar ichida)
    ├── Setup.bat                # muqobil: exe'siz ishga tushirish (bin\ kerak)
    ├── Setup.ps1                # o'rnatuvchi: oyna (UI) + buyruq satri
    ├── installer/               # exe manbasi: Setup.cs, app.manifest, build-exe.sh
    ├── bin/
    │   ├── x64/  kbduzq.dll  kbduzcw.dll
    │   └── x86/  kbduzq.dll  kbduzcw.dll
    ├── klc/     uzq.klc  uzcw.klc        # MSKLC manbalari (ixtiyoriy yo'l)
    ├── src/     kbd.h  kbd*.c  kbd*.def  # layout DLL manbalari (avtomatik hosil bo'ladi)
    └── tools/
        ├── generate.py          # layoutlarning YAGONA manbasi
        ├── build.sh             # DLL'larni yig'adi (mingw-w64)
        ├── verify.py            # tayyor DLL'ni binar darajada tekshiradi
        └── pe_checksum.py
```

---

## Windows

**Talab:** Windows 10/11 (x64 yoki x86). ARM64 qo'llab-quvvatlanmaydi.

### O'rnatish va o'chirish — oyna orqali

1. **`Uzbek-Keyboard-Setup.exe`** ni ikki marta bosing → administrator ruxsatini bering (UAC).
   Fayl yagona: DLL'lar va o'rnatuvchi uning ichida, boshqa fayl kerak emas.
   (Muqobil: ZIP'ni to'liq chiqarib, `Setup.bat` ni ishga tushiring.)
3. Oynada kerakli layout(lar)ni belgilab, **O'rnatish** yoki **O'chirish** tugmasini bosing.
   Oyna har bir layout o'rnatilgan/o'rnatilmaganligini ko'rsatadi.
4. **Win + Space** bilan layoutni tanlang. Ko'rinmasa — tizimdan chiqib qayta kiring
   (yoki **Til sozlamalari** tugmasi orqali qo'lda qo'shing).

Til tanlash: odatda **English (US)** — u har qanday Windows'da bor. Xohlasangiz **Uzbek (Latin)** ga
ham o'rnatish mumkin.

### Buyruq satri (oynasiz)

```powershell
.\Uzbek-Keyboard-Setup.exe -Action Install   -Layout uzq,uzcw
.\Uzbek-Keyboard-Setup.exe -Action Uninstall -Layout uzq,uzcw
# yoki exe'siz:
.\Setup.ps1 -Action Install   -Layout uzq,uzcw -Language en-US
.\Setup.ps1 -Action Install   -Layout uzcw -NoLanguageList     # faqat reestr + fayl
.\Setup.ps1 -Action Uninstall -Layout uzq,uzcw
.\Setup.ps1 -Action Status
```

### O'rnatuvchi nima qiladi

1. `kbd*.dll` ni `System32` ga (64-bitli tizimda `SysWOW64` ga x86 nusxasini ham) nusxalaydi.
2. `HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\` ostida kalit yaratadi
   (band bo'lmagan `a00N….` KLID va noyob `Layout Id` ni o'zi tanlaydi — boshqa
   o'rnatilgan layoutlarga tegmaydi).
3. Layoutni joriy foydalanuvchining til ro'yxatiga qo'shadi.

O'chirish buni teskari tartibda bajaradi. Agar DLL band bo'lsa, u kompyuter qayta ishga
tushganda o'chiriladi.

### DLL'larni qayta yig'ish (ixtiyoriy)

```bash
sudo apt install gcc-mingw-w64-x86-64 gcc-mingw-w64-i686 binutils-mingw-w64
bash windows/tools/build.sh        # generate.py -> kompilyatsiya -> checksum
python3 windows/tools/verify.py    # tayyor DLL'larni binar darajada tekshirish
```

Layoutni o'zgartirmoqchi bo'lsangiz — faqat `windows/tools/generate.py` dagi jadvalni tahrirlang.

`verify.py` tayyor `.dll` fayllarini o'qib (PE → `KBDTABLES`), Windows'ning tugma→belgi
tarjimasini simulyatsiya qiladi: oddiy/Shift/AltGr/Ctrl/CapsLock holatlari, asosiy qatorlar,
`E0`/`E1` tugmalari (o'ng Alt, o'ng Ctrl, strelkalar, Pause) hammasini tekshiradi.

### exe'ni qayta yig'ish

```bash
sudo apt install mono-mcs libmono-system-windows-forms4.0-cil binutils-mingw-w64
bash windows/installer/build-exe.sh     # DLL'lar oldindan yig'ilgan bo'lishi kerak
```

exe — kichik .NET Framework (Windows 10/11'da o'rnatilgan) dasturi: administrator manifestiga ega,
ichidagi `Setup.ps1` va DLL'larni vaqtinchalik papkaga ochib, oynani ishga tushiradi va tugagach tozalaydi.
Imzolanmagan bo'lgani uchun SmartScreen "Baribir ishga tushirish" so'rashi mumkin.

### MSKLC orqali (muqobil yo'l)

Agar o'rnatilgan DLL ishlamasa yoki o'zingiz yig'moqchi bo'lsangiz,
[Microsoft Keyboard Layout Creator](https://www.microsoft.com/en-us/download/details.aspx?id=102134)
da `windows/klc/uzq.klc` yoki `uzcw.klc` ni oching → **Project → Build DLL and Setup Package**.

> **Eslatma.** Windows DLL'lari mingw-w64 bilan yig'ilgan va binar darajada tekshirilgan,
> lekin tizim yadrosi tomonidan yuklanishi haqiqiy Windows'da sinab ko'rilishi kerak.
> Imzolanmagan layout DLL'lari MSKLC yaratganlari kabi xulq qiladi. Muammo bo'lsa,
> `Setup.ps1 -Action Uninstall` bilan qaytaring yoki yuqoridagi MSKLC yo'lidan foydalaning.

---

## Linux

Standart QWERTY (`us`) asos. Ikki variant bitta `uzq` fayli ichida: `uzq+basic` va `uzq+cw`.

### .deb paket (Ubuntu / Debian) — tavsiya etiladi

```bash
sudo apt install ./uzbek-new-keyboard-layout_2.0.0_all.deb     # yoki: sudo dpkg -i ...
```

O'rnatish paytida **savol chiqadi** — qaysi layout(lar) yoqilsin: *Q joylashuvi (basic)*,
*C/W joylashuvi (cw)* yoki ikkalasi (probel bilan belgilang). Sukut bo'yicha `basic`.
Tanlov o'rnatayotgan foydalanuvchining GNOME "Input Sources" ro'yxatiga qo'shiladi.

Keyin istalgan vaqtda (root kerak emas):

```bash
uzbek-keyboard enable  cw        # yoki basic | all
uzbek-keyboard disable basic
uzbek-keyboard status
uzbek-keyboard gui               # yoki ilovalar menyusida "Uzbek Keyboard Layout"
```

Savolsiz o'rnatish (skript/CI uchun):

```bash
echo "uzbek-new-keyboard-layout uzbek-new-keyboard-layout/variants multiselect basic, cw" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt install ./uzbek-new-keyboard-layout_2.0.0_all.deb
```

Paket `/usr/share/X11/xkb/symbols/uzq` ni o'rnatadi, GNOME Settings uchun chiroyli nomlarni
ro'yxatdan o'tkazadi (xkb-data yangilanganda trigger orqali qayta yoziladi) va
`sudo apt remove uzbek-new-keyboard-layout` qilinganda hammasini tozalaydi.
Yig'ish: `bash linux/deb/build-deb.sh [versiya]` → `linux/dist/*.deb`.

### O'rnatish — oyna orqali

```bash
python3 linux/uz-keyboard-gui.py
```

Ikkala layout uchun holat (o'rnatilgan / o'rnatilmagan), **O'rnatish** va **O'chirish** tugmalari
bor. Root huquqi kerak bo'lganda parol so'rash oynasi (`pkexec`) chiqadi.
GTK3 (`python3-gi`) Ubuntu Desktop'da odatda o'rnatilgan.

### O'rnatish — terminal orqali

```bash
cd linux
chmod +x *.sh
./install.sh            # menyu: 1) basic  2) cw  3) ikkalasi
./install.sh basic      # joriy Q layout
./install.sh cw         # yangi C/W layout
./install.sh all        # ikkalasi (GNOME'da)
```

Skript muhitni avtomatik aniqlaydi:

- **GNOME (Wayland yoki Xorg)** — `gsettings` orqali "Input Sources" ro'yxatiga qo'shadi
  (Wayland'da `setxkbmap` ishlamaydi).
- **Xorg / boshqa DE** — `setxkbmap` + autostart yozuvi (bir vaqtda bitta variant).

O'rnatgach **Super+Space** bilan almashtiring. Darhol ko'rinmasa — seansdan chiqib qayta kiring.

### GNOME Settings'da chiroyli nom

Sukut bo'yicha ro'yxatda `uzq+basic` / `uzq+cw` ko'rinadi. Chiroyli nom uchun:

```bash
./register-name.sh                   # "New Uzbek (Latin)" va "New Uzbek (Latin) - C/W"
./register-name.sh "Boshqa nom"
```

`evdev.xml` / `base.xml` zaxiralanadi (`.bak`). Tizim yangilanganda fayl qayta yozilsa —
skriptni yana ishga tushiring. Nomda apostrof ishlatmang. GUI'da bu "chiroyli nom"
katakchasi orqali avtomatik bajariladi.

### O'chirish

```bash
./uninstall.sh          # hammasi
./uninstall.sh cw       # faqat C/W
./uninstall.sh basic    # faqat Q
```

`/usr/share/X11/xkb/symbols/uzq` faqat ikkala layout ham ishlatilmay qolganda o'chiriladi.

### Qo'lda (GNOME)

```bash
sudo cp linux/xkb/symbols/uzq /usr/share/X11/xkb/symbols/uzq
gsettings set org.gnome.desktop.input-sources sources \
  "[('xkb', 'us'), ('xkb', 'uzq+basic'), ('xkb', 'uzq+cw')]"
```

> Bu buyruq mavjud ro'yxatni almashtiradi — avval `gsettings get org.gnome.desktop.input-sources sources`
> bilan joriy ro'yxatni ko'ring. `install.sh` buni xavfsiz bajaradi.

### AltGr o'rniga chap Alt

`linux/xkb/symbols/uzq` dagi `include "level3(ralt_switch)"` qatorini `level3(lalt_switch)` ga
almashtirsangiz, eski belgilar chap Alt bilan chiqadi (Alt+Tab kabi yorliqlarga ta'sir qilishi mumkin).
O'zgargach faylni qayta o'rnating va seansdan chiqib qayta kiring.

---

## Muammolar

- **Linux: ro'yxatda ko'rinmayapti** — seansdan chiqib qayta kiring;
  `gsettings get org.gnome.desktop.input-sources sources` da `uzq+basic` / `uzq+cw` borligini tekshiring.
- **Linux: Super+Space ishlamayapti** — Settings → Keyboard → Shortcuts → Typing →
  "Switch to next input source" ni tekshiring.
- **Windows: layout ro'yxatda yo'q** — tizimdan chiqib qayta kiring; yoki Sozlamalar → Vaqt va til →
  Til → English (US) → Klaviatura qo'shish.
- **Windows: "Fayl topilmadi: …\bin\x64\…"** — ZIP'ni ichidan ishga tushirdingiz; avval **Extract All**.
- **Windows: SmartScreen / ruxsat oynasi** — skript imzolanmagan; "Ko'proq ma'lumot → Baribir ishga tushirish".
- **Windows: DLL o'chmadi** — u band; kompyuterni qayta ishga tushirganda o'chiriladi.

## Hissa qo'shish

Takliflar, xatoliklar yoki boshqa joylashuvlar (masalan, "F" joylashuvi) uchun Pull Request yoki Issue oching.

## Litsenziya

MIT — [LICENSE](LICENSE) fayliga qarang.
