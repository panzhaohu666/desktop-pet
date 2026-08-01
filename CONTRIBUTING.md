# Contributing to Desktop Pet

Thanks for your interest in contributing! 🐾

## Getting Started

```bash
git clone https://github.com/panzhaohu666/desktop-pet.git
cd desktop-pet
pip install -r requirements.txt
python run.py
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point, system tray, resource management |
| `pet_window.py` | Core pet window — drag, animations, physics, menus |
| `bubble_widget.py` | Speech bubble overlay |
| `phrases.py` | Chinese phrase database |
| `config_manager.py` | QSettings persistence |
| `build_exe.py` | PyInstaller build script |
| `run.py` | Convenience launcher |

## Code Style

- Python 3.8+ compatible
- Type hints on public methods (`-> None`, `-> str`, etc.)
- Follow existing patterns in each file
- No `as any` / `@ts-ignore` / bare `except:`

## Submitting Changes

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test: `python run.py` (ensure it starts without errors)
5. Commit with a [conventional commit](https://www.conventionalcommits.org/) message:
   - `feat:` — new feature
   - `fix:` — bug fix
   - `docs:` — documentation
   - `refactor:` — code cleanup
   - `ci:` — CI / build
6. Push and open a Pull Request

## Adding Phrases

Edit `phrases.py`. Add to the appropriate category or create a new one. Keep phrases short (< 30 chars) and family-friendly.

## Adding Animations

In `pet_window.py`, add a new `anim_xxx` method following the pattern:
```python
def anim_xxx(self) -> None:
    self._is_animating = True
    # ... animation logic ...
    # call self._anim_done() when finished
```

Then register it in `trigger_random_interaction()` or `_trigger_special_interaction()`.

## Reporting Issues

Use the [Bug Report](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml) or [Feature Request](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml) template.
