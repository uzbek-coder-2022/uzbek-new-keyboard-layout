#!/usr/bin/env python3
"""
Yig'ilgan layout DLL'larining BINAR faylini o'qib (PE -> KBDTABLES), Windows'ning
tugma->belgi tarjimasini simulyatsiya qiladi va natijani kutilgan qiymatlar bilan
solishtiradi. Windows'ning o'zida sinashdan oldingi eng yaxshi avtomatik tekshiruv.

    python3 tools/verify.py            # bin/x64 va bin/x86 dagi hamma DLL'lar
"""
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VK = {"LCONTROL": 0xA2, "RCONTROL": 0xA3, "LMENU": 0xA4, "RMENU": 0xA5, "LSHIFT": 0xA0,
      "RSHIFT": 0xA1, "UP": 0x26, "LWIN": 0x5B, "PAUSE": 0x13, "OEM_3": 0xC0}
KBDEXT = 0x0100
SHIFT, CTRL, ALT = 1, 2, 4
ALTGR = CTRL | ALT
CAPLOK, CAPLOKALTGR = 1, 4
NONE = 0xF000


class Image:
    def __init__(self, path):
        d = open(path, "rb").read()
        self.data = d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        assert d[pe:pe + 4] == b"PE\0\0", "PE imzosi yo'q"
        machine, nsec, _, _, _, optsz, _ = struct.unpack_from("<HHIIIHH", d, pe + 4)
        opt = pe + 24
        magic = struct.unpack_from("<H", d, opt)[0]
        self.is64 = magic == 0x20B
        self.ptr = 8 if self.is64 else 4
        if self.is64:
            self.base = struct.unpack_from("<Q", d, opt + 24)[0]
            dd = opt + 112
        else:
            self.base = struct.unpack_from("<I", d, opt + 28)[0]
            dd = opt + 96
        self.subsystem = struct.unpack_from("<H", d, opt + 68)[0]
        self.checksum = struct.unpack_from("<I", d, opt + 64)[0]
        self.sections = []
        sec = opt + optsz
        for i in range(nsec):
            name, vsz, va, rsz, raw = struct.unpack_from("<8sIIII", d, sec + 40 * i)
            self.sections.append((va, max(vsz, rsz), raw, rsz))
        exp_rva, _ = struct.unpack_from("<II", d, dd)
        self.exports = self._exports(exp_rva)
        eo = self.rva2off(exp_rva)
        funcs_rva = struct.unpack_from("<I", d, eo + 28)[0]
        self.first_export_rva = struct.unpack_from("<I", d, self.rva2off(funcs_rva))[0]

    def rva2off(self, rva):
        for va, size, raw, rsz in self.sections:
            if va <= rva < va + size:
                return raw + rva - va
        raise ValueError("RVA %x topilmadi" % rva)

    def _exports(self, rva):
        o = self.rva2off(rva)
        nnames, _, names_rva = struct.unpack_from("<III", self.data, o + 24)
        names = []
        n_off = self.rva2off(names_rva)
        for i in range(nnames):
            nrva = struct.unpack_from("<I", self.data, n_off + 4 * i)[0]
            s = self.rva2off(nrva)
            names.append(self.data[s:self.data.index(b"\0", s)].decode())
        return names

    def va2off(self, va):
        return self.rva2off(va - self.base)

    def u(self, fmt, va):
        return struct.unpack_from("<" + fmt, self.data, self.va2off(va))

    def ptr_at(self, va):
        return self.u("Q" if self.is64 else "I", va)[0]


def load_tables(img):
    """KbdLayerDescriptor() kodidan KBDTABLES manzilini o'qiydi."""
    fn_off = img.rva2off(img.first_export_rva)
    code = img.data[fn_off:fn_off + 16]
    if img.is64:                      # lea rax,[rip+rel32] ; ret
        assert code[:3] == b"\x48\x8d\x05", "kutilmagan x64 kod: %s" % code.hex()
        rel = struct.unpack_from("<i", code, 3)[0]
        return img.base + img.first_export_rva + 7 + rel
    assert code[0] == 0xB8, "kutilmagan x86 kod: %s" % code.hex()   # mov eax, imm32 ; ret
    return struct.unpack_from("<I", code, 1)[0]


