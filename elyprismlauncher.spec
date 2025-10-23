# Change these variables if you want to use custom keys
# Leave blank if you want to build Prism Launcher without an MSA ID or CurseForge API key
%global msa_id default
%global curseforge_key default

# Set the Qt version
%global qt_version 6
%global min_qt_version 6.0

# Give the launcher our build platform
%global build_platform unknown

%if 0%{?fedora}
%global build_platform Fedora
%endif

%if 0%{?rhel}
%global build_platform RedHat
%endif

%if 0%{?centos}
%global build_platform CentOS
%endif

Name:             elyprismlauncher
Version:          9.4
Release:          1

License:          GPL-3.0-only AND Apache-2.0 AND LGPL-3.0-only AND OFL-1.1 AND LGPL-2.1 AND MIT AND BSD-3-Clause
Group:            Amusements/Games
Summary:          Minecraft launcher with ability to manage multiple instances
URL:              https://elyprismlauncher.github.io/
Source0:          https://github.com/ElyPrismLauncher/ElyPrismLauncher/releases/download/%{version}/ElyPrismLauncher-%{version}.tar.gz

ExcludeArch:	  %{ix86}

BuildRequires:    cmake >= 3.15
BuildRequires:    extra-cmake-modules
BuildRequires:    gcc-c++
# JDKs less than the most recent release & LTS are no longer in the default
# Fedora repositories
# Make sure you have Adoptium's repositories enabled
# https://fedoraproject.org/wiki/Changes/ThirdPartyLegacyJdks
# https://adoptium.net/installation/linux/#_centosrhelfedora_instructions
%if 0%{?fedora} > 41
BuildRequires:    temurin-17-jdk
%else
BuildRequires:    java-17-openjdk-devel
%endif
BuildRequires:    libappstream-glib

BuildRequires:    cmake(Qt%{qt_version}Concurrent) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Core) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Gui) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Network) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}NetworkAuth) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Test) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Widgets) >= %{min_qt_version}
BuildRequires:    cmake(Qt%{qt_version}Xml) >= %{min_qt_version}
%if %{qt_version} == 6
BuildRequires:    cmake(Qt6Core5Compat)
%endif

BuildRequires:    cmake(ghc_filesystem)

BuildRequires:    pkgconfig(libcmark)
# https://bugzilla.redhat.com/show_bug.cgi?id=2166815
# Fedora versions < 38  (and thus RHEL < 10) don't contain cmark's binary target
# We need that
%if 0%{?fedora} && 0%{?fedora} < 38 || 0%{?rhel} && 0%{?rhel} < 10
BuildRequires:    cmark
%endif

BuildRequires:    pkgconfig(scdoc)
BuildRequires:    pkgconfig(zlib)

Requires:         qt%{qt_version}-qtimageformats
Requires:         qt%{qt_version}-qtsvg

Requires:         javapackages-filesystem
Recommends:       java-21-openjdk
# See note above
%if 0%{?fedora} && 0%{?fedora} < 42
Recommends:       java-17-openjdk
Suggests:         java-1.8.0-openjdk

%endif

# xrandr needed for LWJGL [2.9.2, 3) https://github.com/LWJGL/lwjgl/issues/128
Recommends:       xrandr
# libflite needed for using narrator in minecraft
Recommends:       flite
# Prism supports enabling gamemode
Suggests:         gamemode
Conflicts:        prismlauncher

%description
A custom launcher for Minecraft that allows you to easily manage
multiple installations of Minecraft at once (Fork of MultiMC)


%prep
%autosetup -n ElyPrismLauncher-%{version}

rm -rf libraries/{extra-cmake-modules,filesystem,zlib}


%build
%cmake \
  -DLauncher_QT_VERSION_MAJOR="%{qt_version}" \
  -DLauncher_BUILD_PLATFORM="%{build_platform}" \
  %if 0%{?fedora} > 41
  -DLauncher_ENABLE_JAVA_DOWNLOADER=ON \
  %endif
  %if "%{msa_id}" != "default"
  -DLauncher_MSA_CLIENT_ID="%{msa_id}" \
  %endif
  %if "%{curseforge_key}" != "default"
  -DLauncher_CURSEFORGE_API_KEY="%{curseforge_key}" \
  %endif


%cmake_build


%install
%cmake_install

# Don't run on RHEL as it ships an older version of appstream-util
# || 0%{?rhel} > 9
%if 0%{?fedora} > 37
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml
%endif


%files
%doc README.md
%license LICENSE COPYING.md
%dir %{_datadir}/ElyPrismLauncher
%{_bindir}/elyprismlauncher
%{_bindir}/elyprismlauncher_updater
%{_datadir}/ElyPrismLauncher/*
%{_datadir}/applications/org.prismlauncher.PrismLauncher.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.prismlauncher.PrismLauncher.svg
%{_datadir}/mime/packages/modrinth-mrpack-mime.xml
%{_datadir}/qlogging-categories?/elyprismlauncher.categories
%{_mandir}/man?/prismlauncher.*
%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml


%changelog
%autochangelog
