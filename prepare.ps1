Remove-Item -Recurse -Force venv

python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt