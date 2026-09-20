@echo off
chcp 65001 >nul
echo =========================================================================
echo    KHỞI ĐỘNG HỆ THỐNG WEB TEST MÔ HÌNH HỌC MÁY PHÂN LOẠI ẢNH CHÁY RỪNG
echo =========================================================================
echo.
echo Đang kiểm tra môi trường Python và thư viện...
cd /d "%~dp0"

echo Khởi chạy FastAPI Server tại: http://localhost:8000
echo Mở trình duyệt và truy cập: http://localhost:8000
echo Bấm Ctrl + C để dừng server khi hoàn thành.
echo.

python -m uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload

pause
