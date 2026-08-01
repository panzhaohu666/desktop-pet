"""真正独立的后台启动器"""
import subprocess, os, sys

DIR = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.expanduser("~/.local/lib/desktop_pet")

# 确保库存在
if not os.path.exists(os.path.join(LIB, "libxcb-xinerama.so.0")):
    print("首次运行，安装依赖...")
    subprocess.run(["apt", "download", "libxcb-xinerama0"], cwd="/tmp", capture_output=True)
    subprocess.run(["dpkg", "-x", "/tmp/libxcb-xinerama0" + ".deb", LIB], capture_output=True)
    import glob
    for f in glob.glob(LIB + "/usr/lib/x86_64-linux-gnu/*"):
        os.rename(f, os.path.join(LIB, os.path.basename(f)))

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = LIB + ":" + env.get("LD_LIBRARY_PATH", "")
env["DISPLAY"] = env.get("DISPLAY", ":0")

# 清理缓存
import shutil
cache = os.path.join(DIR, "desktop_pet", "__pycache__")
if os.path.exists(cache):
    shutil.rmtree(cache)

# 启动独立进程
subprocess.Popen(
    [sys.executable, "run.py"],
    cwd=DIR, env=env,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,
)
print("桌宠精灵已在后台启动")
