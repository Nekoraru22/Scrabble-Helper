python -m venv myvenv
myvenv\Scripts\activate
pip install -r requirements.txt
cd front
npm install
npm run build
cd ..
python main.py