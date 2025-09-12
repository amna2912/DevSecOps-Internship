@echo off
title Logging Pipeline Starter
echo ========================================
echo    STARTING LOGGING PIPELINE
echo ========================================
echo.

:: Check prerequisites
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not installed or not running
    pause
    exit /b 1
)
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed or not in PATH
    pause
    exit /b 1
)

:: Sync system clock
echo Syncing system clock...
w32tm /resync

:: Clean up old state
echo Cleaning up old logs and DBs...
del /q app.log system.log flask_logs.db system_logs.db 2>nul

:: Start Docker (Loki + Grafana)
echo [1/4] Starting Loki and Grafana...
docker-compose up -d

:: Check Loki readiness
echo Checking Loki readiness...
curl http://localhost:3100/ready
if errorlevel 1 (
    echo ERROR: Loki not ready
    pause
    exit /b 1
)

:: Start Fluent Bit
echo [2/4] Starting Fluent Bit...
start "Fluent Bit" cmd /k "run_fluentbit.bat"

:: Start Flask
echo [3/4] Starting Flask application...
start "Flask App" cmd /k "python app.py"

:: Start traffic and system logs
echo [4/4] Starting traffic generator and system logs...
start "Traffic Generator" cmd /k "python generate_traffic.py"
start "System Logs" cmd /k "run_system_logs.bat"

echo.
echo Pipeline started! Check Grafana at http://localhost:3000
echo Run 'python check_logs.py' to verify logs
echo To stop: Ctrl+C in each window, then 'docker-compose down'
pause