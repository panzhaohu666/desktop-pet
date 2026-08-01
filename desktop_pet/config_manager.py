"""
配置管理器 - 使用 QSettings 持久化桌面宠物的位置、大小和置顶状态。

Windows 存储路径: %APPDATA%/desktop_pet/config.ini
Linux 存储路径:   ~/.config/desktop_pet/config.ini
"""

import os
import sys
from typing import Optional

from PyQt5.QtCore import QSettings, QPoint


# 组织名和应用名决定了配置文件存储路径
ORG_NAME = "DesktopPet"
APP_NAME = "desktop_pet"

# 默认值
DEFAULT_SIZE = 128
DEFAULT_SCALE = 1.0
DEFAULT_ALWAYS_ON_TOP = True
CONFIG_VERSION = 2  # 配置结构版本号，升级时自动迁移


class ConfigManager:
    """管理桌面宠物的持久化配置。"""

    def __init__(self) -> None:
        self._settings = QSettings(ORG_NAME, APP_NAME)
        self._migrate()

    # ---- 读写 ------------------------------------------------------------

    def _migrate(self) -> None:
        """配置版本迁移。"""
        stored = int(self._settings.value("config_version", 1))
        if stored < CONFIG_VERSION:
            self._settings.setValue("config_version", CONFIG_VERSION)

    def get_position(self) -> Optional[QPoint]:
        """读取保存的位置，如果从未保存过则返回 None。"""
        x_val = self._settings.value("position/x")
        y_val = self._settings.value("position/y")
        if x_val is not None and y_val is not None:
            return QPoint(int(x_val), int(y_val))
        return None

    def get_scale(self) -> float:
        """读取缩放比例，默认 1.0。"""
        val = self._settings.value("size/scale", DEFAULT_SCALE)
        try:
            return float(val)
        except (TypeError, ValueError):
            return DEFAULT_SCALE

    def get_always_on_top(self) -> bool:
        """读取置顶状态，默认 True。"""
        val = self._settings.value("window/always_on_top", DEFAULT_ALWAYS_ON_TOP)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes")
        return DEFAULT_ALWAYS_ON_TOP

    # ---- 写入 ------------------------------------------------------------

    def save_position(self, pos: QPoint) -> None:
        """保存窗口位置。"""
        self._settings.setValue("position/x", pos.x())
        self._settings.setValue("position/y", pos.y())

    def save_scale(self, scale: float) -> None:
        """保存缩放比例。"""
        self._settings.setValue("size/scale", scale)

    def save_always_on_top(self, on_top: bool) -> None:
        """保存置顶状态。"""
        self._settings.setValue("window/always_on_top", on_top)

    def save_all(self, pos: QPoint, scale: float, on_top: bool) -> None:
        """一次性保存所有配置项。"""
        self.save_position(pos)
        self.save_scale(scale)
        self.save_always_on_top(on_top)

    # ---- 通用存取 ----------------------------------------------------------

    def get(self, key: str, default=None):
        """通用读取，支持带默认值。"""
        return self._settings.value(key, default)

    def set(self, key: str, value) -> None:
        """通用写入。"""
        self._settings.setValue(key, value)

    # ---- 工具 ------------------------------------------------------------

    @staticmethod
    def config_dir() -> str:
        """返回配置文件所在的目录路径。"""
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
        else:
            base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return os.path.join(base, "desktop_pet")

    @staticmethod
    def config_path() -> str:
        """返回配置文件的完整路径。"""
        return os.path.join(ConfigManager.config_dir(), "config.ini")
