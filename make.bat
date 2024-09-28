@echo off
setlocal

:: Define service paths
set MAIN_WEB_PATH=main-web
set REC_MODEL_PATH=reccommendation-ai

:: Check the first argument to determine which section to run
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="rebuild" goto rebuild
if "%1"=="status" goto status
if "%1"=="test-all" goto test-all
if "%1"=="logs" goto logs
if "%1"=="down-v" goto down-v
if "%1"=="down" goto down

echo Invalid argument. Here is the Usage:
echo   %0 start
echo   %0 stop
echo   %0 rebuild
echo   %0 status
echo   %0 test-main
echo   %0 test-ai-rec-model
echo   %0 test-all
echo   %0 logs
echo   %0 down
echo   %0 down-v
goto end

:: Start Docker services with delay
:start
cd %MAIN_WEB_PATH%
docker compose up -d --build
:: Wait for 30 seconds before starting the users service
timeout /t 5 /nobreak
cd ..\%REC_MODEL_PATH%
docker compose up -d --build
goto end

:: Stop Docker services
:stop
cd %MAIN_WEB_PATH%
docker compose down
cd ..\%REC_MODEL_PATH%
docker compose down
goto end

:: Rebuild Docker services
:rebuild
cd %MAIN_WEB_PATH%
docker compose up --build
cd ..\%REC_MODEL_PATH%
docker compose up --build
goto end

:: Check status of Docker services
:status
cd %MAIN_WEB_PATH%
docker compose ps
cd ..\%REC_MODEL_PATH%
docker compose ps
goto end

:logs
cd %MAIN_WEB_PATH%
docker compose logs
cd ..\%REC_MODEL_PATH%
docker compose logs
goto end

:down
cd %MAIN_WEB_PATH%
docker compose down
cd ..\%REC_MODEL_PATH%
docker compose down
goto end

:down-v
cd %MAIN_WEB_PATH%
docker compose down -v
cd ..\%REC_MODEL_PATH%
docker compose down -v
goto end

:: Run tests for the main service
:test-main
cd %MAIN_WEB_PATH%
docker compose exec api python manage.py test tests
cd ..
goto end


:: Run tests for both services
:test-all
call :test-main
@REM call :test-ai-rec-model
goto end

:end
endlocal
