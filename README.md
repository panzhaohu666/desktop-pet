# 🐾 桌宠精灵 — Desktop Pet

轻量级桌面宠物程序，支持 Windows、Linux、macOS。透明无边框、始终置顶。基于 Python + PyQt5。

<p align="center">
  <img src="desktop_pet/resources/pet.png" width="200" alt="桌宠精灵">
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
| 🪟 **Windows** | [下载 ZIP](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-windows.zip) — 解压后双击 |
| 🐧 **Linux** | [下载 ZIP](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-linux.zip) — 解压后运行 |
| 🍎 **macOS** | [下载 ZIP](https://github.com/panzhaohu666/desktop-pet/releases/latest/download/DesktopPet-macos.zip) — 解压后运行 |

> [查看所有版本 →](https://github.com/panzhaohu666/desktop-pet/releases)

---

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| **10 套皮肤** | 🦆小黄鸭(默认) 🐶柯基 🐱猫咪 🟡噜噜 🐼熊猫 🦊狐狸 🐰兔子 🐸青蛙 🐧企鹅 🐉小龙 |
| **序列帧动画** | 每皮肤 2~4 种专属动作（跳跃/扭动/旋转/冲刺/压扁），精灵图逐帧播放 |
| **独立语音包** | 120 条专属短语，每皮肤 12 条，角色人设各不相同 |
| **透明无边框** | 完美融入桌面，去除背景、无边框、始终置顶 |
| **拖拽移动** | 鼠标左键按住即可拖动，屏幕边界限制 + 边缘磁吸 |
| **双击彩蛋** | 单击/双击分别触发不同动画 |
| **呼吸动画** | 闲置时正弦微动，仿佛在呼吸 |
| **自动游走** | 每 25~50 秒自动随机漫步 |
| **滚轮缩放** | 50%~250% 自由调节 |
| **对话气泡** | 自适应高度，白/粉两色，永不截断 |
| **系统托盘** | 最小化到托盘，点击显示/隐藏 |
| **图形化设置** | 外观/行为/音效 面板集中管理 |
| **跨平台** | Windows / Linux / macOS 功能一致 |

---

## 🎮 操作指南

| 操作 | 方式 |
|------|------|
| 移动宠物 | 左键按住拖拽 |
| 随机互动 | 单击左键 |
| 特殊互动 | 双击左键 |
| 右键菜单 | 右键（切换皮肤/设置/游走/聊天/退出） |
| 调整大小 | 鼠标滚轮 |

---

## 🚀 源码运行

```bash
git clone https://github.com/panzhaohu666/desktop-pet.git
cd desktop-pet
pip install -r requirements.txt
python run.py
# 或: python launch.py  # 独立后台进程
# 或: ./start_pet.sh    # Linux 一键启动
```

---

## 👗 皮肤系统

皮肤在 `desktop_pet/skins/` 下，每套包含：

```
skins/柯基犬/
├── pet.png           # 默认站姿
├── phrases.json      # 专属语音包（12条）
└── click/
    ├── jump/         # 跳跃序列帧
    ├── wiggle/       # 扭动序列帧
    └── ...           # 更多动作
```

**自定义皮肤**：新建文件夹 → 放入 `pet.png` + 序列帧子目录 + `phrases.json` → 右键切换即可。

---

## 📁 项目结构

```
desktop-pet/
├── run.py / launch.py / start_pet.sh  # 启动方式
├── build_exe.py / build.bat           # 打包脚本
├── requirements.txt / LICENSE
└── desktop_pet/         # Python 包
    ├── main.py          # 入口 + 托盘 + 日志
    ├── pet_window.py    # 核心（拖拽/动画/物理/菜单）
    ├── bubble_widget.py # 自适应对话气泡
    ├── phrases.py       # 短语加载引擎
    ├── config_manager.py
    ├── settings_dialog.py
    ├── sound.py
    ├── resources/
    └── skins/           # 10 套角色皮肤
```

---

## 📄 开源协议

MIT © [panzhaohu666](https://github.com/panzhaohu666)

---

## 🤝 社区

- [📋 更新日志](CHANGELOG.md)
- [🤝 贡献指南](CONTRIBUTING.md)
- [🐛 提交 Bug](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml)
- [✨ 功能建议](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml)
