"""图形化设置面板 —— 集中管理所有可配置项。"""

from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QCheckBox, QSpinBox, QPushButton, QComboBox,
    QGroupBox, QFormLayout, QDialogButtonBox,
)

from .config_manager import ConfigManager


class SettingsDialog(QDialog):
    """桌宠精灵设置对话框"""

    def __init__(self, parent=None, config_mgr: Optional[ConfigManager] = None,
                 skins: Optional[list] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("桌宠精灵 — 设置")
        self.setMinimumWidth(420)
        self.setStyleSheet("""
            QDialog { background: #f5f5f5; font-family: 'Microsoft YaHei'; }
            QGroupBox { font-weight: bold; border: 1px solid #ddd; border-radius: 6px; margin-top: 8px; padding-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
        """)

        self._cfg = config_mgr or ConfigManager()
        self._skins = skins or []

        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.addTab(self._appearance_tab(), "外观")
        tabs.addTab(self._behavior_tab(), "行为")
        layout.addWidget(tabs)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._load_values()

    # ---- 外观页 -------------------------------------------------------------

    def _appearance_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        # 缩放
        g1 = QGroupBox("大小")
        f1 = QFormLayout()
        self._scale_slider = QSlider(Qt.Horizontal)
        self._scale_slider.setRange(50, 250)
        self._scale_slider.setTickPosition(QSlider.TicksBelow)
        self._scale_slider.setTickInterval(25)
        self._scale_label = QLabel("100%")
        self._scale_slider.valueChanged.connect(
            lambda v: self._scale_label.setText(f"{v}%"))
        row = QHBoxLayout()
        row.addWidget(self._scale_slider)
        row.addWidget(self._scale_label)
        f1.addRow("缩放比例", row)
        g1.setLayout(f1)
        layout.addWidget(g1)

        # 置顶
        g2 = QGroupBox("窗口")
        f2 = QFormLayout()
        self._top_cb = QCheckBox("始终置顶")
        f2.addRow(self._top_cb)
        g2.setLayout(f2)
        layout.addWidget(g2)

        # 皮肤
        g3 = QGroupBox("皮肤")
        f3 = QFormLayout()
        self._skin_combo = QComboBox()
        self._skin_combo.addItem("默认", "default")
        for skin_name in self._skins:
            self._skin_combo.addItem(skin_name, skin_name)
        f3.addRow("当前皮肤", self._skin_combo)
        g3.setLayout(f3)
        layout.addWidget(g3)

        layout.addStretch()
        return w

    # ---- 行为页 -------------------------------------------------------------

    def _behavior_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        g1 = QGroupBox("自动行为")
        f1 = QFormLayout()
        self._wander_spin = QSpinBox()
        self._wander_spin.setRange(10, 120)
        self._wander_spin.setSuffix(" 秒")
        self._wander_spin.setToolTip("宠物自动游走的间隔时间")
        f1.addRow("游走间隔", self._wander_spin)

        self._chat_spin = QSpinBox()
        self._chat_spin.setRange(5, 60)
        self._chat_spin.setSuffix(" 秒")
        self._chat_spin.setToolTip("宠物自动说话的间隔时间")
        f1.addRow("聊天间隔", self._chat_spin)
        g1.setLayout(f1)
        layout.addWidget(g1)

        g2 = QGroupBox("音效")
        f2 = QFormLayout()
        self._sound_cb = QCheckBox("启用音效")
        f2.addRow(self._sound_cb)
        g2.setLayout(f2)
        layout.addWidget(g2)

        layout.addStretch()
        return w

    # ---- 加载 / 保存 --------------------------------------------------------

    def _load_values(self) -> None:
        v = int(self._cfg.get_scale() * 100)
        self._scale_slider.setValue(v)
        self._scale_label.setText(f"{v}%")
        self._top_cb.setChecked(self._cfg.get_always_on_top())
        self._wander_spin.setValue(int(self._cfg.get("behavior/wander_interval", 35)))
        self._chat_spin.setValue(int(self._cfg.get("behavior/chat_interval", 20)))
        self._sound_cb.setChecked(self._cfg.get("sound/enabled", True))

        current_skin = self._cfg.get("appearance/skin", "default")
        idx = self._skin_combo.findData(current_skin)
        if idx >= 0:
            self._skin_combo.setCurrentIndex(idx)

    def _save_and_accept(self) -> None:
        self._cfg.save_scale(self._scale_slider.value() / 100.0)
        self._cfg.save_always_on_top(self._top_cb.isChecked())
        self._cfg.set("behavior/wander_interval", self._wander_spin.value())
        self._cfg.set("behavior/chat_interval", self._chat_spin.value())
        self._cfg.set("sound/enabled", self._sound_cb.isChecked())
        self._cfg.set("appearance/skin", self._skin_combo.currentData())
        self.accept()

    @property
    def selected_skin(self) -> str:
        return self._skin_combo.currentData()
