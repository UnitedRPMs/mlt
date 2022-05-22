%global commit0 576b4c7ab210c8edd1cbe04ad5b4d5f0b6c88cb6
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}
# 
#%define _legacy_common_support 1

%global debug_package %{nil}

%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%bcond_without ruby
%bcond_without php

Summary:        Toolkit for broadcasters, video editors, media players, transcoders
Name:           mlt
Version:        7.6.0
Release:        6%{?dist}

License:        GPLv3 and LGPLv2+
URL:            http://www.mltframework.org/twiki/bin/view/MLT/
Group:          System Environment/Libraries
Source0:        https://github.com/mltframework/mlt/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

Obsoletes:	mlt7 

BuildRequires:  cmake

BuildRequires:  frei0r-devel
BuildRequires:  rtaudio-devel
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  opencv-devel >= 4.5.0
BuildRequires:  opencv-static >= 4.5.0
BuildRequires:  qt-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qt3d-devel
BuildRequires:  libquicktime-devel
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_image-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_image-devel
BuildRequires:  gtk2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libogg-devel
BuildRequires:  swig >= 3.0.11
BuildRequires:	php-devel

#Deprecated dv, kino, and vorbis modules are not built.
#https://github.com/mltframework/mlt/commit/9d082192a4d79157e963fd7f491da0f8abab683f
#BuildRequires:  libdv-devel
#BuildRequires:  libvorbis-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  ladspa-devel
BuildRequires:  libxml2-devel
BuildRequires:  sox-devel
BuildRequires:  swig
BuildRequires:  python3-devel
BuildRequires:	python3-setuptools
BuildRequires:  freetype-devel
BuildRequires:  libexif-devel
BuildRequires:  fftw-devel
BuildRequires:  xine-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:	lua-devel
BuildRequires:	tcl-devel
BuildRequires:	ninja-build

BuildRequires:	vid.stab-devel
BuildRequires:	movit-devel
BuildRequires:	eigen3-devel
BuildRequires:	libebur128-devel
BuildRequires:	libatomic
BuildRequires:	chrpath
Provides:	mlt%{?_isa} = %{version}-%{release}

%if %{with ruby}
BuildRequires:  ruby-devel ruby
%endif

Requires:  opencv-core
Recommends:  %{name}-freeworld%{?_isa} = %{version}-%{release}


%description
MLT is an open source multimedia framework, designed and developed for 
television broadcasting.

It provides a toolkit for broadcasters, video editors,media players, 
transcoders, web streamers and many more types of applications. The 
functionality of the system is provided via an assortment of ready to use 
tools, xml authoring components, and an extendible plug-in based API.


%package devel
Summary:        Libraries, includes to develop applications with %{name}
License:        LGPLv2+
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:	mlt7-devel 

%package -n python3-mlt
Requires: python3
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes:	python3-mlt7 
Obsoletes:	mlt7-python3 
Summary: Python3 package to work with MLT

%if %{with ruby}
%package ruby
Requires: ruby >= 1.9.1
Requires: %{name}%{_isa} = %{version}-%{release}
Obsoletes:	mlt7-ruby 
Summary: Ruby package to work with MLT
%endif

%package freeworld
BuildRequires: ffmpeg-devel >= 5.0
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes:	mlt7-freeworld 
Summary: Freeworld support part of MLT.

%if %{with php}
%package php
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes:	mlt7-php 
Summary: PHP package to work with MLT
 
%description php
This module allows to work with MLT using PHP.
%endif

%description devel
The %{name}-devel package contains the header files and static libraries for
building applications which use %{name}.

%description -n python3-mlt
This module allows to work with MLT using python. 

%if %{with ruby}
%description ruby
This module allows to work with MLT using ruby.
%endif

%description freeworld
This package give us the freeworld (ffmpeg support) part of MLT.


%prep
%autosetup -n mlt-%{commit0} -p1

