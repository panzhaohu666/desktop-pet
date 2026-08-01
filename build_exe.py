import os
import subprocess
import sys


def build() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # 数据文件夹

    print("开始使用 PyInstaller 打包桌面宠物程序...")

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("未检测到 PyInstaller，正在自动安装...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "pyinstaller"]
        )

    separator = ";" if sys.platform == "win32" else ":"
    resources_src = os.path.join(current_dir, "resources")
    resources_arg = f"{resources_src}{separator}resources"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=DesktopPet",
        f"--paths={parent_dir}",
        f"--add-data={resources_arg}",
        "run.py",
    ]

    print(f"执行命令: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=current_dir)

    dist = os.path.join(current_dir, "dist")
    print(f"\n打包完成！可执行文件: {os.path.join(dist, 'DesktopPet')}")
    print("你可以直接双击该文件运行桌面宠物！")


if __name__ == "__main__":
    build()
