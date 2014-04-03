Summary:	MATE utility programs
Summary(pl.UTF-8):	Programy użytkowe dla środowiska MATE
Name:		mate-utils
Version:	1.8.0
Release:	2.1
License:	LGPL v2+ (libmatedict), GPL v2+ (programs), FDL (documentation)
Group:		X11/Applications/Multimedia
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	7961435ec1b5210e886c5a223b67d02a
URL:		https://github.com/mate-desktop/mate-utils
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-gtk-devel >= 0.4
BuildRequires:	libgtop-devel >= 1:2.12.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	mate-panel-devel >= 1.5.0
BuildRequires:	rarian-compat
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.26.0
Requires:	gtk+2 >= 2:2.20.0
Requires:	hicolor-icon-theme
Requires:	libcanberra-gtk >= 0.4
Requires:	libmatedict = %{version}-%{release}
Requires:	mate-panel >= 1.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/mate-panel

%description
MATE utility programs.

%description -l pl.UTF-8
Programy użytkowe dla środowiska MATE.

%package -n libmatedict
Summary:	MATE Dictionary Protocol client library
Summary(pl.UTF-8):	Biblioteka kliencka protokołu słownika MATE
License:	LGPL v2+
Group:		X11/Libraries
Requires:	glib2 >= 1:2.20.0
Requires:	gtk+2 >= 2:2.20.0

%description -n libmatedict
MATE Dictionary Protocol client library.

%description -n libmatedict -l pl.UTF-8
Biblioteka kliencka protokołu słownika MATE.

%package -n libmatedict-devel
Summary:	Header files for libmatedict library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmatedict
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	glib2-devel >= 1:2.20.0
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	libmatedict = %{version}-%{release}

%description -n libmatedict-devel
Header files for libmatedict library.

%description -n libmatedict-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmatedict.

%package -n libmatedict-apidocs
Summary:	API documentation for libmatedict library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmatedict
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n libmatedict-apidocs
API documentation for libmatedict library.

%description -n libmatedict-apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmatedict.

%package -n mate-screenshot
Summary:	Screenshot utility
Summary(pl.UTF-8):	Narzędzie do robienia zrzutów ekranu
Group:		X11/Applications
Requires(post,postun):	glib2 >= 1:2.26.0
Requires:	glib2 >= 1:2.36.0
Conflicts:	mate-utils < 1.8.0-2.1

%description -n mate-screenshot
Allows to make a desktop screenshot.

%description -n mate-screenshot -l pl.UTF-8
Pozwala na zrobienie zrzutu ekranu biurka.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

# this package uses shave, not AM_SILENT_RULES, thus only V=1 works
%{__make} -j1 \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmatedict.la

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/cmn

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-*.convert

# mate-utils gettext domain, mate-{dictionary,disk-usage,analyzer,search-tool,system-log} mate,omf dirs
%find_lang %{name} --with-mate --with-omf --all-name

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-dictionary
%attr(755,root,root) %{_bindir}/mate-disk-usage-analyzer
%attr(755,root,root) %{_bindir}/mate-search-tool
%attr(755,root,root) %{_bindir}/mate-system-log
%attr(755,root,root) %{_libexecdir}/mate-dictionary-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.DictionaryAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.dictionary.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.disk-usage-analyzer.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.search-tool.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.system-log.gschema.xml
%{_datadir}/mate-dict
%{_datadir}/mate-dictionary
%{_datadir}/mate-disk-usage-analyzer
%{_datadir}/mate-panel/applets/org.mate.DictionaryApplet.mate-panel-applet
%{_datadir}/mate-utils
%{_desktopdir}/mate-dictionary.desktop
%{_desktopdir}/mate-disk-usage-analyzer.desktop
%{_desktopdir}/mate-search-tool.desktop
%{_desktopdir}/mate-system-log.desktop
%{_iconsdir}/hicolor/*/apps/mate-disk-usage-analyzer.*
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
%{_datadir}/glib-2.0/schemas/org.mate.screenshot.gschema.xml
%{_datadir}/mate-screenshot
%{_desktopdir}/mate-screenshot.desktop
%{_mandir}/man1/mate-screenshot.1*
