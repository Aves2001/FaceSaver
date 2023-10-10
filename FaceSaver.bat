@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "VENV_PATH=%2\venv"

set "SCRIPT=%2\main.py"

set "PYTHON_EXECUTABLE=python"
set "ACTIVATE_SCRIPT=%VENV_PATH%\Scripts\activate"

set IS_CREATE_VENV=0

"%PYTHON_EXECUTABLE%" --version >nul 2>&1
if !errorlevel! equ 1 (
    echo Python не знайдено у системі.
    echo Скачайте та встановіть його: https://www.python.org/downloads/release/python-3810/
    pause
    exit
)

if not exist "%VENV_PATH%" (
    :CREATED_VENV
    echo Створення віртуального середовища...
    "%PYTHON_EXECUTABLE%" -m venv "%VENV_PATH%"
    set IS_CREATE_VENV=1
    if !errorlevel! equ 1 (
        echo Виникла помилка при створенні віртуального середовища.
        goto end
    )
    echo Віртуальне середовище створено у %VENV_PATH%.
)


call "%ACTIVATE_SCRIPT%"
if !errorlevel! equ 1 (
    echo Віртуальне середовище пошкоджено. Зачекайте будь ласка...
    goto CREATED_VENV
)

REM Після створення віртуально середовищя, перевіряє оновлення для pip
if %IS_CREATE_VENV%==1 (
    echo Перевірка оновлень для pip...
    "%PYTHON_EXECUTABLE%" -m pip install --upgrade pip
	
	echo Встановлення залежностей...
	"%PYTHON_EXECUTABLE%" -m pip install -r requirements.txt
	 cls
)


"%PYTHON_EXECUTABLE%" "%SCRIPT%" %1 %2
if !errorlevel! equ 1 (
    echo Помилка при виконанні скрипта
)

:end
echo Натисніть будь яку клавішу, або на хрестик, щоб закрити це вікно.
pause > nul