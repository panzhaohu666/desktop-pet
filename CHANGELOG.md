# Changelog

## v1.0.2 (2026-08-01)

### Added
- Cross-platform CI/CD via GitHub Actions (Windows / Linux / macOS)
- Pre-built binaries in release assets
- Detailed release notes with feature table
- Repository topics and metadata

### Fixed
- Windows CI build: removed non-ASCII chars from build script

---

## v1.0.1

### Added
- Idle breathing animation (sinusoidal micro-motion)
- Auto-wander mode (random roaming every 25~50s)
- Screen boundary clamping + edge snap
- Double-click detection with 3 exclusive animations (backflip, sneeze, rapid spin)
- 3 new single-click animations (wiggle, bounce, rapid spin)
- Pink speech bubbles for exciting phrases
- System tray integration
- Context-aware phrases (double_click, wander, idle categories)
- Expanded phrase library to 60+ entries

### Fixed
- Bubble parent window causing clipping — now independent top-level window
- Python 3.8/3.9 compatibility (replaced `|` type syntax with `Optional`)
- `setPen(QColor, width)` → `setPen(QPen(QColor, width))` for PyQt5 compatibility
- `run.py` import path resolution
- Missing `__init__.py` for package imports
- `anim_squash` geometry overrun → pixmap transform approach
- `AA_EnableHighDpiScaling` deprecation warning
- `_fade_out` signal leak (repeated `connect`)
- `ensure_pet_image` now works in PyInstaller frozen environment
- Removed unused `Tuple` import
- Fixed floating-point scale precision

---

## v1.0.0

### Initial Release
- Transparent frameless always-on-top window
- Drag to move
- Scroll wheel resize (50%–250%)
- 4 click animations: jump, squash, shake, spin-tilt
- 35 Chinese phrases in speech bubbles
- Right-click context menu (zoom, always-on-top, exit)
- QSettings-based persistent configuration
- PyInstaller packaging support
- Default character sprite auto-generation
