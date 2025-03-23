Summary:	Extras Plugins for DNF
Name:		dnf-plugins-extras
Version:	4.0.16
Release:	4
License:	GPL v2+
Source0:	https://github.com/rpm-software-management/dnf-plugins-extras/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	22c566100be065e770a6b0032f8a4ad3
Patch0:		install.patch
URL:		https://github.com/rpm-software-management/dnf-plugins-extras
BuildRequires:	cmake
BuildRequires:	dnf >= 4.4.3
BuildRequires:	gettext
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	sphinx-pdg
BuildRequires:	systemd-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extras Plugins for DNF.

%package common
Summary:	Common files for Extras Plugins for DNF
Requires:	dnf >= 4.4.3

%description common
Common files for Extras Plugins for DNF.

%package -n dnf-plugin-kickstart
Summary:	Kickstart Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-pykickstart

%description -n dnf-plugin-kickstart
Kickstart Plugin for DNF. Install packages listed in a Kickstart file.

%package -n dnf-plugin-rpmconf
Summary:	RpmConf Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-rpmconf

%description -n dnf-plugin-rpmconf
RpmConf Plugin for DNF. Handles .rpmnew, .rpmsave every transaction.

%package -n dnf-plugin-snapper
Summary:	Snapper Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-dbus
Requires:	snapper

%description -n dnf-plugin-snapper
Snapper Plugin for DNF. Creates snapshot every transaction.

%package -n dnf-plugin-system-upgrade
Summary:	System Upgrade Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-systemd

%description -n dnf-plugin-system-upgrade
System Upgrade Plugin for DNF. Enables offline system upgrades using
the "dnf system-upgrade" command.

%package -n dnf-plugin-tracer
Summary:	Tracer Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-tracer >= 0.6.12

%description -n dnf-plugin-tracer
Tracer Plugin for DNF. Finds outdated running applications in your
system every transaction.

%package -n dnf-plugin-torproxy
Summary:	Tor Proxy Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	python3-pycurl

%description -n dnf-plugin-torproxy
Tor proxy plugin forces DNF to use Tor to download packages. It makes
sure that Tor is working and avoids leaking the hostname by using the
proper SOCKS5 interface.

%package -n dnf-plugin-showvars
Summary:	showvars Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}

%description -n dnf-plugin-showvars
This plugin dumps the current value of any defined DNF variables. For
example $releasever and $basearch.

%prep
%setup -q
%patch -P 0 -p1

%build
mkdir -p build
cd build
%cmake ../ \
	-DPYTHON_DESIRED:FILEPATH=%{__python3} \
	-DPYTHON_INSTALL_DIR:PATH=%{py3_sitescriptdir} \
	-DSYSTEMD_DIR:PATH=%{systemdunitdir}

%{__make}
%{__make} doc-man

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}/system-update.target.wants

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sr $RPM_BUILD_ROOT%{systemdunitdir}/{,system-update.target.wants/}dnf-system-upgrade.service

for d in $RPM_BUILD_ROOT%{py3_sitescriptdir}/{dnf-plugins,dnfpluginsextras}; do
%py3_comp $d
%py3_ocomp $d
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files common -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%{py3_sitescriptdir}/dnfpluginsextras
%{py3_sitescriptdir}/dnf-plugins/__pycache__/*

%files -n dnf-plugin-kickstart
%defattr(644,root,root,755)
%{py3_sitescriptdir}/dnf-plugins/kickstart.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/kickstart.*
%{_mandir}/man8/dnf-kickstart.*

%files -n dnf-plugin-rpmconf
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{py3_sitescriptdir}/dnf-plugins/rpm_conf.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/rpm_conf.*
%{_mandir}/man8/dnf-rpmconf.*

%files -n dnf-plugin-snapper
%defattr(644,root,root,755)
%{py3_sitescriptdir}/dnf-plugins/snapper.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/snapper.*
%{_mandir}/man8/dnf-snapper.*

%files -n dnf-plugin-system-upgrade
%defattr(644,root,root,755)
%{systemdunitdir}/dnf-system-upgrade.service
%{systemdunitdir}/dnf-system-upgrade-cleanup.service
%{systemdunitdir}/system-update.target.wants/dnf-system-upgrade.service
%{py3_sitescriptdir}/dnf-plugins/system_upgrade.py
%{py3_sitescriptdir}/dnf-plugins/__pycache__/system_upgrade.*
%{_mandir}/man8/dnf-system-upgrade.*

%files -n dnf-plugin-tracer
%defattr(644,root,root,755)
%{py3_sitescriptdir}/dnf-plugins/tracer.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/tracer.*
%{_mandir}/man8/dnf-tracer.*

%files -n dnf-plugin-torproxy
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/dnf/plugins/torproxy.conf
%{py3_sitescriptdir}/dnf-plugins/torproxy.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/torproxy.*
%{_mandir}/man8/dnf-torproxy.*

%files -n dnf-plugin-showvars
%defattr(644,root,root,755)
%{py3_sitescriptdir}/dnf-plugins/showvars.*
%{py3_sitescriptdir}/dnf-plugins/__pycache__/showvars.*
%{_mandir}/man8/dnf-showvars.*
