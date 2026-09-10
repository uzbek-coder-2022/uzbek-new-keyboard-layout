# O'zbek klaviatura layouti (yangi lotin alifbosi) — Ubuntu/Linux uchun

Bu loyiha 2026-yilgi o'zbek lotin alifbosi islohotida kiritilayotgan yangi harflar —
**Ö, Ğ, Ş, Ç** hamda tutuq belgisi **ʼ** — uchun Ubuntu (va boshqa X11/XKB asosidagi
Linux distributivlari) uchun tayyor klaviatura layoutini taqdim etadi.

Islohotga ko'ra, avvalgi ikki belgili harflar bittaga almashtirilmoqda:

| Eski yozuv | Yangi harf |
|---|---|
| Sh, sh | Ş, ş |
| Ch, ch | Ç, ç |
| Oʻ, oʻ | Ö, ö |
| Gʻ, gʻ | Ğ, ğ |

## Qanday ishlaydi?

Standart QWERTY (`us`) layout asos qilib olingan, faqat 5 ta tugma o'zgartirilgan —
xuddi turk "Q" klaviaturasidagi kabi joylashuv qo'llanilgan, chunki bu harflar
turk alifbosida ham mavjud va o'sha tugmalar allaqachon shu maqsadga moslashtirilgan:

| Tugma | Oddiy holat | Shift bilan | Chap Alt bilan (eski belgi) |
|---|---|---|---|
| `` ` `` | ʼ (tutuq belgisi) | ~ | ` |
| `[` | ö | Ö | [ |
| `]` | ğ | Ğ | ] |
| `;` | ş | Ş | ; |
| `'` | ç | Ç | ' |

