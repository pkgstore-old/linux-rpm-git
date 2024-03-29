# Pass --without docs to rpmbuild if you don't want the documentation.
%bcond_without docs

# Pass --without tests to rpmbuild if you don't want to run the tests.
%bcond_without tests

%global gitexecdir          %{_libexecdir}/git-core

# Settings for Fedora >= 34.
%if 0%{?fedora} >= 34
%bcond_with                 emacs
%else
%bcond_without              emacs
%endif

# Settings for Fedora.
%if 0%{?fedora}
# linkchecker is not available on EL.
%bcond_without              linkcheck
%else
%bcond_with                 linkcheck
%endif

# Settings for Fedora and EL >= 9.
%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without              asciidoctor
%else
%bcond_with                 asciidoctor
%endif

# Settings for Fedora and EL >= 8.
%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_with                 python2
%bcond_without              python3
%global gitweb_httpd_conf   gitweb.conf
%global use_glibc_langpacks 1
%global use_perl_generators 1
%global use_perl_interpreter 1
%else
%bcond_without              python2
%bcond_with                 python3
%global gitweb_httpd_conf   git.conf
%global use_glibc_langpacks 0
%global use_perl_generators 0
%global use_perl_interpreter 0
%endif

# Settings for Fedora and EL >= 7.
%if 0%{?fedora} || 0%{?rhel} >= 7
%global bashcompdir         %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global bashcomproot        %(dirname %{bashcompdir} 2>/dev/null)
%endif

# Allow cvs subpackage to be toggled via --with/--without.
# Disable cvs subpackage by default on EL >= 8.
%if 0%{?rhel} >= 8
%bcond_with                 cvs
%else
%bcond_without              cvs
%endif

# Allow credential-libsecret subpackage to be toggled via --with/--without.
%bcond_without              libsecret

# Allow p4 subpackage to be toggled via --with/--without.
# Disable by default if we lack python2 or python3 support.
%if %{with python2} || %{with python3}
%bcond_without              p4
%else
%bcond_with                 p4
%endif

# Hardening flags for EL-7.
%if 0%{?rhel} == 7
%global _hardened_build     1
%endif

# Define for release candidates.
# global rcrev   .rc0

%global release_prefix          100

Name:                           git
Version:                        2.32.0
Release:                        %{release_prefix}%{?rcrev}%{?dist}
Summary:                        Fast Version Control System
License:                        GPLv2
URL:                            https://git-scm.com
Vendor:                         Package Store <https://pkgstore.github.io>
Packager:                       Kitsune Solar <kitsune.solar@gmail.com>

Source0:                        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{version}%{?rcrev}.tar.xz
Source1:                        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}%{name}-%{version}%{?rcrev}.tar.sign

# Junio C Hamano's key is used to sign git releases, it can be found in the
# junio-gpg-pub tag within git.
#
# (Note that the tagged blob in git contains a version of the key with an
# expired signing subkey. The subkey expiration has been extended on the
# public keyservers, but the blob in git has not been updated.)
#
# https://git.kernel.org/cgit/git/git.git/tag/?h=junio-gpg-pub
# https://git.kernel.org/cgit/git/git.git/blob/?h=junio-gpg-pub&id=7214aea37915ee2c4f6369eb9dea520aec7d855b
Source2:                        gpgkey-junio.asc

# Local sources begin at 10 to allow for additional future upstream sources.
Source11:                       git.xinetd.in
Source12:                       git-gui.desktop
Source13:                       gitweb-httpd.conf
Source14:                       gitweb.conf.in
Source15:                       git@.service.in
Source16:                       git.socket

# Script to print test failure output (used in %%check).
Source99:                       print-failed-test-output

# https://bugzilla.redhat.com/490602
Patch0:                         git-cvsimport-Ignore-cvsps-2.2b1-Branches-output.patch

%if %{with docs}
# pod2man is needed to build "Git.3pm".
BuildRequires:                  %{_bindir}/pod2man
%if %{with asciidoctor}
BuildRequires:                  docbook5-style-xsl
BuildRequires:                  rubygem-asciidoctor
%else
BuildRequires:                  asciidoc >= 8.4.1
%endif
# endif with asciidoctor.
BuildRequires:                  perl(File::Compare)
BuildRequires:                  xmlto
%if %{with linkcheck}
BuildRequires:                  linkchecker
%endif
# endif with linkcheck.
%endif
# endif with docs.
BuildRequires:                  coreutils
BuildRequires:                  desktop-file-utils
BuildRequires:                  diffutils
%if %{with emacs}
BuildRequires:                  emacs-common
%endif
# endif emacs-common.
%if 0%{?rhel} && 0%{?rhel} < 9
# Require epel-rpm-macros for the %%gpgverify macro on EL-7/EL-8, and
# %%build_cflags & %%build_ldflags on EL-7.
BuildRequires:                  epel-rpm-macros
%endif
# endif rhel < 9.
BuildRequires:                  expat-devel
BuildRequires:                  findutils
BuildRequires:                  gawk
BuildRequires:                  gcc
BuildRequires:                  gettext
BuildRequires:                  gnupg2
BuildRequires:                  libcurl-devel
BuildRequires:                  make
BuildRequires:                  openssl-devel
BuildRequires:                  pcre2-devel
BuildRequires:                  perl(Error)
BuildRequires:                  perl(lib)
BuildRequires:                  perl(Test)
%if %{use_perl_generators}
BuildRequires:                  perl-generators
%endif
# endif use_perl_generators.
%if %{use_perl_interpreter}
BuildRequires:                  perl-interpreter
%else
BuildRequires:                  perl
%endif
# endif use_perl_interpreter.
BuildRequires:                  pkgconfig(bash-completion)
BuildRequires:                  sed
# For macros.
BuildRequires:                  systemd
BuildRequires:                  tcl
BuildRequires:                  tk
BuildRequires:                  xz
BuildRequires:                  zlib-devel >= 1.2

