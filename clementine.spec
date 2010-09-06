# TODO:
# - add missing BRs
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

Summary:	A music player and library organiser
Summary(hu.UTF-8):	Egy zenelejátszó és gyűjtemény-kezelő
Name:		clementine
Version:	0.5
Release:	0.1
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://www.clementine-player.org/
Source0:	http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	59a94906394c7e22da567841770dab86
Patch0:		desktop-install.patch
Patch1:		no-private_header.patch
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtIOCompressor-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtSingleApplication-devel >= 2.6-3
BuildRequires:	QtSql-devel
%{?with_tests:BuildRequires:	QtTest-devel}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
#BuildRequires:	desktop-file-utils
#%{?with_static_projectm:BuildRequires:	ftgl-devel >= 2.1.3}
BuildRequires:	gettext-devel
%{?with_static_projectm:BuildRequires:	glew-devel}
%{?with_engine_gstreamer:BuildRequires:	gstreamer-devel >= 0.10}
%{?with_engine_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 0.10}
BuildRequires:	gtest-devel
BuildRequires:	liblastfm-devel
BuildRequires:	libnotify-devel
%{!?with_static_projectm:BuildRequires:	libprojectM-devel >= 1:2.0.1-4}
BuildRequires:	libqxt-devel
#BuildRequires:	libqxt-devel >= 0.6.0-0.2
BuildRequires:	notification-daemon
%{?with_engine_phonon:BuildRequires:	phonon-devel}
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
%{!?with_static_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	taglib-devel >= 1.6
%{?with_engine_vlc:BuildRequires:	vlc-devel}
%{?with_engine_xine:BuildRequires:	xine-lib-devel}
Requires(post,postun):	desktop-file-utils
%{!?with_static_sqlite:Requires:	QtSql-sqlite3}
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
%setup -q
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_bindir}/clementine
%{_desktopdir}/clementine.desktop
%{_pixmapsdir}/clementine.png
