@echo off
:loop
python system_logs.py
timeout /t 60 /nobreak
goto loop