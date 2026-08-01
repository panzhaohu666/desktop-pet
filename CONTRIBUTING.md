# 贡献指南

感谢你对桌宠精灵的关注！🐾

## 快速开始

```bash
git clone https://github.com/panzhaohu666/desktop-pet.git
cd desktop-pet
pip install -r requirements.txt
python run.py
```

## 项目结构

| 文件 | 用途 |
|------|------|
| `run.py` / `launch.py` / `start_pet.sh` | 启动脚本 |
| `build_exe.py` | PyInstaller 打包 |
| `desktop_pet/main.py` | 入口、系统托盘、日志 |
| `desktop_pet/pet_window.py` | 核心窗口 — 拖拽、动画、皮肤、菜单 |
| `desktop_pet/bubble_widget.py` | 自适应对话气泡 |
| `desktop_pet/phrases.py` | 皮肤短语加载引擎 |
| `desktop_pet/config_manager.py` | QSettings 持久化 |
| `desktop_pet/settings_dialog.py` | 图形化设置面板 |
| `desktop_pet/sound.py` | 音效模块 |

## 代码规范

- 兼容 Python 3.8+
- 公开方法需添加类型标注
- 遵循已有代码风格
- 禁止 `as any` / `@ts-ignore` / 裸 `except:`

## 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/功能名`
3. 修改代码，本地测试 `python run.py`
4. 提交：`feat:` 新功能 / `fix:` 修复 / `docs:` 文档 / `ci:` 构建
5. Push 并创建 PR

## 添加新皮肤

在 `desktop_pet/skins/` 下创建文件夹，放入：

```
skins/新皮肤/
├── pet.png           # 默认站姿（透明PNG）
├── phrases.json      # 专属语音包 ["短语1", "短语2", ...]
└── click/
    ├── jump/         # 跳跃序列帧 (01.png, 02.png...)
    └── wiggle/       # 扭动序列帧
```

支持的动画类型：`jump` `wiggle` `spin` `dash` `squash`

## 反馈

- [🐛 Bug 报告](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml)
- [✨ 功能建议](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml)
