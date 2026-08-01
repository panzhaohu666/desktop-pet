# 🐾 Desktop Pet — 桌宠精灵

A lightweight, transparent desktop companion for Windows, Linux & macOS, built with Python + PyQt5.

<p align="center">
  <img src="resources/pet.png" width="200" alt="Desktop Pet">
</p>

<p align="center">
  <a href="https://github.com/panzhaohu666/desktop-pet/releases"><img src="https://img.shields.io/github/v/release/panzhaohu666/desktop-pet?style=flat-square" alt="Release"></a>
  <a href="https://github.com/panzhaohu666/desktop-pet/blob/main/LICENSE"><img src="https://img.shields.io/github/license/panzhaohu666/desktop-pet?style=flat-square" alt="License"></a>
  <a href="https://github.com/panzhaohu666/desktop-pet/actions"><img src="https://img.shields.io/github/actions/workflow/status/panzhaohu666/desktop-pet/release.yml?style=flat-square" alt="Build"></a>
</p>

---

## 📥 Download (Pre-built)

| Platform | Download |
|----------|----------|
| 🪟 **Windows** | [DesktopPet-windows.exe](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-windows.exe) |
| 🐧 **Linux** | [DesktopPet-linux](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-linux) |
| 🍎 **macOS** | [DesktopPet-macos](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-macos) |

> **Windows**: Double-click the `.exe` to run.  
> **Linux**: `chmod +x DesktopPet-linux && ./DesktopPet-linux`  
> **macOS**: Right-click → Open (first time to bypass Gatekeeper).

[All Releases →](https://github.com/panzhaohu666/desktop-pet/releases)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Transparent & Frameless** | No background, no border, always-on-top window |
| **Drag to Move** | Left-click drag anywhere on screen |
| **9 Animations** | Jump, squash, shake, tilt, wiggle, bounce, backflip, sneeze, rapid spin |
| **Double-click Eggs** | 3 special double-click-exclusive animations |
| **Idle Breathing** | Subtle sinusoidal breathing — feels alive |
| **Auto-Wander** | Randomly roams the screen every 25~50 seconds |
| **Screen Bounds** | Cannot be dragged off-screen; snaps to edges |
| **Scroll Resize** | 50% ~ 250% via mouse wheel |
| **Speech Bubbles** | 60+ Chinese phrases; pink bubbles for exciting moments |
| **System Tray** | Minimize to tray, click to show/hide, right-click to quit |
| **Persistent Config** | Remembers position, scale, always-on-top |
| **Cross-Platform** | Identical features on Windows & Linux |

---

## 🎮 Controls

| Action | Trigger |
|--------|---------|
| Move | Left-click & drag |
| Random interaction (6 types) | Single click |
| Special interaction (3 types) | Double click |
| Context menu | Right-click |
| Resize | Mouse scroll wheel |

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- PyQt5 >= 5.15
- Pillow >= 8.0

### Run

```bash
git clone https://github.com/panzhaohu666/desktop-pet.git
cd desktop-pet
pip install -r requirements.txt
python run.py
```

### Custom Character

Replace `resources/pet.png` with your own **transparent PNG** — anime, game mascot, or pet photo.

---

## 📦 Build EXE (Windows)

Double-click `build.bat` or:

```bash
python build_exe.py
```

Output: `dist/DesktopPet.exe` — standalone, no Python required.

---

## 📁 Project Structure

```
desktop_pet/
├── main.py             # Entry point + system tray + resource management
├── pet_window.py       # Core: drag, 9 animations, screen physics, menus
├── bubble_widget.py    # Speech bubble overlay (white / pink)
├── phrases.py          # 60 Chinese phrases across 4 categories
├── config_manager.py   # QSettings-based persistent configuration
├── run.py              # Convenience launcher
├── build_exe.py        # PyInstaller packaging script
├── build.bat           # Windows one-click build
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── resources/
    └── pet.png         # Character sprite (replaceable!)
```

---

## 🎨 Customization

| What | How |
|------|-----|
| **Character** | Replace `resources/pet.png` with any transparent PNG |
| **Phrases** | Edit `phrases.py` |
| **Animation speed** | Tune `duration` / `interval_ms` in `pet_window.py` |
| **Wander frequency** | Adjust `wander_timer` interval |
| **Edge snap** | Change `EDGE_SNAP_DISTANCE` constant |

---

## 📄 License

MIT © [panzhaohu666](https://github.com/panzhaohu666)

---

## 🤝 Community

- [📋 Changelog](CHANGELOG.md) — version history
- [🤝 Contributing](CONTRIBUTING.md) — how to contribute
- [🐛 Bug Report](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml)
- [✨ Feature Request](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml)
