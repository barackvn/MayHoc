@echo off
title Khoi Dong Toan Bo He Thong May Hoc Chay Rung
echo =========================================================================
echo    KHOI DONG TOAN BO HE THONG: BACKEND (PORT 8000) + FRONTEND (PORT 3000)
echo =========================================================================
echo.
cd /d "%~dp0"

echo [1/2] Dang khoi dong Backend FastAPI...
start "MayHoc Backend (FastAPI)" cmd /c "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Dang khoi dong Frontend React Vite...
start "MayHoc Frontend (React Vite)" cmd /c "cd /d "%~dp0frontend" && npm run dev"

echo.
echo =========================================================================
echo    HE THONG DA KHOI CHAY THANH CONG!
echo    - Backend API: http://127.0.0.1:8000
echo    - Frontend Web: http://localhost:3000
echo =========================================================================
echo.
pause
