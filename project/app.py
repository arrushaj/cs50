import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_paginate import Pagination, get_page_parameter

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

    try:
        id = session["user_id"]

    except KeyError:
        id = ""

    row_user = db.execute("SELECT * FROM users WHERE id = ?", id)

    if len(row_user) < 1:
        user = ""
    else:
        user = row_user[0]["username"]

    rows = db.execute("SELECT * FROM thread WHERE board = 'music' ORDER BY latest DESC")

    page = request.args.get(get_page_parameter(), type=int, default=1)

    pagination = Pagination(page=page, per_page=5, total=len(rows), record_name='rows')

    i=(page-1) * 5
    rows1=rows[i:i+5]
    return render_template('music.html', pagination=pagination, rows=rows1, user=user)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        try:
            id = session["user_id"]

        except KeyError:
            id = ""

        row_user = db.execute("SELECT * FROM users WHERE id = ?", id)

        if len(row_user) < 1:
            user = ""
        else:
            user = row_user[0]["username"]

        title = request.args.get("search")
        board = request.args.get("board")

        title = "%" + title + "%"

        rows = db.execute("SELECT * FROM thread WHERE board = ? AND title LIKE ? ORDER BY latest DESC", board, title)

        return_html = board + ".html"

        page = request.args.get(get_page_parameter(), type=int, default=1)

        pagination = Pagination(page=page, per_page=5, total=len(rows), record_name='rows')

        i=(page-1) * 5
        rows1=rows[i:i+5]

        return render_template(return_html, rows=rows1, user=user, pagination=pagination)


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

        db.execute("INSERT INTO thread (user, title, board, creation, latest, user_id, latest_user, latest_id) VALUES (?, ?, ?, strftime('%Y/%m/%d %H:%M:%S'), strftime('%Y/%m/%d %H:%M:%S'), ?, ?, ?)", username, request.form.get("title"), request.form.get("board"), session["user_id"], username, session["user_id"])

        rows2 = db.execute("SELECT * FROM thread ORDER BY creation DESC")
        id = rows2[0]["id"]

        db.execute("INSERT INTO replies (thread_id, user, message, date, user_id) VALUES (?, ?, ?, strftime('%Y/%m/%d %H:%M:%S'), ?)", id, username, request.form.get("message"), session["user_id"])

        flash('Thread posted!')
        return redirect('/')

    else:
        return render_template("thread.html")

@app.route("/viewthread", methods=["GET", "POST"])
def viewthread():
    if request.method == "GET":
        id = request.args.get("id")

        rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", id)

        if len(rows) < 1:
            return apology("This thread doesn't exist!")

        try:
            row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            pls_work = row[0]["username"]

        except KeyError:
            pls_work = ""

        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=5, total=len(rows), record_name='rows')

        i=(page-1) * 5
        rows1=rows[i:i+5]

        return render_template("viewthread.html", rows=rows1, id=id, pls_work=pls_work, pagination=pagination)


@app.route("/reply", methods=["GET", "POST"])
@login_required
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

        db.execute("INSERT INTO replies (thread_id, user, message, date, user_id) VALUES (?, ?, ?, strftime('%Y/%m/%d %H:%M:%S'), ?)", thread, username, message, session["user_id"])
        db.execute("UPDATE thread SET replies = replies + 1 WHERE id = ?", thread)
        db.execute("UPDATE thread SET latest = strftime('%Y/%m/%d %H:%M:%S') WHERE id = ?", thread)
        db.execute("UPDATE thread SET latest_user = ? WHERE id = ?", username, thread)
        db.execute("UPDATE thread SET latest_id = ? WHERE id = ?", session["user_id"], thread)

        redir = "/viewthread?id=" + thread

        return redirect(redir)

@app.route("/like", methods=["GET", "POST"])
@login_required
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

        page = request.form.get("page")
        redir = "/viewthread?id=" + str(thread) + "&page=" + page

        #rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", thread)
        flash("Post liked!")
        return redirect(redir)

@app.route("/unlike", methods=["GET", "POST"])
@login_required
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

        page = request.form.get("page")
        redir = "/viewthread?id=" + str(thread) + "&page=" + page

        #rows = db.execute("SELECT * FROM replies WHERE thread_id = ?", thread)

        flash("Post unliked!")
        return redirect(redir)

@app.route("/delete_comment", methods=["GET", "POST"])
@login_required
def delete_comment():
    if request.method == "POST":
        reply_id = request.form.get("reply_id")

        thread_id = db.execute("SELECT thread_id FROM replies WHERE id = ?", reply_id)
        thread = thread_id[0]["thread_id"]

        x = db.execute("SELECT * FROM thread WHERE id = ?", thread)
        check = x[0]["replies"]

        if check == 1:
            db.execute("UPDATE thread SET replies = replies - 1 WHERE id = ?", thread)
            db.execute("DELETE FROM likes WHERE reply_id = ?", reply_id)
            db.execute("DELETE FROM replies WHERE id = ?", reply_id)
            db.execute("DELETE FROM thread WHERE id = ?", thread)
            redir = "/"

        else:
            db.execute("UPDATE thread SET replies = replies - 1 WHERE id = ?", thread)
            db.execute("DELETE FROM likes WHERE reply_id = ?", reply_id)
            db.execute("DELETE FROM replies WHERE id = ?", reply_id)
            redir = "/viewthread?id=" + str(thread)

        flash("Successfully deleted!")
        return redirect(redir)

