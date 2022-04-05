import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    rows = db.execute("SELECT ticker, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY ticker", session["user_id"])

    sum = 0
    for row in rows:
        sum = sum + ((row["SUM(shares)"]) * lookup(row["ticker"])["price"])

    row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = row[0]["cash"]
    return render_template("index.html", rows=rows, lookup=lookup, sum=sum, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        ticker = request.form.get("symbol")

        check = lookup(ticker)

        if check == None:
            return apology("ticker not found")

        shares = float(request.form.get("shares"))

        id = session["user_id"]

        stock = lookup(ticker)
        price = stock["price"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", id)
        cash = rows[0]["cash"]
        cost = price * shares
        new_cash = cash - cost

        if new_cash < 0:
            return apology("not enough cash to purchase")

        # Get current date and time
        dt = datetime.datetime.now()

        # This is going to remove the milliseconds
        time = dt.replace(microsecond=0)

        db.execute("INSERT INTO transactions (user_id, ticker, shares, price, cost, time) VALUES (?, ?, ?, ?, ?, ?)", id, ticker, shares, price, cost, time)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, id)

        flash('Buy successful!')
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT ticker, shares, price, time FROM transactions WHERE user_id = 1 ORDER BY time", session["user_id"])


    return render_template("history.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        stock = lookup(symbol)

        if stock == None:
            return apology("ticker doesn't exist")

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username already taken")

        elif not request.form.get("password"):
            return apology("must provide username")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        user = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hash)

        flash('Registered!')
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        ticker = request.form.get("symbol")
        shares = float(request.form.get("shares"))

        check = lookup(ticker)

        if check == None:
            return apology("ticker not found")

        if shares < 0:
            return apology("shares cannot be negative")

        rows = db.execute("SELECT ticker, SUM(shares) FROM transactions WHERE user_id = ? AND ticker = ? GROUP BY ticker", session["user_id"], ticker)

        if len(rows) != 1:
            return apology("ticker not found in portfolio")

        if (rows[0]["SUM(shares)"] < shares):
            return apology("you own less shares than that")

        stock = lookup(ticker)
        price = stock["price"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        gain = price * shares
        new_cash = cash + gain

        # For database purposes, we want shares to be negative so that when we sum it up it is deducted
        shares = shares * -1

        # Get current date and time
        dt = datetime.datetime.now()

        # This is going to remove the milliseconds
        time = dt.replace(microsecond=0)

        db.execute("INSERT INTO transactions (user_id, ticker, shares, price, cost, time) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], ticker, shares, price, gain, time)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        flash('Sell successful!')
        return redirect("/")

    else:
        return render_template("sell.html")
