Summary:	Document viewer for multiple document formats
Name:		mate-document-viewer
Version:	1.6.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	8805ad4b0818681c5871d36bb77f8a74
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	djvulibre-devel
BuildRequires:	ghostscript
BuildRequires:	mate-doc-utils
BuildRequires:	mate-icon-theme-devel
BuildRequires:	intltool
BuildRequires:	libspectre-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxslt-progs
BuildRequires:	mate-file-manager-devel
BuildRequires:	pkg-config
BuildRequires:	poppler-glib-devel
BuildRequires:	python-libxml2
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires:	xdg-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/atril

%description
Atril is a document viewer for multiple document formats like pdf,
postscript, and many others.

%package libs
Summary:	Atril libraries
Group:		Libraries

%description libs
Atril libraries.

%package devel
Summary:	Header files for Atril libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Atril libraries.

%package -n mate-file-manager-extension-document-viewer
Summary:	Atril extension for Nautilus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-file-manager

%description -n mate-file-manager-extension-document-viewer
Shows Atril document properties in Caja file manager.

%package apidocs
Summary:	Evince API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Evince API documentation.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gtkdocize}
%{__gnome_doc_prepare}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-comics		\
	--disable-schemas-compile 	\
	--disable-scrollkeeper		\
	--disable-static		\
	--enable-dbus			\
	--enable-dvi			\
	--enable-impress		\
	--enable-pixbuf			\
	--enable-tiff			\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/atril/?/backends/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ks,ps}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la

%find_lang atril --with-omf --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f atril.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO

%dir %{_libexecdir}
%dir %{_libexecdir}/?
%dir %{_libexecdir}/?/backends

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/atril/?/backends/*.so
%attr(755,root,root) %{_libexecdir}/atril-convert-metadata
%{_libexecdir}/?/backends/*.atril-backend
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/mate-document-viewer
%{_datadir}/thumbnailers/atril.thumbnailer
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/*/*.*

%{_mandir}/man1/atril-previewer.1*
%{_mandir}/man1/atril-thumbnailer.1*

%attr(755,root,root) %{_libdir}/atril/atrild
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_mandir}/man1/atril.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libat*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libat*.so.?

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libatril*.so
%{_includedir}/atril
%{_pkgconfigdir}/*.pc

%files -n mate-file-manager-extension-document-viewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/*.so*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*

