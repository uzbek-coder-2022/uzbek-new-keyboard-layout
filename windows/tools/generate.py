#!/usr/bin/env python3
"""
Windows layoutlarining YAGONA manbasi.

Bu skript quyidagilarni hosil qiladi:
  src/kbd<nom>.c     — layout DLL'i uchun C manba (tools/build.sh yig'adi)
  src/kbd<nom>.def   — eksport ro'yxati (KbdLayerDescriptor)
  klc/<nom>.klc      — Microsoft Keyboard Layout Creator (MSKLC) uchun manba
                       (ixtiyoriy muqobil yo'l; DLL'ni o'zingiz yig'ish uchun)

Layoutni o'zgartirmoqchi bo'lsangiz — faqat shu faylni tahrirlang va
`python3 tools/generate.py && bash tools/build.sh` ni ishga tushiring.

Ustunlar tartibi (Windows "shift state"lari):
    0: oddiy | 1: Shift | 2: Ctrl | 3: AltGr (Ctrl+Alt) | 4: Shift+AltGr
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")
KLC = os.path.join(ROOT, "klc")

# ── Yangi alifbo harflari (Unicode kod nuqtalari) ──────────────────────────
O_, O_C = 0x00F6, 0x00D6   # ö Ö
G_, G_C = 0x011F, 0x011E   # ğ Ğ
S_, S_C = 0x015F, 0x015E   # ş Ş
C_, C_C = 0x00E7, 0x00C7   # ç Ç
TUTUQ = 0x02BC             # ʼ  tutuq belgisi

CAPLOK, SGCAPS, CAPLOKALTGR = 0x01, 0x02, 0x04
N = None                   # belgi yo'q (WCH_NONE)

# ── Ikkala layout uchun asos: standart AQSh (US QWERTY) ────────────────────
# vk_nomi -> (atribut, [col0, col1, col2(Ctrl), col3(AltGr), col4(Shift+AltGr)])
def us_base():
    t = {}
    for i in range(26):
        L = chr(ord("A") + i)
        t["'%s'" % L] = (CAPLOK, [ord(L.lower()), ord(L), i + 1, N, N])
    digits = "1234567890"
    shifted = "!@#$%^&*()"
    for d, s in zip(digits, shifted):
        t["'%s'" % d] = (0, [ord(d), ord(s), N, N, N])
    t["VK_OEM_MINUS"] = (0, [ord("-"), ord("_"), N, N, N])
    t["VK_OEM_PLUS"] = (0, [ord("="), ord("+"), N, N, N])
    t["VK_OEM_4"] = (0, [ord("["), ord("{"), 0x1B, N, N])
    t["VK_OEM_6"] = (0, [ord("]"), ord("}"), 0x1D, N, N])
    t["VK_OEM_5"] = (0, [ord("\\"), ord("|"), 0x1C, N, N])
    t["VK_OEM_1"] = (0, [ord(";"), ord(":"), N, N, N])
    t["VK_OEM_7"] = (0, [ord("'"), ord('"'), N, N, N])
    t["VK_OEM_3"] = (0, [ord("`"), ord("~"), N, N, N])
    t["VK_OEM_COMMA"] = (0, [ord(","), ord("<"), N, N, N])
    t["VK_OEM_PERIOD"] = (0, [ord("."), ord(">"), N, N, N])
    t["VK_OEM_2"] = (0, [ord("/"), ord("?"), N, N, N])
    t["VK_OEM_102"] = (0, [ord("\\"), ord("|"), 0x1C, N, N])
    t["VK_SPACE"] = (0, [0x20, 0x20, 0x20, N, N])
    t["VK_BACK"] = (0, [0x08, 0x08, 0x7F, N, N])
    t["VK_ESCAPE"] = (0, [0x1B, 0x1B, 0x1B, N, N])
    t["VK_RETURN"] = (0, [0x0D, 0x0D, 0x0A, N, N])
    t["VK_CANCEL"] = (0, [0x03, 0x03, 0x03, N, N])
    t["VK_TAB"] = (0, [0x09, 0x09, 0x09, N, N])
    t["VK_ADD"] = (0, [ord("+"), ord("+"), ord("+"), N, N])
    t["VK_SUBTRACT"] = (0, [ord("-"), ord("-"), ord("-"), N, N])
    t["VK_MULTIPLY"] = (0, [ord("*"), ord("*"), ord("*"), N, N])
    t["VK_DIVIDE"] = (0, [ord("/"), ord("/"), ord("/"), N, N])
    t["VK_DECIMAL"] = (0, [ord("."), ord("."), ord("."), N, N])
    return t


# ── Layoutlar ──────────────────────────────────────────────────────────────
LAYOUTS = [
    {
        "id": "uzq",                          # DLL: kbduzq.dll
        "klc_name": "UzQ",                    # MSKLC nomi (<= 8 belgi)
        "text": "New Uzbek (Latin)",          # Windows'da ko'rinadigan nom
        "overrides": {
            # `  -> ʼ   (Shift: ~,  AltGr: `)
            "VK_OEM_3": (0, [TUTUQ, ord("~"), N, ord("`"), ord("`")]),
            # [ ] ; '  -> ö ğ ş ç ; eski belgilar AltGr orqali
            "VK_OEM_4": (CAPLOK, [O_, O_C, 0x1B, ord("["), ord("{")]),
            "VK_OEM_6": (CAPLOK, [G_, G_C, 0x1D, ord("]"), ord("}")]),
            "VK_OEM_1": (CAPLOK, [S_, S_C, N, ord(";"), ord(":")]),
            "VK_OEM_7": (CAPLOK, [C_, C_C, N, ord("'"), ord('"')]),
        },
    },
    {
        "id": "uzcw",                         # DLL: kbduzcw.dll
        "klc_name": "UzCW",
        "text": "New Uzbek (Latin) - C/W",
        "overrides": {
            "VK_OEM_3": (0, [TUTUQ, ord("~"), N, ord("`"), ord("`")]),
            # c w ; ,  -> ç ş ö ğ ; eski belgilar AltGr orqali
            "'C'": (CAPLOK | CAPLOKALTGR, [C_, C_C, 0x03, ord("c"), ord("C")]),
            "'W'": (CAPLOK | CAPLOKALTGR, [S_, S_C, 0x17, ord("w"), ord("W")]),
            "VK_OEM_1": (CAPLOK, [O_, O_C, N, ord(";"), ord(":")]),
            "VK_OEM_COMMA": (CAPLOK, [G_, G_C, N, ord(","), ord("<")]),
        },
    },
]

# ── Skan-kod -> VK (AQSh klaviaturasi, kbdus.c bilan bir xil) ──────────────
def scan_to_vk():
    t = {}
    t[0x01] = "VK_ESCAPE"
    for i, d in enumerate("1234567890"):
        t[0x02 + i] = "'%s'" % d
    t[0x0C], t[0x0D], t[0x0E], t[0x0F] = "VK_OEM_MINUS", "VK_OEM_PLUS", "VK_BACK", "VK_TAB"
    for i, L in enumerate("QWERTYUIOP"):
        t[0x10 + i] = "'%s'" % L
    t[0x1A], t[0x1B], t[0x1C], t[0x1D] = "VK_OEM_4", "VK_OEM_6", "VK_RETURN", "VK_LCONTROL"
    for i, L in enumerate("ASDFGHJKL"):
        t[0x1E + i] = "'%s'" % L
    t[0x27], t[0x28], t[0x29], t[0x2A], t[0x2B] = "VK_OEM_1", "VK_OEM_7", "VK_OEM_3", "VK_LSHIFT", "VK_OEM_5"
    for i, L in enumerate("ZXCVBNM"):
        t[0x2C + i] = "'%s'" % L
    t[0x33], t[0x34], t[0x35] = "VK_OEM_COMMA", "VK_OEM_PERIOD", "VK_OEM_2"
    t[0x36] = "VK_RSHIFT | KBDEXT"
    t[0x37] = "VK_MULTIPLY | KBDMULTIVK"
    t[0x38], t[0x39], t[0x3A] = "VK_LMENU", "VK_SPACE", "VK_CAPITAL"
    for i in range(10):
        t[0x3B + i] = "VK_F%d" % (i + 1)
    t[0x45] = "VK_NUMLOCK | KBDEXT | KBDMULTIVK"
    t[0x46] = "VK_SCROLL | KBDMULTIVK"
    np = "KBDNUMPAD | KBDSPECIAL"
    t[0x47], t[0x48], t[0x49] = "VK_HOME | " + np, "VK_UP | " + np, "VK_PRIOR | " + np
    t[0x4A] = "VK_SUBTRACT"
    t[0x4B], t[0x4C], t[0x4D] = "VK_LEFT | " + np, "VK_CLEAR | " + np, "VK_RIGHT | " + np
    t[0x4E] = "VK_ADD"
    t[0x4F], t[0x50], t[0x51] = "VK_END | " + np, "VK_DOWN | " + np, "VK_NEXT | " + np
    t[0x52], t[0x53] = "VK_INSERT | " + np, "VK_DELETE | " + np
    t[0x54] = "VK_SNAPSHOT"
    t[0x56], t[0x57], t[0x58], t[0x59] = "VK_OEM_102", "VK_F11", "VK_F12", "VK_CLEAR"
    for i in range(11):                       # T64..T6E  -> F13..F23
        t[0x64 + i] = "VK_F%d" % (13 + i)
    t[0x73] = "VK_ABNT_C1"
    t[0x76] = "VK_F24"
    t[0x7E] = "VK_ABNT_C2"
    return t


E0 = [  # (skan-kod, VK) — "extended" (E0 prefiksli) tugmalar
    (0x10, "VK_MEDIA_PREV_TRACK"), (0x19, "VK_MEDIA_NEXT_TRACK"), (0x1D, "VK_RCONTROL"),
    (0x20, "VK_VOLUME_MUTE"), (0x21, "VK_LAUNCH_APP2"), (0x22, "VK_MEDIA_PLAY_PAUSE"),
    (0x24, "VK_MEDIA_STOP"), (0x2E, "VK_VOLUME_DOWN"), (0x30, "VK_VOLUME_UP"),
    (0x32, "VK_BROWSER_HOME"), (0x35, "VK_DIVIDE"), (0x37, "VK_SNAPSHOT"), (0x38, "VK_RMENU"),
    (0x46, "VK_CANCEL"), (0x47, "VK_HOME"), (0x48, "VK_UP"), (0x49, "VK_PRIOR"),
    (0x4B, "VK_LEFT"), (0x4D, "VK_RIGHT"), (0x4F, "VK_END"), (0x50, "VK_DOWN"),
    (0x51, "VK_NEXT"), (0x52, "VK_INSERT"), (0x53, "VK_DELETE"), (0x5B, "VK_LWIN"),
    (0x5C, "VK_RWIN"), (0x5D, "VK_APPS"), (0x5F, "VK_SLEEP"), (0x65, "VK_BROWSER_SEARCH"),
    (0x66, "VK_BROWSER_FAVORITES"), (0x67, "VK_BROWSER_REFRESH"), (0x68, "VK_BROWSER_STOP"),
    (0x69, "VK_BROWSER_FORWARD"), (0x6A, "VK_BROWSER_BACK"), (0x6B, "VK_LAUNCH_APP1"),
    (0x6C, "VK_LAUNCH_MAIL"), (0x6D, "VK_LAUNCH_MEDIA_SELECT"), (0x1C, "VK_RETURN"),
]

KEY_NAMES = [
    (0x01, "Esc"), (0x0E, "Backspace"), (0x0F, "Tab"), (0x1C, "Enter"), (0x1D, "Ctrl"),
    (0x2A, "Shift"), (0x36, "Right Shift"), (0x37, "Num *"), (0x38, "Alt"), (0x39, "Space"),
    (0x3A, "Caps Lock"), (0x3B, "F1"), (0x3C, "F2"), (0x3D, "F3"), (0x3E, "F4"), (0x3F, "F5"),
    (0x40, "F6"), (0x41, "F7"), (0x42, "F8"), (0x43, "F9"), (0x44, "F10"), (0x45, "Pause"),
    (0x46, "Scroll Lock"), (0x47, "Num 7"), (0x48, "Num 8"), (0x49, "Num 9"), (0x4A, "Num -"),
    (0x4B, "Num 4"), (0x4C, "Num 5"), (0x4D, "Num 6"), (0x4E, "Num +"), (0x4F, "Num 1"),
    (0x50, "Num 2"), (0x51, "Num 3"), (0x52, "Num 0"), (0x53, "Num Del"), (0x54, "Sys Req"),
    (0x57, "F11"), (0x58, "F12"),
]
KEY_NAMES_EXT = [
    (0x1C, "Num Enter"), (0x1D, "Right Ctrl"), (0x35, "Num /"), (0x37, "Prnt Scrn"),
    (0x38, "Right Alt"), (0x45, "Num Lock"), (0x46, "Break"), (0x47, "Home"), (0x48, "Up"),
    (0x49, "Page Up"), (0x4B, "Left"), (0x4D, "Right"), (0x4F, "End"), (0x50, "Down"),
    (0x51, "Page Down"), (0x52, "Insert"), (0x53, "Delete"), (0x5B, "Left Windows"),
    (0x5C, "Right Windows"), (0x5D, "Application"),
]


def wch(v):
    return "WCH_NONE" if v is None else "0x%04X" % v


def build_table(layout):
    t = us_base()
    t.update(layout["overrides"])
    return t


def vk_order(table):
    """VK nomlarini barqaror tartibda qaytaradi (generatsiya deterministik bo'lsin)."""
    return sorted(table.keys(), key=lambda k: (k.startswith("'"), k))


def gen_c(layout):
    table = build_table(layout)
    out = []
    w = out.append
    w("/* AVTOMATIK YARATILGAN — tools/generate.py. Qo'lda tahrirlamang. */")
    w("/* Layout: %s */" % layout["text"])
    w('#include "kbd.h"')
    w("")
    w("static VK_TO_BIT aVkToBits[] = {")
    w("    { VK_SHIFT,   KBDSHIFT },")
    w("    { VK_CONTROL, KBDCTRL  },")
    w("    { VK_MENU,    KBDALT   },")
    w("    { 0, 0 }")
    w("};")
    w("")
    w("/* Ustunlar: 0 oddiy | 1 Shift | 2 Ctrl | 3 AltGr(Ctrl+Alt) | 4 Shift+AltGr */")
    w("static MODIFIERS CharModifiers = {")
    w("    &aVkToBits[0],")
    w("    7,")
    w("    {")
    w("        0,            /*                       */")
    w("        1,            /* Shift                 */")
    w("        2,            /* Ctrl                  */")
    w("        SHFT_INVALID, /* Shift+Ctrl            */")
    w("        SHFT_INVALID, /* Alt                   */")
    w("        SHFT_INVALID, /* Shift+Alt             */")
    w("        3,            /* Ctrl+Alt (AltGr)      */")
    w("        4             /* Shift+Ctrl+Alt        */")
    w("    }")
    w("};")
    w("")
    w("static VK_TO_WCHARS5 aVkToWch5[] = {")
    for vk in vk_order(table):
        attr, cols = table[vk]
        w("    { %-14s, 0x%02X, { %s } }," % (vk, attr, ", ".join(wch(c) for c in cols)))
    w("    { 0, 0, { 0, 0, 0, 0, 0 } }")
    w("};")
    w("")
    w("/* Numpad raqamlari (faqat 1 ustun) */")
    w("static VK_TO_WCHARS1 aVkToWch1[] = {")
    for i in range(10):
        w("    { VK_NUMPAD%d, 0, { '%d' } }," % (i, i))
    w("    { 0, 0, { 0 } }")
    w("};")
    w("")
    w("static VK_TO_WCHAR_TABLE aVkToWcharTable[] = {")
    w("    { (VK_TO_WCHARS1 *)aVkToWch5, 5, sizeof(aVkToWch5[0]) },")
    w("    { (VK_TO_WCHARS1 *)aVkToWch1, 1, sizeof(aVkToWch1[0]) },")
    w("    { NULL, 0, 0 }")
    w("};")
    w("")

    # skan-kod jadvallari
    s2v = scan_to_vk()
    w("static WORD ausVK[] = {")
    for sc in range(0x80):
        w("    /* %02X */ %s," % (sc, s2v.get(sc, "0")))
    w("};")
    w("")
    w("static VSC_VK aE0VscToVk[] = {")
    for sc, vk in E0:
        w("    { 0x%02X, %s | KBDEXT }," % (sc, vk))
    w("    { 0, 0 }")
    w("};")
    w("")
    w("static VSC_VK aE1VscToVk[] = {")
    w("    { 0x1D, VK_PAUSE | KBDEXT },")
    w("    { 0, 0 }")
    w("};")
    w("")

    def names(var, items):
        w("static VSC_LPWSTR %s[] = {" % var)
        for sc, text in items:
            w('    { 0x%02X, (WCHAR *)u"%s" },' % (sc, text))
        w("    { 0, NULL }")
        w("};")
        w("")

    names("aKeyNames", KEY_NAMES)
    names("aKeyNamesExt", KEY_NAMES_EXT)

    w("static KBDTABLES KbdTables = {")
    w("    &CharModifiers,")
    w("    aVkToWcharTable,")
    w("    NULL,                 /* o'lik tugmalar yo'q */")
    w("    aKeyNames,")
    w("    aKeyNamesExt,")
    w("    NULL,                 /* o'lik tugma nomlari yo'q */")
    w("    ausVK,")
    w("    sizeof(ausVK) / sizeof(ausVK[0]),")
    w("    aE0VscToVk,")
    w("    aE1VscToVk,")
    w("    MAKELONG(KLLF_ALTGR, KBD_VERSION),")
    w("    0, 0, NULL,           /* ligaturalar yo'q */")
    w("    0, 0")
    w("};")
    w("")
    w("KBD_EXPORT KBDTABLES *KbdLayerDescriptor(void)")
    w("{")
    w("    return &KbdTables;")
    w("}")
    w("")
    return "\n".join(out)


def gen_def(layout):
    return "LIBRARY KBD%s\nEXPORTS\n    KbdLayerDescriptor @1\n" % layout["id"].upper()


# ── MSKLC (.klc) ───────────────────────────────────────────────────────────
KLC_VKNAME = {"VK_OEM_MINUS": "OEM_MINUS", "VK_OEM_PLUS": "OEM_PLUS", "VK_OEM_4": "OEM_4",
              "VK_OEM_6": "OEM_6", "VK_OEM_5": "OEM_5", "VK_OEM_1": "OEM_1", "VK_OEM_7": "OEM_7",
              "VK_OEM_3": "OEM_3", "VK_OEM_COMMA": "OEM_COMMA", "VK_OEM_PERIOD": "OEM_PERIOD",
              "VK_OEM_2": "OEM_2", "VK_OEM_102": "OEM_102", "VK_SPACE": "SPACE",
              "VK_DECIMAL": "DECIMAL"}


def uni_name(cp):
    import unicodedata
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return "<control>"


def gen_klc(layout):
    table = build_table(layout)
    s2v = scan_to_vk()
    rows = []
    for sc in sorted(s2v):
        vk_expr = s2v[sc].split("|")[0].strip()
        if vk_expr not in table or vk_expr in ("VK_BACK", "VK_ESCAPE", "VK_RETURN", "VK_TAB", "VK_CANCEL",
                                                "VK_ADD", "VK_SUBTRACT", "VK_MULTIPLY", "VK_DIVIDE"):
            continue
        attr, cols = table[vk_expr]
        name = KLC_VKNAME.get(vk_expr, vk_expr.strip("'"))
        # shift-state ustunlari: 0, 1, 2, 6, 7  == col0, col1, col2, col3, col4
        cells = ["-1" if c is None else "%04x" % c for c in cols]
        cap = {0: "0", CAPLOK: "1", CAPLOKALTGR: "4", CAPLOK | CAPLOKALTGR: "5"}[attr]
        comment = ", ".join(uni_name(c) if c is not None else "<none>" for c in cols)
        rows.append("%02x\t%s\t\t%s\t%s\t\t//%s" % (sc, name, cap, "\t".join(cells), comment))
    # numpad o'nlik nuqta
    rows.append("53\tDECIMAL\t\t0\t002e\t002e\t-1\t-1\t-1\t\t//FULL STOP")

    lines = [
        'KBD\t%s\t"%s"' % (layout["klc_name"], layout["text"]),
        "",
        'COPYRIGHT\t"(c) 2026 uzbek-new-keyboard-layout (MIT)"',
        "",
        'COMPANY\t"uzbek-new-keyboard-layout"',
        "",
        'LOCALENAME\t"uz-Latn-UZ"',
        "",
        'LOCALEID\t"00000443"',
        "",
        "VERSION\t1.0",
        "",
        "SHIFTSTATE",
        "",
        "0\t//Column 4",
        "1\t//Column 5 : Shft",
        "2\t//Column 6 :       Ctrl",
        "6\t//Column 7 :       Ctrl Alt",
        "7\t//Column 8 : Shft  Ctrl Alt",
        "",
        "LAYOUT\t\t;an extra '@' at the end is a dead key",
        "",
        "//SC\tVK_\t\tCap\t0\t1\t2\t6\t7",
        "//--\t----\t\t----\t----\t----\t----\t----\t----",
        "",
    ] + rows + [
        "",
        "KEYNAME",
        "",
        "01\tEsc", "0e\tBackspace", "0f\tTab", "1c\tEnter", "1d\tCtrl", "2a\tShift",
        "36\tRight Shift", "37\tNum *", "38\tAlt", "39\tSpace", "3a\tCaps Lock",
        "",
        "KEYNAME_EXT",
        "",
        "1c\tNum Enter", "1d\tRight Ctrl", "35\tNum /", "37\tPrnt Scrn", "38\tRight Alt",
        "45\tNum Lock", "46\tBreak", "47\tHome", "48\tUp", "49\tPage Up", "4b\tLeft",
        "4d\tRight", "4f\tEnd", "50\tDown", "51\tPage Down", "52\tInsert", "53\tDelete",
        "",
        "DESCRIPTIONS",
        "",
        "0409\t%s" % layout["text"],
        "",
        "LANGUAGENAMES",
        "",
        "0409\tEnglish (United States)",
        "",
        "ENDKBD",
        "",
    ]
    return "\r\n".join(lines)


def main():
    os.makedirs(SRC, exist_ok=True)
    os.makedirs(KLC, exist_ok=True)
    for lay in LAYOUTS:
        base = "kbd" + lay["id"]
        with open(os.path.join(SRC, base + ".c"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(gen_c(lay))
        with open(os.path.join(SRC, base + ".def"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(gen_def(lay))
        with open(os.path.join(KLC, lay["id"] + ".klc"), "wb") as fh:   # MSKLC: UTF-16LE + BOM
            fh.write(b"\xff\xfe" + gen_klc(lay).encode("utf-16-le"))
        print("yaratildi:", base + ".c / .def,", lay["id"] + ".klc")


if __name__ == "__main__":
    sys.exit(main())
