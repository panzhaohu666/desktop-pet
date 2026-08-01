import os
import sys

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon, QPen
from PyQt5.QtCore import Qt

from desktop_pet.pet_window import PetWindow


def _get_resource_dir() -> str:
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "resources")


def _make_tray_icon() -> QIcon:
    """生成一个 32x32 的托盘图标。"""
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
    print(f"已自动生成默认宠物图片: {pet_img_path}")
    print("提示：你可以随时将你喜欢的透明 PNG 图片替换到此路径！")
    return pet_img_path


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口不退出，驻留托盘

    major = Qt.__version_info__[1] if hasattr(Qt, '__version_info__') else 15
    if major < 14:
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    image_path = ensure_pet_image()
    pet = PetWindow(image_path)

    # ---- 系统托盘 ----
    tray = QSystemTrayIcon(_make_tray_icon(), app)
    tray.setToolTip("桌面宠物 — 点击显示/隐藏")

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
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
