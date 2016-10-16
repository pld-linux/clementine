# TODO:
# - Gstreamer error: "A text/uri-list decoder plugin is required to play this stream, but not installed."
# - apply patches to libprojectM.spec and use
# - sub-package for kde4 stuff (or nuke them):
#        /usr/share/kde4/services/clementine-feed.protocol
#        /usr/share/kde4/services/clementine-itms.protocol
#        /usr/share/kde4/services/clementine-itpc.protocol
#        /usr/share/kde4/services/clementine-zune.protocol
#
# Conditional build:
%bcond_with	static_projectm	# with static projectM
%bcond_with	libspotify	# build with system libspotify instead of downloading blob
%bcond_with	tests		# build without tests

%define		qtver	%(pkg-config --silence-errors --modversion QtCore 2>/dev/null || echo ERROR)
%define		sqlitever	3.14.0-2
Summary:	A music player and library organiser
Summary(hu.UTF-8):	Egy zenelejátszó és gyűjtemény-kezelő
Name:		clementine
Version:	1.3.1
Release:	5
License:	GPL v3 and GPL v2+
Group:		X11/Applications/Multimedia
Source0:	https://github.com/clementine-player/Clementine/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	18cc5f66aa5fbb2781198a65439bd38a
Patch1:		unbundle-po.patch
Patch2:		%{name}-udisks-headers.patch
Patch3:		%{name}-mygpo.patch
URL:		http://www.clementine-player.org/
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtDBus-devel >= %{qtver}
BuildRequires:	QtGui-devel >= %{qtver}
BuildRequires:	QtIOCompressor-devel >= 2.3
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtOpenGL-devel >= %{qtver}
BuildRequires:	QtSingleApplication-devel >= 2.6-4
BuildRequires:	QtSql-devel >= %{qtver}
%{?with_tests:BuildRequires:	QtTest-devel >= %{qtver}}
BuildRequires:	QtXml-devel >= %{qtver}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	cryptopp-devel >= 5.6.1-4
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
%{?with_static_projectm:BuildRequires:	glew-devel}
BuildRequires:	glib2-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtest-devel
BuildRequires:	libcdio-devel
BuildRequires:	libchromaprint-devel
BuildRequires:	libechonest-devel
BuildRequires:	libgpod-devel >= 0.7.92
BuildRequires:	libimobiledevice-devel >= 1.1.5
BuildRequires:	liblastfm-devel >= 0.3.3
BuildRequires:	libmtp-devel >= 1.0
BuildRequires:	libmygpo-qt-devel >= 1.0.7
BuildRequires:	libplist-devel
%{!?with_static_projectm:BuildRequires:	libprojectM-devel >= 1:2.0.1-4}
BuildRequires:	libqxt-devel
%{?with_libspotify:BuildRequires:	libspotify-devel >= 12.1.45}
BuildRequires:	libusbmuxd-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	qjson-devel
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(find_lang) >= 1.38
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
BuildRequires:	sparsehash-devel
BuildRequires:	sqlite3-devel >= %{sqlitever}
BuildRequires:	taglib-devel >= 1.8
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRequires:	sqlite3 >= %{sqlitever}
Requires:	QtSingleApplication >= 2.6-4
Requires:	QtSql-sqlite3 >= %{qtver}
Requires:	gstreamer-audio-effects-base
Requires:	gstreamer-mad
Suggests:	gstreamer-flac
# if we do not link, we use datafiles
%{!?with_static_projectm:Requires:	libprojectM}
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
%patch1 -p1
%patch2 -p1
#%patch3 -p1

# cleanup vendor. keep only needed libraries.
mv 3rdparty 3rdparty.dist
vendor() {
	local path dir
	for path; do
		dir=$(dirname $path)
		test -d 3rdparty/$dir || mkdir -p 3rdparty/$dir
		mv 3rdparty.dist/$path 3rdparty/$path
	done
}
vendor sha2 qocoa
vendor qsqlite
%{?with_static_projectm:vendor libprojectm}
# missing in pld
vendor vreen
# requires 1.0.9, but only 1.0.8 is released
vendor libmygpo-qt

# Don't build tests. They require gmock
sed -i -e '/add_subdirectory(tests)/d' CMakeLists.txt
# remove -Wall
sed -i -e 's/-Wall//' src/CMakeLists.txt

%build
install -d build
install -d build/src/translations
cd build
# as our buildtype is not Release, need to pass these manually. see CMakeLists.txt ~135
CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG_OUTPUT"
%cmake \
	-DBUILD_WERROR:BOOL=OFF \
	-DCMAKE_POSITION_INDEPENDENT_CODE=ON \
	-DCMAKE_INCLUDE_PATH=%{_includedir}/qt4 \
	-DBUNDLE_PROJECTM_PRESETS=OFF \
	-DUSE_SYSTEM_QTSINGLEAPPLICATION=ON \
	-DUSE_SYSTEM_QXT=ON \
	-DUSE_SYSTEM_PROJECTM=ON \
	-DQTSINGLEAPPLICATION_INCLUDE_DIRS=%{_includedir}/qt4/QtSolutions \
	..
%{__make}

desktop-file-validate ../dist/%{name}.desktop

%if %{with tests}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/kde4/services

# not in our glibc?
rm -r $RPM_BUILD_ROOT%{_localedir}/tr_TR
rm -r $RPM_BUILD_ROOT%{_localedir}/he_IL
rm -r $RPM_BUILD_ROOT%{_localedir}/mk_MK
rm -r $RPM_BUILD_ROOT%{_localedir}/si_LK

%find_lang %{name} --with-qm

install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps
cp -p dist/icons/ubuntu-mono-light/clementine-panel-grey.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps/clementine-panel-grey.png
cp -p dist/icons/ubuntu-mono-light/clementine-panel.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/24x24/apps/clementine-panel.png

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
%{_iconsdir}/hicolor/*/apps/clementine-panel-grey.png
%{_iconsdir}/hicolor/*/apps/clementine-panel.png
%{_iconsdir}/hicolor/*/apps/clementine.png
%{_iconsdir}/hicolor/*/apps/clementine.svg
%{_datadir}/appdata/clementine.appdata.xml
