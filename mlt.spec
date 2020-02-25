%global commit0 af9b08853e4ce88733ec7e358ba6ae7af5c26fad
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}
# 
%define _legacy_common_support 1

%bcond_without ruby

Summary:        Toolkit for broadcasters, video editors, media players, transcoders
Name:           mlt
Epoch:		1
Version:        6.20.0
Release:        2%{?dist}

License:        GPLv3 and LGPLv2+
URL:            http://www.mltframework.org/twiki/bin/view/MLT/
Group:          System Environment/Libraries
Source0:        https://github.com/mltframework/mlt/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  frei0r-devel
BuildRequires:  opencv-devel >= 4.2.0
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qt3d-devel
BuildRequires:  libquicktime-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_image-devel
BuildRequires:  gtk2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libogg-devel
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
BuildRequires:	vid.stab-devel
BuildRequires:	movit-devel
BuildRequires:	eigen3-devel
BuildRequires:	libebur128-devel
BuildRequires:	libatomic
Provides:	mlt%{?_isa} = %{version}-%{release}

%if %{with ruby}
BuildRequires:  ruby-devel ruby
%else
Obsoletes: mlt-ruby < 0.8.8-5
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

%package -n python3-mlt
Requires: python3
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Python3 package to work with MLT

%package ruby
Requires: ruby >= 1.9.1
Requires: %{name}%{_isa} = %{version}-%{release}
Summary: Ruby package to work with MLT

%package lua
Requires: lua
Requires: %{name}%{_isa} = %{version}-%{release}
Summary: Lua package to work with MLT

%package tcl
Requires: tcl
Requires: %{name}%{_isa} = %{version}-%{release}
Summary: Tcl package to work with MLT

%package freeworld
BuildRequires: ffmpeg-devel >= 4.1
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Freeworld support part of MLT.


%description devel
The %{name}-devel package contains the header files and static libraries for
building applications which use %{name}.

%description -n python3-mlt
This module allows to work with MLT using python. 

%description ruby
This module allows to work with MLT using ruby.

%description lua
This module allows to work with MLT using Lua. 

%description tcl
This module allows to work with MLT using tcl. 

%description freeworld
This package give us the freeworld (ffmpeg support) part of MLT.


%prep
%autosetup -n %{name}-%{commit0} -p1

chmod 644 src/modules/qt/kdenlivetitle_wrapper.cpp
chmod 644 src/modules/kdenlive/filter_freeze.c
chmod -x demo/demo

# Don't overoptimize (breaks debugging)
sed -i -e '/fomit-frame-pointer/d' configure
sed -i -e '/ffast-math/d' configure

# respect CFLAGS LDFLAGS when building shared libraries. Bug #308873
	for x in python lua; do
		sed -i "/mlt.so/s: -lmlt++ :& ${CFLAGS} ${LDFLAGS} :" src/swig/$x/build || die
	done

# swig fix
sed -i "/^LDFLAGS/s: += :& ${LDFLAGS} :" src/swig/ruby/build

%if 0%{?fedora} >= 26
# xlocale.h is gone in F26/RAWHIDE
sed -r -i 's/#include <xlocale.h>/#include <locale.h>/' src/framework/mlt_property.h
%endif

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find src/swig/python -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|'


%build

#export STRIP=/bin/true
%configure \
	--avformat-swscale 			\
        --enable-gpl                            \
        --enable-gpl3                           \
        --enable-motion-est                     \
%ifarch ppc ppc64
        --disable-mmx                           \
        --disable-sse                           \
        --disable-xine                          \
%endif
        --rename-melt=%{name}-melt              \
        --swig-languages="lua python ruby tcl"

make %{?_smp_mflags}


%install

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Quick_Opt-Out
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

make DESTDIR=%{buildroot} install

# manually do what 'make install' skips
install -D -pm 0644 src/swig/python/mlt.py %{buildroot}%{python3_sitelib}/mlt.py
install -D -pm 0755 src/swig/python/_mlt.so %{buildroot}%{python3_sitearch}/_mlt.so

%if %{with ruby}
install -D -pm 0755 src/swig/ruby/play.rb %{buildroot}%{ruby_vendorlibdir}/play.rb
install -D -pm 0755 src/swig/ruby/thumbs.rb %{buildroot}%{ruby_vendorlibdir}/thumbs.rb
install -D -pm 0755 src/swig/ruby/mlt.so %{buildroot}%{ruby_vendorarchdir}/mlt.so
%endif

