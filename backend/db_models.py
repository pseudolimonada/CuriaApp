from extensions import db
from constants import UserType, OrderStateType, WeekDay


class User(db.Model):
    user_id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True
    )
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class Business(db.Model):
    business_id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True
    )
    business_name = db.Column(db.String(100), nullable=False)


class BusinessUser(db.Model):
    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), nullable=False, primary_key=True
    )
    user_type = db.Column(db.Enum(UserType), nullable=False)


class Catalog(db.Model):
    catalog_id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False,
    )
    catalog_date = db.Column(db.Date, nullable=False)


class Product(db.Model):
    product_id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False,
    )
    image_url = db.Column(db.String(100), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    product_price = db.Column(db.Float, nullable=False)


class CatalogProduct(db.Model):
    catalog_id = db.Column(
        db.Integer,
        db.ForeignKey("catalog.catalog_id"),
        nullable=False,
        primary_key=True,
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.product_id"),
        nullable=False,
        primary_key=True,
    )
    product_quantity_total = db.Column(db.Integer, nullable=False)
    product_quantity_sold = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    order_id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True
    )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey("business.business_id"),
        nullable=False,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    order_state = db.Column(db.Enum(OrderStateType), nullable=False)


class OrderProduct(db.Model):
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.order_id"),
        nullable=False,
        primary_key=True,
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.product_id"),
        nullable=False,
        primary_key=True,
    )
    product_quantity = db.Column(db.Integer, nullable=False)
