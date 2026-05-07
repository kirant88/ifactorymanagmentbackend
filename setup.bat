@echo off
echo Setting up Django Backend for iFactory Management System
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Please update .env file with your database credentials
)

echo.
echo Setup complete! Next steps:
echo 1. Update .env file with your PostgreSQL credentials
echo 2. Create PostgreSQL database: ifactory_db
echo 3. Run: python manage.py migrate
echo 4. Run: python manage.py createsuperuser
echo 5. Run: python manage.py runserver
