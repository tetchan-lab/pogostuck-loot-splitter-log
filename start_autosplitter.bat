@echo off
chcp 65001 > nul
echo Pogostuck Auto-Splitter 起動中...
python "%~dp0autosplitter.py"
pause
