# Umumiy o'rnatish (RPM, Arch, tar.gz uchun). deb alohida skript bilan yig'iladi.
#   make install                       # /usr ga (root kerak)
#   make install DESTDIR=/tmp/pkg      # paket yig'ish uchun
#   make uninstall
PREFIX  ?= /usr
DESTDIR ?=
# XKB fayllarini tizim faqat shu yerdan qidiradi (PREFIX=/usr/local bo'lsa ham)
XKBDIR  ?= /usr/share/X11/xkb
BINDIR   = $(DESTDIR)$(PREFIX)/bin
SHAREDIR = $(DESTDIR)$(PREFIX)/share
LIBDIR   = $(SHAREDIR)/uzbek-keyboard
DOCDIR   = $(SHAREDIR)/doc/uzbek-new-keyboard-layout

install:
	install -Dm0644 xkb/symbols/uzq              $(DESTDIR)$(XKBDIR)/symbols/uzq
	install -Dm0755 deb/uzbek-keyboard           $(BINDIR)/uzbek-keyboard
	printf '#!/bin/sh\nexec uzbek-keyboard gui "$$@"\n' > $(BINDIR)/uzbek-keyboard-gui
	chmod 0755 $(BINDIR)/uzbek-keyboard-gui
	install -Dm0644 lib/xkb_register.py          $(LIBDIR)/xkb_register.py
	install -Dm0755 uz-keyboard-gui.py           $(LIBDIR)/uz-keyboard-gui.py
	install -Dm0644 deb/uzbek-keyboard.desktop   $(SHAREDIR)/applications/uzbek-keyboard.desktop
	install -Dm0644 ../LICENSE                   $(DOCDIR)/LICENSE
	@if [ -z "$(DESTDIR)" ]; then $(BINDIR)/uzbek-keyboard register || true; \
	  echo; echo "Tayyor. Yoqish:  uzbek-keyboard enable basic|cw|all   (yoki: uzbek-keyboard gui)"; fi

uninstall:
	@if [ -z "$(DESTDIR)" ] && [ -x $(BINDIR)/uzbek-keyboard ]; then $(BINDIR)/uzbek-keyboard unregister || true; fi
	rm -f  $(DESTDIR)$(XKBDIR)/symbols/uzq $(BINDIR)/uzbek-keyboard $(BINDIR)/uzbek-keyboard-gui \
	       $(SHAREDIR)/applications/uzbek-keyboard.desktop
	rm -rf $(LIBDIR) $(DOCDIR)

.PHONY: install uninstall
