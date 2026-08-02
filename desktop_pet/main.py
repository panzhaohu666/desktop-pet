import logging
import os
import sys

os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
os.environ.setdefault("QT_SCALE_FACTOR_ROUNDING_POLICY", "PassThrough")

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon, QPen
from PyQt5.QtCore import Qt, QPoint

from desktop_pet.config_manager import ConfigManager
from desktop_pet.pet_window import PetWindow


def _get_resource_dir() -> str:
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "resources")


def _setup_logging() -> None:
    log_dir = ConfigManager.config_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "desktop_pet.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.info("桌宠精灵启动")


def _make_tray_icon() -> QIcon:
    pix = QPixmap(32, 32)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    # 小黄鸭身体
    p.setBrush(QColor(255, 230, 80))
    p.setPen(QPen(QColor(200, 170, 30), 2))
    p.drawEllipse(5, 10, 22, 18)
    # 翅膀
    p.setBrush(QColor(255, 210, 50))
    p.drawEllipse(16, 12, 10, 10)
    # 头
    p.setBrush(QColor(255, 240, 100))
    p.drawEllipse(8, 2, 16, 14)
    # 眼睛
    p.setBrush(QColor(20, 20, 20))
    p.drawEllipse(12, 6, 3, 3)
    p.drawEllipse(18, 6, 3, 3)
    # 嘴
    p.setBrush(QColor(255, 140, 30))
    p.drawPolygon(QPoint(22, 8), QPoint(28, 10), QPoint(22, 12))
    p.end()
    return QIcon(pix)


def ensure_pet_image() -> str:
    res_dir = _get_resource_dir()
    os.makedirs(res_dir, exist_ok=True)
    pet_img_path = os.path.join(res_dir, "pet.png")
    if os.path.exists(pet_img_path):
        return pet_img_path

    pix = QPixmap(300, 300)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    p.setBrush(QColor(255, 230, 80))
    p.setPen(QPen(QColor(200, 170, 30), 3))
    p.drawEllipse(60, 100, 180, 150)
    p.setBrush(QColor(255, 210, 50))
    p.drawEllipse(140, 105, 90, 110)
    p.setBrush(QColor(255, 240, 100))
    p.drawEllipse(90, 50, 130, 100)
    p.setBrush(QColor(20, 20, 20))
    p.drawEllipse(125, 70, 12, 16)
    p.drawEllipse(175, 70, 12, 16)
    p.setBrush(Qt.white)
    p.drawEllipse(129, 74, 4, 6)
    p.drawEllipse(179, 74, 4, 6)
    p.setBrush(QColor(255, 140, 30))
    p.setPen(QPen(QColor(200, 100, 20), 2))
    pts = [QPoint(200, 80), QPoint(240, 88), QPoint(200, 96)]
    p.drawPolygon(*pts)
    p.end()
    pix.save(pet_img_path, "PNG")
    logging.info("已生成默认宠物图片: %s", pet_img_path)
    return pet_img_path


def _scan_skins() -> dict:
    """扫描 skins/ 目录，返回 {名称: pet.png路径} 的字典。"""
    base = os.path.dirname(os.path.abspath(__file__))
    skins_dir = os.path.join(base, "skins")
    result = {}
    if not os.path.isdir(skins_dir):
        return result
    for entry in sorted(os.listdir(skins_dir)):
        skin_dir = os.path.join(skins_dir, entry)
        pet_file = os.path.join(skin_dir, "pet.png")
        if os.path.isdir(skin_dir) and os.path.isfile(pet_file):
            result[entry] = pet_file
    return result


def _acquire_lock() -> bool:
    """跨平台单实例锁。成功返回True，已有实例返回False。"""
    lock_file = os.path.join(ConfigManager.config_dir(), "desktop_pet.lock")
    os.makedirs(os.path.dirname(lock_file), exist_ok=True)
    try:
        if os.path.exists(lock_file):
            with open(lock_file, "r") as f:
                old_pid = f.read().strip()
            if old_pid:
                try:
                    os.kill(int(old_pid), 0)
                    return False  # 进程还在
                except (OSError, ValueError):
                    pass  # 进程已死
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))
        return True
    except Exception:
        return True  # 出错时允许启动


def main() -> None:
    if not _acquire_lock():
        print("桌宠精灵已在运行中")
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    _setup_logging()

    def _exception_hook(exc_type, exc_value, exc_tb):
        logging.critical("未捕获异常", exc_info=(exc_type, exc_value, exc_tb))
    sys.excepthook = _exception_hook

    major = Qt.__version_info__[1] if hasattr(Qt, '__version_info__') else 15
    if major < 14:
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    image_path = ensure_pet_image()
    skins = _scan_skins()
    logging.info("已加载 %d 套皮肤: %s", len(skins), list(skins.keys()))

    pet = PetWindow(image_path, skins)

    tray = QSystemTrayIcon(_make_tray_icon(), app)
    tray.setToolTip("桌宠精灵 — 点击显示/隐藏")

    tray_menu = QMenu()
    show_action = QAction("显示/隐藏宠物")
    show_action.triggered.connect(lambda: pet.show() if pet.isHidden() else pet.hide())
    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    quit_action = QAction("退出")
    quit_action.triggered.connect(app.quit)
    tray_menu.addAction(quit_action)
    tray.setContextMenu(tray_menu)

    def on_tray_activated(reason):
        if reason == QSystemTrayIcon.Trigger:
            pet.setVisible(not pet.isVisible())

    tray.activated.connect(on_tray_activated)
    tray.show()
    pet.show()

    app.aboutToQuit.connect(lambda: logging.info("桌宠精灵退出"))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
