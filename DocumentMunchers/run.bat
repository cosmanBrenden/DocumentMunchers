@echo off
@REM call venv\Scripts\activate.bat
start "API Server" python "./BackEnd/API/api.py"
timeout /t 3 /nobreak > nul
cd "./FrontEnd/" && npm run dev
