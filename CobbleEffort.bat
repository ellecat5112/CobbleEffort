@echo off
setlocal
rem Drag a .bbmodel or .geo.json onto this file to turn it into a Cobblemon Pokemon.
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
if "%~1"=="" (
  echo.
  echo  CobbleEffort - drag a .bbmodel or .geo.json file onto CobbleEffort.bat
  echo  ^(or run: %PY% -m cobbleeffort --help^)
  echo.
  pause
  exit /b 1
)
%PY% -m cobbleeffort quick "%~1"
echo.
pause
