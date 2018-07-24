%define _default_patch_fuzz 2
%define gitshort 2cc35b0

Name:		vboot-utils
Version:	20180531
Release:	2.git%{gitshort}%{?dist}
Summary:	Verified Boot Utility from Chromium OS
License:	BSD
URL:		https://chromium.googlesource.com/chromiumos/platform/vboot_reference

ExclusiveArch:	%{arm} aarch64 %{ix86} x86_64

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone https://git.chromium.org/git/chromiumos/platform/vboot_reference.git
#  cd vboot_reference/
#  git archive --format=tar --prefix=vboot-utils-a1c5f7c/ a1c5f7c | xz > vboot-utils-a1c5f7c.tar.xz
Source0:	%{name}-%{gitshort}.tar.xz

## Patch0 disabled static building.
Patch0:		vboot-utils-00-disable-static-linking.patch

#make sure get the rpmbuild flags passed in
Patch1:		vboot-utils-cflags.patch

BuildRequires:  gcc
BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
BuildRequires:	libyaml-devel
BuildRequires:	xz-devel
BuildRequires:	libuuid-devel

# for the test scripts
BuildRequires:	python2

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.


%prep
%setup -q -n %{name}-%{gitshort}
%patch0 -p1 -b .nostatic
%patch1 -p1 -b .cflags


%build

%ifarch %{arm} aarch64
%global ARCH arm
%endif

%ifarch x86_64
%global ARCH x86_64
%endif

%ifarch i686
%global ARCH i386
%endif


make V=1 ARCH=%{ARCH} COMMON_FLAGS="$RPM_OPT_FLAGS"


%install
make install V=1 DESTDIR=%{buildroot}/usr ARCH=%{ARCH} COMMON_FLAGS="$RPM_OPT_FLAGS"

# Remove unneeded build artifacts
rm -rf %{buildroot}/usr/lib/pkgconfig/
rm -rf %{buildroot}/usr/default/

## Tests are enabled but ignored (will not break the build).
## This is because tests fail in a chroot (mock) but work otherwise.
%check
make runtests || true


%files
%license LICENSE
%doc README
%{_bindir}/*

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180531-2.git2cc35b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun  3 2018 Peter Robinson <pbrobinson@fedoraproject.org> 20180531-1.2cc35b0
- New upstream snapshot

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 20170302-5.gita1c5f7c
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20170302-4.gita1c5f7c
- Escape macros in %%changelog

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170302-3.gita1c5f7c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170302-2.gita1c5f7c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 20170302-1.gita1c5f7c
- Move to newer upstream snapshot needed for some devices
- Spec cleanups

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20130222gite6cf2c2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20130222gite6cf2c2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 20130222gite6cf2c2-7
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Jon Disnard <jdisnard@gmail.com> 20130222gite6cf2c2-3
- Clean up spec file
- Honor rpmbuild CFLAGS
- Fix strncat arguments in cgpt/cgpt_add.c

* Sat Feb 23 2013 Jon Disnard <jdisnard@gmail.com> 20130222gite6cf2c2-2
- Put back wcohen's fixes for i686 builds.
- Put back the patch to fix bmpblk_utility.cc printf formating %%ld -> %%zu
- Put back BR for gcc-c++ & libstdc++

* Fri Feb 22 2013 Jon Disnard <jdisnard@gmail.com> 20130222gite6cf2c2-1
- Pull upstream git
- Adjust ifarch conditionals to follow upstream changes in Makefile.
- Use XZ instead of BZIP2 for source archive, smaller SRPM size.
- Upstream fixed bug, so removing CC printf formating patch.
- Refactor patch that disabled static building for new Makefile.
- Enable test scripts again, but ignore failures (for mock builds).
- Remove BuildRequires for gcc-c++ & libstdc++, removed upstream.

* Tue Feb  5 2013 William Cohen <wcohen@redhat.c>  20130129git68f54d4-4
- Correct logic for setting 32-bit/64-bit x86.

* Tue Feb  5 2013 William Cohen <wcohen@redhat.c>  20130129git68f54d4-3
- Disable smp build because of problem with make dependencies

* Mon Feb  4 2013 William Cohen <wcohen@redhat.c>  20130129git68f54d4-2
- spec file clean up.

* Sat Jan  5 2013 Jon Disnard <jdisnard@gmail.com> 20130129git68f54d4-1
- Inception
- Patch0 prevents static building.
- Patch1 fixes minor printf formating bug in c++ code.
- tests disabled as they do not work in mock chroot.