class Layout:
    def __init__(self, path):
        self.img = img = Image(path)
        p = img.ptr
        kt = load_tables(img)
        a = lambda n: kt + n * p  # noqa: E731
        self.pmod = img.ptr_at(a(0))
        self.pvk2w = img.ptr_at(a(1))
        self.pdead = img.ptr_at(a(2))
        self.pvsc = img.ptr_at(a(6))
        off = 7 * p
        self.maxvsc = img.u("B", kt + off)[0]
        off = (off + 1 + p - 1) // p * p
        self.pe0 = img.ptr_at(kt + off)
        self.pe1 = img.ptr_at(kt + off + p)
        self.flags = img.u("I", kt + off + 2 * p)[0]
        # CharModifiers
        self.maxmod = img.u("H", self.pmod + p)[0]
        self.modnum = list(img.u("%dB" % (self.maxmod + 1), self.pmod + p + 2))
        # jadvallar
        self.tables = []
        t = self.pvk2w
        while True:
            ptr = img.ptr_at(t)
            nmod, cb = img.u("BB", t + p)
            if ptr == 0:
                break
            self.tables.append((ptr, nmod, cb))
            t += 2 * p
        self.vk2w = {}
        for ptr, nmod, cb in self.tables:
            q = ptr
            while True:
                vk, attr = img.u("BB", q)
                if vk == 0 and attr == 0:
                    break
                chars = img.u("%dH" % nmod, q + 2)
                self.vk2w[vk] = (attr, chars)
                q += cb

    def vk_of(self, sc, e0=False):
        img = self.img
        if not e0:
            return img.u("H", self.pvsc + 2 * sc)[0]
        q = self.pe0
        while True:
            s, v = img.u("B", q)[0], img.u("H", q + 2)[0]
            if s == 0 and v == 0:
                return None
            if s == sc:
                return v
            q += 4

    def vk_e1(self, sc):
        q = self.pe1
        while True:
            s, v = self.img.u("B", q)[0], self.img.u("H", q + 2)[0]
            if s == 0 and v == 0:
                return None
            if s == sc:
                return v
            q += 4

    def char(self, sc, mods=0, caps=False):
        vk = self.vk_of(sc) & 0xFF
        if vk not in self.vk2w:
            return None
        attr, chars = self.vk2w[vk]
        bits = mods
        if caps:
            if attr & CAPLOK and bits in (0, SHIFT):
                bits ^= SHIFT
            elif attr & CAPLOKALTGR and bits in (ALTGR, ALTGR | SHIFT):
                bits ^= SHIFT
        n = self.modnum[bits]
        if n == 0x0F or n >= len(chars):
            return None
        c = chars[n]
        return None if c == NONE else chr(c)


US_ROWS = [
    (0x02, "1234567890-=", "!@#$%^&*()_+"),
    (0x10, "qwertyuiop[]", "QWERTYUIOP{}"),
    (0x1E, "asdfghjkl;'`", 'ASDFGHJKL:"~'),
    (0x2B, "\\zxcvbnm,./", "|ZXCVBNM<>?"),
]

OVERRIDES = {
    "kbduzq.dll": {  # sc: (base, shift, altgr, shift+altgr)
        0x1A: ("ö", "Ö", "[", "{"), 0x1B: ("ğ", "Ğ", "]", "}"),
        0x27: ("ş", "Ş", ";", ":"), 0x28: ("ç", "Ç", "'", '"'),
        0x29: ("ʼ", "~", "`", "`"),
    },
    "kbduzcw.dll": {
        0x2E: ("ç", "Ç", "c", "C"), 0x11: ("ş", "Ş", "w", "W"),
        0x27: ("ö", "Ö", ";", ":"), 0x33: ("ğ", "Ğ", ",", "<"),
        0x29: ("ʼ", "~", "`", "`"),
    },
}


