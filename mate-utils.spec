Summary:	MATE utility programs
Summary(pl.UTF-8):	Programy użytkowe dla środowiska MATE
Name:		mate-utils
Version:	1.28.0
Release:	1
License:	LGPL v2+ (libmatedict), GPL v2+ (programs), FDL (documentation)
Group:		X11/Applications/Multimedia
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	b5820b69d1c292712a7a45a933d9c2da
URL:		https://github.com/mate-desktop/mate-utils
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd45-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	gtk-doc >= 1.10
# wayland not finished yet (there are configure checks, but used minimal versions are not defined)
#BuildRequires:	gtk-layer-shell-devel
BuildRequires:	inkscape
BuildRequires:	libcanberra-gtk3-devel >= 0.4
BuildRequires:	libgtop-devel >= 1:2.12.0
# rsvg-convert
BuildRequires:	librsvg
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.27.1
BuildRequires:	mate-panel-devel >= 1.17.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	udisks2-devel >= 1.90.0
# wayland-client
#BuildRequires:	wayland-devel
BuildRequires:	xorg-lib-libICE-devel >= 1.0.0
BuildRequires:	xorg-lib-libSM-devel >= 1.0.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.50.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22
Requires:	hicolor-icon-theme
Requires:	libcanberra-gtk3 >= 0.4
Requires:	libgtop >= 1:2.12.0
Requires:	libmatedict = %{version}-%{release}
Requires:	mate-desktop >= 1.27.1
Requires:	mate-panel >= 1.17.0
Requires:	udisks2-libs >= 1.90.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# use the same libexecdir as mate-panel
# (better solution: store mate-panel libexecdir in libmatepanelapplet-*.pc and read it here)
%define		matepanel_libexecdir	%{_libexecdir}/mate-panel

%description
MATE utility programs.

%description -l pl.UTF-8
Programy użytkowe dla środowiska MATE.

%package -n libmatedict
Summary:	MATE Dictionary Protocol client library
Summary(pl.UTF-8):	Biblioteka kliencka protokołu słownika MATE
License:	LGPL v2+
Group:		X11/Libraries
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22

%description -n libmatedict
MATE Dictionary Protocol client library.

%description -n libmatedict -l pl.UTF-8
Biblioteka kliencka protokołu słownika MATE.

%package -n libmatedict-devel
Summary:	Header files for libmatedict library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmatedict
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	glib2-devel >= 1:2.50.0
Requires:	gtk+3 >= 3.22
Requires:	libmatedict = %{version}-%{release}

%description -n libmatedict-devel
Header files for libmatedict library.

%description -n libmatedict-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmatedict.

%package -n libmatedict-apidocs
Summary:	API documentation for libmatedict library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmatedict
Group:		Documentation
BuildArch:	noarch

%description -n libmatedict-apidocs
API documentation for libmatedict library.

%description -n libmatedict-apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmatedict.

%package -n mate-screenshot
Summary:	Screenshot utility
Summary(pl.UTF-8):	Narzędzie do robienia zrzutów ekranu
Group:		X11/Applications
Requires(post,postun):	glib2 >= 1:2.50.0
Requires:	glib2 >= 1:2.50.0
Conflicts:	mate-utils < 1.8.0-2.1

%description -n mate-screenshot
This utility allows to make a desktop screenshot.

%description -n mate-screenshot -l pl.UTF-8
To narzędzie pozwala na zrobienie zrzutu ekranu biurka.

%prep
%setup -q

%build
%configure \
	--libexecdir=%{matepanel_libexecdir} \
	--enable-gtk-doc \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmatedict.la

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,pms}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/help/{es_ES,frp,ie,jv,ku_IQ,zh-Hans}

# mate-utils gettext domain, mate-{dictionary,disk-usage,analyzer,search-tool,system-log} mate dirs
%find_lang %{name} --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%post	-n libmatedict -p /sbin/ldconfig
%postun	-n libmatedict -p /sbin/ldconfig

%post	-n mate-screenshot
%update_desktop_database
%glib_compile_schemas

%postun	-n mate-screenshot
%update_desktop_database
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_bindir}/mate-dictionary
%attr(755,root,root) %{_bindir}/mate-disk-image-mounter
%attr(755,root,root) %{_bindir}/mate-disk-usage-analyzer
%attr(755,root,root) %{_bindir}/mate-search-tool
%attr(755,root,root) %{_bindir}/mate-system-log
%attr(755,root,root) %{matepanel_libexecdir}/mate-dictionary-applet
%{_datadir}/metainfo/mate-dictionary.appdata.xml
%{_datadir}/metainfo/mate-disk-usage-analyzer.appdata.xml
%{_datadir}/metainfo/mate-search-tool.appdata.xml
%{_datadir}/dbus-1/services/org.mate.panel.applet.DictionaryAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.dictionary.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.disk-usage-analyzer.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.search-tool.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.system-log.gschema.xml
%{_datadir}/mate-dict
%{_datadir}/mate-dictionary
%{_datadir}/mate-panel/applets/org.mate.DictionaryApplet.mate-panel-applet
%{_desktopdir}/mate-dictionary.desktop
%{_desktopdir}/mate-disk-image-mounter.desktop
%{_desktopdir}/mate-disk-usage-analyzer.desktop
%{_desktopdir}/mate-search-tool.desktop
%{_desktopdir}/mate-system-log.desktop
%{_iconsdir}/hicolor/*/apps/mate-disk-usage-analyzer.*
%{_iconsdir}/hicolor/*/apps/mate-system-log.png
%{_iconsdir}/hicolor/scalable/apps/mate-system-log-symbolic.svg
%{_pixmapsdir}/mate-search-tool
%{_mandir}/man1/mate-dictionary.1*
%{_mandir}/man1/mate-disk-usage-analyzer.1*
%{_mandir}/man1/mate-search-tool.1*
%{_mandir}/man1/mate-system-log.1*

%files -n libmatedict
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatedict.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmatedict.so.6

%files -n libmatedict-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatedict.so
%{_includedir}/mate-dict
%{_pkgconfigdir}/mate-dict.pc

%files -n libmatedict-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-dict

%files -n mate-screenshot
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mate-panel-screenshot
%attr(755,root,root) %{_bindir}/mate-screenshot
%{_datadir}/metainfo/mate-screenshot.appdata.xml
%{_datadir}/glib-2.0/schemas/org.mate.screenshot.gschema.xml
%{_desktopdir}/mate-screenshot.desktop
%{_mandir}/man1/mate-panel-screenshot.1*
%{_mandir}/man1/mate-screenshot.1*
