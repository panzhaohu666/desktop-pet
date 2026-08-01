@echo off
chcp 65001 >nul
echo =========================================
echo   桌面宠物 (Desktop Pet) 一键打包
echo =========================================
echo.
echo [1/2] 正在安装依赖...
pip install pyinstaller PyQt5 pillow
if %errorlevel% neq 0 (
    echo 依赖安装失败！请检查网络连接和 Python 环境。
    pause
    exit /b 1
)
echo.
echo [2/2] 正在打包为单文件 EXE...
python build_exe.py
echo.
echo =========================================
echo   打包完成！
echo   生成的文件: dist\DesktopPet.exe
echo =========================================
pause
