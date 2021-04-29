Name:           vmaf
Version:        2.1.1
Release:        2%{?dist}
Summary:        Video Multi-Method Assessment Fusion
License:        BSD-2-Clause-Patent
URL:            https://github.com/netflix/vmaf

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# This project relies on AVX
ExclusiveArch:  x86_64

BuildRequires:  meson
BuildRequires:  nasm
BuildRequires:  vim-common

%if 0%{?rhel} == 7
BuildRequires:  devtoolset-9-gcc-c++
%else
BuildRequires:  gcc-c++
%endif

# Enforce our own build version for library
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description
VMAF is a perceptual video quality assessment algorithm developed by Netflix.
VMAF Development Kit (VDK) is a software package that contains the VMAF
algorithm implementation, as well as a set of tools that allows a user to train
and test a custom VMAF model.

%package -n     lib%{name}
Summary:        Library for %{name}
Provides:       bundled(libsvm) = 3.24

%description -n lib%{name}
Library for Video Multi-Method Assessment Fusion.

%package -n     lib%{name}-devel
Summary:        Development files for %{name}
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n lib%{name}-devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%autosetup -p1
# Unbundle
rm -rf third_party/

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-9/enable
%endif

pushd lib%{name}
%meson -Ddefault_library=shared
%meson_build
popd

%install
pushd lib%{name}
%meson_install
popd

%check
pushd lib%{name}
ninja -vC %{_vpath_builddir} test
popd

%ldconfig_scriptlets -n lib%{name}

%files
%doc FAQ.md README.md
%{_bindir}/%{name}

%files -n lib%{name}
%license LICENSE
%doc CHANGELOG.md
%{_libdir}/lib%{name}.so.1*

%files -n lib%{name}-devel
%doc CONTRIBUTING.md
%{_includedir}/lib%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%changelog
* Thu Apr 29 2021 Simone Caronni <negativo17@gmail.com> - 2.1.1-2
- Clean up & build on CentOS 7/8.

* Wed Mar 10 2021 Leigh Scott <leigh123linux@gmail.com> - 2.1.1-1
- Update to 2.1.1
