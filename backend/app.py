from flask import Flask, jsonify
from flask_cors import CORS
from config import Config, APP_PORT, APP_HOST, REDEPLOY, APP_ADMIN_PASSWORD
from extensions import db
from api.users import users_blueprint
from api.businesses import businesses_blueprint
from api.products import products_blueprint
from api.orders import orders_blueprint
from api.catalog import catalog_blueprint
from db_models import *
from constants import UserType, LOGGER, hash_password
from db_redeploy import db_redeploy
import json
import os

STATIC_FOLDER_PATH = "../assets/images/"
app = Flask(__name__, static_folder=STATIC_FOLDER_PATH)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(businesses_blueprint, url_prefix="/businesses")
app.register_blueprint(products_blueprint, url_prefix="/businesses")
app.register_blueprint(orders_blueprint, url_prefix="/businesses")
app.register_blueprint(catalog_blueprint, url_prefix="/businesses")


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == "__main__":
    with app.app_context():
        if REDEPLOY:
            db_redeploy(app)
            LOGGER.warning("Database redeployed")

            db.session.add(
                User(user_name="admin", password=hash_password(APP_ADMIN_PASSWORD))
            )
            db.session.flush()

            db.session.add(Business(business_name="Farinha e Afeto"))
            db.session.flush()
            db.session.add(
                BusinessUser(user_id=1, business_id=1, user_type=UserType.MANAGER)
            )
            LOGGER.warning("Admin user created for business_id=1")

            db.session.commit()
            # load json from a file
            with open("../assets/product_data.json") as f:
                data = json.load(f)
                for i, product in enumerate(data, 1):
                    db.session.add(
                        Product(
                            **product,
                            business_id=1,
                            image_url=f"{app.static_url_path}/{i}.png",
                        )
                    )
                db.session.commit()
            LOGGER.warning("Products created for business_id=1")

    app.run(debug=True, host=APP_HOST, port=APP_PORT)
