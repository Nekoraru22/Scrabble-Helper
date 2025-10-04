@REM Build next js project
cd scrabble-helper
call npm run build

@REM Copy build output and public folder to the frontend folder
cd ..
mkdir frontend
mkdir frontend\.next\static
mkdir frontend\.next\server
mkdir frontend\public
xcopy /E /I /Y scrabble-helper\.next\static frontend\.next\static
xcopy /E /I /Y scrabble-helper\.next\server frontend\.next\server
xcopy /E /I /Y scrabble-helper\public frontend\public

@REM Remove old compiled file if exists
if exist scrabble-helper.exe del /Q scrabble-helper.exe

@REM Build the compiled project
pyinstaller --onefile --add-data "frontend;frontend" --add-data "data_api.json:." --icon=frontend/public/icon.ico main.py

@REM Move dist file to root directory
move /Y dist\main.exe scrabble-helper.exe
timeout /T 1 /NOBREAK >nul
rd /S /Q dist
rd /S /Q build
del /Q main.spec

@echo Build complete: scrabble-helper.exe
