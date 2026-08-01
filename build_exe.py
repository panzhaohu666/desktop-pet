import os
import shutil
import subprocess
import sys


def build() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    print(f"目标平台: {sys.platform}")
    print("开始使用 PyInstaller 打包...")

    # install pyinstaller if missing
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        pip_cmd = [sys.executable, "-m", "pip", "install", "pyinstaller"]
        if sys.platform == "linux":
            pip_cmd.append("--break-system-packages")
        subprocess.check_call(pip_cmd)

    # platform-specific settings
    is_win = sys.platform == "win32"
    separator = ";" if is_win else ":"

    resources_src = os.path.join(current_dir, "resources")
    resources_arg = f"{resources_src}{separator}resources"

    # binary name: DesktopPet.exe (win) / DesktopPet (linux/mac)
    binary_name = "DesktopPet.exe" if is_win else "DesktopPet"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name={binary_name.replace('.exe', '')}",
        f"--paths={parent_dir}",
        f"--add-data={resources_arg}",
        "run.py",
    ]

    print(f"PyInstaller 命令: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=current_dir)

    # rename for platform suffix in CI
    dist_dir = os.path.join(current_dir, "dist")
    src = os.path.join(dist_dir, binary_name)
    if is_win:
        artifact = os.path.join(dist_dir, "DesktopPet-windows.exe")
    elif sys.platform == "darwin":
        artifact = os.path.join(dist_dir, "DesktopPet-macos")
    else:
        artifact = os.path.join(dist_dir, "DesktopPet-linux")

    if os.path.exists(src):
        shutil.move(src, artifact)
        print(f"\n打包完成: {artifact}")
        print(f"文件大小: {os.path.getsize(artifact) / 1024 / 1024:.1f} MB")
    else:
        print(f"\n错误: 未找到生成的文件 {src}")
        sys.exit(1)


if __name__ == "__main__":
    build()
