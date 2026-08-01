import math
import os
import random
from typing import Optional, Callable

from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QRect,
)
from PyQt5.QtGui import (
    QMouseEvent, QWheelEvent, QPixmap, QPainter, QTransform, QColor, QPen,
)
from PyQt5.QtWidgets import (
    QWidget, QLabel, QMenu, QApplication,
)

from .bubble_widget import BubbleWidget
from .config_manager import ConfigManager
from .phrases import get_random_phrase, get_phrase
from . import sound
from .settings_dialog import SettingsDialog


class PetWindow(QWidget):

    EDGE_SNAP_DISTANCE = 30

    def __init__(self, image_path: str, skins: Optional[dict] = None) -> None:
        super().__init__()
        self.config_mgr = ConfigManager()
        self._skins = skins or {}

        self.base_size = 180
        self.scale = self.config_mgr.get_scale()
        self.always_on_top = self.config_mgr.get_always_on_top()
        self._skin_key = self.config_mgr.get("appearance/skin", "")

        resolved = self._skins.get(self._skin_key, image_path)
        self.original_pixmap = QPixmap(resolved) if os.path.exists(resolved) else self._create_default_pixmap()
        if self.original_pixmap.isNull():
            self.original_pixmap = self._create_default_pixmap()

        self._is_dragging = False
        self._drag_position = QPoint()
        self._drag_distance = 0
        self._is_animating = False
        self._active_step_timers = []
        self._anim_cancelled = False

        # 双击检测
        self._click_timer = QTimer(self)
        self._click_timer.setSingleShot(True)
        self._click_timer.setInterval(300)
        self._click_timer.timeout.connect(self._on_single_click)
        self._pending_click = False

        self._init_window_flags()
        self._init_ui()
        self._init_timers()

        self.bubble = BubbleWidget(None)

        self._restore_position()
        self._start_breathing()
        self._start_auto_wander()

    # ---- 默认图像 -----------------------------------------------------------

    def _create_default_pixmap(self) -> QPixmap:
        pix = QPixmap(200, 200)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(255, 200, 50))
        p.setPen(QPen(QColor(200, 140, 20), 3))
        p.drawEllipse(30, 50, 140, 130)
        p.setBrush(QColor(255, 120, 40))
        p.drawEllipse(85, 20, 30, 35)
        p.setBrush(QColor(80, 160, 60))
        p.drawRect(82, 12, 6, 14)
        p.setBrush(QColor(30, 30, 30))
        p.drawEllipse(70, 90, 12, 18)
        p.drawEllipse(118, 90, 12, 18)
        p.setBrush(Qt.white)
        p.drawEllipse(74, 94, 5, 7)
        p.drawEllipse(122, 94, 5, 7)
        p.setBrush(QColor(200, 60, 60))
        p.drawEllipse(90, 145, 20, 15)
        p.end()
        return pix

    # ---- 窗口初始化 ---------------------------------------------------------

    def _init_window_flags(self) -> None:
        flags = Qt.FramelessWindowHint | Qt.Tool
        if self.always_on_top:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def _init_ui(self) -> None:
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self._update_image_size()

    def _init_timers(self) -> None:
        chat_secs = int(self.config_mgr.get("behavior/chat_interval", 20))
        self.idle_chat_timer = QTimer(self)
        self.idle_chat_timer.setInterval(chat_secs * 1000)
        self.idle_chat_timer.timeout.connect(self._on_idle_timeout)
        self.idle_chat_timer.start()

    def _update_image_size(self, scale_override: Optional[float] = None) -> None:
        s = scale_override if scale_override is not None else self.scale
        current_dim = int(self.base_size * s)
        self.setFixedSize(current_dim, current_dim)
        self.label.setFixedSize(current_dim, current_dim)
        self.label.move(0, 0)
        scaled_pix = self.original_pixmap.scaled(
            current_dim, current_dim,
            Qt.KeepAspectRatio, Qt.SmoothTransformation,
        )
        self.label.setPixmap(scaled_pix)

    def _restore_position(self) -> None:
        saved_pos = self.config_mgr.get_position()
        if saved_pos is not None:
            self.move(self._clamp_to_screen(saved_pos))
        else:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)

    # ---- 屏幕边界逻辑 -------------------------------------------------------

    def _screen_geometry(self) -> QRect:
        return QApplication.primaryScreen().availableGeometry()

    def _clamp_to_screen(self, pos: QPoint) -> QPoint:
        scr = self._screen_geometry()
        x = max(scr.left(), min(pos.x(), scr.right() - self.width()))
        y = max(scr.top(), min(pos.y(), scr.bottom() - self.height()))
        return QPoint(x, y)

    def _snap_to_edge(self, pos: QPoint) -> QPoint:
        """如果宠物靠近屏幕边缘，吸附过去。"""
        scr = self._screen_geometry()
        cx = pos.x() + self.width() // 2
        cy = pos.y() + self.height() // 2

        snap_x = pos.x()
        snap_y = pos.y()

        if cx - scr.left() < self.EDGE_SNAP_DISTANCE:
            snap_x = scr.left()
        elif scr.right() - cx < self.EDGE_SNAP_DISTANCE:
            snap_x = scr.right() - self.width()

        if cy - scr.top() < self.EDGE_SNAP_DISTANCE:
            snap_y = scr.top()
        elif scr.bottom() - cy < self.EDGE_SNAP_DISTANCE:
            snap_y = scr.bottom() - self.height()

        return QPoint(snap_x, snap_y)

    # ---- 呼吸动画 -----------------------------------------------------------

    def _start_breathing(self) -> None:
        self._breath_phase = 0.0
        self._breath_timer = QTimer(self)
        self._breath_timer.setInterval(100)  # 10fps — 足够平滑，不阻塞事件循环
        self._breath_timer.timeout.connect(self._on_breath_tick)
        self._breath_timer.start()

    def _on_breath_tick(self) -> None:
        if self._is_animating:
            return
        self._breath_phase += 0.21  # ≈ 每 3 秒一个完整周期
        breath_scale = 1.0 + 0.015 * math.sin(self._breath_phase)
        self._update_image_size(self.scale * breath_scale)

    # ---- 自动游走 -----------------------------------------------------------

    def _start_auto_wander(self) -> None:
        wander_secs = int(self.config_mgr.get("behavior/wander_interval", 35))
        interval = wander_secs * 1000
        self._wander_timer = QTimer(self)
        self._wander_timer.setInterval(random.randint(interval - 5000, interval + 5000))
        self._wander_timer.timeout.connect(self._do_wander)
        self._wander_timer.start()

    def _do_wander(self) -> None:
        if self._is_animating or self._is_dragging:
            return
        self._anim_cancelled = False
        scr = self._screen_geometry()
        margin = self.width()
        dx = random.randint(-120, 120)
        dy = random.randint(-80, 80)
        target = self._clamp_to_screen(QPoint(
            self.x() + dx, self.y() + dy
        ))

        self._is_animating = True
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(800 + random.randint(0, 400))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.setStartValue(self.pos())
        anim.setEndValue(target)
        self._safe_anim_finished(anim, self._anim_done, 4000)
        anim.finished.connect(lambda: self.config_mgr.save_position(self.pos()))
        anim.start()
        self.bubble.show_bubble(get_phrase("wander", self._get_skin_dir()), self.pos())
        sound.play_wander()

        wander_secs = int(self.config_mgr.get("behavior/wander_interval", 35))
        self._wander_timer.setInterval(random.randint(
            (wander_secs - 5) * 1000, (wander_secs + 5) * 1000))

    # ---- 鼠标事件 -----------------------------------------------------------

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_distance = 0
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self._stop_pos_animations()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_dragging and event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self._drag_position
            dx = abs(new_pos.x() - self.x())
            dy = abs(new_pos.y() - self.y())
            self._drag_distance += dx + dy
            self.move(self._clamp_to_screen(new_pos))
            self.bubble.refresh_position(self.pos())
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            was_drag = self._is_dragging and self._drag_distance > 8
            self._is_dragging = False

            if was_drag:
                snapped = self._snap_to_edge(self.pos())
                if snapped != self.pos():
                    self._animate_move(snapped, 150)
                self.config_mgr.save_position(self.pos())
            elif self._click_timer.isActive():
                self._click_timer.stop()
                self._pending_click = False
                self._on_double_click()
            else:
                self._pending_click = True
                self._click_timer.start()
            event.accept()

    def _on_single_click(self) -> None:
        self._pending_click = False
        self.trigger_random_interaction()

    def _on_double_click(self) -> None:
        self._trigger_special_interaction()

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        old_scale = self.scale
        self.scale = round(min(max(self.scale + (0.1 if delta > 0 else -0.1), 0.5), 2.5), 2)

        if old_scale != self.scale:
            center = self.geometry().center()
            self._update_image_size()
            new_rect = self.rect()
            new_rect.moveCenter(center)
            self.move(self._clamp_to_screen(new_rect.topLeft()))
            self.config_mgr.save_scale(self.scale)
            self.bubble.show_bubble(f"大小: {int(self.scale * 100)}%", self.pos())
        event.accept()

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white; border: 1px solid #d0d0d0;
                border-radius: 6px; padding: 4px;
                font-family: 'Microsoft YaHei'; font-size: 12px;
            }
            QMenu::item { padding: 6px 24px 6px 12px; border-radius: 4px; }
            QMenu::item:selected { background-color: #4a90e2; color: white; }
        """)

        menu.addAction("放大 (+)").triggered.connect(self.zoom_in)
        menu.addAction("缩小 (-)").triggered.connect(self.zoom_out)
        menu.addAction("重置大小 (100%)").triggered.connect(self.reset_size)
        menu.addSeparator()

        if len(self._skins) > 1:
            skin_menu = menu.addMenu("切换皮肤")
            for skin_name in self._skins:
                act = skin_menu.addAction(f"  {skin_name}")
                act.setCheckable(True)
                act.setChecked(skin_name == self._skin_key)
                act.triggered.connect(lambda checked, s=skin_name: self._switch_skin(s))

        menu.addAction(
            "取消置顶" if self.always_on_top else "始终置顶"
        ).triggered.connect(self.toggle_always_on_top)
        menu.addAction("手动游走").triggered.connect(self._do_wander)
        menu.addAction("陪我聊天").triggered.connect(self.trigger_random_interaction)
        menu.addSeparator()
        menu.addAction("设置...").triggered.connect(self._open_settings)
        menu.addAction("最小化到托盘").triggered.connect(self.hide)
        menu.addAction("退出程序").triggered.connect(QApplication.quit)
        menu.exec_(event.globalPos())

    def _switch_skin(self, skin_name: str) -> None:
        if skin_name == self._skin_key:
            return
        resolved = self._skins.get(skin_name)
        if resolved and os.path.exists(resolved):
            self._skin_key = skin_name
            self.original_pixmap = QPixmap(resolved)
            self._update_image_size()
            self.config_mgr.set("appearance/skin", skin_name)
            self.bubble.show_bubble(f"已切换皮肤: {skin_name}", self.pos())

    def _get_skin_dir(self) -> str:
        """获取当前皮肤所在的文件夹路径"""
        resolved = self._skins.get(self._skin_key)
        if resolved and os.path.exists(resolved):
            return os.path.dirname(resolved)
        return ""

    def _open_settings(self) -> None:
        dlg = SettingsDialog(self, self.config_mgr, list(self._skins.keys()))
        if dlg.exec_() == SettingsDialog.Accepted:
            self._apply_settings()

    def _apply_settings(self) -> None:
        self.scale = self.config_mgr.get_scale()
        self._update_image_size()

        new_top = self.config_mgr.get_always_on_top()
        if new_top != self.always_on_top:
            self.always_on_top = new_top
            pos = self.pos()
            self._init_window_flags()
            self.show()
            self.move(pos)

        new_skin = self.config_mgr.get("appearance/skin", "")
        if new_skin != self._skin_key:
            self._switch_skin(new_skin)

        chat_secs = int(self.config_mgr.get("behavior/chat_interval", 20))
        self.idle_chat_timer.setInterval(chat_secs * 1000)

    # ---- 通用动画工具 -------------------------------------------------------

    def _anim_done(self) -> None:
        self._is_animating = False

    def _stop_pos_animations(self) -> None:
        for child in self.children():
            if isinstance(child, QPropertyAnimation):
                try:
                    child.stop()
                except Exception:
                    pass
        for t in self._active_step_timers:
            try:
                t.stop()
            except Exception:
                pass
        self._active_step_timers.clear()
        self._anim_cancelled = True
        self._is_animating = False
        self._update_image_size()

    def _safe_anim_finished(self, anim, done_fn, max_ms: int = 3000) -> None:
        anim.finished.connect(done_fn)
        guard = QTimer(self)
        guard.setSingleShot(True)
        guard.timeout.connect(lambda: (
            anim.stop(),
            done_fn() if not self._anim_cancelled else None
        ))
        guard.start(max_ms)

    def _animate_move(self, target: QPoint, duration_ms: int) -> None:
        self._is_animating = True
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(duration_ms)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.setStartValue(self.pos())
        anim.setEndValue(target)
        self._safe_anim_finished(anim, self._anim_done, 2000)
        anim.start()

    def _run_step_animation(self, step_fn: Callable[[int], None],
                            total_steps: int, interval_ms: int,
                            done_fn: Callable[[], None]) -> None:
        counter = [0]
        timer = QTimer(self)
        timer.setInterval(interval_ms)
        self._active_step_timers.append(timer)

        def _step():
            idx = counter[0]
            if idx >= total_steps:
                timer.stop()
                timer.deleteLater()
                if timer in self._active_step_timers:
                    self._active_step_timers.remove(timer)
                done_fn()
                return
            step_fn(idx)
            counter[0] += 1

        timer.timeout.connect(_step)
        timer.start()

    # ---- 单击互动（随机）----------------------------------------------------

    def trigger_random_interaction(self) -> None:
        if self._is_animating:
            return
        self._anim_cancelled = False
            
        # 尝试播放序列帧动画
        if self._play_random_sprite_anim("click"):
            self.bubble.show_bubble(get_random_phrase(self._get_skin_dir()), self.pos())
            sound.play_click()
            return
            
        # 如果没有序列帧，降级到代码动画
        random.choice([
            self.anim_jump, self.anim_squash,
            self.anim_shake, self.anim_spin_tilt,
            self.anim_wiggle, self.anim_bounce,
        ])()
        self.bubble.show_bubble(get_random_phrase(self._get_skin_dir()), self.pos())
        sound.play_click()

    # ---- 双击特殊互动 -------------------------------------------------------

    def _trigger_special_interaction(self) -> None:
        if self._is_animating:
            return
        self._anim_cancelled = False
            
        if self._play_random_sprite_anim("double_click"):
            self.bubble.show_bubble(get_phrase("double_click", self._get_skin_dir()), self.pos())
            sound.play_special()
            return

        random.choice([
            self.anim_backflip, self.anim_sneeze,
            self.anim_rapid_spin,
        ])()
        self.bubble.show_bubble(get_phrase("double_click", self._get_skin_dir()), self.pos())
        sound.play_special()

    # ---- 序列帧动画支持 -----------------------------------------------------

    def _play_random_sprite_anim(self, category: str) -> bool:
        """尝试在当前皮肤下寻找对应分类的序列帧并播放。找到返回True，否则返回False。"""
        skin_dir = self._get_skin_dir()
        if not skin_dir:
            return False
            
        category_dir = os.path.join(skin_dir, category)
        if not os.path.isdir(category_dir):
            return False
            
        # 找该分类下的所有动作文件夹（例如 skins/default/click/jump/）
        actions = [d for d in os.listdir(category_dir) 
                  if os.path.isdir(os.path.join(category_dir, d))]
        
        if not actions:
            # 如果没有子文件夹，直接把当前目录当成一个动作帧序列
            return self._play_sprite_sequence(category_dir)
            
        # 随机挑一个动作
        chosen_action = random.choice(actions)
        return self._play_sprite_sequence(os.path.join(category_dir, chosen_action))

    def _play_sprite_sequence(self, seq_dir: str) -> bool:
        """播放指定目录下的序列帧 PNG"""
        frames = []
        for f in sorted(os.listdir(seq_dir)):
            if f.lower().endswith('.png'):
                frames.append(os.path.join(seq_dir, f))
                
        if not frames:
            return False
            
        self._is_animating = True
        dim = int(self.base_size * self.scale)
        
        def step(i: int):
            frame_path = frames[i]
            pix = QPixmap(frame_path)
            if not pix.isNull():
                scaled = pix.scaled(dim, dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled)
                
        def done():
            self._update_image_size()  # 恢复默认图片
            self._is_animating = False
            
        # 假设 15fps (约 66ms 一帧)
        self._run_step_animation(step, len(frames), 66, done)
        return True

    # ---- 动画实现 -----------------------------------------------------------

    def anim_jump(self) -> None:
        self._is_animating = True
        orig = self.pos()
        peak = QPoint(orig.x(), max(0, orig.y() - 50))
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(420)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.setStartValue(orig)
        anim.setKeyValueAt(0.5, peak)
        anim.setEndValue(orig)
        self._safe_anim_finished(anim, self._anim_done, 2000)
        anim.start()

    def anim_squash(self) -> None:
        self._is_animating = True
        dim = int(self.base_size * self.scale)

        def step(progress: float):
            t = progress * 2
            if t <= 1.0:
                sx, sy = 1.0 + t * 0.15, 1.0 - t * 0.15
            else:
                t -= 1.0
                sx, sy = 1.15 - t * 0.15, 0.85 + t * 0.15
            squashed = self.original_pixmap.transformed(
                QTransform.fromScale(sx, sy), Qt.SmoothTransformation)
            self.label.setPixmap(squashed.scaled(
                dim, dim, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self._run_step_animation(
            lambda i: step(i / 7.0), 8, 38, self._anim_done)

    def anim_shake(self) -> None:
        self._is_animating = True
        orig = self.pos()

        def step(i: int):
            self.move(orig.x() + (8 if i % 2 == 0 else -8), orig.y())

        def done():
            self.move(orig)
            self._is_animating = False

        self._run_step_animation(step, 6, 45, done)

    def anim_spin_tilt(self) -> None:
        self._is_animating = True
        dim = int(self.base_size * self.scale)
        angles = [0, 10, -10, 8, -8, 0]

        def step(i: int):
            angle = angles[i]
            scaled = self.original_pixmap.scaled(
                dim, dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if angle != 0:
                scaled = scaled.transformed(
                    QTransform().rotate(angle), Qt.SmoothTransformation)
            self.label.setPixmap(scaled)

        self._run_step_animation(step, len(angles), 55, self._anim_done)

    def anim_wiggle(self) -> None:
        """左右扭动"""
        self._is_animating = True
        orig = self.pos()

        def step(i: int):
            offset = int(6 * math.sin(i * 0.8))
            self.move(orig.x() + offset, orig.y())

        def done():
            self.move(orig)
            self._is_animating = False

        self._run_step_animation(step, 10, 50, done)

    def anim_bounce(self) -> None:
        """原地小跳"""
        self._is_animating = True
        orig = self.pos()
        heights = [0, -20, 0, -12, 0, -6, 0]

        def step(i: int):
            self.move(orig.x(), orig.y() + heights[i])

        def done():
            self.move(orig)
            self._is_animating = False

        self._run_step_animation(step, len(heights), 80, done)

    def anim_backflip(self) -> None:
        """后空翻"""
        self._is_animating = True
        dim = int(self.base_size * self.scale)
        orig = self.pos()
        angles = [0, 45, 90, 135, 180, 225, 270, 315, 360]

        def step(i: int):
            progress = i / (len(angles) - 1)
            y_offset = int(-30 * math.sin(progress * math.pi))
            self.move(orig.x(), orig.y() + y_offset)
            angle = angles[i]
            scaled = self.original_pixmap.scaled(
                dim, dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if angle != 0:
                scaled = scaled.transformed(
                    QTransform().rotate(angle), Qt.SmoothTransformation)
            self.label.setPixmap(scaled)

        def done():
            self.move(orig)
            self._update_image_size()
            self._is_animating = False

        self._run_step_animation(step, len(angles), 50, done)

    def anim_sneeze(self) -> None:
        """喷嚏：抖动 + 缩成一团"""
        self._is_animating = True
        dim = int(self.base_size * self.scale)
        orig = self.pos()

        def step(i: int):
            if i < 4:
                offset = 4 if i % 2 == 0 else -4
                self.move(orig.x() + offset, orig.y())
                self._update_image_size(self.scale)
            elif i < 6:
                self.move(orig.x(), orig.y())
                self._update_image_size(self.scale * 0.8)
            else:
                self.move(orig.x(), orig.y())
                self._update_image_size(self.scale * (0.8 + (i - 5) * 0.1))

        def done():
            self.move(orig)
            self._update_image_size()
            self._is_animating = False

        self._run_step_animation(step, 8, 60, done)

    def anim_rapid_spin(self) -> None:
        """快速旋转"""
        self._is_animating = True
        dim = int(self.base_size * self.scale)
        orig = self.pos()

        def step(i: int):
            angle = i * 40
            scaled = self.original_pixmap.scaled(
                dim, dim, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scaled = scaled.transformed(
                QTransform().rotate(angle), Qt.SmoothTransformation)
            self.label.setPixmap(scaled)

        def done():
            self.move(orig)
            self._update_image_size()
            self._is_animating = False

        self._run_step_animation(step, 9, 35, done)

    # ---- 闲置 ---------------------------------------------------------------

    def _on_idle_timeout(self) -> None:
        if not self._is_animating and not self.bubble.isVisible():
            self.bubble.show_bubble(get_phrase("idle", self._get_skin_dir()), self.pos())

    # ---- 菜单操作 -----------------------------------------------------------

    def zoom_in(self) -> None:
        self.scale = min(self.scale + 0.15, 2.5)
        self._update_image_size()
        self.config_mgr.save_scale(self.scale)
        self.bubble.show_bubble(f"大小: {int(self.scale * 100)}%", self.pos())

    def zoom_out(self) -> None:
        self.scale = max(self.scale - 0.15, 0.5)
        self._update_image_size()
        self.config_mgr.save_scale(self.scale)
        self.bubble.show_bubble(f"大小: {int(self.scale * 100)}%", self.pos())

    def reset_size(self) -> None:
        self.scale = 1.0
        self._update_image_size()
        self.config_mgr.save_scale(self.scale)
        self.bubble.show_bubble("已恢复默认大小", self.pos())

    def toggle_always_on_top(self) -> None:
        self.always_on_top = not self.always_on_top
        self.config_mgr.save_always_on_top(self.always_on_top)
        pos = self.pos()
        self._init_window_flags()
        self.show()
        self.move(pos)
        self.bubble.show_bubble(
            "已开启置顶" if self.always_on_top else "已取消置顶", self.pos())
