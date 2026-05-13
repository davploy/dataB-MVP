@echo off
setlocal
cd /d "%~dp0"

echo Starting datab-mvp-backend (Flask on port 5000^)...
cd /d "%~dp0datab-mvp-backend"
start "datab-mvp-backend" cmd /k pipenv run python inputs.py

echo Starting datab-mvp-frontend (Vite dev server^)...
cd /d "%~dp0datab-mvp-frontend"
start "datab-mvp-frontend" cmd /k npm run dev

cd /d "%~dp0"
echo Launched backend and frontend in separate windows.
endlocal
