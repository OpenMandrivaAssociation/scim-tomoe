%define version   0.6.0
%define release   %mkrel 1

%define scim_version         1.4.7
%define tomoe_version        0.6.0
%define libtomoe_gtk_version 0.6.0

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Name:      scim-tomoe
Summary:   SCIM module for tomoe
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPL
URL:       http://sourceforge.jp/projects/scim-imengine/
Source0:   %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:        %{libname} = %{version}
Requires:        scim >= %{scim_version}
Requires:        tomoe >= %{tomoe_version}
Requires:        libtomoe-gtk >= %{libtomoe_gtk_version}
BuildRequires:   scim-devel >= %{scim_version}
BuildRequires:   libtomoe-devel >= %{tomoe_version}
BuildRequires:   libtomoe-gtk-devel >= %{libtomoe_gtk_version}
BuildRequires:   automake1.9

%description
SCIM module for tomoe.


%package -n %{libname}
Summary:    Scim-tomoe library
Group:      System/Internationalization
Provides:   %{libname_orig} = %{version}-%{release}

%description -n %{libname}
scim-tomoe library.


%prep
%setup -q
#cp /usr/share/automake-1.9/mkinstalldirs .

%build
if [[ ! -x configure ]]; then
# (cjw) do not use bootstrap script directly - it runs "aclocal" and "automake"
  libtoolize --copy --force --automake 
  aclocal-1.9 -I m4 --force
  autoheader
  automake-1.9 --add-missing --copy --include-deps
  autoconf
fi

%configure2_5x --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unnecessary files
rm -f %{buildroot}/%{_libdir}/scim-1.0/*/*/Helper/*.la

# fix install dir
mv %{buildroot}/%{_libdir}/scim-1.0/1.4.0/1.4.0/Helper/ \
   %{buildroot}/%{_libdir}/scim-1.0/1.4.0/
rm -rf %{buildroot}/%{_libdir}/scim-1.0/1.4.0/1.4.0/

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING
%{_bindir}/scim-tomoe
%{_datadir}/scim/icons/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/scim-1.0/*/Helper/*.so
