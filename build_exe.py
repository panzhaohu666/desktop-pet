import os
import shutil
import subprocess
import sys


def build() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    print(f"Platform: {sys.platform}")
    print("Building with PyInstaller...")

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    is_win = sys.platform == "win32"
    separator = ";" if is_win else ":"

    resources_src = os.path.join(current_dir, "resources")
    resources_arg = f"{resources_src}{separator}resources"

    skins_src = os.path.join(current_dir, "skins")
    skins_arg = f"{skins_src}{separator}skins" if os.path.isdir(skins_src) else ""

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
    if skins_arg:
        cmd.insert(-1, f"--add-data={skins_arg}")

    print(f"Running PyInstaller...")
    subprocess.check_call(cmd, cwd=current_dir)

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
        size_mb = os.path.getsize(artifact) / 1024 / 1024
        print(f"Done: {artifact} ({size_mb:.1f} MB)")
    else:
        print(f"ERROR: file not found: {src}")
        sys.exit(1)


if __name__ == "__main__":
    build()
