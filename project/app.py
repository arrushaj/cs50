import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///forum.db")

x = ""

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("home.html")

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
        global x
        x = request.form.get("username")

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
    global x
    x = ""
    # Redirect user to login form
    return redirect("/")


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
            return apology("must provide password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        user = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hash)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('Registered!')
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/music")
def music():
    if session.get("user_id") is None:
        session["user_id"] = ""

    row_user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if len(row_user) < 1:
        user = ""
    else:
        user = row_user[0]["username"]

    rows = db.execute("SELECT * FROM thread WHERE board = 'music' ORDER BY latest DESC")

    if session["user_id"] == "":
        session.clear()

    return render_template("music.html", rows=rows, user=user)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        if session.get("user_id") is None:
            session["user_id"] = ""

        row_user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if len(row_user) < 1:
            user = ""
        else:
            user = row_user[0]["username"]

        title = request.args.get("search")
        board = request.args.get("board")

        title = "%" + title + "%"

        rows = db.execute("SELECT * FROM thread WHERE board = ? AND title LIKE ? ORDER BY latest DESC", board, title)

        return_html = board + ".html"

        if session["user_id"] == "":
            session.clear()

        return render_template(return_html, rows=rows, user=user)


@app.route("/thread", methods=["GET", "POST"])
@login_required
def thread():
    if request.method == "POST":

        if not request.form.get("title"):
            return apology("must provide title")

        elif not request.form.get("board"):
            return apology("must provide board")

        elif not request.form.get("message"):
            return apology("must provide message")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = rows[0]["username"]

        db.execute("INSERT INTO thread (user, title, board, creation, latest) VALUES (?, ?, ?, strftime('%d/%m/%Y %H:%M:%S'), strftime('%d/%m/%Y %H:%M:%S'))", username, request.form.get("title"), request.form.get("board"))

        rows2 = db.execute("SELECT * FROM thread ORDER BY creation DESC")
        id = rows2[0]["id"]

        db.execute("INSERT INTO replies (thread_id, user, message, date) VALUES (?, ?, ?, strftime('%d/%m/%Y %H:%M:%S'))", id, username, request.form.get("message"))

        flash('Thread posted!')
        return redirect('/')

    else:
        return render_template("thread.html")

@app.route("/viewthread", methods=["GET", "POST"])
def viewthread():
    if request.method == "GET":
        id = request.args.get("id")

        global x
        rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", id)

        if len(rows) < 1:
            return apology("This thread doesn't exist!")

        elif x != "":
            row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            pls_work = row[0]["username"]

        elif x == "":
            pls_work = ""

        return render_template("viewthread.html", rows=rows, id=id, pls_work=pls_work)


@app.route("/reply", methods=["GET", "POST"])
def reply():
    if request.method == "POST":

        if request.form.get("thread_id") is None:
            return apology("thread id does not exist")

        elif request.form.get("message") == "":
            return apology("must provide message")

        thread = request.form.get("thread_id")
        message = request.form.get("message")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = rows[0]["username"]

        db.execute("INSERT INTO replies (thread_id, user, message, date) VALUES (?, ?, ?, strftime('%d/%m/%Y %H:%M:%S'))", thread, username, message)
        db.execute("UPDATE thread SET replies = replies + 1 WHERE id = ?", thread)
        db.execute("UPDATE thread SET latest = strftime('%d/%m/%Y %H:%M:%S') WHERE id = ?", thread)

        redir = "/viewthread?id=" + thread

        return redirect(redir)

@app.route("/like", methods=["GET", "POST"])
def like():
    if request.method == "POST":
        reply_id = request.form.get("reply_id")
        user_id = session["user_id"]

        rows = db.execute("SELECT * FROM likes WHERE reply_id = ? AND user_id = ?", reply_id, user_id)
        if len(rows) >= 1:
            return apology("You've already liked this post!")

        db.execute("INSERT INTO likes (reply_id, user_id) VALUES (?, ?)", reply_id, user_id)
        db.execute("UPDATE replies SET likes = likes + 1 WHERE id = ?", reply_id)

        thread_id = db.execute("SELECT thread_id FROM replies WHERE id = ?", reply_id)
        thread = thread_id[0]["thread_id"]
        redir = "/viewthread?id=" + str(thread)

        #rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", thread)

        return redirect(redir)

@app.route("/unlike", methods=["GET", "POST"])
def unlike():
    if request.method == "POST":
        reply_id = request.form.get("reply_id")
        user_id = session["user_id"]

        rows = db.execute("SELECT * FROM likes WHERE reply_id = ? AND user_id = ?", reply_id, user_id)
        if len(rows) < 1:
            return apology("You haven't liked this post!")

        db.execute("DELETE FROM likes WHERE reply_id = ? AND user_id = ?", reply_id, user_id)
        db.execute("UPDATE replies SET likes = likes - 1 WHERE id = ?", reply_id)

        thread_id = db.execute("SELECT thread_id FROM replies WHERE id = ?", reply_id)
        thread = thread_id[0]["thread_id"]
        redir = "/viewthread?id=" + str(thread)

        #rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", thread)

        return redirect(redir)

@app.route("/delete_comment", methods=["GET", "POST"])
def delete_comment():
    if request.method == "POST":
        reply_id = request.form.get("reply_id")

        db.execute("DELETE FROM replies WHERE id = ?", reply_id)

        thread_id = db.execute("SELECT thread_id FROM replies WHERE id = ?", reply_id)
        thread = thread_id[0]["thread_id"]
        redir = "/viewthread?id=" + str(thread)

        return redirect(redir)