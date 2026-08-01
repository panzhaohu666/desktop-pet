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
| `run.py` | 启动脚本（仓库根目录） |
| `build_exe.py` | PyInstaller 打包脚本 |
| `desktop_pet/main.py` | 程序入口、系统托盘、日志 |
| `desktop_pet/pet_window.py` | 核心窗口 — 拖拽、动画、屏幕物理、菜单 |
| `desktop_pet/bubble_widget.py` | 对话气泡悬浮组件 |
| `desktop_pet/phrases.py` | 中文短语库 |
| `desktop_pet/config_manager.py` | QSettings 配置持久化 |
| `desktop_pet/settings_dialog.py` | 图形化设置面板 |
| `desktop_pet/sound.py` | 音效模块 |

## 代码规范

- 兼容 Python 3.8+
- 公开方法需添加类型标注（`-> None`、`-> str` 等）
- 遵循已有代码风格
- 禁止使用 `as any` / `@ts-ignore` / 裸 `except:`

## 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/功能名`
3. 修改代码
4. 本地测试：`python run.py`（确保正常启动无报错）
5. 提交时使用约定式提交格式：
   - `feat:` — 新功能
   - `fix:` — 修复 bug
   - `docs:` — 文档修改
   - `refactor:` — 代码重构
   - `ci:` — CI / 构建相关
6. Push 并创建 Pull Request

## 添加短语

编辑 `phrases.py`，加入合适的分类或新建分类。短语不宜过长（30 字以内），内容健康向上。

## 添加动画

在 `pet_window.py` 中新增 `anim_xxx` 方法，参考现有动画模式：

```python
def anim_xxx(self) -> None:
    self._is_animating = True
    # ... 动画逻辑 ...
    # 完成后调用 self._anim_done()
```

然后在 `trigger_random_interaction()` 或 `_trigger_special_interaction()` 中注册。

## 反馈问题

请使用对应模板提交：

- [🐛 Bug 报告](https://github.com/panzhaohu666/desktop-pet/issues/new?template=bug.yml)
- [✨ 功能建议](https://github.com/panzhaohu666/desktop-pet/issues/new?template=feature.yml)
