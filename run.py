"""
桌宠启动辅助脚本 - 方便直接运行。
使用方式:
    python run.py          # 直接从 desktop_pet/ 目录运行
    python -m desktop_pet  # 从父目录以模块方式运行
"""
import sys
import os

# 将父目录（数据文件夹）加入 sys.path，使得 from desktop_pet.main import main 可以正常工作
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from desktop_pet.main import main

if __name__ == "__main__":
    main()
