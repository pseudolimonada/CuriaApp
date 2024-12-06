from flask import Flask
from extensions import db
from config import Config
from db_models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("All tables dropped")

    # Create all tables
    db.create_all()
    print("All tables created")
