#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$HOME/.local/lib/desktop_pet"

if [ ! -f "$LIB_DIR/libxcb-xinerama.so.0" ]; then
    mkdir -p "$LIB_DIR"
    cd /tmp
    apt download libxcb-xinerama0 2>/dev/null
    dpkg -x libxcb-xinerama0*.deb "$LIB_DIR/" 2>/dev/null
    cp "$LIB_DIR/usr/lib/x86_64-linux-gnu/"* "$LIB_DIR/" 2>/dev/null
    rm -f libxcb-xinerama0*.deb
fi

cd "$DIR"
rm -rf desktop_pet/__pycache__

export LD_LIBRARY_PATH="$LIB_DIR:$LD_LIBRARY_PATH"
export DISPLAY="${DISPLAY:-:0}"

python3 run.py &
disown
echo "桌宠精灵已启动"
