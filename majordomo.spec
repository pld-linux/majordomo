#
# TODO:	- package rest of the files
#	- set attributes
#	- some files must go to /usr/bin instead of /usr/share/majordomo
#	- pl desc
#	- try to automate aliases creation in /etc/mail/aliases
#	- set $whereami variable to machine's hostname
#	- fix %postun error
#
%include	/usr/lib/rpm/macros.perl
Summary:	An Internet mailing list manager
Name:		majordomo
Version:	1.94.5
Release:	0.1
License:	distributable
Group:		Applications/Networking
Source0:	http://www.greatcircle.com/majordomo/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	337b2bbcc866803c6700e403e27390a7
Patch0:		%{name}-config.patch
Patch1:		%{name}-wrapper.patch
Patch2:		%{name}-install.patch
Patch3:		%{name}-Makefile.patch
URL:		http://www.greatcircle.com/majordomo/
Requires:	perl-base >= 1:5.0
Provides:	group(majordomo)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Majordomo is a program which automates the management of Internet
mailing lists. Commands are sent to Majordomo via electronic mail to
handle all aspects of list maintainance. Once a list is set up
virtually all operations can be performed remotely, requiring no
intervention by the postmaster of the list site.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -f sample.cf majordomo.cf

%build
%{__make} wrapper \
	PERL="%{__perl}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_mandir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TMPDIR=$RPM_BUILD_ROOT \
	PERL="%{__perl}" \
	W_USER="majordomo" \
	W_GROUP="majordomo" \

%{__make} install-wrapper \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# how we choose proper GID and UID?
%groupadd -g 235 %{name}
%useradd -u 235 -d /var/lib/%{name} -g %{name} -c "Majordomo User" %{name}

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE NEWLIST NEWS README* Doc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Tools
%{_mandir}/man8/majordomo.8*
