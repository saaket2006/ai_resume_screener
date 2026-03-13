@echo off
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python generate_mock_data.py
echo Setup complete
