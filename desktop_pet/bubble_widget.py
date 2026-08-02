from typing import Optional
import json
import os

from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QRectF, QPropertyAnimation, pyqtProperty,
)
from PyQt5.QtGui import (
    QPainter, QPainterPath, QPen, QBrush, QColor, QFont, QFontMetrics,
)
from PyQt5.QtWidgets import QWidget, QApplication


BUBBLE_WIDTH = 240
MAX_BUBBLE_BODY_HEIGHT = 140
MIN_BUBBLE_BODY_HEIGHT = 40
ARROW_HEIGHT = 10
ARROW_WIDTH = 16
BORDER_RADIUS = 12
PADDING_H = 14
PADDING_V = 8
FONT_SIZE = 13
LINE_SPACING = 4

WHITE_BG = QColor(255, 255, 255)
WHITE_BORDER = QColor(180, 180, 180)
WHITE_TEXT = QColor(60, 60, 60)
PINK_BG = QColor(255, 240, 245)
PINK_BORDER = QColor(255, 150, 180)
PINK_TEXT = QColor(180, 50, 80)


def _measure_text_height(text: str, width: int, font: QFont) -> int:
    """计算文本在指定宽度内所需的高度。"""
    fm = QFontMetrics(font)
    text_width = width - 2 * PADDING_H

    lines = 1
    line_w = 0
    for ch in text:
        char_w = fm.width(ch)
        if line_w + char_w > text_width and line_w > 0:
            lines += 1
            line_w = char_w
        else:
            line_w += char_w

    line_height = fm.height() + LINE_SPACING
    return max(lines * line_height + 2 * PADDING_V, MIN_BUBBLE_BODY_HEIGHT)


class BubbleWidget(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(None)
        self._text: str = ""
        self._opacity: float = 1.0
        self._bg: QColor = WHITE_BG
        self._border: QColor = WHITE_BORDER
        self._text_color: QColor = WHITE_TEXT
        self._skin_bg: QColor = WHITE_BG
        self._skin_border: QColor = WHITE_BORDER
        self._skin_text: QColor = WHITE_TEXT
        self._has_skin_colors: bool = False
        self._body_height: int = MIN_BUBBLE_BODY_HEIGHT
        self._font = QFont()
        self._font.setPixelSize(FONT_SIZE)
        self._font.setStyleHint(QFont.SansSerif)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self._show_anim = QPropertyAnimation(self, b"opacity")
        self._show_anim.setDuration(200)
        self._show_anim.setStartValue(0.0)
        self._show_anim.setEndValue(1.0)

        self._hide_anim = QPropertyAnimation(self, b"opacity")
        self._hide_anim.setDuration(250)
        self._hide_anim.setStartValue(1.0)
        self._hide_anim.setEndValue(0.0)
        self._hide_anim.finished.connect(self.hide)

        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self._fade_out)

        self.setFixedSize(BUBBLE_WIDTH, MIN_BUBBLE_BODY_HEIGHT + ARROW_HEIGHT)

    def _get_opacity(self) -> float:
        return self._opacity

    def _set_opacity(self, value: float) -> None:
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, _get_opacity, _set_opacity)

    def load_skin_colors(self, skin_dir: str) -> None:
        """从皮肤目录加载气泡配色，无则保持默认。"""
        if not skin_dir:
            return
        path = os.path.join(skin_dir, "bubble_colors.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._skin_bg = QColor(data.get("bg", "#FFFFFF"))
            self._skin_border = QColor(data.get("border", "#B4B4B4"))
            self._skin_text = QColor(data.get("text", "#3C3C3C"))
            self._has_skin_colors = True
        except (json.JSONDecodeError, OSError, KeyError):
            self._has_skin_colors = False

    def _choose_colors(self, text: str) -> None:
        if self._has_skin_colors:
            self._bg = self._skin_bg
            self._border = self._skin_border
            self._text_color = self._skin_text
            return

    def show_bubble(self, text: str, target_pos: QPoint) -> None:
        self._text = text
        self._choose_colors(text)

        body_h = min(_measure_text_height(text, BUBBLE_WIDTH, self._font),
                     MAX_BUBBLE_BODY_HEIGHT)
        self._body_height = body_h
        total_h = body_h + ARROW_HEIGHT
        self.setFixedSize(BUBBLE_WIDTH, total_h)

        x = target_pos.x() - (BUBBLE_WIDTH // 4)
        y = target_pos.y() - total_h - 4

        if QApplication.primaryScreen():
            scr = QApplication.primaryScreen().availableGeometry()
            x = max(0, min(x, scr.right() - BUBBLE_WIDTH))
            y = max(0, y)

        self.move(x, y)
        self._show_anim.stop()
        self._hide_anim.stop()
        self._opacity = 1.0
        self.show()
        self._show_anim.start()
        self._auto_hide_timer.start(3000)

    def refresh_position(self, target_pos: QPoint) -> None:
        if not self.isVisible():
            return
        x = target_pos.x() - (BUBBLE_WIDTH // 4)
        y = target_pos.y() - self.height() - 4
        if QApplication.primaryScreen():
            scr = QApplication.primaryScreen().availableGeometry()
            x = max(0, min(x, scr.right() - BUBBLE_WIDTH))
        self.move(x, y)

    def _fade_out(self) -> None:
        self._hide_anim.stop()
        self._hide_anim.start()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)

        w, bh, r = BUBBLE_WIDTH, self._body_height, BORDER_RADIUS

        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, w, bh), r, r)
        ac = w // 2
        path.moveTo(ac - ARROW_WIDTH // 2, bh)
        path.lineTo(ac, bh + ARROW_HEIGHT)
        path.lineTo(ac + ARROW_WIDTH // 2, bh)
        path.closeSubpath()

        simplified = path.simplified()
        painter.setPen(QPen(self._border, 1.5))
        painter.setBrush(QBrush(self._bg))
        painter.drawPath(simplified)

        painter.setFont(self._font)
        painter.setPen(self._text_color)
        text_rect = QRectF(PADDING_H, PADDING_V, w - 2 * PADDING_H, bh - 2 * PADDING_V)
        painter.drawText(
            text_rect,
            Qt.AlignVCenter | Qt.AlignHCenter | Qt.TextWordWrap,
            self._text,
        )
        painter.end()