def check(path):
    name = os.path.basename(path)
    L = Layout(path)
    fails = []

    def eq(what, got, exp):
        if got != exp:
            fails.append("%s: kutilgan %r, chiqdi %r" % (what, exp, got))

    img = L.img
    eq("eksport", img.exports, ["KbdLayerDescriptor"])
    eq("subsystem native", img.subsystem, 1)
    eq("ALTGR bayrog'i", L.flags & 1, 1)
    eq("maxVSCtoVK", L.maxvsc, 0x80)

    # 1) Asosiy qator — AQSh QWERTY + layout o'zgarishlari
    ov = OVERRIDES[name]
    for start, low, up in US_ROWS:
        for i, (lo, hi) in enumerate(zip(low, up)):
            sc = start + i
            exp = ov.get(sc, (lo, hi, None, None))
            tag = "%s sc=%02X" % (name, sc)
            eq(tag + " oddiy", L.char(sc), exp[0])
            eq(tag + " shift", L.char(sc, SHIFT), exp[1])
            if sc in ov:
                eq(tag + " altgr", L.char(sc, ALTGR), exp[2])
                eq(tag + " shift+altgr", L.char(sc, ALTGR | SHIFT), exp[3])
            else:
                eq(tag + " altgr yo'q", L.char(sc, ALTGR), None)

    # 2) CapsLock
    for sc, (lo, hi, ag, sag) in ov.items():
        if lo.isalpha() and sc != 0x29:   # 0x29 = tutuq (ʼ): CapsLock ta'sir qilmaydi
            eq("%s caps sc=%02X" % (name, sc), L.char(sc, 0, True), hi)
            eq("%s caps+shift sc=%02X" % (name, sc), L.char(sc, SHIFT, True), lo)
    if name == "kbduzcw.dll":
        eq("caps+AltGr c", L.char(0x2E, ALTGR, True), "C")
    eq("caps tutuq", L.char(0x29, 0, True), "ʼ")
    eq("caps ;", L.char(0x27, 0, True), "Ö" if name == "kbduzcw.dll" else "Ş")

    # 3) Ctrl kodlari (terminal/Ctrl+C va h.k.)
    eq("Ctrl+C", L.char(0x2E, CTRL), "\x03")
    eq("Ctrl+W", L.char(0x11, CTRL), "\x17")
    eq("Ctrl+A", L.char(0x1E, CTRL), "\x01")
    if name == "kbduzq.dll":
        eq("Ctrl+[ (Esc)", L.char(0x1A, CTRL), "\x1b")
        eq("Ctrl+] ", L.char(0x1B, CTRL), "\x1d")

    # 4) Maxsus tugmalar
    eq("space", L.char(0x39), " ")
    eq("enter", L.char(0x1C), "\r")
    eq("tab", L.char(0x0F), "\t")
    eq("numpad 7 vk", L.vk_of(0x47) & 0xFF, 0x24)
    eq("VK LCtrl", L.vk_of(0x1D), VK["LCONTROL"])
    eq("VK LAlt", L.vk_of(0x38), VK["LMENU"])
    eq("VK LShift", L.vk_of(0x2A), VK["LSHIFT"])
    eq("VK RShift", L.vk_of(0x36), VK["RSHIFT"] & 0xFF | KBDEXT)
    eq("E0 RCtrl", L.vk_of(0x1D, True) & 0xFF, VK["RCONTROL"])
    eq("E0 RAlt (AltGr)", L.vk_of(0x38, True) & 0xFF, VK["RMENU"])
    eq("E0 Up", L.vk_of(0x48, True) & 0xFF, VK["UP"])
    eq("E0 LWin", L.vk_of(0x5B, True) & 0xFF, VK["LWIN"])
    eq("E1 Pause", (L.vk_e1(0x1D) or 0) & 0xFF, VK["PAUSE"])

    return fails


def main():
    paths = sys.argv[1:] or [os.path.join(ROOT, "bin", a, n)
                             for a in ("x64", "x86") for n in ("kbduzq.dll", "kbduzcw.dll")]
    bad = 0
    for p in paths:
        try:
            fails = check(p)
        except Exception as exc:  # noqa: BLE001
            fails = ["ISTISNO: %r" % exc]
        rel = os.path.relpath(p, ROOT)
        if fails:
            bad += 1
            print("XATO  %s" % rel)
            for f in fails[:12]:
                print("      -", f)
        else:
            print("OK    %s" % rel)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
