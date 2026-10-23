#!/usr/bin/env python3
"""
O'zbek klaviatura layouti — o'rnatish / o'chirish oynasi (Linux, GTK3).

Ishga tushirish:   python3 uz-keyboard-gui.py

Oyna install.sh / uninstall.sh / register-name.sh skriptlarini chaqiradi.
Root huquqi kerak bo'lganda pkexec parol so'rash oynasini o'zi ochadi.
Ubuntu Desktop'da python3-gi va GTK3 odatda allaqachon o'rnatilgan bo'ladi.
"""

import os
import re
import shutil
import subprocess
import sys
import threading

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
AUTOSTART = os.path.expanduser("~/.config/autostart/uz-keyboard.desktop")
# .deb paketi o'rnatilgan bo'lsa — root so'ramaydigan tizim buyrug'idan foydalanamiz
SYSTEM_CLI = shutil.which("uzbek-keyboard") if not os.path.exists(os.path.join(HERE, "install.sh")) else None

LAYOUTS = [
    {
        "id": "basic",
        "title": "New Uzbek (Latin) — Q joylashuvi",
        "keys": "[ → ö    ] → ğ    ; → ş    ' → ç    ` → ʼ",
    },
    {
        "id": "cw",
        "title": "New Uzbek (Latin) — C/W joylashuvi",
        "keys": "c → ç    w → ş    ; → ö    , → ğ    ` → ʼ",
    },
]


def gsettings_sources():
    try:
        out = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.input-sources", "sources"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def is_installed(variant):
    src = gsettings_sources()
    if src is not None:
        return ("uzq+%s" % variant) in src
    try:
        with open(AUTOSTART, encoding="utf-8") as fh:
            return ("uzq(%s)" % variant) in fh.read()
    except OSError:
        return False


class App(Gtk.Window):
    def __init__(self):
        super().__init__(title="O'zbek klaviatura layouti")
        self.set_default_size(640, 520)
        self.set_border_width(14)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(root)

        head = Gtk.Label()
        head.set_markup(
            "<span size='x-large' weight='bold'>Yangi o'zbek lotin klaviaturasi</span>\n"
            "Ö  Ğ  Ş  Ç  ʼ  harflari uchun layout o'rnatish"
        )
        head.set_xalign(0)
        root.pack_start(head, False, False, 0)

        self.rows = {}
        for lay in LAYOUTS:
            root.pack_start(self._make_row(lay), False, False, 0)

        self.pretty = Gtk.CheckButton(
            label="GNOME Settings'da chiroyli nom ko'rsatish (register-name.sh)"
        )
        self.pretty.set_active(True)
        if SYSTEM_CLI:                      # paket nomlarni o'zi ro'yxatdan o'tkazgan
            self.pretty.set_active(False)
            self.pretty.set_no_show_all(True)
        root.pack_start(self.pretty, False, False, 4)

        self.log = Gtk.TextView(editable=False, monospace=True)
        self.log.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.log)
        root.pack_start(scroll, True, True, 0)

        self.refresh()

    # ── UI qismlari ──────────────────────────────────────────────────────
    def _make_row(self, lay):
        frame = Gtk.Frame()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_border_width(10)
        frame.add(box)

        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        title = Gtk.Label()
        title.set_markup("<b>%s</b>" % GLib.markup_escape_text(lay["title"]))
        title.set_xalign(0)
        keys = Gtk.Label(label=lay["keys"])
        keys.set_xalign(0)
        status = Gtk.Label()
        status.set_xalign(0)
        for w in (title, keys, status):
            text.pack_start(w, False, False, 0)
        box.pack_start(text, True, True, 0)

        b_inst = Gtk.Button(label="O'rnatish")
        b_inst.connect("clicked", lambda _b, v=lay["id"]: self.run_install(v))
        b_rem = Gtk.Button(label="O'chirish")
        b_rem.connect("clicked", lambda _b, v=lay["id"]: self.run_uninstall(v))
        box.pack_end(b_rem, False, False, 0)
        box.pack_end(b_inst, False, False, 0)

        self.rows[lay["id"]] = (status, b_inst, b_rem)
        return frame

    def refresh(self):
        for vid, (status, b_inst, b_rem) in self.rows.items():
            ok = is_installed(vid)
            status.set_markup(
                "<span foreground='#2e7d32'>● o'rnatilgan</span>" if ok
                else "<span foreground='#888888'>○ o'rnatilmagan</span>"
            )
            b_inst.set_sensitive(not ok)
            b_rem.set_sensitive(ok)

    def append(self, text):
        buf = self.log.get_buffer()
        buf.insert(buf.get_end_iter(), text)
        mark = buf.create_mark(None, buf.get_end_iter(), False)
        self.log.scroll_to_mark(mark, 0, False, 0, 0)

    def set_busy(self, busy):
        for _s, b1, b2 in self.rows.values():
            b1.set_sensitive(not busy)
            b2.set_sensitive(not busy)
        if not busy:
            self.refresh()

    # ── Amallar ───────────────────────────────────────────────────────────
    def run_install(self, variant):
        if SYSTEM_CLI:
            return self.run([[SYSTEM_CLI, "enable", variant]])
        cmds = [[os.path.join(HERE, "install.sh"), variant]]
        if self.pretty.get_active():
            cmds.append([os.path.join(HERE, "register-name.sh")])
        self.run(cmds)

    def run_uninstall(self, variant):
        if SYSTEM_CLI:
            return self.run([[SYSTEM_CLI, "disable", variant]])
        self.run([[os.path.join(HERE, "uninstall.sh"), variant]])

    def run(self, cmds):
        self.set_busy(True)
        threading.Thread(target=self._worker, args=(cmds,), daemon=True).start()

    def _worker(self, cmds):
        for cmd in cmds:
            GLib.idle_add(self.append, "$ %s\n" % " ".join(os.path.basename(c) if i == 0 else c
                                                           for i, c in enumerate(cmd)))
            try:
                proc = subprocess.Popen(
                    cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True,
                )
                for line in proc.stdout:
                    GLib.idle_add(self.append, line)
                code = proc.wait()
            except OSError as exc:
                GLib.idle_add(self.append, "Xato: %s\n" % exc)
                break
            if code != 0:
                GLib.idle_add(self.append, "[!] Buyruq xato bilan tugadi (kod %d)\n\n" % code)
                break
            GLib.idle_add(self.append, "\n")
        GLib.idle_add(self.set_busy, False)


def main():
    if not re.search(r"\S", os.environ.get("DISPLAY", "") + os.environ.get("WAYLAND_DISPLAY", "")):
        print("Grafik muhit topilmadi. Terminal uchun ./install.sh dan foydalaning.")
        return 1
    win = App()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
