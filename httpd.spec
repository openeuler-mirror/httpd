%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define suexec_caller apache
%define mmn 20120211
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%global mpm event

Name:             httpd
Summary:          Apache HTTP Server
Version:          2.4.43
Release:          5
License:          ASL 2.0
URL:              https://httpd.apache.org/
Source0:          https://archive.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1:          index.html
Source2:          httpd.logrotate
Source3:          instance.conf
Source4:          httpd-ssl-pass-dialog
Source5:          httpd.tmpfiles
Source6:          httpd.service
Source7:          action-graceful.sh
Source8:          action-configtest.sh
Source9:          server-status.conf
Source10:         httpd.conf
Source11:         00-base.conf
Source12:         00-mpm.conf
Source13:         00-lua.conf
Source14:         01-cgi.conf
Source15:         00-dav.conf
Source16:         00-proxy.conf
Source17:         00-ssl.conf
Source18:         01-ldap.conf
Source19:         00-proxyhtml.conf
Source20:         userdir.conf
Source21:         ssl.conf
Source22:         welcome.conf
Source23:         manual.conf
Source24:         00-systemd.conf
Source25:         01-session.conf
Source26:         10-listen443.conf
Source27:         httpd.socket
Source28:         00-optional.conf
Source29:         01-md.conf
Source30:         README.confd
Source31:         README.confmod
Source32:         httpd.service.xml
Source40:         htcacheclean.service
Source41:         htcacheclean.sysconf
Source42:         httpd-init.service
Source43:         httpd-ssl-gencerts
Source44:         httpd@.service

Patch0:           httpd-2.4.1-apctl.patch
Patch1:           httpd-2.4.9-apxs.patch
Patch2:           httpd-2.4.1-deplibs.patch
Patch3:           httpd-2.4.3-apctl-systemd.patch
Patch4:           httpd-2.4.25-detect-systemd.patch
Patch5:           httpd-2.4.33-export.patch
Patch6:           httpd-2.4.1-corelimit.patch
Patch7:           httpd-2.4.25-selinux.patch
Patch8:           httpd-2.4.2-icons.patch
Patch9:           httpd-2.4.4-cachehardmax.patch
Patch10:          httpd-2.4.17-socket-activation.patch
Patch11:          httpd-2.4.34-sslciphdefault.patch
Patch12:          httpd-2.4.34-sslprotdefault.patch
Patch13:          httpd-2.4.34-enable-sslv3.patch
Patch14:          layout_add_openEuler.patch
Patch15:          httpd-2.4.43-lua-resume.patch 
Patch16:          CVE-2020-11984.patch 
Patch17:          CVE-2020-11993.patch 
Patch18:          CVE-2020-9490.patch
Patch19:          CVE-2021-26691.patch
Patch20:          CVE-2020-13950.patch
Patch21:          CVE-2020-35452.patch

BuildRequires:    gcc autoconf pkgconfig findutils xmlto perl-interpreter perl-generators systemd-devel
BuildRequires:    zlib-devel libselinux-devel lua-devel brotli-devel
BuildRequires:    apr-devel >= 1.5.0 apr-util-devel >= 1.5.0 pcre-devel >= 5.0
Requires:         mailcap system-logos mod_http2
Requires:         httpd-tools = %{version}-%{release} httpd-filesystem = %{version}-%{release}
Requires(pre):    httpd-filesystem
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(post):   systemd-units
Provides:         mod_proxy_uwsgi = %{version}-%{release}
Provides:         webserver httpd-mmn = %{mmn} httpd-mmn = %{mmnisa}
Provides:         mod_dav = %{version}-%{release} httpd-suexec = %{version}-%{release}
Obsoletes:        mod_proxy_uwsgi < 2.0.17.1-2 httpd-suexec
Conflicts:        apr < 1.5.0-1

%description
Apache HTTP Server is a powerful and flexible HTTP/1.1 compliant web server.

%package devel
Summary: Development files for %{name}
Requires: apr-devel apr-util-devel pkgconfig httpd = %{version}-%{release}

%description devel
This package provides APXS binary and other files used to compile
and develop additional modules for Apache.

%package help
Summary: Documents and man pages for HTTP Server
Requires: httpd = %{version}-%{release}
BuildArch: noarch

%description help
This packages provides manual and reference guide for HTTP Server.

%package filesystem
Summary: The basic directory for HTTP Server
BuildArch: noarch
Requires(pre): shadow-utils

%description filesystem
This package contains the basic directory layout for HTTP Server.

%package tools
Summary: Related tools for use HTTP Server