%if %{with tests}
# Test suite requirements.
BuildRequires:                  acl
%if 0%{?fedora} || 0%{?rhel} >= 8
# Needed by "t5540-http-push-webdav.sh".
BuildRequires:                  apr-util-bdb
%endif
# endif fedora >= 27.
BuildRequires:                  bash
%if %{with cvs}
BuildRequires:                  cvs
BuildRequires:                  cvsps
%endif
# endif with cvs.
%if %{use_glibc_langpacks}
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:                  glibc-all-langpacks
BuildRequires:                  glibc-langpack-en
BuildRequires:                  glibc-langpack-is
%endif
# endif use_glibc_langpacks.
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires:                  gnupg2-smime
%endif
# endif fedora or el >= 9.
%if 0%{?fedora} || ( 0%{?rhel} >= 7 && ( "%{_arch}" == "ppc64le" || "%{_arch}" == "x86_64" ) )
BuildRequires:                  highlight
%endif
# endif fedora or el7+ (ppc64le/x86_64).
BuildRequires:                  httpd
%if 0%{?fedora} && ! ( 0%{?fedora} >= 35 || "%{_arch}" == "i386" || "%{_arch}" == "s390x" )
BuildRequires:                  jgit
%endif
# endif fedora (except i386 and s390x).
BuildRequires:                  mod_dav_svn
BuildRequires:                  perl(App::Prove)
BuildRequires:                  perl(CGI)
BuildRequires:                  perl(CGI::Carp)
BuildRequires:                  perl(CGI::Util)
BuildRequires:                  perl(DBD::SQLite)
BuildRequires:                  perl(Digest::MD5)
BuildRequires:                  perl(Fcntl)
BuildRequires:                  perl(File::Basename)
BuildRequires:                  perl(File::Copy)
BuildRequires:                  perl(File::Find)
BuildRequires:                  perl(filetest)
BuildRequires:                  perl(HTTP::Date)
BuildRequires:                  perl(IO::Pty)
BuildRequires:                  perl(JSON)
BuildRequires:                  perl(JSON::PP)
BuildRequires:                  perl(Mail::Address)
BuildRequires:                  perl(Memoize)
BuildRequires:                  perl(POSIX)
BuildRequires:                  perl(Term::ReadLine)
BuildRequires:                  perl(Test::More)
BuildRequires:                  perl(Time::HiRes)
%if %{with python3}
BuildRequires:                  python3-devel
%else
%if %{with python2}
BuildRequires:                  python2-devel
%endif
# endif with python2.
%endif
# endif with python3.
BuildRequires:                  subversion
BuildRequires:                  subversion-perl
BuildRequires:                  tar
BuildRequires:                  time
BuildRequires:                  zip
%endif
# endif with tests.

Requires:                       git-core = %{version}-%{release}
Requires:                       git-core-doc = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:                       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap.
Requires:                       perl-Git = %{version}-%{release}

%if %{with emacs} && %{defined _emacs_version}
Requires:                       emacs-filesystem >= %{_emacs_version}
%endif
# endif with emacs && defined _emacs_version.

# Obsolete emacs-git if it's disabled.
%if %{without emacs}
Obsoletes:                      emacs-git < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without emacs.

# Obsolete git-cvs if it's disabled.
%if %{without cvs}
Obsoletes:                      git-cvs < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without cvs.

# Obsolete git-p4 if it's disabled.
%if %{without p4}
Obsoletes:                      git-p4 < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without p4.

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: all
# -------------------------------------------------------------------------------------------------------------------- #

%package all
Summary:                        Meta-package to pull in all git tools
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
%if %{with libsecret}
Requires:                       git-credential-libsecret = %{version}-%{release}
%endif
# endif with libsecret.
%if %{with cvs}
Requires:                       git-cvs = %{version}-%{release}
%endif
# endif with cvs.
Requires:                       git-daemon = %{version}-%{release}
Requires:                       git-email = %{version}-%{release}
Requires:                       git-gui = %{version}-%{release}
%if %{with p4}
Requires:                       git-p4 = %{version}-%{release}
%endif
# endif with p4.
Requires:                       git-subtree = %{version}-%{release}
Requires:                       git-svn = %{version}-%{release}
Requires:                       git-instaweb = %{version}-%{release}
Requires:                       gitk = %{version}-%{release}
Requires:                       perl-Git = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:                       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap.
%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: core
# -------------------------------------------------------------------------------------------------------------------- #

%package core
Summary:                        Core package of git with minimal functionality
Requires:                       less
Requires:                       openssh-clients
Requires:                       zlib >= 1.2
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: core-doc
# -------------------------------------------------------------------------------------------------------------------- #

%package core-doc
Summary:                        Documentation files for git-core
BuildArch:                      noarch
Requires:                       git-core = %{version}-%{release}
%description core-doc
Documentation files for git-core package including man pages.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: credential-libsecret
# -------------------------------------------------------------------------------------------------------------------- #

%if %{with libsecret}
%package credential-libsecret
Summary:                        Git helper for accessing credentials via libsecret
BuildRequires:                  libsecret-devel
Requires:                       git = %{version}-%{release}
%description credential-libsecret
%{summary}.
%endif
# endif with libsecret.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: cvs
# -------------------------------------------------------------------------------------------------------------------- #

