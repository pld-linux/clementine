Summary:	A music player and library organiser
Name:		clementine
Version:	0.2
Release:	0.3
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://code.google.com/p/clementine-player
Source0:	http://clementine-player.googlecode.com/files/%{name}_%{version}-1.tar.gz
# Source0-md5:	bf89adb26808fec6201499375de95507
Patch0:		%{name}-dont-bundle-external-lib.patch
Patch1:		%{name}-static.patch
Patch2:		desktop-install.patch
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtSingleApplication-devel
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	desktop-file-utils
BuildRequires:	gtest-devel
BuildRequires:	liblastfm-devel
BuildRequires:	libnotify-devel
BuildRequires:	libqxt-devel
BuildRequires:	notification-daemon
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(macros) >= 1.198
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite-devel
BuildRequires:	sqlite3-devel
BuildRequires:	taglib-devel
BuildRequires:	xine-lib-devel
Requires(post,postun):	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Clementine is a modern music player and library organiser. It is
largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# We already don't use these but just to make sure
rm -fr 3rdparty

# Don't build tests. They require gmock
sed -i -e '/tests/d' CMakeLists.txt

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
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
