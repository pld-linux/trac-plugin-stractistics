%define		trac_ver	0.12
%define		plugin		stractistics
Summary:	Repository, ticket and wiki statistics
Name:		trac-plugin-%{plugin}
Version:	0.5.0b
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/stractisticsplugin?old_path=/&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	46d88e22c664cbf57e625319dc705421
Patch0:		web_path.patch
URL:		http://trac-hacks.org/wiki/StractisticsPlugin
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	python-modules
Requires:	python-simplejson
Requires:	trac >= %{trac_ver}
# for htdocs alias, can be removed in 0.13
Requires:	trac >= 0.12.2-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		trac_htdocs	/usr/share/trac/htdocs

%description
Stractistics is a plugin designed to estimate recent project activity
by providing repository, ticket and wiki statistics.

%prep
%setup -qc
mv %{plugin}plugin/trunk/* .
%undos README.txt stractistics/*.py
%patch0 -p1

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

# mv htdocs
install -d $RPM_BUILD_ROOT%{trac_htdocs}
mv $RPM_BUILD_ROOT{%{py_sitescriptdir}/%{plugin}/htdocs,%{trac_htdocs}/%{plugin}}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "stractistics.web_ui.*"

%files
%defattr(644,root,root,755)
%doc README.txt
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/STractistics-%{version}-py*.egg-info
%{trac_htdocs}/%{plugin}