%if %{with cvs}
%package cvs
Summary:                        Git tools for importing CVS repositories
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       cvs
Requires:                       cvsps
Requires:                       perl(DBD::SQLite)
%description cvs
%{summary}.
%endif
# endif with cvs.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: daemon
# -------------------------------------------------------------------------------------------------------------------- #

%package daemon
Summary:                        Git protocol daemon
Requires:                       git-core = %{version}-%{release}
Requires:                       systemd
Requires(post): systemd
Requires(preun):  systemd
Requires(postun): systemd
%description daemon
The git daemon for supporting git:// access to git repositories

# -------------------------------------------------------------------------------------------------------------------- #
# Package: email
# -------------------------------------------------------------------------------------------------------------------- #

%package email
Summary:                        Git tools for sending patches via email
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       perl(Authen::SASL)
Requires:                       perl(Net::SMTP::SSL)
%description email
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: gitk
# -------------------------------------------------------------------------------------------------------------------- #

%package -n gitk
Summary:                        Git repository browser
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       git-gui = %{version}-%{release}
Requires:                       tk >= 8.4
%description -n gitk
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: gitweb
# -------------------------------------------------------------------------------------------------------------------- #

%package -n gitweb
Summary:                        Simple web interface to git repositories
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
%description -n gitweb
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: gui
# -------------------------------------------------------------------------------------------------------------------- #

%package gui
Summary:                        Graphical interface to Git
BuildArch:                      noarch
Requires:                       gitk = %{version}-%{release}
Requires:                       tk >= 8.4
%description gui
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: instaweb
# -------------------------------------------------------------------------------------------------------------------- #

%package instaweb
Summary:                        Repository browser in gitweb
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       gitweb = %{version}-%{release}
%if 0%{?rhel} >= 9
Requires:                       httpd
%else
Requires:                       lighttpd
%endif

%description instaweb
A simple script to set up gitweb and a web server for browsing the local
repository.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: p4
# -------------------------------------------------------------------------------------------------------------------- #

%if %{with p4}
%package p4
Summary:                        Git tools for working with Perforce depots
BuildArch:                      noarch
%if %{with python3}
BuildRequires:                  python3-devel
%else
%if %{with python2}
BuildRequires:                  python2-devel
%endif
# endif with python2.
%endif
# endif with python3.
Requires:                       git = %{version}-%{release}
%description p4
%{summary}.
%endif
# endif with p4.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: perl-Git
# -------------------------------------------------------------------------------------------------------------------- #

%package -n perl-Git
Summary:                        Perl interface to Git
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo ${version}))
%description -n perl-Git
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: perl-Git-SVN
# -------------------------------------------------------------------------------------------------------------------- #

%package -n perl-Git-SVN
Summary:                        Perl interface to Git::SVN
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo ${version}))
%description -n perl-Git-SVN
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: subtree
# -------------------------------------------------------------------------------------------------------------------- #

%package subtree
Summary:                        Git tools to merge and split repositories
Requires:                       git-core = %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: svn
# -------------------------------------------------------------------------------------------------------------------- #

%package svn
Summary:                        Git tools for interacting with Subversion repositories
BuildArch:                      noarch
Requires:                       git = %{version}-%{release}
Requires:                       perl(Digest::MD5)
%if ! %{defined perl_bootstrap}
Requires:                       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap.
Requires:                       subversion
%description svn
%{summary}.

# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------------< SCRIPT >----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

%prep
# Verify GPG signatures.
%{__xz} -dc '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-

%autosetup -p1 -n %{name}-%{version}%{?rcrev}

# Install print-failed-test-output script.
%{__install} -p -m 755 %{SOURCE99} print-failed-test-output

# Remove git-archimport from command list.
%{__sed} -i '/^git-archimport/d' command-list.txt

%if %{without cvs}
# Remove git-cvs* from command list.
%{__sed} -i '/^git-cvs/d' command-list.txt
%endif
# endif without cvs.

%if %{without p4}
# Remove git-p4 from command list.
%{__sed} -i '/^git-p4/d' command-list.txt
%endif
# endif without p4.

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
# Pipe to tee to aid confirmation/verification of settings.
cat << \EOF | tee config.mak
V = 1
CFLAGS = %{build_cflags}
LDFLAGS = %{build_ldflags}
USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
INSTALL_SYMLINKS = 1
GITWEB_PROJECTROOT = %{_localstatedir}/lib/git
GNU_ROFF = 1
NO_PERL_CPAN_FALLBACKS = 1
%if %{with python3}
PYTHON_PATH = %{__python3}
%else
%if %{with python2}
PYTHON_PATH = %{__python2}
%else
NO_PYTHON = 1
%endif
%endif
%if %{with asciidoctor}
USE_ASCIIDOCTOR = 1
%endif
htmldir = %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
prefix = %{_prefix}
perllibdir = %{perl_vendorlib}
gitwebdir = %{_localstatedir}/www/git

# Test options.
DEFAULT_TEST_TARGET = prove
GIT_PROVE_OPTS = --verbose --normalize %{?_smp_mflags} --formatter=TAP::Formatter::File
GIT_TEST_OPTS = -x --verbose-log
EOF

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid.
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(packed-refs\\)
%if ! %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Term::ReadKey\\)
%endif
# endif ! defined perl_bootstrap.

# Remove Git::LoadCPAN to ensure we use only system perl modules. This also
# allows the dependencies to be automatically processed by rpm.
%{__rm} -rf perl/Git/LoadCPAN{.pm,/}
%{__grep} -rlZ '^use Git::LoadCPAN::' | xargs -r0 %{__sed} -i 's/Git::LoadCPAN:://g'