%description tools
This package contains tools used for HTTP Server.

%package -n mod_ssl
Summary: SSL and TLS modules for HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(pre): httpd-filesystem
Requires: httpd = 0:%{version}-%{release} httpd-mmn = %{mmnisa} sscg >= 2.2.0
Conflicts: openssl-libs < 1:1.0.1h-4

%description -n mod_ssl
This module provides strong cryptography via SSL and TLS for HTTP Server.

%package -n mod_md
Summary: Certificate provisioning using ACME for HTTP Server
Requires: httpd = 0:%{version}-%{release} httpd-mmn = %{mmnisa}
BuildRequires: jansson-devel libcurl-devel

%description -n mod_md
This module manages common properties for one or more virtual hosts.
It uses the ACME protocol to automate certificate provisioning.

%package -n mod_proxy_html
Summary: HTML content filters for the HTTP Server
Requires: httpd = 0:%{version}-%{release} httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
Epoch: 1
Obsoletes: mod_proxy_html < 1:2.4.1-2

%description -n mod_proxy_html
This module provides filters which can modify HTML link.

%package -n mod_ldap
Summary: LDAP authentication module for Apache HTTP Server
Requires: httpd = 0:%{version}-%{release} httpd-mmn = %{mmnisa}
Requires: apr-util-ldap

%description -n mod_ldap
This module adds support for LDAP authentication to Apache HTTP Server.

%package -n mod_session
Summary: Session support for Apache HTTP Server
Requires: httpd = 0:%{version}-%{release} httpd-mmn = %{mmnisa}

%description -n mod_session
Ths module provides session support for per-user.

%prep
%autosetup -p1

sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

# Example conf for instances
cp $RPM_SOURCE_DIR/instance.conf .
sed < $RPM_SOURCE_DIR/httpd.conf >> instance.conf '
0,/^ServerRoot/d;
/# Supplemental configuration/,$d
/^ *CustomLog .logs/s,logs/,logs/${HTTPD_INSTANCE}_,
/^ *ErrorLog .logs/s,logs/,logs/${HTTPD_INSTANCE}_,
'
touch -r $RPM_SOURCE_DIR/instance.conf instance.conf
cp -p $RPM_SOURCE_DIR/server-status.conf server-status.conf

sed 's/@MPM@/%{mpm}/' < $RPM_SOURCE_DIR/httpd.service.xml \
    > httpd.service.xml

xmlto man ./httpd.service.xml

%build
rm -rf srclib/{apr,apr-util,pcre}

autoheader && autoconf || exit 1

%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"
export LYNX_PATH=/usr/bin/links

./configure \
   --prefix=%{_sysconfdir}/httpd --exec-prefix=%{_prefix} --bindir=%{_bindir} \
   --sbindir=%{_sbindir} --mandir=%{_mandir} --libdir=%{_libdir} \
   --sysconfdir=%{_sysconfdir}/httpd/conf --includedir=%{_includedir}/httpd \
   --libexecdir=%{_libdir}/httpd/modules --datadir=%{contentdir} \
   --with-installbuilddir=%{_libdir}/httpd/build --enable-layout=openEuler \
   --enable-mpms-shared=all --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
   --enable-suexec --with-suexec --enable-suexec-capabilities \
   --with-suexec-caller=%{suexec_caller} --with-suexec-docroot=%{docroot} \
   --without-suexec-logfile --with-suexec-syslog \
   --with-suexec-bin=%{_sbindir}/suexec --with-brotli --enable-pie --with-pcre \
   --with-suexec-uidmin=1000 --with-suexec-gidmin=1000 \
   --enable-mods-shared=all --enable-ssl --with-ssl --disable-distcache \
   --enable-proxy --enable-proxy-fdpass --enable-cache --enable-disk-cache \
   --enable-ldap --enable-authnz-ldap --enable-cgid --enable-cgi \
   --enable-authn-anon --enable-authn-alias --enable-systemd \
   --disable-imagemap --disable-file-cache --disable-http2 $*

%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install

install -d $RPM_BUILD_ROOT%{_unitdir}
install -p -m644 $RPM_SOURCE_DIR/httpd.service $RPM_BUILD_ROOT%{_unitdir}/httpd.service
install -p -m644 $RPM_SOURCE_DIR/{htcacheclean.service,httpd.socket,httpd@.service,httpd-init.service} $RPM_BUILD_ROOT%{_unitdir}/

install -D -m644 $RPM_SOURCE_DIR/README.confd $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
install -D -m644 $RPM_SOURCE_DIR/README.confmod $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/README
install -p -m644 $RPM_SOURCE_DIR/0*.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/

