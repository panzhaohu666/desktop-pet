import os
import shutil
import subprocess
import sys
import zipfile


def build() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    is_win = sys.platform == "win32"
    separator = ";" if is_win else ":"

    pkg_dir = os.path.join(current_dir, "desktop_pet")
    resources_src = os.path.join(pkg_dir, "resources")
    resources_arg = f"{resources_src}{separator}resources"

    skins_src = os.path.join(pkg_dir, "skins")
    skins_arg = ""
    if os.path.isdir(skins_src):
        skins_arg = f"{skins_src}{separator}skins"

    binary_name = "DesktopPet"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onedir",
        f"--name={binary_name}",
        f"--paths={current_dir}",
        f"--add-data={resources_arg}",
        "run.py",
    ]
    if skins_arg:
        cmd.insert(-1, f"--add-data={skins_arg}")

    print("Building with --onedir ...")
    subprocess.check_call(cmd, cwd=current_dir)

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


if __name__ == "__main__":
    build()
