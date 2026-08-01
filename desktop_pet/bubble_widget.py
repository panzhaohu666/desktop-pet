from typing import Optional

from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QRectF, QPropertyAnimation, pyqtProperty,
)
from PyQt5.QtGui import (
    QPainter, QPainterPath, QPen, QBrush, QColor, QFont,
)
from PyQt5.QtWidgets import QWidget


BUBBLE_WIDTH = 200
BUBBLE_HEIGHT = 52
ARROW_HEIGHT = 10
ARROW_WIDTH = 16
BORDER_RADIUS = 12
PADDING_H = 16
FONT_SIZE = 13

# 普通气泡颜色
WHITE_BG = QColor(255, 255, 255)
WHITE_BORDER = QColor(180, 180, 180)
WHITE_TEXT = QColor(60, 60, 60)

# 激动气泡颜色
PINK_BG = QColor(255, 240, 245)
PINK_BORDER = QColor(255, 150, 180)
PINK_TEXT = QColor(180, 50, 80)


class BubbleWidget(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(None)
        self._text: str = ""
        self._opacity: float = 1.0
        self._bg: QColor = WHITE_BG
        self._border: QColor = WHITE_BORDER
        self._text_color: QColor = WHITE_TEXT

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

        self.setFixedSize(BUBBLE_WIDTH, BUBBLE_HEIGHT + ARROW_HEIGHT)

    def _get_opacity(self) -> float:
        return self._opacity

    def _set_opacity(self, value: float) -> None:
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, _get_opacity, _set_opacity)

    def _choose_colors(self, text: str) -> None:
        """根据内容选择气泡配色。"""
        excited_keywords = ["！", "哇", "耶", "超", "好厉害", "开心", "热情"]
        if any(kw in text for kw in excited_keywords):
            self._bg, self._border, self._text_color = PINK_BG, PINK_BORDER, PINK_TEXT
        else:
            self._bg, self._border, self._text_color = WHITE_BG, WHITE_BORDER, WHITE_TEXT

    def show_bubble(self, text: str, target_pos: QPoint) -> None:
        self._text = text
        self._choose_colors(text)
        x = target_pos.x() - (BUBBLE_WIDTH // 4)
        y = target_pos.y() - BUBBLE_HEIGHT - ARROW_HEIGHT - 4
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
        y = target_pos.y() - BUBBLE_HEIGHT - ARROW_HEIGHT - 4
        self.move(x, y)

    def _fade_out(self) -> None:
        self._hide_anim.stop()
        self._hide_anim.start()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)

        w, h, r = BUBBLE_WIDTH, BUBBLE_HEIGHT, BORDER_RADIUS

        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, w, h), r, r)
        ac = w // 2
        path.moveTo(ac - ARROW_WIDTH // 2, h)
        path.lineTo(ac, h + ARROW_HEIGHT)
        path.lineTo(ac + ARROW_WIDTH // 2, h)
        path.closeSubpath()

        simplified = path.simplified()

        painter.setPen(QPen(self._border, 1.5))
        painter.setBrush(QBrush(self._bg))
        painter.drawPath(simplified)

        font = QFont("Microsoft YaHei", FONT_SIZE)
        font.setStyleHint(QFont.SansSerif)
        painter.setFont(font)
        painter.setPen(self._text_color)
        text_rect = QRectF(PADDING_H, 0, w - 2 * PADDING_H, h)
        painter.drawText(
            text_rect,
            Qt.AlignVCenter | Qt.AlignHCenter | Qt.TextWordWrap,
            self._text,
        )
        painter.end()