# Update gitweb default home link string.
%{__sed} -i 's@"++GITWEB_HOME_LINK_STR++"@$ENV{"SERVER_NAME"} ? "git://" . $ENV{"SERVER_NAME"} : "projects"@' \
  gitweb/gitweb.perl

# Move contrib/{contacts,subtree} docs to Documentation so they build with the
# proper asciidoc/docbook/xmlto options.
%{__mv} contrib/{contacts,subtree}/git-*.txt Documentation/


%build
# Improve build reproducibility.
export TZ=UTC
export SOURCE_DATE_EPOCH=$( date -r version +%%s 2>/dev/null )

%{make_build} all %{?with_docs:doc}

%{make_build} -C contrib/contacts/ all

%if %{with libsecret}
%{make_build} -C contrib/credential/libsecret/
%endif
# endif with libsecret.

%{make_build} -C contrib/credential/netrc/

%{make_build} -C contrib/diff-highlight/

%{make_build} -C contrib/subtree/ all

# Fix shebang in a few places to silence rpmlint complaints.
%if %{with python2}
%{__sed} -i -e '1s@#! */usr/bin/env python$@#!%{__python2}@' \
  contrib/fast-import/import-zips.py \
  contrib/hooks/multimail/git_multimail.py \
  contrib/hooks/multimail/migrate-mailhook-config \
  contrib/hooks/multimail/post-receive.example
%else
# Remove contrib/fast-import/import-zips.py which requires python2.
%{__rm} -rf contrib/fast-import/import-zips.py
%endif
# endif with python2.

# The multimail hook is installed with git. Use python3 to avoid an
# unnecessary python2 dependency, if possible. Also fix contrib/hg-to-git
# while here.
%if %{with python3}
%{__sed} -i -e '1s@#!\( */usr/bin/env python\|%{__python2}\)$@#!%{__python3}@' \
  contrib/hg-to-git/hg-to-git.py \
  contrib/hooks/multimail/git_multimail.py \
  contrib/hooks/multimail/migrate-mailhook-config \
  contrib/hooks/multimail/post-receive.example
%endif
# endif with python3.


%install
%{make_install} %{?with_docs:install-doc}

%{make_install} -C contrib/contacts

%if %{with emacs}
%global elispdir %{_emacs_sitelispdir}/git
pushd contrib/emacs >/dev/null
for el in *.el ; do
  # Note: No byte-compiling is done.  These .el files are one-line stubs
  # which only serve to point users to better alternatives.
  %{__install} -Dpm 644 ${el} %{buildroot}%{elispdir}/${el}
  %{__rm} -f ${el} # clean up to avoid cruft in git-core-doc.
done
popd >/dev/null
%endif
# endif with emacs.

%if %{with libsecret}
%{__install} -pm 755 contrib/credential/libsecret/git-credential-libsecret \
  %{buildroot}%{gitexecdir}
%endif
# endif with libsecret.
%{__install} -pm 755 contrib/credential/netrc/git-credential-netrc \
  %{buildroot}%{gitexecdir}
# Temporarily move contrib/credential/netrc aside to prevent it from being
# deleted in the docs preparation, so the tests can be run in %%check.
%{__mv} contrib/credential/netrc .

%{make_install} -C contrib/subtree

%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__install} -pm 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
%{__sed} "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
  %{SOURCE14} > %{buildroot}%{_sysconfdir}/gitweb.conf

# Install contrib/diff-highlight and clean up to avoid cruft in git-core-doc.
%{__install} -Dpm 0755 contrib/diff-highlight/diff-highlight \
  %{buildroot}%{_datadir}/git-core/contrib/diff-highlight
%{__rm} -rf contrib/diff-highlight/{Makefile,diff-highlight,*.perl,t}

# Clean up contrib/subtree to avoid cruft in the git-core-doc docdir.
%{__rm} -rf contrib/subtree/{INSTALL,Makefile,git-subtree*,t}

# "git-archimport" is not supported.
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec %{__rm} -f {} ';'

%if %{without cvs}
# Remove "git-cvs*" and "gitcvs*".
find %{buildroot} Documentation \( -type f -o -type l \) \
  \( -name 'git-cvs*' -o -name 'gitcvs*' \) -exec %{__rm} -f {} ';'
%endif
# endif without cvs.

%if %{without p4}
# Remove "git-p4*" and mergetools/p4merge.
find %{buildroot} Documentation -type f -name 'git-p4*' -exec %{__rm} -f {} ';'
%{__rm} -f %{buildroot}%{gitexecdir}/mergetools/p4merge
%endif
# endif without p4.

# Remove unneeded "git-remote-testsvn" so "git-svn" can be noarch.
%{__rm} -f %{buildroot}%{gitexecdir}/git-remote-testsvn