mv src/modules/motion_est/README README.motion_est

# LUA
lua_ver=$(lua -v | awk '{print $2}' | cut -c-3)
pushd src/swig/lua
install -D -m 0755 mlt.so %{buildroot}/%{_libdir}/lua/$lua_ver/mlt.so
install -D -m 0644 play.lua %{buildroot}/%{_docdir}/mlt-%{version}/play.lua
popd

# TCL
tcl_ver=$(echo 'puts $tcl_version;exit 0' | tclsh)
pushd src/swig/tcl
install -D -m 0755 mlt.so %{buildroot}/%{_libdir}/tcl$tcl_ver/mlt.so
install -D -m 0755 play.tcl %{buildroot}/%{_docdir}/mlt-%{version}/play.tcl
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS README*
%license COPYING GPL
%{_bindir}/mlt-melt
%{_libdir}/mlt/
%{_libdir}/libmlt++.so.*
%{_libdir}/libmlt.so.*
%{_datadir}/mlt/

%files -n python3-mlt
%{python3_sitelib}/mlt.py*
%{python3_sitearch}/_mlt.so
%{python3_sitelib}/__pycache__/mlt.*

%if %{with ruby}
%files ruby
%{ruby_vendorlibdir}/play.rb
%{ruby_vendorlibdir}/thumbs.rb
%{ruby_vendorarchdir}/mlt.so
%endif

%files lua
%{_libdir}/lua/*/mlt.so
%{_datadir}/doc/mlt-%{version}/play.lua

%files tcl
%{_libdir}/tcl*/mlt.so
%{_datadir}/doc/mlt-%{version}/play.tcl

