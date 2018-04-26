# Set up a new macro to define MOC's 'mocp' executable
%global   exec   mocp

# Globals for svn 
# Get current revision:
# svn info svn://svn.daper.net/moc/trunk 
%global svn_rev 2963
%global svn_url svn://svn.daper.net/moc/trunk
%global svn_ver .svn%{svn_rev}

Name:    moc
Summary: Music on Console - Console audio player for Linux/UNIX
Version: 2.6
Release: 	1.21%{?svn_ver}%{?dist}
License: GPLv2+ and GPLv3+
URL:     http://moc.daper.net

Source0: %{name}-%{svn_rev}.tar.gz
Patch:   TiMidity_Config.patch
Patch1:  ffmpeg4_fix.patch

BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(alsa) 
BuildRequires: pkgconfig(jack)
BuildRequires: pkgconfig(libcurl) 
BuildRequires: pkgconfig(samplerate) 
BuildRequires: pkgconfig(taglib) 
BuildRequires: pkgconfig(speex) 
BuildRequires: pkgconfig(id3tag) 
BuildRequires: pkgconfig(vorbis) 
BuildRequires: pkgconfig(flac) 
BuildRequires: pkgconfig(zlib) 
BuildRequires: pkgconfig(sndfile) 
BuildRequires: pkgconfig(libmodplug) 
BuildRequires: pkgconfig(libtimidity) 
BuildRequires: pkgconfig(wavpack) 
BuildRequires: libdb-devel 
BuildRequires: libtool-ltdl-devel 
BuildRequires: gettext-devel 
BuildRequires: pkgconfig(opus)
BuildRequires: libtool
BuildRequires: librcc-devel
BuildRequires: popt-devel
BuildRequires: ffmpeg-devel >= 4.0
BuildRequires: libmad-devel
BuildRequires: faad2-devel

BuildRequires: autoconf, automake

%description
MOC (music on console) is a console audio player for LINUX/UNIX designed to be
powerful and easy to use. You just need to select a file from some directory
using the menu similar to Midnight Commander, and MOC will start playing all
files in this directory beginning from the chosen file.

Configuration
Sample configuration file can be found in /usr/share/doc/moc/config.example. On mocp first run the local ~/.moc/ directory is created. To configure, copy the examples to it and edit accordingly.
cp -f /usr/share/doc/moc/config.example ~/.moc/config

%prep
%autosetup -n %{name}-%{svn_rev} -p1

%build
autoreconf -ivf

%configure --disable-static --disable-silent-rules --disable-rpath --with-rcc \
 --with-oss --with-alsa --with-jack --with-aac --with-mp3 \
 --with-musepack --with-vorbis --with-flac --with-wavpack \
 --with-sndfile --with-modplug --with-ffmpeg --with-speex \
 --with-samplerate --with-curl --disable-cache --disable-debug --without-magic \
 CPPFLAGS="-I%{_includedir}/libdb -fPIC" 
 
%make_build

