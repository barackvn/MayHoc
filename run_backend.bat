@echo off
title MayHoc Backend (FastAPI)
echo ========================================================
echo   KHOI DONG BACKEND FASTAPI - MAY HOC CHAY RUNG (PORT 8000)
echo ========================================================
cd /d "%~dp0"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
