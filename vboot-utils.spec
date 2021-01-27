%define gitshort 595108c0

Name:		vboot-utils
Version:	20190823
Release:	6.git%{gitshort}%{?dist}
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

# Fix FTBFS agsinst gcc10
Patch0:		vboot-utils-595108c0-gcc10.patch

BuildRequires: make
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	glibc-static
BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
BuildRequires:	libyaml-devel
BuildRequires:	xz-devel
BuildRequires:	libuuid-devel

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.


%prep
%autosetup -p1 -n %{name}-%{gitshort}

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


%files
%license LICENSE
%doc README
%{_bindir}/*

%changelog
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20190823-6.git595108c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190823-5.git595108c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 01 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 20190823-4.git595108c0
- Drop tests to drop python2 dep

* Thu Feb 27 2020 Than Ngo <than@redhat.com> - 20190823-3.git595108c
- Fix FTBFS

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190823-2.git595108c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Peter Robinson <pbrobinson@fedoraproject.org> 20190823.1.git595108c0
- Rebase to upstream 595108c0 snapshot

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180531-4.git2cc35b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180531-3.git2cc35b0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

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
