@echo off
echo ========================================
echo Starting Resume Parser Backend
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing/Updating dependencies...
pip install -q -r requirements.txt

echo.
echo Testing job scraping...
python test_scraping.py

echo.
echo ========================================
echo VBA Excel Features Available:
echo - Excel Report Generation
echo - Bulk Resume Processing
echo ========================================
echo.

echo Starting Flask server on port 5000...
echo.

python app.py

pause
