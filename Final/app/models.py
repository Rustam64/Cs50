from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupang_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(40), nullable=False, unique=True)
    brand = db.Column(db.String(20))
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    alternative_price = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(10), nullable=False, default="waiting")
    description = db.Column(db.String(50))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class MonthlySales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    total_spent = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_sales = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)