from models import db, Products, Users, MonthlySales
from flask import current_app
from werkzeug.security import generate_password_hash
from datetime import datetime
from decimal import Decimal

now = datetime.now()
current_year = now.year
current_month = now.month

def insert_monthly_sales(year, month, total_spent, total_sales=0):
    """Insert monthly sales data into the database"""
    with current_app.app_context():
        if MonthlySales.query.filter_by(year=year, month=month).first():
            sales = MonthlySales.query.filter_by(year=year, month=month).first()
            sales.total_spent += Decimal(total_spent)
            sales.total_sales += Decimal(total_sales)
        else:
            sales = MonthlySales(year=year, month=month, total_spent=total_spent, total_sales=total_sales)
            db.session.add(sales)
        db.session.commit()

def insert_product(coupang_id, name, brand, category, price, alternative_price, quantity, status, description=""):
    with current_app.app_context():
        if Products.query.filter_by(name=name).first():
            print(f"Product '{name}' already exists.")
            return
        
        try:
            prod = Products(
                coupang_id=coupang_id,
                name=name,
                brand=brand,
                category=category,
                price=price,
                alternative_price=alternative_price,
                quantity=quantity,
                status=status,
                description=description
            )
            db.session.add(prod)
            db.session.commit()
            insert_monthly_sales(current_year, current_month, Decimal(price) * Decimal(quantity))
        
        except Exception as e:
            db.session.rollback()
            print(f"Error while inserting product: {e}")

def insert_user(username, password):
    """Insert a new user into the database"""
    with current_app.app_context():
        if Users.query.filter_by(username=username).first():
            print(f"User '{username}' already exists.")
            return
        
        hashed_password = generate_password_hash(password)
        user = Users(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

def view_all_products():
    products = Products.query.all()  # Fetch all rows
    if not products:
        print("No products found.")
        return

    # Get column names
    headers = Products.__table__.columns.keys()
    
    # Print headers
    print("\t".join(headers))
    
    # Print row data
    for product in products:
        print("\t".join(str(getattr(product, col)) for col in headers))

def get_product(product_name):
    with current_app.app_context():
        return Products.query.filter_by(name=product_name).first()

def get_user(username):
    """Get user by ID"""
    with current_app.app_context():
        return Users.query.filter_by(username=username).first()

def get_monthly_sales(year, month):
    """Get monthly sales data"""
    with current_app.app_context():
        return MonthlySales.query.filter_by(year=year, month=month).first()

def delete_product(product_name):
    with current_app.app_context():
        product = Products.query.filter_by(name=product_name).first()
        if not product:
            print(f"Product '{product_name}' not found.")
            return
        
        db.session.delete(product)
        db.session.commit()

def edit_monthly_sales(year, month, total_spent):
    with current_app.app_context():
        month = MonthlySales.query.filter_by(year=year, month=month).first()
        if not month:
            print(f"Month '{month}' not found.")
            return
        
        month.total_spent = total_spent
        db.session.commit()

def ship(product_name):
    with current_app.app_context():
        product = Products.query.filter_by(name=product_name).first()
        if not product:
            print(f"Product '{product_name}' not found.")
            return
        
        product.status = "shipped"
        db.session.commit()

def inventory(product_name):
    with current_app.app_context():
        product = Products.query.filter_by(name=product_name).first()
        if not product:
            print(f"Product '{product_name}' not found.")
            return
        
        product.status = "inventory"
        db.session.commit()