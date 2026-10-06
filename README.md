# Fritzing Builder (Windows Unofficial Build)

> **⚠️ Disclaimer:** This project is for **educational purposes only**. All trademarks, logos, brand names, and copyrights belong exclusively to [Fritzing GmbH](https://fritzing.org/).

This repository does **not** host Fritzing's source code, nor does it claim any ownership of it. It simply fetches the official open-source code from Fritzing's public GitHub repositories and fully automates the complex compilation and linking process for Windows, packaging it into an easy-to-use installer and portable zip via GitHub Actions.

## ❤️ **Support the Creators!**

If you use Fritzing and find it valuable for designing circuits and PCBs, **please consider downloading Fritzing from their official site and [donating to the Fritzing project](https://fritzing.org/donate/)**. The donations are what keep the core developers working on the software and fund Fritzing's future features. Support open-source hardware tools!

---

## 🚀 Build Overview

This repository uses GitHub Actions to compile Fritzing (`fritzing-app`) entirely from source alongside its component repository (`fritzing-parts`).

### Windows (`windows-2022`)
1. **Portable Version (`.zip`)**: A fully self-contained directory containing Fritzing and its 300MB component database.
2. **Offline Setup (`.exe`)**: An Inno Setup installer that tightly bundles the component database inside.
3. **Online Setup (`.exe`)**: A lightweight installer that downloads the component database natively from GitHub during installation.

### macOS (Apple Silicon `arm64` & Intel `x86_64`)
1. **Apple Silicon (`arm64`, `macos-26`)**: Standalone `.dmg` disk image and portable `.zip` with Qt 6.8 LTS and components bundled for Apple Silicon (M1/M2/M3/M4).
2. **Intel (`x86_64`, `macos-26-intel`)**: Standalone `.dmg` disk image and portable `.zip` with Qt 6.8 LTS and components bundled for Intel-based Macs.

### 📦 Dependencies Used for the Build

To compile Fritzing successfully from source, this build script pulls and links the following open-source dependencies:

- [**Fritzing App**](https://github.com/fritzing/fritzing-app) - The core IDE and Application.
- [**Fritzing Parts**](https://github.com/fritzing/fritzing-parts) - The database of electronic components and SVGs.
- [**Qt 6.8**](https://www.qt.io/) - Cross-platform application framework (utilizing `qtbase`, `qtsvg`, `qtserialport`, `qt5compat`, and `qttools`).
- [**libgit2 (1.7.1)**](https://github.com/libgit2/libgit2) - Portable C implementation of Git core methods utilized for parts database synchronization.
- [**QuaZip (1.4intuisphere)**](https://github.com/stachenov/quazip) - C++ wrapper for ZIP operations utilizing Qt.
- [**ngspice (v42)**](https://sourceforge.net/projects/ngspice/) - The open-source spice simulator used for circuit simulations.
- [**ZLib (1.3.1)**](https://github.com/madler/zlib) - The ubiquitous data compression library (statically linked).
- [**Boost (1.85.0)**](https://github.com/boostorg/boost) - Heavyweight C++ source libraries.
- [**Clipper (v6.4.2)**](https://sourceforge.net/projects/polyclipping/) - Polygon and line clipping library.
- [**SVGpp (v1.3.1)**](https://github.com/svgpp/svgpp) - Parsing library for SVG vector files.
- [**Inno Setup 6**](https://jrsoftware.org/isinfo.php) - Powerful script-driven installer compiler utilized to generate both `Setup.exe` files.