chmod 644 src/modules/qt/kdenlivetitle_wrapper.cpp
chmod 644 src/modules/kdenlive/filter_freeze.c
chmod -x demo/demo


%if 0%{?fedora} >= 26
# xlocale.h is gone in F26/RAWHIDE
sed -r -i 's/#include <xlocale.h>/#include <locale.h>/' src/framework/mlt_property.h
%endif

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
#find src/swig/python -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|'


%build
mkdir -p build
%cmake -B build  \
    -DMOD_OPENCV=ON \
    -DMOD_MOVIT=ON \
    -DSWIG_LUA=ON \
    -DSWIG_PYTHON=ON \
%if %{with php}
    -DSWIG_PHP=ON \
%endif
%if %{with ruby}
    -DSWIG_RUBY=ON  \
%endif
    
%make_build -C build


%install
%make_install -C build

chrpath --delete %{buildroot}/usr/bin/melt-7

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README*
%license COPYING GPL
%{_mandir}/man1/melt-7.1.gz
%{_bindir}/melt
%{_bindir}/melt-7
%{_libdir}/libmlt++-7.so.*
%{_libdir}/libmlt-7.so.*
%{_datadir}/mlt-7/

%files -n python3-mlt
%{python3_sitearch}/__pycache__/mlt7.cpython-*.pyc
%{python3_sitearch}/_mlt7.so
%{python3_sitearch}/mlt7.py


%if %{with ruby}
%files ruby
%{ruby_vendorarchdir}/mlt.so
%endif

%if %{with php}
%files php
%{php_extdir}/mlt.so
/usr/lib64/php/modules/mlt.php
%endif

%{_libdir}/mlt-7/libmltcore.so
%{_libdir}/mlt-7/libmltdecklink.so
%{_libdir}/mlt-7/libmltfrei0r.so
%{_libdir}/mlt-7/libmltgdk.so
%{_libdir}/mlt-7/libmltjackrack.so
%{_libdir}/mlt-7/libmltkdenlive.so
%{_libdir}/mlt-7/libmltmovit.so
%{_libdir}/mlt-7/libmltnormalize.so
%{_libdir}/mlt-7/libmltoldfilm.so
%{_libdir}/mlt-7/libmltopencv.so
%{_libdir}/mlt-7/libmltplus.so
%{_libdir}/mlt-7/libmltplusgpl.so
%{_libdir}/mlt-7/libmltqt.so
%{_libdir}/mlt-7/libmltresample.so
%{_libdir}/mlt-7/libmltrtaudio.so
%{_libdir}/mlt-7/libmltsdl.so
%{_libdir}/mlt-7/libmltsdl2.so
%{_libdir}/mlt-7/libmltsox.so
%{_libdir}/mlt-7/libmltvidstab.so
%{_libdir}/mlt-7/libmltxine.so
%{_libdir}/mlt-7/libmltxml.so

%files devel
%doc docs/* demo/
%{_libdir}/pkgconfig/mlt-framework-7.pc
%{_libdir}/pkgconfig/mlt++-7.pc
%{_libdir}/libmlt-7.so
%{_libdir}/libmlt++-7.so
%{_includedir}/mlt-7/


%{_libdir}/cmake/Mlt7/*.cmake


%files freeworld 
%{_libdir}/mlt-7/libmltavformat.so


%changelog

* Fri May 20 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.6.0-6
- Rebuilt

* Sat Apr 30 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.6.0-5
- Obsoletes mlt7

* Thu Mar 31 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.6.0-4
- Updated to 7.6.0

* Sat Jan 22 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.4.0-4
- Updated to 7.4.0

* Sat Nov 13 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.2.0-4
- Updated to 7.2.0

* Sat Jun 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.0.1-4
- Added missed packages

* Sat Jun 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.0.1-3
- Renamed fool subpackage

* Fri May 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 7.0.1-1
- Initial build
