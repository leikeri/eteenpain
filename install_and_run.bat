python -m pip install -r requirements.txt
from app import db
db.create_all()
python -m flask run