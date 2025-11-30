@echo off
@REM call venv\Scripts\activate.bat
cd "./FrontEnd/" && npm run dev
timeout /t 3 /nobreak > nul
start "API Server" python "./BackEnd/API/api.py"