import os
import re
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from models import db, Products, MonthlySales
from services.product_functions import edit_monthly_sales, insert_product, insert_user, insert_monthly_sales, view_all_products, get_product, get_user, get_monthly_sales, delete_product, ship, inventory 

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///coupang.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
db.init_app(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        if not product_name:
            return ("must provide product name")
        ship(product_name)
        return redirect("/")
    else:
        products = Products.query.all()
        headers = Products.__table__.columns.keys()
        data = []
        for p in products:
            price = float(p.price) / p.quantity
            alt_price = float(p.alternative_price) if p.alternative_price else 0
            final_price = ((alt_price - price * 8.82) / 2) + price * 8.82 if alt_price else 0

            data.append({
                'id': p.id,
                'name': p.name,
                'brand': p.brand,
                'category': p.category,
                'price': price,
                'alternative_price': alt_price,
                'quantity': p.quantity,
                'status': p.status,
                'description': p.description,
                'coupang_id': p.coupang_id,
                'final_price': round(final_price, 2)
            })
        return render_template("index.html", data=data, headers=headers, username=session["username"])

@app.route("/shipped", methods=["GET", "POST"])
@login_required
def shipped():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        if not product_name:
            return ("must provide product name")
        delete_product(product_name)
        return redirect("/shipped")
    else:
        print(Products.__table__.columns.keys())
        products = Products.query.all()
        headers = Products.__table__.columns.keys()
        return render_template("shipped.html", headers=headers, data=products, username=session["username"])
    
@app.route("/waiting", methods=["GET", "POST"])
@login_required
def waiting():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        if not product_name:
            return ("must provide product name")
        inventory(product_name)
        return redirect("/waiting")
    else:
        print(Products.__table__.columns.keys())
        products = Products.query.all()
        headers = Products.__table__.columns.keys()
        return render_template("waiting.html", headers=headers, data=products, username=session["username"])
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password")
        elif not (request.form.get("password") == request.form.get("confirm")):
            return ("passwords don't match")
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            insert_user(username, password)
        except:
            return ("The username exists")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        passw=request.form.get("password")
        username = request.form.get("username")
        # Ensure username was submitted
        if not username:
            return ("must provide username")
        # Ensure password was submitted
        elif not passw:
            return ("must provide password")
        # Query database for username
        user = get_user(username)
        if not user:
            return ("invalid username")
        if not check_password_hash(user.password, passw):
            return ("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user.id
        session["username"] = user.username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        coupang_id = request.form.get("coupang_id")
        pattern = r"\/(\d+\?vendorItemId=\d+)"
        pattern2 = r"\/(\d+\?itemId=\d+\&vendorItemId=\d+)"
        match = re.search(pattern, coupang_id)
        if match:
            result = match.group(1)
        else:
            match = re.search(pattern2, coupang_id)
            if match:
                result = match.group(1)
            else:
                print("No match found")
            name = request.form.get("name")
            brand = request.form.get("brand")
            category = request.form.get("category")
            price = request.form.get("price")
            alternative_price = request.form.get("alternative_price")
            quantity = request.form.get("quantity")
            status = request.form.get("status")
            description = request.form.get("description")
            if not coupang_id or not name or not brand or not category or not price or not status:
                return ("must provide all fields")
            try:
                insert_product(result, name, brand, category, price, alternative_price, quantity, status, description)
            except Exception as e:
                return f"An error occurred: {e}", 500


        # Redirect user to home page    
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("orders.html")

@app.route("/monthly", methods=["GET", "POST"])
@login_required
def monthly():
    if request.method == "POST":
        return redirect("/")
    else:
        monthly = MonthlySales.query.all()
        headers = MonthlySales.__table__.columns.keys()
        products = Products.query.all()
        await_current = 0.00
        inv_current = 0.00
        shipped_current = 0.00
        for row in products:
            if row.status == "inventory":
                inv_current = inv_current + float(row.price * row.quantity)
            elif row.status == "waiting":
                await_current = await_current + float(row.price * row.quantity)
            elif row.status == "shipped":
                shipped_current = shipped_current + float(row.price * row.quantity)
        return render_template("monthly.html", headers=headers, data=monthly, await_current=await_current, inv_current=inv_current, shipped_current=shipped_current)