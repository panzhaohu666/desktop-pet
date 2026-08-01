import os
import shutil
import subprocess
import sys
import zipfile


def build() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    is_win = sys.platform == "win32"
    separator = ";" if is_win else ":"

    resources_src = os.path.join(current_dir, "resources")
    resources_arg = f"{resources_src}{separator}resources"

    skins_src = os.path.join(current_dir, "skins")
    skins_arg = ""
    if os.path.isdir(skins_src):
        skins_arg = f"{skins_src}{separator}skins"

    binary_name = "DesktopPet"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onedir",
        f"--name={binary_name}",
        f"--paths={parent_dir}",
        f"--add-data={resources_arg}",
        "run.py",
    ]
    if skins_arg:
        cmd.insert(-1, f"--add-data={skins_arg}")

    print(f"Building with --onedir (anti-false-positive)...")
    subprocess.check_call(cmd, cwd=current_dir)

    # Zip the directory
    dist_dir = os.path.join(current_dir, "dist")
    src_dir = os.path.join(dist_dir, binary_name)

    if is_win:
        zip_name = "DesktopPet-windows.zip"
    elif sys.platform == "darwin":
        zip_name = "DesktopPet-macos.zip"
    else:
        zip_name = "DesktopPet-linux.zip"

    zip_path = os.path.join(dist_dir, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                file_path = os.path.join(root, f)
                arcname = os.path.relpath(file_path, src_dir)
                zf.write(file_path, arcname)

    size_mb = os.path.getsize(zip_path) / 1024 / 1024
    print(f"Done: {zip_path} ({size_mb:.1f} MB)")
    print("Windows 用户解压后运行 DesktopPet.exe 即可，不会再被误报病毒")


if __name__ == "__main__":
    build()
