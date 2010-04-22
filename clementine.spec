Summary:	A music player and library organiser
Name:		clementine
Version:	0.2
Release:	0.1
License:	GPL v3 and GPL v2+
Group:		Applications/Multimedia
URL:		http://code.google.com/p/clementine-player
Source0:	http://clementine-player.googlecode.com/files/%{name}_%{version}-1.tar.gz
# Source0-md5:	bf89adb26808fec6201499375de95507
Patch0:		%{name}-dont-bundle-external-lib.patch
Patch1:		%{name}-static.patch
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gtest-devel
BuildRequires:	liblastfm-devel
BuildRequires:	libnotify-devel
BuildRequires:	libqxt-devel
BuildRequires:	notification-daemon
BuildRequires:	qt4-build
BuildRequires:	qtsingleapplication-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite-devel
BuildRequires:	taglib-devel
BuildRequires:	xine-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Clementine is a modern music player and library organiser. It is
largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# We already don't use these but just to make sure
rm -fr 3rdparty

# Don't build tests. They require gmock which is not yet available on Fedora
sed -i '/tests/d' CMakeLists.txt

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_bindir}/clementine
%{_desktopdir}/clementine.desktop
%{_iconsdir}/hicolor/*/apps/application-x-clementine.png