sed -i '/^#LoadModule mpm_%{mpm}_module /s/^#//' $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf
touch -r $RPM_SOURCE_DIR/00-mpm.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf

install -d $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d
install -D -m 644 -p $RPM_SOURCE_DIR/10-listen443.conf $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d/10-listen443.conf
install -m644 -p $RPM_SOURCE_DIR/{welcome.conf,ssl.conf,manual.conf,userdir.conf} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -m 644 docs/conf/extra/httpd-autoindex.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/autoindex.conf

rm -v docs/conf/extra/httpd-{ssl,userdir}.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf

install -m 644 -p $RPM_SOURCE_DIR/httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

install -D -m 644 -p $RPM_SOURCE_DIR/htcacheclean.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/htcacheclean

install -D -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
   $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd.conf

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/{dav,httpd} \
         $RPM_BUILD_ROOT/run/httpd/htcacheclean

sed -i \
   "s,@@ServerRoot@@/var,%{_localstatedir}/lib/dav,;
    s,@@ServerRoot@@/user.passwd,/etc/httpd/conf/user.passwd,;
    s,@@ServerRoot@@/docs,%{docroot},;
    s,@@ServerRoot@@,%{docroot},;
    s,@@Port@@,80,;" \
    docs/conf/extra/*.conf

install -d $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/{proxy,ssl}

install -d $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat > $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_bindir}/apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
EOF

