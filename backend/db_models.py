from extensions import db
from constants import UserType, OrderStateType


class User(db.Model):
    user_id = db.Column(db.String(100), nullable=False, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Business(db.Model):
    business_id = db.Column(db.String(100), nullable=False, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)


class BusinessUser(db.Model):
    business_id = db.Column(
        db.String(100),
        db.ForeignKey("business.business_id"),
        nullable=False,
        primary_key=True,
    )
    user_id = db.Column(
        db.String(100), db.ForeignKey("user.user_id"), nullable=False, primary_key=True
    )
    user_type = db.Column(db.Enum(UserType), nullable=False)