Eski belgilarga ([ ] ; ' `) o'tish uchun **chap Alt** tugmasi ishlatiladi
(ba'zi noutbuklarda o'ng Alt/AltGr ishlamasligi mumkinligi sababli, standart
o'ng Alt o'rniga tanlangan). Agar sizga aksincha, o'ng Alt (AltGr) qulayroq
bo'lsa, `uzq` faylining oxiridagi

```
include "level3(lalt_switch)"
```

qatorini

```
include "level3(ralt_switch)"
```

ga almashtirib, faylni qayta o'rnating (`sudo cp uzq /usr/share/X11/xkb/symbols/uzq`)
va seansdan chiqib qayta kiring.

Qolgan barcha tugmalar (harflar, raqamlar, belgilar) odatdagidek — standart
ingliz klaviaturasi kabi ishlaydi. Ya'ni, matn terish uchun hech qanday qo'shimcha
o'rganish kerak emas, faqat shu 5 ta tugma yangi vazifaga ega bo'ladi.

## Muhim: Wayland va Xorg farqi

Zamonaviy Ubuntu (22.04+) da GNOME odatda **Wayland** protokolida ishlaydi.
`setxkbmap` buyrug'i faqat **Xorg** uchun mo'ljallangan va Wayland'da
`WARNING: Running setxkbmap against an Xwayland server` ogohlantirishi bilan
birga amalda hech narsani o'zgartirmaydi. Shuning uchun `install.sh` skripti
muhitni avtomatik aniqlaydi:

- **GNOME (Wayland yoki Xorg)** — `gsettings` orqali layoutni to'g'ridan-to'g'ri
  "Input Sources" ro'yxatiga qo'shadi (GNOME o'z klaviatura boshqaruviga ega,
  `setxkbmap`ga bog'liq emas).
- **Xorg / boshqa DE (XFCE, i3, va h.k.)** — an'anaviy `setxkbmap` usulidan
  foydalanadi.

## GNOME Settings ro'yxatida "uzq+basic" o'rniga chiroyli nom ko'rsatish

`install.sh` orqali qo'shilgan layout GNOME Settings'da texnik nomi bilan —
**`uzq+basic`** — ko'rinadi, chunki u faqat `gsettings` orqali qo'shilgan va
GNOME'ning "chiroyli ism" reestrida (`/usr/share/X11/xkb/rules/evdev.xml`)
hali ro'yxatdan o'tmagan.

Buni tuzatish uchun:

```bash
chmod +x register-name.sh
./register-name.sh
```

Bu skript ikkita fayldan iborat — `register-name.sh` (bosh skript) va
`xkb_register.py` (asosiy ishni bajaruvchi yordamchi) — ikkalasi bir papkada
bo'lishi shart. Skript `evdev.xml` (va mavjud bo'lsa `base.xml`) fayllariga
yangi `<layout>` yozuvini qo'shadi va **"New Uzbek (Latin)"** nomini
belgilaydi (o'zgartirilgan fayllar avtomatik `.bak` nusxa sifatida
zaxiralanadi). Boshqa nom xohlasangiz:

```bash
./register-name.sh "Ozbekcha yangi alifbo"
```

> Eslatma: nomni kiritishda apostrof (`'`) belgisidan saqlaning — ba'zi
> matn muharrirlari yoki messenjerlar uni "aqlli tirnoq" (`'`) ga
> avtomatik almashtirib qo'yishi mumkin, bu esa skriptni buzadi. Shu sabab
> standart nomda ham apostrof ishlatilmagan.

O'zgarish ko'rinishi uchun **seansdan chiqib qayta kiring**. Shundan so'ng
Settings → Keyboard → Input Sources ro'yxatida `uzq+basic` o'rniga siz
tanlagan nom chiqadi — mavjud layoutni qayta qo'shishning hojati yo'q,
faqat ismi yangilanadi.

> Eslatma: `evdev.xml`/`base.xml` `xkb-data` paketiga tegishli bo'lgani
> uchun, tizim yangilanishida bu fayl qayta yozilib ketishi mumkin. Bunday
> holatda `./register-name.sh` ni qayta ishga tushirsangiz kifoya.

## O'rnatish

### 1-usul: Avtomatik skript orqali (tavsiya etiladi)

```bash
git clone https://github.com/<sizning-nomingiz>/uzbek-keyboard-layout.git
cd uzbek-keyboard-layout
chmod +x install.sh
./install.sh
```

Skript quyidagilarni bajaradi:
1. `uzq` faylini `/usr/share/X11/xkb/symbols/` papkasiga nusxalaydi (sudo talab qiladi).
2. Muhitni aniqlaydi:
   - GNOME bo'lsa — `gsettings` orqali input source sifatida qo'shadi.
   - Xorg/boshqa DE bo'lsa — `setxkbmap` bilan darhol yoqadi va autostart
     yozuvi qo'shadi.

O'rnatgandan so'ng GNOME'da **Super+Space** (yoki tepadagi panelda til
belgisi) orqali layoutlar o'rtasida almashtiring. Agar darhol ko'rinmasa,
seansdan chiqib qayta kiring.

### 2-usul: Qo'lda o'rnatish

**GNOME (Wayland/Xorg):**

```bash
sudo cp uzq /usr/share/X11/xkb/symbols/uzq
gsettings set org.gnome.desktop.input-sources sources \
  "[('xkb', 'us'), ('xkb', 'uzq+basic')]"
```

> Diqqat: bu buyruq mavjud input source ro'yxatingizni butunlay almashtiradi.
> Boshqa layoutlaringiz bo'lsa, avval `gsettings get org.gnome.desktop.input-sources sources`
> buyrug'i bilan joriy ro'yxatni ko'rib, uni qo'lda kengaytiring
> (`install.sh` buni avtomatik va xavfsiz tarzda bajaradi).

**Xorg / boshqa DE:**

```bash
sudo cp uzq /usr/share/X11/xkb/symbols/uzq
setxkbmap -symbols "pc+us+uzq(basic)"
```

Doimiy qilish uchun yuqoridagi `setxkbmap` buyrug'ini `~/.xprofile` fayliga
yoki avtostart ilovalariga qo'shing.

## Sinab ko'rish

O'rnatgandan so'ng matn maydoniga o'tib, quyidagi tugmalarni bosib ko'ring:

