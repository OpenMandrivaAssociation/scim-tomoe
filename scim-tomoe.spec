%define scim_version         1.4.7
%define tomoe_version        0.6.0

Name:		scim-tomoe
Summary:	SCIM module for tomoe
Version:	0.6.0
Release:	%{mkrel 5}
Group:		System/Internationalization
License:	GPLv2+
URL:		http://sourceforge.jp/projects/scim-imengine/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/tomoe/%{name}-%{version}.tar.bz2
Patch0:		scim-tomoe-0.6.0-gcc43-cstring-440886.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	scim-client = %scim_api
Requires:	tomoe >= %{tomoe_version}
BuildRequires:	scim-devel >= %{scim_version}
BuildRequires:	tomoe-devel >= %{tomoe_version}
BuildRequires:	libtomoe-gtk-devel
BuildRequires:	automake
BuildRequires:	intltool
Obsoletes:	%{mklibname scim-tomoe 0}

%description
SCIM module for tomoe.

%prep
%setup -q
%patch0 -p1

%build
if [[ ! -x configure ]]; then
# (cjw) do not use bootstrap script directly - it runs "aclocal" and "automake"
  libtoolize --copy --force --automake 
  aclocal -I m4 --force
  autoheader
  automake --add-missing --copy --include-deps
  autoconf
fi

%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{scim_plugins_dir}/Helper/*.la

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS
%{_bindir}/scim-tomoe
%{_datadir}/scim/icons/*
%{scim_plugins_dir}/Helper/*.so