@app.route("/delete_thread", methods=["GET", "POST"])
@login_required
def delete_thread():
    if request.method == "POST":
        thread_id = request.form.get("thread")

        board = db.execute("SELECT board FROM thread WHERE id = ?", thread_id)
        board_name = board[0]["board"]

        rows = db.execute("SELECT replies.thread_id, replies.id FROM replies JOIN thread ON thread.id = replies.thread_id AND thread.id = ?", thread_id)

        for row in rows:
            db.execute("DELETE FROM likes WHERE reply_id = ?", row["id"])
            db.execute("DELETE FROM replies WHERE id = ?", row["id"])

        db.execute("DELETE FROM thread WHERE id = ?", thread_id)

        redir = "/" + board_name

        flash("Successfully deleted")
        return redirect(redir)

@app.route("/update_post", methods=["GET", "POST"])
@login_required
def update_post():
    if request.method == "GET":
        id = request.args.get("reply_id")

        message_row = db.execute("SELECT * FROM replies WHERE id = ?", id)

        x = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = x[0]["username"]

        y = db.execute("SELECT * FROM replies WHERE user = ? AND id = ?", username, id)

        if len(y) < 1:
            return apology("Post unable to be edited")

        return render_template("edit.html", message_row=message_row)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        message = request.form.get("message")
        id = request.form.get("reply_id")

        x = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = x[0]["username"]

        y = db.execute("SELECT * FROM replies WHERE user = ? AND id = ?", username, id)

        if len(y) < 1:
            return apology("Post unable to be edited")

        db.execute("UPDATE replies SET message = ? WHERE id = ?", message, id)

        a = db.execute("SELECT * FROM replies WHERE id = ?", id)
        thread = a[0]["thread_id"]

        redir = "/viewthread?id=" + str(thread)

        return redirect(redir)

@app.route("/reply_form", methods=["GET", "POST"])
@login_required
def reply_form():
    if request.method == "GET":
        id = request.args.get("reply_id")

        row = db.execute("SELECT * FROM replies WHERE id = ?", id)

        thread_id = row[0]["thread_id"]

        y = db.execute("SELECT * FROM replies WHERE id = ? AND thread_id = ?", id, thread_id)

        if len(y) < 1:
            return apology("That post is not in this thread!")

        return render_template("reply.html", row=row)

@app.route("/reply_legit", methods=["GET", "POST"])
@login_required
def reply_legit():
    if request.method == "POST":
        id = request.form.get("reply_id")

        print(id)

        row = db.execute("SELECT * FROM replies WHERE id = ?", id)

        thread_id = row[0]["thread_id"]
        response_message = row[0]["message"]
        response_user = row[0]["user"]
        response_date = row[0]["date"]

        y = db.execute("SELECT * FROM replies WHERE id = ? AND thread_id = ?", id, thread_id)

        if len(y) < 1:
            return apology("That post is not in this thread!")

        elif request.form.get("message") == "":
            return apology("must provide message")

        message = request.form.get("message")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = rows[0]["username"]

        db.execute("INSERT INTO replies (thread_id, user, message, date, response, response_id, response_message, response_user, response_date, user_id) VALUES (?, ?, ?, strftime('%Y/%m/%d %H:%M:%S'), ?, ?, ?, ?, ?, ?)",
        thread_id, username, message, 1, id, response_message, response_user, response_date, session["user_id"])
        db.execute("UPDATE thread SET replies = replies + 1 WHERE id = ?", thread_id)
        db.execute("UPDATE thread SET latest = strftime('%Y/%m/%d %H:%M:%S') WHERE id = ?", thread_id)
        db.execute("UPDATE thread SET latest_user = ? WHERE id = ?", username, thread_id)
        db.execute("UPDATE thread SET latest_id = ? WHERE id = ?", session["user_id"], thread_id)

        redir = "/viewthread?id=" + str(thread_id)
        flash("Reply posted!")
        return redirect(redir)

@app.route("/profile")
def profile():
    id = request.args.get("id")
    get = db.execute("SELECT * FROM users WHERE id = ?", id)
    user = get[0]["username"]
    bio = get[0]["bio"]

    rows = db.execute("SELECT * FROM thread WHERE user = ?", user)

    return render_template("profile.html", user=user, bio=bio, id=int(id), rows=rows)

@app.route("/edit_bio_form", methods=["GET", "POST"])
@login_required
def edit_bio_form():
    if request.method == "GET":
        id = session["user_id"]

        row = db.execute("SELECT * FROM users WHERE id = ?", id)

        bio = row[0]["bio"]

        return render_template("edit_bio.html", bio=bio)

@app.route("/update_bio", methods=["GET", "POST"])
@login_required
def update_bio():
    if request.method == "POST":
        id = session["user_id"]
        bio = request.form.get("bio")

        db.execute("UPDATE users SET bio = ? WHERE id = ?", bio, id)

        redir = "/profile?id=" + str(session["user_id"])

        flash("Bio updated!")
        return redirect(redir)


