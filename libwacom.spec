%define major		2
%define libname		%mklibname wacom %{major}
%define develname	%mklibname wacom -d

Name:		libwacom
Summary:	A library to identify wacom tablets
Epoch:		1
Version:	0.28
Release:	%mkrel 3
Group:		Development/X11
License:	MIT
URL:		http://sourceforge.net/projects/linuxwacom/
Source0:	http://prdownloads.sourceforge.net/linuxwacom/%{name}/%{name}-%{version}.tar.bz2


BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gudev-1.0)

%description
libwacom is a library to identify wacom tablets and their model-specific
features. It provides easy access to information such as "is this a built-in
on-screen tablet", "what is the size of this model", etc.

%files
%{_datadir}/libwacom
%{_udevrulesdir}/65-libwacom.rules

#-----------------------------------------------------------

%package -n %{libname}
Summary:	A library to identify wacom tablets
Group:		Development/X11
Requires:	%{name} >= %{epoch}:%{version}-%{release}

%description -n %{libname}
libwacom is a library to identify wacom tablets and their model-specific
features. It provides easy access to information such as "is this a built-in
on-screen tablet", "what is the size of this model", etc.

%files -n %{libname}
%{_libdir}/*.so.%{major}{,.*}
%_bindir/libwacom-list-local-devices

#-----------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{develname}
Development files for %{name}.

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

#-----------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

# auto-generate the udev rule from the database entries
mkdir -p %{buildroot}/%{_udevrulesdir}
pushd tools
./generate-udev-rules > %{buildroot}/%{_udevrulesdir}/65-libwacom.rules
popd
# Remove failed entries from rule file
sed -i '/failed/d' %{buildroot}/%{_udevrulesdir}/65-libwacom.rules

rm -f %{buildroot}%{_libdir}/*.la
