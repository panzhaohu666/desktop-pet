#!/bin/bash
# 桌宠精灵启动脚本 — 自动处理依赖，保证每次都能启动
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$HOME/.local/lib/desktop_pet"

# 1. 确保 xcb 库永久存在（不依赖 /tmp）
if [ ! -f "$LIB_DIR/libxcb-xinerama.so.0" ]; then
    echo "[桌宠] 首次启动，安装依赖库..."
    mkdir -p "$LIB_DIR"
    cd /tmp
    apt download libxcb-xinerama0 2>/dev/null
    dpkg -x libxcb-xinerama0*.deb "$LIB_DIR/" 2>/dev/null
    cp "$LIB_DIR/usr/lib/x86_64-linux-gnu/"* "$LIB_DIR/" 2>/dev/null
    rm -f libxcb-xinerama0*.deb
    cd "$DIR"
fi

# 2. 清理旧缓存
rm -rf "$DIR/desktop_pet/__pycache__"

# 3. 启动
echo "[桌宠] 启动中..."
export LD_LIBRARY_PATH="$LIB_DIR:$LD_LIBRARY_PATH"
export DISPLAY="${DISPLAY:-:0}"

cd "$DIR"
python3 run.py

echo "[桌宠] 已退出"