%files devel
%doc docs/* demo/
%{_libdir}/pkgconfig/mlt-framework.pc
%{_libdir}/pkgconfig/mlt++.pc
%{_libdir}/libmlt.so
%{_libdir}/libmlt++.so
%{_includedir}/mlt/
%{_includedir}/mlt++/

%files freeworld 
%{_libdir}/mlt/libmltavformat.so


%changelog

* Sun Feb 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1:6.20.0-2
- Updated to 6.20.0

* Sun Dec 29 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.18.0-2.git221ff23
- Rebuilt for opencv

* Mon Nov 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.18.0-1.git221ff23
- Updated to 6.18.0-1.git221ff23

* Mon Oct 14 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.16.0-3.git434dbcf
- Updated to june commit stable
- Drop python2 package and fix compatibility

* Sat May 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.16.0-2.git02bc879
- Updated to 6.16.0

* Thu Dec 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.12.0-2.gitf608b96
- Python2 fix
- Rebuilt for ffmpeg

* Fri Nov 30 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.12.0-1.gitf608b96
- Updated to 6.12.0-1.gitf608b96

* Sun Oct 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.10.0-4.git4171072
- Rebuilt for opencv

* Tue Jul 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.10.0-2.git4171072
- Updated to 6.10.0-2.git4171072

* Sat May 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.8.0-2.gitc1ef8ae
- Compatibility patch

* Sat May 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.8.0-1.gitc1ef8ae
- Updated to 6.8.0-1.gitc1ef8ae

* Mon Apr 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.6.0-4.gitd7dfb47
- Updated to current commit stable

* Fri Apr 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.6.0-3
- Rebuilt for opencv

* Tue Feb 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.6.0-2
- Rebuilt for movit 1.6.0

* Wed Jan 24 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.6.0-1
- Updated to 6.6.0

* Sat Oct 07 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.4.1-9
- Fix build with glibc 2.26 
- vid.stab enabled 

* Sat Aug 12 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.4.1-8  
- Fix kdenlive crash on exit

* Tue Apr 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 6.4.1-7  
- Automatic Mass Rebuild

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 6.4.1-6
- Rebuilt for libbluray

* Sat Feb 25 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 6.4.1-5
- Updated to 6.4.1-5

* Fri Sep 02 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 6.2.0-5
- Our MLT provides a separated mlt-freeworld with ffmpeg support. MLT is now provided officially for Fedora without ffmpeg support.

* Thu Jun 30 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 6.2.0-4
- Enabled lua
- Enabled tcl

* Sun Jun 26 2016 The UnitedRPMs Project (Key for UnitedRPMs infrastructure) <unitedrpms@protonmail.com> - 6.2.0-3
- Rebuild with new ffmpeg

* Wed May 25 2016 Sérgio Basto <sergio@serjux.com> - 6.2.0-2
- Bump release

* Thu Apr 21 2016 Sérgio Basto <sergio@serjux.com> - 6.2.0-1
- Update MLT to 6.2.0

* Sun Feb 21 2016 Sérgio Basto <sergio@serjux.com> - 6.0.0-2
- Add license tag. 
- More spec modernizations and rpmlint fixes.
- Configure conditional build for Ruby.
- Remove old BuilRequires that aren't needed anymore. 
- Remove old config options (avformat-swscale and qimage-libdir) that no longer
  exist in configure.
- Fix Ruby build.

* Fri Feb 19 2016 Sérgio Basto <sergio@serjux.com> - 6.0.0-1
- Update 6.0.0 (This is a bugfix and minor enhancement release. Note that our
  release versioning scheme has changed. We were approaching 1.0 but decided to
  synchronize release version with the C library ABI version, which is currently
  at v6)
- Switch to qt5 to fix rfbz #3810 and copy some BRs from Debian package.

* Wed Nov 18 2015 Sérgio Basto <sergio@serjux.com> - 0.9.8-1
- Update MLT to 0.9.8

* Mon May 11 2015 Sérgio Basto <sergio@serjux.com> - 0.9.6-2
- Workaround #3523

* Thu May 07 2015 Sérgio Basto <sergio@serjux.com> - 0.9.6-1
- Update mlt to 0.9.6 .
- Added BuildRequires of libexif-devel .

* Thu May 07 2015 Sérgio Basto <sergio@serjux.com> - 0.9.2-4
- Added BuildRequires of opencv-devel, rfbz #3523 .

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.9.2-3
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.9.2-2
- Rebuilt for FFmpeg 2.4.x

* Mon Sep 15 2014 Sérgio Basto <sergio@serjux.com> - 0.9.2-1
- New upstream release.

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-6
- Rebuilt for ffmpeg-2.3

* Sat Jul 26 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-5
- Rebuild for new php, need by mlt-php

* Sun Mar 30 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-4
- Rebuilt for ffmpeg-2.2 and fix for freetype2 changes.

* Wed Dec 04 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-3
- Update License tag .

* Wed Nov 20 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-2
- Enable gplv3 as asked in rfbz #3040
- Fix a changelog date.
- Fix Ruby warning with rpmbuild "Use RbConfig instead of obsolete and deprecated Config". 
- Remove obsolete tag %%clean and rm -rf 

* Mon Oct 07 2013 Sérgio Basto <sergio@serjux.com> - 0.9.0-1
- Update to 0.9.0

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-7
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-6
- Rebuilt for FFmpeg 2.0.x

* Mon Jun 10 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.8-5
- mlt-ruby FTBFS, omit until fixed (#2816)

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-4
- Rebuilt for x264/FFmpeg

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Feb 1  2013 Ryan Rix <ry@n.rix.si> - 0.8.8-1
- Fix ABI requirement to Ruby 1.9

* Fri Feb 1  2013 Ryan Rix <ry@n.rix.si> - 0.8.8-1
- Update to 0.8.8

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8.6-2
- Rebuilt for ffmpeg

* Sun Dec 30 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.6-1
- Update to 0.8.6

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-3
- Rebuilt for FFmpeg 1.0

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-2
- Rebuilt for FFmpeg

* Tue Jun 19 2012 Richard Shaw <hobbes1069@gmail.com> - 0.8.0-1
- Update to latest upstream release.

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 0.7.8-3
- fix filter

* Thu Jun 14 2012 Remi Collet <remi@fedoraproject.org> 0.7.8-2
- update PHP requirement for PHP Guildelines
- add php extension configuration file
- filter php private shared so

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-1
- 0.7.8

* Tue May 08 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-8
- rebuild (sox)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-7
- Rebuilt for c++ ABI breakage

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-6
- Rebuilt for x264/FFmpeg

* Fri Jan 27 2012 Ryan Rix <ry@n.rix.si> 0.7.6-5
- Include patch to fix building on gcc47 (upstreaming)

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Ryan Rix <ry@n.rix.si> 0.7.6-3
- s/%%[?_isa}/%%{?_isa}

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-2
- rebuild

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.6-1
- 0.7.6
- track files/sonames closer
- tighten subpkg deps via %%{?_isa}
- drop dup'd %%doc items

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-2
- Rebuilt for ffmpeg-0.8

* Thu Jul 21 2011 Ryan Rix <ry@n.rix.si> - 0.7.4-1
- New upstream

* Sun Apr 10 2011 Ryan Rix <ry@n.rix.si> - 0.7.0-2
- Add SDL_image-devel BR per Kdenlive wiki page

* Thu Apr 7 2011 Ryan Rix <ry@n.rix.si> - 0.7.0-1
- New upstream

* Tue Dec 21 2010 Ryan Rix <ry@n.rix.si> - 0.5.4-2
- Fix build, needed a patch from mlt's git repo.

* Sat Nov 20 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.5.4-1.1
- rebuilt - was missing in repo

* Wed Apr 21 2010 Ryan Rix <ry@n.rix.si> - 0.5.4-1
- New upstream version to fix reported crashes against Kdenlive

* Fri Feb 19 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-2
- disabled xine module for PPC arch.

* Thu Feb 18 2010 Zarko Pintar <zarko.pintar@gmail.com> - 0.5.0-1
- new version

* Wed Dec 09 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.10-1
- new version
- added subpackage for ruby

* Wed Oct 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.6-1
- new version
- added subpackages for: python, PHP

* Mon Sep 07 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.4-1
- new version
- renamed melt binary to mlt-melt

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.2-1
- new version
- removed obsolete patches

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-3
- added linker and license patches
- set license of MLT devel subpackage to LGPLv2+ 

* Wed May 20 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-2
- some PPC clearing

* Mon May 18 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.4.0-1
- update to 0.4.0

* Wed May 13 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-2
- spec cleaning

* Mon May 11 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.9-1
- new release
- MLT++  is now a part of this package

* Fri May  8 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-3
- unused-direct-shlib-dependency fix

* Fri Apr 17 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-2
- spec clearing
- added patches for resolving broken lqt-config, lib64 and execstack

* Wed Apr 15 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.8-1
- New release

* Thu Apr  9 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-3
- Enabled MMX support (not for PPC & PPC64)
- include demo files
- some spec cosmetics

* Thu Mar 12 2009 Zarko Pintar <zarko.pintar@gmail.com> - 0.3.6-2
- Change URL address
- devel Requires: pkgconfig

* Fri Feb 20 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.3.6-1
- Update to 0.3.6

* Wed Nov  5 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.1-0.1.svn1180
- update to upstream r1180
- add --avformat-swscale configure option

* Tue Nov  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.3.0-5
- rebuilt with proper qt4 paths

* Mon Oct 13 2008 jeff <moe@blagblagblag.org> - 0.3.0-4
- Build without fomit-frame-pointer ffmath
- Add BuildRequires: prelink
- clear-execstack libmltgtk2.so
- Don't strip binaries
- Group: Development/Libraries
- Prefix albino, humperdink, and miracle binaries with mlt-

* Sun Oct  5 2008 jeff <moe@blagblagblag.org> - 0.3.0-3
- License: GPLv2+ and LGPLv2+
- Group: Development/Tools
- ExcludeArch: x86_64 s390 s390x ppc ppc64
- %%defattr(-,root,root)
- %%doc docs/
- %%{_libdir}/%%{name} to main package


* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-2
- Change BuildRoot:
- Full source URL
- ExcludeArch: x86_64
- -devel Requires: pkgconfig, Requires: %%{name} = %%{version}-%%{release}

* Sun Aug 24 2008 jeff <moe@blagblagblag.org> - 0.3.0-1
- Update to 0.3.0
- --enable-gpl
- mlt-filehandler.patch

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f10
- Build for blaghead

* Mon Jul  7 2008 jeff <moe@blagblagblag.org> - 0.2.5-0.svn1155.0blag.f9
- Update to svn r1155
- Remove sox-st.h.patch
- Add configure --disable-sox as it breaks build

* Sun Nov 11 2007 jeff <moe@blagblagblag.org> - 0.2.4-0blag.f7
- Update to 0.2.4
- Clean up spec

* Sat Jun 23 2007 jeff <moe@blagblagblag.org> - 0.2.3-0blag.f7
- Update to 0.2.3

* Sat Dec 30 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc6
- Rebuild for 60k
- Remove --disable-sox
- Add mlt-0.2.2-sox-st.h.patch

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.2-0blag.fc5
- Update to 0.2.2

* Sat Oct 21 2006 jeff <moe@blagblagblag.org> - 0.2.1-0blag.fc5
- BLAG'd
- Removed "olib" from path, name, etc.
- Add changelog
- Update summary/description
