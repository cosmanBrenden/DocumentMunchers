@echo off
@REM call venv\Scripts\activate.bat
cd "./FrontEnd/" && npm run dev
timeout /t 3 /nobreak > nul
cd "./FrontEnd/" && npm run dev