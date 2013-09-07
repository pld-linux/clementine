# TODO:
# - Gstreamer error: "A text/uri-list decoder plugin is required to play this stream, but not installed."
# - apply patches to libprojectM.spec and use
# - checking for module 'libspotify>=12.1.45' - Spotify support: non-GPL binary helper (missing libspotify)
# - checking for module 'libchromaprint'
# - Google Drive support (missing Google sparsehash)
# - package for kde4 stuff (or nuke them):
#        /usr/share/kde4/services/clementine-feed.protocol
#        /usr/share/kde4/services/clementine-itms.protocol
#        /usr/share/kde4/services/clementine-itpc.protocol
#        /usr/share/kde4/services/clementine-zune.protocol
#
# Conditional build:
%bcond_without	static_sqlite	# with static sqlite3
%bcond_with	static_projectm	# with static projectM

%define		qtver	%(pkg-config --silence-errors --modversion QtCore 2>/dev/null || echo ERROR)
Summary:	A music player and library organiser
Summary(hu.UTF-8):	Egy zenelejátszó és gyűjtemény-kezelő
Name:		clementine
Version:	1.1.1
Release:	6
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://www.clementine-player.org/
Source0:	http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	28e4afb822388bd337a761db8f86febf
Patch0:		desktop-install.patch
Patch1:		unbundle-po.patch
Patch2:		%{name}-1.1.1-libimobiledevice-fix.patch
Patch3:		%{name}-dt_categories.patch
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
BuildRequires:	QtXmlPatterns-devel >= %{qtver}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
#%{?with_static_projectm:BuildRequires:	ftgl-devel >= 2.1.3}
BuildRequires:	gettext-devel
%{?with_static_projectm:BuildRequires:	glew-devel}
BuildRequires:	glib2-devel
BuildRequires:	gstreamer0.10-devel
BuildRequires:	gstreamer0.10-plugins-base-devel
BuildRequires:	gtest-devel
BuildRequires:	libgpod-devel >= 0.7.92
BuildRequires:	libimobiledevice-devel
BuildRequires:	libindicate-qt-devel
BuildRequires:	liblastfm-devel >= 0.3.3
BuildRequires:	libmtp-devel
BuildRequires:	libplist-devel
%{!?with_static_projectm:BuildRequires:	libprojectM-devel >= 1:2.0.1-4}
BuildRequires:	libqxt-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	qca-devel
BuildRequires:	qjson-devel
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(find_lang) >= 1.33
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
%{!?with_static_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	usbmuxd-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	QtSingleApplication >= 2.6-4
%{!?with_static_sqlite:Requires:	QtSql-sqlite3 >= %{qtver}}
Requires:	gstreamer0.10-audio-effects-base
Requires:	gstreamer0.10-mad
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
%patch2 -p1
%patch3 -p1

# We already don't use these but just to make sure
rm -rf 3rdparty/gmock
%{!?with_static_sqlite:rm -rf 3rdparty/qsqlite}
rm -rf 3rdparty/qtsingleapplication
rm -rf 3rdparty/qxt
rm -rf 3rdparty/qtiocompressor
%{!?with_static_projectm:rm -rf 3rdparty/libprojectM}

# Don't build tests. They require gmock
sed -i -e '/add_subdirectory(tests)/d' CMakeLists.txt
# remove -Wall
sed -i -e 's/-Wall//' src/CMakeLists.txt
# ...and -Werror
sed -i -e 's/-Werror//' src/CMakeLists.txt

%build
install -d build
install -d build/src/translations
cd build
# as our buildtype is not Release, need to pass these manually. see CMakeLists.txt ~125
CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG_OUTPUT"
%cmake \
	-DBUNDLE_PROJECTM_PRESETS=OFF \
	-DUSE_SYSTEM_QTSINGLEAPPLICATION=ON \
	-DQTSINGLEAPPLICATION_INCLUDE_DIRS=%{_includedir}/qt4/QtSolutions/ \
	-DUSE_SYSTEM_QXT=ON \
	-DUSE_SYSTEM_PROJECTM=ON \
	-DSTATIC_SQLITE=%{?with_static_sqlite:ON}%{!?with_static_sqlite:OFF} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/application-x-clementine.svg

# not in our glibc?
rm -r $RPM_BUILD_ROOT%{_localedir}/tr_TR

%find_lang %{name} --with-qm

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps
cp -a dist/icons/ubuntu-mono-light/clementine-panel-grey.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps/clementine-panel-grey.png
cp -a dist/icons/ubuntu-mono-light/clementine-panel.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps/clementine-panel.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Changelog
%attr(755,root,root) %{_bindir}/clementine
%attr(755,root,root) %{_bindir}/clementine-tagreader
%{_desktopdir}/clementine.desktop
%{_pixmapsdir}/clementine.png
%{_iconsdir}/hicolor/*/apps/clementine-panel-grey.png
%{_iconsdir}/hicolor/*/apps/clementine-panel.png
