@echo off
cd /d "%~dp0"
echo [SenseNova U1] 正在启动本地服务器...
echo.
echo 浏览器将自动打开 http://localhost:8080
echo 在浏览器中选择保存目录后，下次关闭再打开
echo 目录权限会自动恢复，无需重新选择！
echo.
echo 按 Ctrl+C 关闭服务器
echo.

start http://localhost:8080
"E:\Conda\envs_dirs\Agent\python.exe" -m http.server 8080
pause
