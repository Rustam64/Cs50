import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    user = id[0]['username']
    stocks = db.execute(
        "SELECT symbol, stock, SUM(amount) AS total_amount FROM history WHERE user_id = ? GROUP BY symbol, stock;", user)
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    prices = {}
    for stock in stocks:
        search = lookup(stock['symbol'])
        prices[stock['symbol']] = float(search["price"])
    return render_template("index.html", balance=balance[0]['cash'], username=user, stocks=stocks, prices=prices)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        search = lookup(symbol)
        if not search:
            return apology("Please verify the stock symbol.", 400)
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please enter an integer.", 400)
        if (shares <= 0):
            flash("Please enter an amount higher than 0.")
            return apology("Please enter a valid integer.", 400)
        else:
            id = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            username = id[0]['username']
            price = float(shares*float(search['price']))
            balance = db.execute(
                "SELECT cash FROM users WHERE id = ?", session["user_id"])
            balance = balance[0]['cash']
            if (float(balance) >= float(price)):
                db.execute("INSERT INTO history (user_id, type, stock, symbol, amount, price, balance, time) VALUES (?, 'BUY', ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                           username, search['name'], search['symbol'], shares, price, balance-price)
                db.execute("UPDATE users SET cash = ? WHERE username=?", balance-price, username)
                return redirect("/")
            else:
                flash("Insufficient funds.", "danger")
                return redirect(url_for("buy"))
    else:
        return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    user = id[0]['username']
    stocks = db.execute("SELECT * FROM history WHERE user_id = ?", user)
    prices = {}
    for stock in stocks:
        search = lookup(stock['symbol'])
        prices[stock['symbol']] = float(search["price"])
        stock['balance'] = stock['balance']
    return render_template("history.html", username=user, stocks=stocks, prices=prices)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    """Reset password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif (not request.form.get("newpass")) or (not request.form.get("confirm")):
            return apology("Please provide and confirm the new password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        else:
            user = request.form.get("username")
            hashed_password = generate_password_hash(request.form.get("newpass"))
            db.execute("UPDATE users SET hash = ? WHERE username = ?", hashed_password, user)
            # Forget any user_id
            session.clear()
            flash("Reset successful!")
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("reset.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        search = lookup(symbol)
        if not search:
            return apology("Please verify the stock symbol.", 400)
        else:
            return render_template("quoted.html", search=search)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("passwords don't match", 400)
        try:
            hashed_password = generate_password_hash(request.form.get("password"))
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                    "username"), hashed_password
            )
        except:
            return apology("The username exists", 400)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        search = lookup(symbol)
        if not search:
            return apology("Please enter a valid share name", 400)
        else:
            name = search["name"]
            price = float(search["price"])
            id = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            user = id[0]['username']
            try:
                shares = float(request.form.get("shares"))
            except:
                return apology("Please enter an integer.", 400)
            stocks = db.execute(
                "SELECT SUM(amount) AS total_amount FROM history WHERE user_id = ? AND symbol=? GROUP BY symbol, stock;", user, symbol)
            amount = stocks[0]['total_amount']
            if (shares <= 0):
                return apology("Please enter an valid integer.", 400)
            elif (shares > amount):
                return apology("Please enter an valid integer.", 400)
            else:
                shares = -shares
                balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
                afterbalance = (float(balance[0]['cash'])-float(search["price"])*shares)
                db.execute("INSERT INTO history (user_id, type, stock, symbol, amount, price, balance, time) VALUES (?, 'SELL', ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                           user, name, symbol, shares, price, afterbalance)
                db.execute("UPDATE users SET cash = ? WHERE username=?", afterbalance, user)
                flash("Transaction successful!", "success")
                return redirect("/")
    else:
        id = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        user = id[0]['username']
        stocks = db.execute(
            "SELECT symbol, stock, SUM(amount) AS total_amount FROM history WHERE user_id = ? GROUP BY symbol, stock;", user)
        return render_template("sell.html", stocks=stocks, user=user)