exclude_re="archimport|email|git-(citool|credential-libsecret|cvs|daemon|gui|instaweb|p4|subtree|svn)|gitk|gitweb|p4merge"
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f -o -type l | %{__grep} -vE "${exclude_re}" | %{__sed} -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | %{__grep} -vE "${exclude_re}" | %{__sed} -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | %{__sed} -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | %{__sed} -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files.
grep Git/SVN perl-git-files > perl-git-svn-files
%{__sed} -i "/Git\/SVN/ d" perl-git-files
%if %{with docs}
(find %{buildroot}%{_mandir} -type f | %{__grep} -vE "${exclude_re}|Git" | %{__sed} -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
%{__rm} -rf %{buildroot}%{_mandir}
%endif
# endif with docs.

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/git
%{__install} -Dp -m 0644 %{SOURCE16} %{buildroot}%{_unitdir}/git.socket
perl -p \
  -e "s|\@GITEXECDIR\@|%{gitexecdir}|g;" \
  -e "s|\@BASE_PATH\@|%{_localstatedir}/lib/git|g;" \
  %{SOURCE15} > %{buildroot}%{_unitdir}/git@.service

# Setup bash completion.
%{__install} -Dpm 644 contrib/completion/git-completion.bash %{buildroot}%{bashcompdir}/git
ln -s git %{buildroot}%{bashcompdir}/gitk

# Install tcsh completion.
%{__mkdir_p} %{buildroot}%{_datadir}/git-core/contrib/completion
%{__install} -pm 644 contrib/completion/git-completion.tcsh \
  %{buildroot}%{_datadir}/git-core/contrib/completion/

# Drop ".py" extension from git_multimail to avoid byte-compiling.
%{__mv} contrib/hooks/multimail/git_multimail{.py,}

# Move contrib/hooks out of %%docdir.
%{__mkdir_p} %{buildroot}%{_datadir}/git-core/contrib
%{__mv} contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
pushd contrib > /dev/null
ln -s ../../../git-core/contrib/hooks
popd > /dev/null

# Install "git-prompt.sh".
%{__mkdir_p} %{buildroot}%{_datadir}/git-core/contrib/completion
%{__install} -pm 644 contrib/completion/git-prompt.sh \
  %{buildroot}%{_datadir}/git-core/contrib/completion/

# Install git-gui .desktop file.
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE12}

# Symlink git-citool to git-gui if they are identical.
pushd %{buildroot}%{gitexecdir} >/dev/null
if cmp -s git-gui git-citool 2>/dev/null; then
  ln -svf git-gui git-citool
fi
popd >/dev/null

# Find translations.
%{find_lang} %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# Quiet some rpmlint complaints.
chmod -R g-w %{buildroot}
chmod a-x %{buildroot}%{gitexecdir}/git-mergetool--lib
# These files probably are not needed.
find . -regex '.*/\.\(git\(attributes\|ignore\)\|perlcriticrc\)' -delete
chmod a-x Documentation/technical/api-index.sh
find contrib -type f -print0 | xargs -r0 chmod -x

# Split core files.
not_core_re="git-(add--interactive|contacts|credential-netrc|filter-branch|instaweb|request-pull|send-mail)|gitweb"
%{__grep} -vE "${not_core_re}|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
%if %{with docs}
%{__grep} -vE "${not_core_re}" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core
%endif
# endif with docs.
%{__grep} -E  "${not_core_re}" bin-man-doc-files > bin-man-doc-git-files

##### DOC
# Place doc files into %%{_pkgdocdir} and split them into expected packages
# contrib.
not_core_doc_re="(git-(cvs|gui|citool|daemon|instaweb|subtree))|p4|svn|email|gitk|gitweb"
%{__mkdir_p} %{buildroot}%{_pkgdocdir}/
cp -pr CODE_OF_CONDUCT.md README.md Documentation/*.txt Documentation/RelNotes contrib %{buildroot}%{_pkgdocdir}/
# Remove contrib/ files/dirs which have nothing useful for documentation.
%{__rm} -rf %{buildroot}%{_pkgdocdir}/contrib/{contacts,credential}/
cp -p gitweb/INSTALL %{buildroot}%{_pkgdocdir}/INSTALL.gitweb
cp -p gitweb/README %{buildroot}%{_pkgdocdir}/README.gitweb

%if %{with docs}
cp -pr Documentation/*.html Documentation/docbook-xsl.css %{buildroot}%{_pkgdocdir}/
cp -pr Documentation/{howto,technical} %{buildroot}%{_pkgdocdir}/
find %{buildroot}%{_pkgdocdir}/{howto,technical} -type f \
  |%{__grep} -o "%{_pkgdocdir}.*$" >> man-doc-files-core
%endif
# endif with docs.

{
  find %{buildroot}%{_pkgdocdir} -type f -maxdepth 1 \
    | %{__grep} -o "%{_pkgdocdir}.*$" \
    | %{__grep} -vE "${not_core_doc_re}"
  find %{buildroot}%{_pkgdocdir}/{contrib,RelNotes} -type f \
    | %{__grep} -o "%{_pkgdocdir}.*$"
  find %{buildroot}%{_pkgdocdir} -type d | %{__grep} -o "%{_pkgdocdir}.*$" \
    | %{__sed} "s/^/\%dir /"
} >> man-doc-files-core
##### #DOC


%check
%if %{without tests}
echo "*** Skipping tests"
exit 0
%endif
# endif without tests.

%if %{with docs} && %{with linkcheck}
# Test links in HTML documentation.
find %{buildroot}%{_pkgdocdir} -name "*.html" -print0 | xargs -r0 linkchecker
%endif
# endif with docs && with linkcheck.

# Tests to skip on all releases and architectures.
GIT_SKIP_TESTS=""

%ifarch aarch64 %{arm} %{power64}
# Skip tests which fail on aarch64, arm, and ppc.
#
# The following 2 tests use run_with_limited_cmdline, which calls ulimit -s 128
# to limit the maximum stack size.
# t5541.35 'push 2000 tags over http'
# t5551.25 'clone the 2,000 tag repo to check OS command line overflow'
GIT_SKIP_TESTS="${GIT_SKIP_TESTS} t5541.35 t5551.25"
%endif
# endif aarch64 %%{arm} %%{power64}.

%ifarch %{power64}
# Skip tests which fail on ppc.
#
# t9115-git-svn-dcommit-funky-renames is disabled because it frequently fails.
# The port it uses (9115) is already in use. It is unclear if this is
# due to an issue in the test suite or a conflict with some other process on
# the build host. It only appears to occur on ppc-arches.
GIT_SKIP_TESTS="${GIT_SKIP_TESTS} t9115"
%endif
# endif %%{power64}.

export GIT_SKIP_TESTS

# Set LANG so various UTF-8 tests are run.
export LANG=en_US.UTF-8

# Explicitly enable tests which may be skipped opportunistically
# Check for variables set via test_bool_env in the test suite:
#   git grep 'test_bool_env GIT_' -- t/{lib-,t[0-9]}*.sh |
#       sed -r 's/.* (GIT_[^ ]+) .*/\1/g' | sort -u
export GIT_TEST_GIT_DAEMON=true
export GIT_TEST_HTTPD=true
export GIT_TEST_SVNSERVE=true
export GIT_TEST_SVN_HTTPD=true

