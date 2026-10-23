#!/usr/bin/env python3
"""
evdev.xml / base.xml fayliga yangi <layout> yozuvini qo'shadi, shunda
GNOME Settings da klaviatura layoutlari texnik "uzq+basic" / "uzq+cw" nomi
o'rniga o'qilishi qulay nom bilan ko'rinadi (ikkala variant bitta <layout>
ichida ro'yxatdan o'tadi).

Agar "uzq" yozuvi faylda allaqachon mavjud bo'lsa, uni o'chirib
tashlamasdan, ichidagi nomni (description) yangi nomga yangilaydi.

Ishlatilishi:
    sudo python3 xkb_register.py <fayl_yoli> <korsatiladigan_nom>
"""

import re
import sys


def build_block(desc):
    variants = (
        ("basic", desc),
        ("cw", desc + " - C/W"),
    )
    items = ""
    for name, text in variants:
        items += (
            "      <variant>\n"
            "        <configItem>\n"
            "          <name>" + name + "</name>\n"
            "          <description>" + text + "</description>\n"
            "        </configItem>\n"
            "      </variant>\n"
        )
    return (
        "  <layout>\n"
        "    <configItem>\n"
        "      <name>uzq</name>\n"
        "      <shortDescription>uz</shortDescription>\n"
        "      <description>" + desc + "</description>\n"
        "      <languageList>\n"
        "        <iso639Id>uzb</iso639Id>\n"
        "      </languageList>\n"
        "    </configItem>\n"
        "    <variantList>\n"
        + items +
        "    </variantList>\n"
        "  </layout>\n"
    )


def remove(path):
    """XKB reestridan "uzq" <layout> blokini olib tashlaydi (paketni o'chirishda)."""
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    block_re = re.compile(
        r"  <layout>\n(?:(?!</layout>).)*?<name>uzq</name>(?:(?!</layout>).)*?  </layout>\n",
        re.DOTALL,
    )
    new_content, n = block_re.subn("", content)
    if n:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        print("Olib tashlandi: " + path)
    else:
        print("O'tkazib yuborildi (yozuv yo'q): " + path)


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--remove":
        remove(sys.argv[2])
        return
    if len(sys.argv) != 3:
        print("Xato: 2 ta argument kerak: fayl_yoli va nom")
        sys.exit(1)

    path = sys.argv[1]
    desc = sys.argv[2]

    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()

    new_block = build_block(desc)

    # <name>uzq</name> ni o'z ichiga olgan mavjud <layout>...</layout>
    # blokini qidiramiz (bor bo'lsa, uni yangi nom bilan almashtiramiz).
    existing_block_re = re.compile(
        r"  <layout>\n(?:(?!</layout>).)*?<name>uzq</name>(?:(?!</layout>).)*?  </layout>\n",
        re.DOTALL,
    )
    match = existing_block_re.search(content)

    if match:
        if match.group(0) == new_block:
            print("O'tkazib yuborildi (nom allaqachon to'g'ri): " + path)
            return
        new_content = content[: match.start()] + new_block + content[match.end():]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        print("Nom yangilandi: " + path)
        return

    marker = "</layoutList>"
    idx = content.rfind(marker)
    if idx == -1:
        print("XATO: </layoutList> topilmadi: " + path)
        sys.exit(1)

    new_content = content[:idx] + new_block + content[idx:]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_content)

    print("Qo'shildi: " + path)


if __name__ == "__main__":
    main()