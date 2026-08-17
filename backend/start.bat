@echo off
cd "C:\Users\ADITYA GIRI\omnirag-platform\backend"
call venv\Scripts\activate
uvicorn main:app --reload