install -d $RPM_BUILD_ROOT%{contentdir}/{noindex,server-status}
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{contentdir}/noindex/index.html
install -m 644 -p docs/server-status/* \
        $RPM_BUILD_ROOT%{contentdir}/server-status

rm -rf %{contentdir}/htdocs
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f



for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done

rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

ln -s ../../pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/lib/httpd $RPM_BUILD_ROOT/etc/httpd/state
ln -s /run/httpd $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

install -D -m755 $RPM_SOURCE_DIR/httpd-ssl-pass-dialog \
   $RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-pass-dialog

install -m755 $RPM_SOURCE_DIR/httpd-ssl-gencerts $RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-gencerts

install -D -p -m 755 $RPM_SOURCE_DIR/action-graceful.sh $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/graceful
install -p -m 755 $RPM_SOURCE_DIR/action-configtest.sh $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/configtest

install -D -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
   $RPM_BUILD_ROOT/etc/logrotate.d/httpd

install -m 644 -p httpd.service.8 httpd-init.service.8 httpd.socket.8 httpd@.service.8 \
   $RPM_BUILD_ROOT%{_mandir}/man8

sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/run/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

%pre filesystem
getent group apache >/dev/null || groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{contentdir} -c "Apache" apache
exit 0

%post
%systemd_post httpd.service htcacheclean.service httpd.socket

%preun
%systemd_preun httpd.service htcacheclean.service httpd.socket

%postun
%systemd_postun httpd.service htcacheclean.service httpd.socket

%triggerun -- httpd < 2.2.21-5
/usr/bin/systemd-sysv-convert --save httpd.service >/dev/null 2>&1 ||:
/sbin/chkconfig --del httpd >/dev/null 2>&1 || :

%posttrans
test -f /etc/sysconfig/httpd-disable-posttrans || \
  /bin/systemctl try-restart --no-block httpd.service htcacheclean.service >/dev/null 2>&1 || :

%check
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi
set +x
rv=0
for f in $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so; do
  m=${f##*/}
  if ! grep -q $m $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/*.conf; then
    echo ERROR: Module $m not configured.  Disable it, or load it.
    rv=1
  fi
done
mods=`grep -h ^LoadModule $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/*.conf | sed 's,.*modules/,,'`
for m in $mods; do
  f=$RPM_BUILD_ROOT%{_libdir}/httpd/modules/${m}
  if ! test -x $f; then
    echo ERROR: Module $m is configured but not built.
    rv=1
  fi
done
set -x
exit $rv

%files
%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf
%doc instance.conf server-status.conf

%{_sysconfdir}/httpd/{modules,logs,*run,state}
%config(noreplace) %{_sysconfdir}/httpd/conf/{httpd.conf,magic}
%config(noreplace) %{_sysconfdir}/logrotate.d/httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.d/ssl.conf
%exclude %{_sysconfdir}/httpd/conf.d/manual.conf
%{_sysconfdir}/httpd/conf.modules.d/README
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-md.conf

%config(noreplace) %{_sysconfdir}/sysconfig/htcacheclean
%ghost %{_sysconfdir}/sysconfig/httpd
%{_prefix}/lib/tmpfiles.d/httpd.conf
%{_libexecdir}/initscripts/legacy-actions/httpd/*
%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_md.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%exclude %{_libdir}/httpd/modules/mod_session*.so

%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html
%{contentdir}/server-status/*

%attr(0710,root,apache) %dir /run/httpd
%attr(0700,apache,apache) %dir /run/httpd/htcacheclean
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy

%{_mandir}/man8/*
%exclude %{_mandir}/man8/httpd-init.*

%{_unitdir}/httpd.service
%{_unitdir}/httpd@.service
%{_unitdir}/htcacheclean.service
%{_unitdir}/*.socket

%files filesystem
%{_sysconfdir}/httpd/conf.d/README
%dir %{docroot}/cgi-bin
%dir %{docroot}/html
%dir %{contentdir}/icons
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%attr(755,root,root) %dir %{_unitdir}/httpd.socket.d

%files tools
%doc LICENSE NOTICE
%{_bindir}/*
%{_mandir}/man1/*
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files help
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n mod_ssl
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_unitdir}/httpd-init.service
%{_libexecdir}/httpd-ssl-pass-dialog
%{_libexecdir}/httpd-ssl-gencerts
%{_unitdir}/httpd.socket.d/10-listen443.conf
%{_mandir}/man8/httpd-init.*

%files -n mod_proxy_html
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n mod_ldap
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n mod_session
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files -n mod_md
%{_libdir}/httpd/modules/mod_md.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-md.conf

%files devel
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_rpmconfigdir}/macros.d/macros.httpd

%changelog
* Mon Jun 21 2021 yanglu <yanglu72@huawei.com> - 2.4.43-5
- Type:cves
- ID:CVE-2020-13950 CVE-2020-35452
- SUG:restart
- DESC:fix CVE-2020-13950 CVE-2020-35452

* Wed Jun 16 2021 yanglu <yanglu72@huawei.com> - 2.4.43-4
- Type:cves
- ID:CVE-2021-26691
- SUG:restart
- DESC:fix CVE-2021-26691

* Sun Sep 27 2020 yuboyun <yuboyun@huawei.com> - 2.4.43-3
- Type:cves
- ID:CVE-2020-9490 CVE-2020-11984 CVE-2020-11993
- SUG:restart
- DESC:fix CVE-2020-9490CVE-2020-11984CVE-2020-11993

* Sat Sep 5 2020 zhaowei<zhaowei23@huawei.com> - 2.4.43-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: update source URL

* Wed Aug 26 2020 yuboyun <yuboyun@huawei.com> - 2.4.43-1
- Type:NA
- ID:NA
- SUG:NA
- DESC:Update to 2.4.43

* Mon May 18 2020 wangchen <wangchen137@huawei.com> - 2.4.34-18
- rebuild for httpd

* Thu Apr 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.34-17
- Type:cves
- ID:CVE-2019-9517 CVE-2019-10081 CVE-2019-10082 CVE-2020-1927 CVE-2020-1934
- SUG:restart
- DESC:fix CVE-2019-9517 CVE-2019-10081 CVE-2019-10082 CVE-2020-1927 CVE-2020-1934

* Wed Apr 15 2020 chenzhen <chenzhen44@huawei.com> - 2.4.34-16
- Type:cves
- ID:CVE-2019-10092 CVE-2019-10097 CVE-2019-10098 CVE-2019-0196 CVE-2019-0197
- SUG:NA
- DESC:fix CVE-2019-10092 CVE-2019-10097 CVE-2019-10098 CVE-2019-0196 CVE-2019-0197

* Mon Feb 03 2020 yanzhihua <yanzhihua4@huawei.com> - 2.4.34-15
- Type:cves
- ID:CVE-2018-17199
- SUG:NA
- DESC:fix CVE-2018-17199

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.34-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add SSLCipherSuite 

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.34-13
- Type:NA
- ID:NA
- SUG:NA
- DESC:delete patches

* Wed Dec 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.4.34-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change source

* Tue Oct 29 2019 zhuchengliang <zhuchengliang4@huawei.com> - 2.4.34-11
- Type:NA
- ID:NA
- SUG:NA
- DESC:add systemd_postun para

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.4.34-10
- Type:cves
- ID:CVE-2019-0220
- SUG:NA
- DESC:fix CVE-2019-0220

* Sat Sep 21 2019 liyongqiang<liyongqiang10@huawei.com> - 2.4.34-9
- Package init
