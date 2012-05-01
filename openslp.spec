%global srcname		%{name}-%{version}.beta2

Name:			openslp
Version:		2.0
Release:		0.2.beta2%{?dist}
Summary:		Open implementation of Service Location Protocol V2

Group:			System Environment/Libraries
License:		BSD
URL:			http://www.openslp.org
Source0:		http://downloads.sourceforge.net/openslp/openslp-2.0.beta2.tar.gz
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:		bison flex openssl-devel doxygen
BuildRequires:		automake libtool

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.

%package server
Summary:		OpenSLP server daemon
Group:			System Environment/Daemons
Requires:		%{name} = %{version}-%{release}
Requires(preun):	chkconfig, /sbin/service
Requires(post):		chkconfig
Requires(postun):	/sbin/service

%description server
Service Location Protocol is an IETF standards track protocol that
provides a framework that allows networking applications to discover
the existence, location, and configuration of networked services in
enterprise networks.

This package contains the SLP server. Every system, which provides any
services that should be used via an SLP client must run this server and
register the service.

%package devel
Summary:		OpenSLP headers and libraries
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description devel
Service Location Protocol is an IETF standards track protocol that
provides a framework that allows networking applications to discover
the existence, location, and configuration of networked services in
enterprise networks.

This package contains header and library files to compile applications
with SLP support. It also contains developer documentation to develop
such applications.

%prep
%setup -q -n %{srcname}


%build
export CFLAGS="-fPIC -fno-strict-aliasing $RPM_OPT_FLAGS"
export LDFLAGS="-pie"
%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --sysconfdir=%{_sysconfdir} \
  --enable-async-api \
  --disable-rpath \
  --enable-slpv2-security \
  --localstatedir=/var
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/etc/slp.reg.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d/
install -m 0755 etc/slpd.all_init ${RPM_BUILD_ROOT}/etc/rc.d/init.d/slpd
ln -sf ../../etc/rc.d/init.d/slpd ${RPM_BUILD_ROOT}/usr/sbin/rcslpd
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add slpd

%postun server
# on upgrade
if [ $1 -gt 0 ]; then
  /sbin/service slpd condrestart >/dev/null 2>&1 ||:
fi

%preun server
# on remove
if [ $1 -eq 0 ]; then
  /sbin/service slpd stop >/dev/null 2>&1 ||:
  /sbin/chkconfig --del slpd
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc doc/doc/*
%{_libdir}/libslp.so.*
%{_bindir}/slptool
%config(noreplace) %{_sysconfdir}/slp.conf
%config(noreplace) %{_sysconfdir}/slp.spi

%files server
%defattr(-,root,root,-)
%dir /etc/slp.reg.d/
%{_sbindir}/rcslpd
%{_sbindir}/slpd
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) /etc/rc.d/init.d/slpd

%files devel
%defattr(-,root,root,-)
%{_includedir}/slp.h
%{_libdir}/libslp.so


%changelog
* Thu Jul 28 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0-0.2.beta2
- Build with -fno-strict-aliasing

* Wed Jul 20 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0-0.1.beta2
- Fix N-V-R

* Wed Jul 20 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.beta2-2
- Build

* Tue Jul 19 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.beta2-1
- Initial support
