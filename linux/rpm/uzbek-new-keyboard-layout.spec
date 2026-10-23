Name:           uzbek-new-keyboard-layout
Version:        %{?pkgver}%{!?pkgver:2.0.0}
Release:        1%{?dist}
Summary:        New Uzbek (Latin) keyboard layouts (Ö Ğ Ş Ç ʼ)
License:        MIT
URL:            https://github.com/uzbek-coder-2022/uzbek-new-keyboard-layout
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3
Requires:       xkeyboard-config
Recommends:     python3-gobject
Recommends:     gtk3
Recommends:     xorg-x11-xkb-utils

%description
Two XKB layout variants for the new Uzbek Latin alphabet:
"basic" (Q layout: [ ] ; ' -> ö ğ ş ç) and "cw" (c w ; , -> ç ş ö ğ).
Old characters stay available via AltGr. Enable the variants you want with
"uzbek-keyboard enable basic|cw|all" or the "uzbek-keyboard gui" window.

%prep
%setup -q

%build
# nothing to build

%install
make -C linux install DESTDIR=%{buildroot} PREFIX=/usr
rm -rf %{buildroot}%{_docdir}/uzbek-new-keyboard-layout

%post
/usr/bin/uzbek-keyboard register >/dev/null 2>&1 || :
echo "Uzbek keyboard: layoutni yoqish uchun ishga tushiring:  uzbek-keyboard enable basic|cw|all   (yoki: uzbek-keyboard gui)"

%preun
if [ "$1" -eq 0 ]; then
    /usr/bin/uzbek-keyboard unregister >/dev/null 2>&1 || :
fi

# xkeyboard-config yangilanganda nomlarni qayta yozish
%transfiletriggerin -- /usr/share/X11/xkb/rules
/usr/bin/uzbek-keyboard register >/dev/null 2>&1 || :

%files
%license LICENSE
%{_bindir}/uzbek-keyboard
%{_bindir}/uzbek-keyboard-gui
%{_datadir}/X11/xkb/symbols/uzq
%{_datadir}/uzbek-keyboard/
%{_datadir}/applications/uzbek-keyboard.desktop

%changelog
* Fri Oct 23 2026 Uzbek keyboard layout <noreply@example.com> - 2.0.0-1
- Initial RPM: basic and cw variants, uzbek-keyboard CLI and GTK window
