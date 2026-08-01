"""音效模块 —— 使用 QSoundEffect 播放简短音效。无音频文件时静默降级。"""

import struct
import wave
import os
import tempfile

from PyQt5.QtCore import QUrl

try:
    from PyQt5.QtMultimedia import QSoundEffect
    _HAS_MULTIMEDIA = True
except ImportError:
    _HAS_MULTIMEDIA = False

from .config_manager import ConfigManager


def _generate_beep(freq: int, duration_ms: int, volume: float = 0.3) -> str:
    """生成简单的正弦波 WAV 文件，返回路径。"""
    sample_rate = 22050
    num_samples = int(sample_rate * duration_ms / 1000)
    path = os.path.join(tempfile.gettempdir(), f"dp_beep_{freq}_{duration_ms}.wav")
    if os.path.exists(path):
        return path

    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            value = int(volume * 32767 * __import__('math').sin(2 * 3.14159 * freq * t))
            frames.append(struct.pack('<h', value))
        wf.writeframes(b''.join(frames))
    return path


# 预生成音效文件路径
_SOUNDS = {
    "click": _generate_beep(800, 80, 0.25),
    "special": _generate_beep(1200, 100, 0.3),
    "wander": _generate_beep(500, 60, 0.15),
}


def _is_enabled() -> bool:
    cfg = ConfigManager()
    val = cfg.get("sound/enabled", True)
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes")
    return bool(val)


def play_click() -> None:
    if not _is_enabled():
        return
    _play("click")


def play_special() -> None:
    if not _is_enabled():
        return
    _play("special")


def play_wander() -> None:
    if not _is_enabled():
        return
    _play("wander")


_players = {}

def _play(name: str) -> None:
    if not _HAS_MULTIMEDIA:
        return
    path = _SOUNDS.get(name)
    if not path or not os.path.exists(path):
        return
    if name not in _players:
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(path))
        effect.setVolume(0.5)
        _players[name] = effect
    _players[name].play()
