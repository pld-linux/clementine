# TODO:
# - Gstreamer error: "A text/uri-list decoder plugin is required to play this stream, but not installed."
# -- Building engines: gst
# -- Skipping engines: vlc xine qt-phonon
#    The following engines are NOT supported by clementine developers:
#     vlc xine qt-phonon
# - apply patches to libprojectM.spec and use
# - make engines pluggable not statically linked, then could enable the bconds
#
# Conditional build:
%bcond_with		engine_xine		# without xine engine
%bcond_with		engine_vlc		# without vlc engine
%bcond_with		engine_qt_phonon	# without qt-phonon engine
%bcond_without	engine_gstreamer	# without gstreamer engine
%bcond_without	static_sqlite	# with static sqlite3
%bcond_with		static_projectm	# with static projectM

%define		qtver	4.5
Summary:	A music player and library organiser
Summary(hu.UTF-8):	Egy zenelejátszó és gyűjtemény-kezelő
Name:		clementine
Version:	0.6
Release:	0.1
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://www.clementine-player.org/
Source0:	http://clementine-player.googlecode.com/files/%{name}-%{version}rc1.tar.gz
# Source0-md5:	cbe2b70a8df53b19e5d881a674708c5d
Patch0:		desktop-install.patch
Patch1:		unbundle-po.patch
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtDBus-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtIOCompressor-devel
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtOpenGL-devel >= %{qtver}
BuildRequires:	QtSingleApplication-devel >= 2.6-4
BuildRequires:	QtSql-devel >= %{qtver}
%{?with_tests:BuildRequires:	QtTest-devel >= %{qtver}}
BuildRequires:	QtXml-devel >= %{qtver}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
#BuildRequires:	desktop-file-utils
#%{?with_static_projectm:BuildRequires:	ftgl-devel >= 2.1.3}
BuildRequires:	gettext-devel
%{?with_static_projectm:BuildRequires:	glew-devel}
BuildRequires:	glib2-devel
%{?with_engine_gstreamer:BuildRequires:	gstreamer-devel >= 0.10}
%{?with_engine_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 0.10}
BuildRequires:	gtest-devel
BuildRequires:	libgpod-devel >= 0.7.92
BuildRequires:	libimobiledevice-devel
BuildRequires:	liblastfm-devel
BuildRequires:	libmtp-devel
BuildRequires:	libnotify-devel
BuildRequires:	libplist-devel
%{!?with_static_projectm:BuildRequires:	libprojectM-devel >= 1:2.0.1-4}
BuildRequires:	libqxt-devel
#BuildRequires:	libqxt-devel >= 0.6.0-0.2
BuildRequires:	libxml2-devel
BuildRequires:	notification-daemon
BuildRequires:	phonon
%{?with_engine_phonon:BuildRequires:	phonon-devel}
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(find_lang) = 1.33
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
%{!?with_static_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	usbmuxd-devel
%{?with_engine_vlc:BuildRequires:	vlc-devel}
%{?with_engine_xine:BuildRequires:	xine-lib-devel}
Requires(post,postun):	desktop-file-utils
Requires:	QtSingleApplication >= 2.6-4
%{!?with_static_sqlite:Requires:	QtSql-sqlite3 >= %{qtver}}
# while we do not link (yet), we use datafiles
Requires:	libprojectM
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# see libprojectM.spec for explanation
%define		filterout_ld	-Wl,--as-needed -Wl,--no-copy-dt-needed-entries

%description
Clementine is a modern music player and library organiser. It is
largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%description -l hu.UTF-8
Clementine egy modern zenelejátszó és gyűjtemény kezelő. Túlnyomórészt
az Amarok 1.4 port-ja, néhány funkciója újraírva, hogy kihasználhassa
a Qt4 előnyeit.

%prep
%setup -q -n clementine-0.5.90
%patch0 -p1
%patch1 -p1

# We already don't use these but just to make sure
rm -rf 3rdparty/gmock
%{!?with_static_sqlite:rm -rf 3rdparty/qsqlite}
rm -rf 3rdparty/qtsingleapplication
rm -rf 3rdparty/qxt
rm -rf 3rdparty/qtiocompressor
%{!?with_static_projectm:rm -rf 3rdparty/libprojectM}

# Don't build tests. They require gmock
sed -i -e '/add_subdirectory(tests)/d' CMakeLists.txt

%build
install -d build
install -d build/src/translations
cd build
%cmake \
	-DBUNDLE_PROJECTM_PRESETS=OFF \
	-DUSE_SYSTEM_QTSINGLEAPPLICATION=ON \
	-DUSE_SYSTEM_QXT=ON \
	-DUSE_SYSTEM_PROJECTM=ON \
	-DENGINE_GSTREAMER_ENABLED=%{?with_engine_gstreamer:ON}%{!?with_engine_gstreamer:OFF} \
	-DENGINE_LIBVLC_ENABLED=%{?with_engine_vlc:ON}%{!?with_engine_vlc:OFF} \
	-DENGINE_LIBXINE_ENABLED=%{?with_engine_xine:ON}%{!?with_engine_xine:OFF} \
	-DENGINE_QT_PHONON_ENABLED=%{?with_engine_qt_phonon:ON}%{!?with_engine_qt_phonon:OFF} \
	-DSTATIC_SQLITE=%{?with_static_sqlite:ON}%{!?with_static_sqlite:OFF} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/application-x-clementine.svg

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_bindir}/clementine
%{_desktopdir}/clementine.desktop
%{_pixmapsdir}/clementine.png
