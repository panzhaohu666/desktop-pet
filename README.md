# 🐾 桌宠精灵 — Desktop Pet

轻量级桌面宠物程序，支持 Windows、Linux、macOS。透明无边框、始终置顶。基于 Python + PyQt5 构建。

<p align="center">
  <img src="resources/pet.png" width="200" alt="桌宠精灵">
</p>

<p align="center">
  <a href="https://github.com/panzhaohu666/desktop-pet/releases"><img src="https://img.shields.io/github/v/release/panzhaohu666/desktop-pet?style=flat-square" alt="版本"></a>
  <a href="https://github.com/panzhaohu666/desktop-pet/blob/main/LICENSE"><img src="https://img.shields.io/github/license/panzhaohu666/desktop-pet?style=flat-square" alt="许可"></a>
  <a href="https://github.com/panzhaohu666/desktop-pet/actions"><img src="https://img.shields.io/github/actions/workflow/status/panzhaohu666/desktop-pet/release.yml?style=flat-square" alt="构建状态"></a>
</p>

---

## 📥 下载安装

| 平台 | 文件 |
|------|------|
| 🪟 **Windows** | [下载 EXE](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-windows.exe) — 双击运行 |
| 🐧 **Linux** | [下载 Linux 版](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-linux) — `chmod +x` 后运行 |
| 🍎 **macOS** | [下载 macOS 版](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-macos) — 右键打开 |

> [查看所有版本 →](https://github.com/panzhaohu666/desktop-pet/releases)

---

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| **透明无边框** | 完美融入桌面，去除背景、无边框、始终置顶 |
| **拖拽移动** | 鼠标左键按住即可拖动，带屏幕边界限制与边缘磁吸 |
| **9 种互动动画** | 跳跃、压扁回弹、左右抖动、摇晃倾斜、扭动、弹跳、后空翻、喷嚏、快速旋转 |
| **双击彩蛋** | 单击随机触发 6 种动画，双击触发 3 种隐藏特殊动画 |
| **呼吸动画** | 闲置时持续正弦微动，仿佛在呼吸 |
| **自动游走** | 每 25~50 秒自动随机漫步，宠物有「自主意识」 |
| **滚轮缩放** | 鼠标滚轮调节 50%~250% 大小 |
| **中文对话气泡** | 60 多条中文短语，4 类上下文匹配，激动内容变粉色气泡 |
| **系统托盘** | 最小化到托盘驻留，点击显示/隐藏，右键退出 |
| **配置记忆** | 自动记住位置、大小、置顶状态 |
| **跨平台** | Windows / Linux / macOS 功能完全一致 |

---

## 🎮 操作指南

| 操作 | 方式 |
|------|------|
| 移动宠物 | 鼠标左键按住拖拽 |
| 随机互动（6 种） | 单击左键 |
| 特殊互动（3 种） | 双击左键 |
| 右键菜单 | 右键点击（含皮肤切换、设置面板） |
| 调整大小 | 鼠标滚轮 |
| **设置面板** | 右键 → 设置... → 外观 / 行为 / 音效 |
| **音效** | 单击 / 双击 / 游走时播放简短音效 |

---

## 🚀 源码运行

### 环境要求

- Python 3.8+
- PyQt5 >= 5.15
- Pillow >= 8.0

### 运行步骤

```bash
git clone https://github.com/panzhaohu666/desktop-pet.git
cd desktop-pet
pip install -r requirements.txt
python run.py
```

### 自定义角色与皮肤

- **单角色**：将透明 PNG 重命名为 `pet.png` 替换 `resources/pet.png`
- **多皮肤**：在 `skins/` 目录下创建子文件夹（如 `skins/猫猫/pet.png`），右键菜单即可一键切换

### 图形化设置

右键 → **设置...** 打开设置面板，可调整：外观（大小、皮肤）、行为（游走/聊天间隔）、音效开关。

---

## 📦 手动打包

双击 `build.bat`（Windows）或运行：

```bash
python build_exe.py
```

---

## 📁 项目结构

```
desktop_pet/
├── main.py              # 程序入口 + 系统托盘 + 资源管理
├── pet_window.py        # 核心：拖拽、9 种动画、屏幕物理、右键菜单
├── bubble_widget.py     # 对话气泡组件（白色 / 粉色）
├── phrases.py           # 60 条中文短语库（4 个分类）
├── config_manager.py    # QSettings 配置持久化
├── run.py               # 便捷启动脚本
├── build_exe.py         # PyInstaller 打包脚本
├── build.bat            # Windows 一键打包批处理
├── requirements.txt     # 依赖列表
├── LICENSE              # MIT 开源协议
└── resources/
    └── pet.png          # 角色图片（可替换）
```

---

## 🎨 自定义配置

| 项目 | 方法 |
|------|------|
| **角色** | 替换 `resources/pet.png` |
| **短语** | 编辑 `phrases.py` |
| **动画速度** | 调整 `pet_window.py` 中的 `duration` / `interval_ms` |
| **游走频率** | 调整 `wander_timer` 间隔 |
| **边缘吸附距离** | 修改 `EDGE_SNAP_DISTANCE` 常量 |

---

## 📄 开源协议

MIT © [panzhaohu666](https://github.com/panzhaohu666)

---

## 🤝 社区

- [📋 更新日志](CHANGELOG.md)
- [🤝 贡献指南](CONTRIBUTING.md)
- [🐛 提交 Bug](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml)
- [✨ 功能建议](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml)
