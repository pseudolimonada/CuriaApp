from flask import Flask, jsonify
from flask_cors import CORS
from config import Config, APP_PORT
from extensions import db
from api.users import users_blueprint
from api.businesses import businesses_blueprint
from api.products import products_blueprint
from api.orders import orders_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(businesses_blueprint, url_prefix="/businesses")
app.register_blueprint(products_blueprint, url_prefix="/businesses")
app.register_blueprint(orders_blueprint, url_prefix="/businesses")


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created")
    app.run(debug=True, host="0.0.0.0", port=APP_PORT)