```
[ -> ö      ]  -> ğ      ; -> ş      ' -> ç      ` -> ʼ
```

## Olib tashlash

```bash
chmod +x uninstall.sh
./uninstall.sh
```

Bu buyruq layoutni standart `us` ga qaytaradi, symbols faylini va autostart
yozuvini o'chiradi.

## GNOME Settings orqali tanlash (ixtiyoriy, ilg'or foydalanuvchilar uchun)

`install.sh` skripti layoutni fon rejimida avtomatik yoqadi, shuning uchun
GNOME "Settings → Keyboard → Input Sources" ro'yxatida ko'rinishi shart emas.
Agar uni rasman input source sifatida ro'yxatga qo'shmoqchi bo'lsangiz,
`/usr/share/X11/xkb/rules/evdev.xml` faylini tahrirlab, `<layoutList>` ichiga
mos `<layout>` yozuvini qo'shishingiz kerak bo'ladi. Bu fayl tizim
yangilanishlarida qayta yozilib ketishi mumkinligi uchun, aksariyat
foydalanuvchilar uchun yuqoridagi avtostart usuli qulayroq va barqarorroq.

## Muammo yuzaga kelsa

- **`[` `]` `;` `'` `` ` `` kabi eski belgilarga umuman o'tib bo'lmayapti** —
  `uzq` faylida `include "level3(lalt_switch)"` qatori borligini tekshiring
  (eski nusxalarda bu qator yo'q edi, shu sabab eski belgilar hech qanday
  tugma bilan yetib bo'lmaydigan holatda qolar edi).
- **Chap Alt tugmasi endi Alt+Tab, Alt+F4 kabi tizim yorliqlarida g'alati
  ishlayapti** — bu `level3(lalt_switch)` ning yon ta'siri bo'lishi mumkin.
  Yuqoridagi "Qanday ishlaydi?" bo'limida ko'rsatilganidek, `lalt_switch`
  ni `ralt_switch` ga almashtirib, eski belgilarni o'ng Alt (AltGr) orqali
  chiqarishga qaytishingiz mumkin.
- **`setxkbmap` ishlatganda "Running setxkbmap against an Xwayland server"
  ogohlantirishi chiqmoqda** — bu normal holat, GNOME Wayland'da ishlayapti
  degani. `setxkbmap` o'rniga yuqoridagi `gsettings` usulini (yoki
  `install.sh` skriptini) ishlating.
- **Layout o'rnatilgandan keyin ro'yxatda ko'rinmayapti** — seansdan chiqib
  qayta kiring, yoki `gsettings get org.gnome.desktop.input-sources sources`
  bilan ro'yxatga `('xkb', 'uzq+basic')` qo'shilganini tekshiring.
- **Boshqa distributiv (Fedora, Arch va h.k.)** — `uzq` fayli standart XKB
  formatida yozilgan, shuning uchun `/usr/share/X11/xkb/symbols/` yo'li mavjud
  bo'lgan istalgan tizimda ishlashi kerak (GNOME'da `gsettings`, boshqa DE'da
  `setxkbmap` orqali).
- **Super+Space layoutlar orasida almashtirmayapti** — Settings → Keyboard →
  Keyboard Shortcuts → "View and Customize Shortcuts" → **Typing** bo'limida
  "Switch to next input source" qaysi tugmaga bog'langanini tekshiring —
  ba'zi tizimlarda bu boshqa amalga (masalan, oyna almashtirishga) band
  bo'lgan bo'lishi mumkin. Muqobil yechim: tepadagi panelda til
  ko'rsatkichini (masalan, "us") sichqoncha bilan bosib, ro'yxatdan qo'lda
  tanlash.
- **register-name.sh ishga tushirilganda g'alati xato yoki butun fayl
  matn sifatida chiqib ketsa** — bu odatda fayl tarkibidagi apostrof (`'`)
  belgisi biror dastur (matn muharriri, messenjer va h.k.) tomonidan
  "aqlli tirnoq"ga (`'`) almashtirilib qo'yilganida yuz beradi. Faylni
  qaytadan zipdan chiqarib, hech qanday GUI matn muharririda ochmasdan,
  to'g'ridan-to'g'ri terminaldan ishga tushiring.

## Hissa qo'shish

Takliflar, xatoliklar yoki boshqa klaviatura joylashuvlari (masalan, "F"
joylashuvi) uchun Pull Request yoki Issue oching.

## Litsenziya

MIT — [LICENSE](LICENSE) fayliga qarang.