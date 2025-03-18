@echo off

title Gemini chatbot

cd "C:\!My\PythonCodes\Botes\"
REM cd /d "%~dp0"

call venv\Scripts\activate
python bot.py

deactivate
@pause