%install
%make_install
install -dm 755 %{buildroot}/%{_sysconfdir}/mocp
echo 'default /tmp/timidity.tmp' >> %{buildroot}/%{_sysconfdir}/mocp/timidity.cfg

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -f $RPM_BUILD_ROOT%_libdir/*.la
rm -f $RPM_BUILD_ROOT%_libdir/moc/decoder_plugins/*.la

%files
%doc README README_equalizer AUTHORS ChangeLog config.example keymap.example NEWS
%license COPYING
%{_bindir}/%{exec}
%{_datadir}/%{name}/
%{_mandir}/man1/%{exec}.*
%{_libdir}/%{name}/
%{_sysconfdir}/mocp/timidity.cfg

%changelog

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.6-1.21.svn2963  
- Automatic Mass Rebuild

* Sat Apr 21 2018 David Vásquez <davidva AT tutanota DOT com> - 2.6-1.2.svn2963
- Updated to 2.6-1.2.svn2963

* Sat Jan 20 2018 David Vásquez <davidva AT tutanota DOT com> - 2.6-1.1.svn2961
- Changed to svn sources

* Tue Jan 16 2018 David Vásquez <davidva AT tutanota DOT com> - 2.6-1.gitdceb31b
- Updated to 2.6-1.gitdceb31b

* Wed Oct 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.6-0.18  
- Automatic Mass Rebuild

* Wed May 31 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 2.6-0.17  
- Automatic Mass Rebuild

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.6-0.16
- Rebuilt for libbluray

* Thu Aug 11 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.6-0.15
- Updated to alpha 3

* Thu Aug 11 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 2.6-0.13.alpha2
- Upstream

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.6-0.12.alpha2
- Rebuilt for ffmpeg-3.1.1

* Thu Jul 07 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.11.alpha2
- Add ffmpeg as Requires package

* Sun Jun 05 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.10.alpha2
- Update to commit 2880
- Rebuild for ffmpeg 2.8.7

* Mon May 16 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.9.alpha2
- Fix faad2 dependencies

* Mon Apr 25 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.8.alpha2
- ldconfig commands removed

* Thu Jan 28 2016 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.7.alpha2
- Force -fstack-protector-all
- Tries upstream patch

* Sun Nov 01 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.6.alpha1
- Hardened builds on <F23

* Tue Sep 29 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.5.alpha1
- Update to svn commit #2776
- Used %%license macro

* Tue Mar 24 2015 Antonio Trande <sagitter@fedoraproject.org> - 2.6-0.4.alpha1
- Update to svn commit #2770

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 2.6-0.3.alpha1
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-0.2.alpha1
- Rebuilt for FFmpeg 2.4.x

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.6-0.1.alpha1
- Leap to 2.6-alpha1 release

* Tue Sep 02 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-2
- Spec cleanups

* Sat Aug 30 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-1
- Update to release 2.5.0 (Consolidation)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 2.5.0-0.16.beta2
- Rebuilt for ffmpeg-2.3
- Conditional builds for ARM

* Tue May 13 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.15.beta2
- New svn commit of MOC-2.5.0 pre-release (r2641)

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> 2.5.0-0.14.beta2
- Rebuilt for ffmpeg-2.2

* Thu Mar 20 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.13.beta2
- New svn commit of MOC-2.5.0 pre-release
- Fixed release increment number for the pre-releases

* Wed Feb 26 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.12.beta2
- Fix unstripped-binary-or-object warnings for ARM builds

* Wed Feb 05 2014 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.11.beta2
- Update to 2.5.0-beta2
- Removed previous patches

* Tue Jun 18 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.10.beta1
- Added patchset to fix "Unsupported sample size!" error
  See http://moc.daper.net/node/862 for more details
- Added patch for 'sizeof' argument bug
- Added BR: Autoconf and Automake-1.13 (temporarily)
- 'configure.in' renaming

* Sat Jun 08 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.9.beta1
- Removed some explicit Requires (curl, jack-audio-connection-kit, ncurses, speex)

* Fri Jun 07 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.8.beta1
- Fixed Source0 line
- Package owns %%{_libdir}/%%{name} directory

* Mon May 20 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.7.beta1
- Dist tag changed to %%{?dist}

* Tue Apr 09 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.6.beta1
- Removed autoreconf task from %%build section

* Fri Apr 05 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.5.beta1
- Removed libRCC explicit require

* Sun Mar 03 2013 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.4.beta1
- Removed DESTDIR from %%make_install
- Changed source link with a public one
- Set up a new macro to define MOC's 'mocp' executable
- Added %%{name} prefix to the patch

* Tue Dec 25 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.3.beta1
- Added librcc support (fixes encoding in broken mp3 tags)

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.2.beta1
- Added patch to fix FSF address

* Mon Oct 22 2012 Antonio Trande <sagitter@fedoraproject.org> 2.5.0-0.1.beta1
- 2.5.0-beta1
