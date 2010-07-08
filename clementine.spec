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

Summary:	A music player and library organiser
Summary(hu.UTF-8):	Egy zenelejátszó és gyűjtemény-kezelő
Name:		clementine
Version:	0.4.2
Release:	0.2
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://code.google.com/p/clementine-player
Source0:	http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	c6819b0d2a8324f1d686fb5a3b1d287b
Patch0:		%{name}-dont-bundle-external-lib.patch
Patch2:		desktop-install.patch
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtIOCompressor-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtSingleApplication-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	gtest-devel
BuildRequires:	liblastfm-devel
BuildRequires:	libnotify-devel
#BuildRequires:	libprojectM-devel
BuildRequires:	libqxt-devel
#BuildRequires:	libqxt-devel >= 0.6.0-0.2
BuildRequires:	notification-daemon
BuildRequires:	phonon-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(macros) >= 1.198
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	vlc-devel
BuildRequires:	xine-lib-devel
Requires(post,postun):	desktop-file-utils
Requires:	QtSql-sqlite3
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
%patch2 -p1

# We already don't use these but just to make sure
rm -rf 3rdparty/gmock
rm -rf 3rdparty/qsqlite
rm -rf 3rdparty/qtsingleapplication
rm -rf 3rdparty/qxt
rm -rf 3rdparty/qtiocompressor

# Don't build tests. They require gmock
sed -i -e '/add_subdirectory(tests)/d' CMakeLists.txt

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUNDLE_PROJECTM_PRESETS=OFF \
	-DENGINE_GSTREAMER_ENABLED=%{?with_engine_gstreamer:ON}%{!?with_engine_gstreamer:OFF} \
	-DENGINE_LIBVLC_ENABLED=%{?with_engine_vlc:ON}%{!?with_engine_vlc:OFF} \
	-DENGINE_LIBXINE_ENABLED=%{?with_engine_xine:ON}%{!?with_engine_xine:OFF} \
	-DENGINE_QT_PHONON_ENABLED=%{?with_engine_qt_phonon:ON}%{!?with_engine_qt_phonon:OFF} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
