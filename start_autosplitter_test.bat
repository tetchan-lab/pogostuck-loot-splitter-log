@echo off
chcp 65001 > nul
echo [テストモード] LiveSplitへの送信は行いません
python "%~dp0autosplitter.py" --test
pause
