@echo off
e:
cd "e:\iFactory Managment System\Code\backend"
echo Running makemigrations...
venv\Scripts\python.exe manage.py makemigrations training engagement accounts
echo Running migrate...
venv\Scripts\python.exe manage.py migrate
echo Done!