# Create tmpdir for test output and update GIT_TEST_OPTS.
# Also update GIT-BUILD-OPTIONS to keep make from any needless rebuilding.
testdir=$( mktemp -d -p /tmp git-t.XXXX )
%{__sed} -i "s@^GIT_TEST_OPTS = .*@& --root=$testdir@" config.mak
touch -r GIT-BUILD-OPTIONS ts
%{__sed} -i "s@\(GIT_TEST_OPTS='.*\)'@\1 --root=$testdir'@" GIT-BUILD-OPTIONS
touch -r ts GIT-BUILD-OPTIONS

# Run the tests.
%{__make} test || ./print-failed-test-output

# Run contrib/credential/netrc tests.
%{__mkdir_p} contrib/credential
%{__mv} netrc contrib/credential/
%{make_build} -C contrib/credential/netrc/ test || \
%{make_build} -C contrib/credential/netrc/ testverbose

# Clean up test dir.
rmdir --ignore-fail-on-non-empty "${testdir}"


%post daemon
%systemd_post git.socket


%preun daemon
%systemd_preun git.socket


%postun daemon
%systemd_postun_with_restart git.socket


%files -f bin-man-doc-git-files
%if %{with emacs}
%{elispdir}
%endif
# endif with emacs.
%{_datadir}/git-core/contrib/diff-highlight
%{_datadir}/git-core/contrib/hooks/multimail
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample


%files all
# No files for you!


%files core -f bin-files-core
#NOTE: This is only use of the %%doc macro in this spec file and should not
#      be used elsewhere.
%{!?_licensedir:%global license %doc}
%license COPYING
# Exclude is best way here because of troubles with symlinks inside "git-core/".
%exclude %{_datadir}/git-core/contrib/diff-highlight
%exclude %{_datadir}/git-core/contrib/hooks/multimail
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%{bashcomproot}
%{_datadir}/git-core/


