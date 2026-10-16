@echo off
title Velocity Japanese - Video Generator
cd /d "%~dp0"

echo ============================================
echo   Velocity Japanese - Video Generator
echo ============================================
echo.

echo [1] Long-form video
echo [2] Reels (short)
echo.
set /p MODE="Choose (1 or 2): "
echo.

if "%MODE%"=="2" (
    py facebook_reels_automation.py
    goto :end
)

set /p PHRASES="Number of phrases (default 60): "
if "%PHRASES%"=="" set PHRASES=60

set /p CATEGORY="Category (blank = random): "
echo.
if not "%CATEGORY%"=="" (
    py youtube_longform_automation.py --phrases %PHRASES% --category "%CATEGORY%"
) else (
    py youtube_longform_automation.py --phrases %PHRASES%
)

:end
echo.
echo Done!
pause
