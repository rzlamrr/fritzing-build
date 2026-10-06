# Fritzing Builder (Unofficial Windows & macOS Builds)

> **⚠️ Disclaimer:** This project is for **educational purposes only**. All trademarks, logos, brand names, and copyrights belong exclusively to [Fritzing GmbH](https://fritzing.org/).

This repository does **not** host Fritzing's source code, nor does it claim any ownership of it. It simply fetches the official open-source code from Fritzing's public GitHub repositories and fully automates the complex compilation and linking process for Windows and macOS, packaging it into easy-to-use installers, disk images and portable zips via GitHub Actions.

## ❤️ **Support the Creators!**

If you use Fritzing and find it valuable for designing circuits and PCBs, **please consider downloading Fritzing from their official site and [donating to the Fritzing project](https://fritzing.org/donate/)**. The donations are what keep the core developers working on the software and fund Fritzing's future features. Support open-source hardware tools!

---

## 🚀 Build Overview

This repository uses GitHub Actions to compile Fritzing (`fritzing-app`, `develop` branch) entirely from source alongside its component repository (`fritzing-parts`, `develop` branch). Every build ships a pre-built `parts.db`, so Fritzing finds its parts on first launch instead of regenerating the database.

### Windows (`windows-2022`)
1. **Portable Version (`.zip`)**: A fully self-contained directory containing Fritzing and its component database.
2. **Offline Setup (`.exe`)**: An Inno Setup installer that tightly bundles the component database inside.
3. **Online Setup (`.exe`)**: A lightweight installer that downloads the component database (`fritzing-parts.zip`) from the same release during installation.

### macOS (Apple Silicon `arm64` & Intel `x86_64`)
1. **Apple Silicon (`arm64`, `macos-15`)**: Standalone `.dmg` disk image and portable `.zip` with components bundled for Apple Silicon (M1/M2/M3/M4).
2. **Intel (`x86_64`, `macos-15-intel`)**: Standalone `.dmg` disk image and portable `.zip` with components bundled for Intel-based Macs.

### ⚙️ How the Workflows Fit Together

| Workflow | Role |
|---|---|
| `build.yml` | Entry point (push to `master`, pull requests, manual run with a `platforms` choice). Reads the Fritzing version and every dependency version from `fritzing-app`, runs both platform builds, then publishes. |
| `windows.yml` | Reusable. Builds the dependencies, compiles Fritzing with MSVC, builds `parts.db` and the Inno Setup installers. |
| `macos.yml` | Reusable. Builds the dependencies, compiles Fritzing for each architecture, builds `parts.db`, and packages the `.dmg` and `.zip`. |

The final `release` job creates one **draft** release per Fritzing version and uploads the files of every platform that built successfully into it. If one platform fails, the other's files are still published and the job summary says which one is missing. Pull requests build but never publish.

### 📦 Dependencies Used for the Build

To compile Fritzing successfully from source, this build script pulls and links the following open-source dependencies. `fritzing-app` decides which versions it expects (`pri/*detect.pri`), so the workflows read libgit2, QuaZip, Clipper, SVGpp, ngspice and Boost versions from there instead of hard-coding them; the versions below are the ones currently in use.

- [**Fritzing App**](https://github.com/fritzing/fritzing-app) - The core IDE and Application.
- [**Fritzing Parts**](https://github.com/fritzing/fritzing-parts) - The database of electronic components and SVGs.
- [**Qt 6.8**](https://www.qt.io/) (6.8.3 on Windows, 6.8.2 on macOS) - Cross-platform application framework (utilizing `qtbase`, `qtsvg`, `qtserialport`, `qt5compat`, and `qttools`).
- [**libgit2 (1.7.1)**](https://github.com/libgit2/libgit2) - Portable C implementation of Git core methods utilized for parts database synchronization.
- [**QuaZip (1.4intuisphere)**](https://github.com/stachenov/quazip) - C++ wrapper for ZIP operations utilizing Qt.
- [**ngspice (v42)**](https://sourceforge.net/projects/ngspice/) - The open-source spice simulator used for circuit simulations.
- [**ZLib (1.3)**](https://github.com/madler/zlib) - The ubiquitous data compression library (statically linked on Windows, system library on macOS).
- [**Boost (1.85.0)**](https://github.com/boostorg/boost) - Heavyweight C++ source libraries.
- [**Clipper (v6.4.2)**](https://sourceforge.net/projects/polyclipping/) - Polygon and line clipping library.
- [**SVGpp (v1.3.1)**](https://github.com/svgpp/svgpp) - Parsing library for SVG vector files.
- [**Inno Setup 6**](https://jrsoftware.org/isinfo.php) - Powerful script-driven installer compiler utilized to generate both Windows `Setup.exe` files.