%files core-doc -f man-doc-files-core
%if 0%{?rhel} && 0%{?rhel} <= 7
# .py files are only bytecompiled on EL <= 7.
%exclude %{_pkgdocdir}/contrib/*/*.py[co]
%endif
# endif rhel <= 7.
%{_pkgdocdir}/contrib/hooks


%if %{with libsecret}
%files credential-libsecret
%{gitexecdir}/git-credential-libsecret
%endif
# endif with libsecret.


%if %{with cvs}
%files cvs
%{_pkgdocdir}/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitexecdir}/*cvs*
%{?with_docs:%{_mandir}/man1/*cvs*.1*}
%{?with_docs:%{_pkgdocdir}/*git-cvs*.html}
%endif
# endif with cvs.


%files daemon
%{_pkgdocdir}/git-daemon*.txt
%{_unitdir}/git.socket
%{_unitdir}/git@.service
%{gitexecdir}/git-daemon
%{_localstatedir}/lib/git
%{?with_docs:%{_mandir}/man1/git-daemon*.1*}
%{?with_docs:%{_pkgdocdir}/git-daemon*.html}


%files email
%{_pkgdocdir}/*email*.txt
%{gitexecdir}/*email*
%{?with_docs:%{_mandir}/man1/*email*.1*}
%{?with_docs:%{_pkgdocdir}/*email*.html}


%files -n gitk
%{_pkgdocdir}/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk
%{?with_docs:%{_mandir}/man1/*gitk*.1*}
%{?with_docs:%{_pkgdocdir}/*gitk*.html}


%files -n gitweb
%{_pkgdocdir}/*.gitweb
%{_pkgdocdir}/gitweb*.txt
%{?with_docs:%{_mandir}/man1/gitweb.1*}
%{?with_docs:%{_mandir}/man5/gitweb.conf.5*}
%{?with_docs:%{_pkgdocdir}/gitweb*.html}
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
%{_localstatedir}/www/git/


%files gui
%{gitexecdir}/git-gui*
%{gitexecdir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/
%{_pkgdocdir}/git-gui.txt
%{_pkgdocdir}/git-citool.txt
%{?with_docs:%{_mandir}/man1/git-gui.1*}
%{?with_docs:%{_pkgdocdir}/git-gui.html}
%{?with_docs:%{_mandir}/man1/git-citool.1*}
%{?with_docs:%{_pkgdocdir}/git-citool.html}


%files instaweb
%{gitexecdir}/git-instaweb
%{_pkgdocdir}/git-instaweb.txt
%{?with_docs:%{_mandir}/man1/git-instaweb.1*}
%{?with_docs:%{_pkgdocdir}/git-instaweb.html}


%if %{with p4}
%files p4
%{gitexecdir}/*p4*
%{gitexecdir}/mergetools/p4merge
%{_pkgdocdir}/*p4*.txt
%{?with_docs:%{_mandir}/man1/*p4*.1*}
%{?with_docs:%{_pkgdocdir}/*p4*.html}
%endif
# endif with p4.


%files -n perl-Git -f perl-git-files
%{?with_docs:%{_mandir}/man3/Git.3pm*}


%files -n perl-Git-SVN -f perl-git-svn-files


%files subtree
%{gitexecdir}/git-subtree
%{_pkgdocdir}/git-subtree.txt
%{?with_docs:%{_mandir}/man1/git-subtree.1*}
%{?with_docs:%{_pkgdocdir}/git-subtree.html}


%files svn
%{gitexecdir}/git-svn
%{_pkgdocdir}/git-svn.txt
%{?with_docs:%{_mandir}/man1/git-svn.1*}
%{?with_docs:%{_pkgdocdir}/git-svn.html}


%changelog
* Sun Jun 20 2021 Package Store <kitsune.solar@gmail.com> - 2.32.0-100
- UPD: Move to Package Store.
- UPD: License.

* Sun Jun 06 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-1
- update to 2.32.0
- add perl(File::Compare) BuildRequires
- fix var to enable git-svn tests with httpd
- remove %%changelog entries prior to 2019

* Thu Jun 03 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.5.rc3
- drop jgit on Fedora >= 35
  Resolves: rhbz#1965808

* Wed Jun 02 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.4.rc3
- update to 2.32.0-rc3

* Fri May 28 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.3.rc2
- update to 2.32.0-rc2

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.32.0-0.2.rc1
- Perl 5.34 re-rebuild of bootstrapped packages

* Sat May 22 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.1.rc1
- update to 2.32.0-rc1
- rearrange python2/python3 conditionals
- re-enable git-p4 with python3
- add coreutils BuildRequires
- remove unneeded NEEDS_CRYPTO_WITH_SSL

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.31.1-3.1
- Perl 5.34 rebuild

* Mon May 17 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.0.rc0
- update to 2.32.0-rc0

* Sun May 16 2021 Todd Zullinger <tmz@pobox.com>
- clean up various dist conditionals

* Wed Apr 21 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-3
- apply upstream patch to fix clone --bare segfault
  Resolves: rhbz#1952030

* Tue Apr 06 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-2
- remove two stray %%defattr macros from %%files sections

* Sat Mar 27 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-1
- update to 2.31.1

* Fri Mar 19 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-2
- fix git bisect with annotaged tags

* Mon Mar 15 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-1
- update to 2.31.0

* Tue Mar 09 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.2.rc2
- update to 2.31.0-rc2

* Wed Mar 03 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.1.rc1
- update to 2.31.0-rc1

* Tue Mar 02 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.0.rc0
- update to 2.31.0-rc0

* Tue Mar 02 2021 Todd Zullinger <tmz@pobox.com> - 2.30.1-3
- use %%{gpgverify} macro to verify tarball signature

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.30.1-2.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Feb 18 2021 Ondřej Pohořelský <opohorel@redhat.com - 2.30.1-2
- include git-daemon in git-all meta-package

* Thu Feb 18 2021 Todd Zullinger <tmz@pobox.com>
- re-enable t7812-grep-icase-non-ascii on s390x

* Tue Feb 09 2021 Todd Zullinger <tmz@pobox.com> - 2.30.1-1
- update to 2.30.1

* Mon Feb 08 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.30.0-2
- add rhel 9 conditional to require httpd instead of lighttpd in git-instaweb

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-1
- update to 2.30.0

* Wed Dec 23 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.2.rc2
- update to 2.30.0-rc2

* Sat Dec 19 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.1.rc1
- update to 2.30.0-rc1

* Mon Dec 14 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.0.rc0
- update to 2.30.0-rc0

* Sun Dec 06 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-4
- move git-difftool to git-core, it does not require perl

* Wed Nov 25 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-3
- apply upstream patch to resolve git fast-import memory leak (#1900335)
- add epel-rpm-macros BuildRequires on EL-7 (#1872865)

* Sat Nov 07 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-2
- apply upstream patch to resolve git log segfault (#1791810)

* Thu Oct 29 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-1
- update to 2.29.2

* Sat Oct 24 2020 Todd Zullinger <tmz@pobox.com> - 2.29.1-1
- update to 2.29.1
- fix bugs in am/rebase handling of committer ident/date

* Mon Oct 19 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-1
- update to 2.29.0

* Thu Oct 15 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.2.rc2
- update to 2.29.0-rc2

* Fri Oct 09 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.1.rc1
- update to 2.29.0-rc1
- drop emacs-git stub for fedora >= 34 (#1882360)
- adjust python hashbang in contrib/hg-to-git, it supports python3

* Mon Oct 05 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.0.rc0
- update to 2.29.0-rc0

* Mon Jul 27 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-1
- update to 2.28.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.2.rc2
- update to 2.28.0-rc2

* Sat Jul 18 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.1.rc1
- update to 2.28.0-rc1

* Thu Jul 09 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.0.rc0
- update to 2.28.0-rc0

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27.0-1.2
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27.0-1.1
- Perl 5.32 rebuild

* Mon Jun 01 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-1
- update to 2.27.0

* Tue May 26 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-0.2.rc2
- update to 2.27.0-rc2

* Thu May 21 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-0.1.rc1
- update to 2.27.0-rc1

* Thu May 21 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.26.2-2
- Minor conditional fixes for ELN

* Mon Apr 20 2020 Todd Zullinger <tmz@pobox.com> - 2.26.2-1
- update to 2.26.2 (CVE-2020-11008)

* Tue Apr 14 2020 Todd Zullinger <tmz@pobox.com> - 2.26.1-1
- update to 2.26.1 (CVE-2020-5260)

* Sat Apr 04 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-2
- fix issue with fast-forward rebases when rebase.abbreviateCommands is set
- fix/quiet rpmlint issues from libsecret split

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 2.26.0-1.1
- Fix string quoting for rpm >= 4.16

* Sun Mar 22 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-1
- update to 2.26.0

* Mon Mar 16 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.3.rc2
- update to 2.26.0-rc2

* Thu Mar 12 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.2.rc1
- remove s390x gcc10 workaround (#1799408)

* Tue Mar 10 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.1.rc1
- update to 2.26.0-rc1
- adjust make test options
- add missing build deps for tests

* Fri Mar 06 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.0.rc0
- update to 2.26.0-rc0

* Wed Feb 26 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-4
- use Asciidoctor to build documentation when possible

* Sat Feb 22 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-3
- work around issue on s390x with gcc10 (#1799408)

* Wed Feb 19 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-2
- split libsecret credential helper into a subpackage (#1804741)
- consolidate macros for Fedora/EPEL
- remove unneeded gnome-keyring obsoletes

* Mon Feb 17 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-1
- update to 2.25.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tom Stellard <tstellar@redhat.com> - 2.25.0-2
- Use make_build macro when running tests

* Tue Jan 14 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-1
- update to 2.25.0

* Thu Jan 09 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.2.rc2
- update to 2.25.0-rc2

* Fri Jan 03 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.1.rc1
- update to 2.25.0-rc1
- only add highlight test BR for ppc64le/x86_64 on EL7+

* Wed Dec 25 2019 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.0.rc0
- update to 2.25.0-rc0

* Thu Dec 19 2019 Todd Zullinger <tmz@pobox.com> - 2.24.1-2
- fix git-daemon systemd scriptlets (#1785088)

* Tue Dec 10 2019 Todd Zullinger <tmz@pobox.com> - 2.24.1-1
- update to 2.24.1 (CVE-2019-1348, CVE-2019-1349, CVE-2019-1350, CVE-2019-1351,
  CVE-2019-1352, CVE-2019-1353, CVE-2019-1354, and CVE-2019-1387)

* Wed Dec 04 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-2
- restore jgit BR for use in tests

* Mon Nov 04 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-1
- update to 2.24.0

* Thu Oct 31 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.2.rc2
- update to 2.24.0-rc2

* Sun Oct 27 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.1.rc1.1
- disable linkchecker on all EL releases

* Thu Oct 24 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.1.rc1
- update to 2.24.0-rc1
- skip failing test in t7812-grep-icase-non-ascii on s390x
- gitk: add Requires:                       git-gui (#1765113)

* Sat Oct 19 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.0.rc0
- update to 2.24.0-rc0
- fix t0500-progress-display on big-endian arches

* Fri Aug 16 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-1
- Update to 2.23.0

* Sun Aug 11 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.2.rc2
- Update to 2.23.0-rc2

* Fri Aug 02 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.1.rc1
- Update to 2.23.0-rc1

* Mon Jul 29 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.0.rc0
- Update to 2.23.0-rc0

* Thu Jul 25 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-2
- completion: do not cache if --git-completion-helper fails
- avoid trailing comments in spec file
- drop jgit on Fedora > 30

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-1
- Update to 2.22.0

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.7.rc3
- Perl 5.30 re-rebuild updated packages

* Mon Jun 03 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.6.rc3
- Update to 2.22.0-rc3

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.5.rc2
- Perl 5.30 re-rebuild of bootstrapped packages

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.4.rc2
- Perl 5.30 rebuild

* Thu May 30 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.3.rc2
- Update to 2.22.0-rc1

* Fri May 24 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.2.rc1
- Apply upstream fixes for diff-parseopt issues on s390x

* Sun May 19 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.1.rc1
- Update to 2.22.0-rc1

* Mon May 13 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.0.rc0
- Update to 2.22.0-rc0
- Ensure a consistent format for test output
- Improve JGIT test prereq (jgit on Fedora >= 30 is broken)
- Add perl(JSON::PP) BuildRequires for trace2 tests

* Sun Feb 24 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-1
- Update to 2.21.0
- Move gitweb manpages to gitweb package
- Link git-citool to git-gui if they are identical

* Tue Feb 19 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.2.rc2
- Update to 2.21.0.rc2

* Fri Feb 15 2019 Todd Zullinger <tmz@pobox.com>
- Set SOURCE_DATE_EPOCH and TZ to improve build reproducibility

* Wed Feb 13 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.1.rc1
- Update to 2.21.0.rc1

* Thu Feb 07 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.0.rc0
- Update to 2.21.0.rc0
- Remove %%changelog entries prior to 2017

* Thu Jan 31 2019 Todd Zullinger <tmz@pobox.com> - 2.20.1-2
- Remove extraneous pcre BuildRequires
- Add additional BuildRequires for i18n locales used in tests
- Replace gitweb home-link with inline sed
- Add gnupg2-smime and perl JSON BuildRequires for tests
- Work around gpg-agent issues in the test suite
- Drop gnupg BuildRequires on fedora >= 30
- Fix formatting of contrib/{contacts,subtree} docs
- Use %%{build_cflags} and %%{build_ldflags}
- Drop unneeded TEST_SHELL_PATH make variable

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
