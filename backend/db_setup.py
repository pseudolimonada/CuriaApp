from flask import Flask
from config import Config
from extensions import db  # Import the db instance
from db_models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)  # Initialize the db instance with the app


def init_db():
    with app.app_context():
        db.create_all()
        print("Tables created")


if __name__ == "__main__":
    init_db()
