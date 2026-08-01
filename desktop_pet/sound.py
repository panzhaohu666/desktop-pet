import logging
import math
import os
import struct
import tempfile
import wave

from PyQt5.QtCore import QUrl

log = logging.getLogger(__name__)

try:
    from PyQt5.QtMultimedia import QSoundEffect
    _HAS_MULTIMEDIA = True
except ImportError:
    _HAS_MULTIMEDIA = False
    log.info("QtMultimedia not available — sound disabled")

from .config_manager import ConfigManager


def _generate_beep(freq: int, duration_ms: int, volume: float = 0.3) -> str:
    try:
        sample_rate = 22050
        num_samples = int(sample_rate * duration_ms / 1000)
        path = os.path.join(tempfile.gettempdir(),
                            f"dp_beep_{freq}_{duration_ms}.wav")
        if os.path.exists(path):
            return path

        with wave.open(path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            frames = []
            for i in range(num_samples):
                t = i / sample_rate
                value = int(volume * 32767 *
                            math.sin(2 * math.pi * freq * t))
                frames.append(struct.pack('<h', value))
            wf.writeframes(b''.join(frames))
        return path
    except Exception:
        return ""


_SOUNDS = {}
for _name, _freq, _dur, _vol in [
    ("click", 800, 80, 0.25),
    ("special", 1200, 100, 0.3),
    ("wander", 500, 60, 0.15),
]:
    p = _generate_beep(_freq, _dur, _vol)
    if p:
        _SOUNDS[_name] = p


def _is_enabled() -> bool:
    try:
        cfg = ConfigManager()
        val = cfg.get("sound/enabled", True)
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes")
        return bool(val)
    except Exception:
        return True


def _play(name: str) -> None:
    if not _HAS_MULTIMEDIA:
        return
    path = _SOUNDS.get(name)
    if not path or not os.path.exists(path):
        return
    try:
        if name not in _players:
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(path))
            effect.setVolume(0.5)
            _players[name] = effect
        _players[name].play()
    except Exception:
        pass


_players = {}


def play_click() -> None:
    try:
        if _is_enabled():
            _play("click")
    except Exception:
        pass


def play_special() -> None:
    try:
        if _is_enabled():
            _play("special")
    except Exception:
        pass


def play_wander() -> None:
    try:
        if _is_enabled():
            _play("wander")
    except Exception:
        pass
