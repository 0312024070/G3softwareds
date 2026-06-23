@echo off
REM VS Code Terminal or Command Prompt from this folder
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python init_db.py
python app.py
