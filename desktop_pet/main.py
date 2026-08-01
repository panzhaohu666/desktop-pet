import logging
import os
import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon, QPen
from PyQt5.QtCore import Qt

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
    p.setBrush(QColor(255, 200, 50))
    p.setPen(QPen(QColor(200, 140, 20), 2))
    p.drawEllipse(4, 6, 24, 22)
    p.setBrush(QColor(255, 120, 40))
    p.drawEllipse(14, 0, 10, 10)
    p.setBrush(QColor(30, 30, 30))
    p.drawEllipse(10, 12, 3, 4)
    p.drawEllipse(19, 12, 3, 4)
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
    p.setBrush(QColor(255, 200, 50))
    p.setPen(QPen(QColor(200, 140, 20), 3))
    p.drawEllipse(50, 80, 200, 190)
    p.setBrush(QColor(255, 120, 40))
    p.drawEllipse(120, 35, 60, 65)
    p.setBrush(QColor(80, 160, 60))
    p.drawRect(147, 20, 6, 18)
    p.setBrush(QColor(30, 30, 30))
    p.drawEllipse(105, 130, 18, 26)
    p.drawEllipse(175, 130, 18, 26)
    p.setBrush(Qt.white)
    p.drawEllipse(111, 135, 6, 8)
    p.drawEllipse(181, 135, 6, 8)
    p.setBrush(QColor(200, 60, 60))
    p.drawEllipse(135, 185, 30, 22)
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


def main() -> None:
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
