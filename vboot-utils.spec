Name:		vboot-utils
Version:	20130222gite6cf2c2
Release:	7%{?dist}
Summary:	Verified Boot Utility from Chromium OS
ExclusiveArch:	%{arm} %{ix86} x86_64

Group:		Applications/System
License:	BSD
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone https://git.chromium.org/git/chromiumos/platform/vboot_reference.git
#  cd vboot_reference/
#  git archive --format=tar --prefix=vboot-utils-20130222gite6cf2c2/ e6cf2c2 | xz > vboot-utils-20130222gite6c.tar.xz
URL:		http://gitrw.chromium.org/gitweb/?p=chromiumos/platform/vboot_reference.git
Source0:	%{name}-%{version}.tar.xz


## Patch0 disabled static building.
Patch0:		vboot-utils-00-disable-static-linking.patch

## Patch1 fixes printf formating issues that break  the build.
## http://code.google.com/p/chromium-os/issues/detail?id=37804
Patch1:		vboot-utils-01-bmpblk_utility-fix-printf.patch

#make sure get the rpmbuild flags passed in
Patch2:		vboot-utils-cflags.patch

# some fixes for picker compile
Patch3:		vboot-utils-strncat.patch
Patch4:		vboot-utils-unused.patch
Patch5:		vboot-utils-pthread.patch


BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
BuildRequires:	libyaml-devel
BuildRequires:	xz-devel
BuildRequires:	libuuid-devel


# for the test scripts
BuildRequires:	python

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.


%prep
%setup -q
%patch0 -p0 -b .nostatic
%patch1 -p0 -b .fixprintf
%patch2 -p1 -b .cflags
%patch3 -p1 -b .strncat
%patch4 -p1 -b .unused
%patch5 -p1 -b .pthread


%build

%ifarch %{arm}
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
make install V=1 DESTDIR=%{buildroot}%{_bindir} ARCH=%{ARCH} COMMON_FLAGS="$RPM_OPT_FLAGS"


## Tests are enabled but ignored (will not break the build).
## This is because tests fail in a chroot (mock) but work otherwise.
%check
make runtests || true


%files
%{_bindir}/*
%doc LICENSE README

%changelog
* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 20130222gite6cf2c2-7
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130222gite6cf2c2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 07 2013 Jon Disnard <jdisnard@gmail.com> 20130222gite6cf2c2-3
- Clean up spec file
- Honor rpmbuild CFLAGS
- Fix strncat arguments in cgpt/cgpt_add.c

* Sat Feb 23 2013 Jon Disnard <jdisnard@gmail.com> 20130222gite6cf2c2-2
- Put back wcohen's fixes for i686 builds.
- Put back the patch to fix bmpblk_utility.cc printf formating %ld -> %zu
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

