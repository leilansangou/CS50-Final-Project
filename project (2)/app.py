import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from jinja2 import Template
from base64 import b64encode

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///musicreviewer.db")

# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


@app.route("/")
@login_required
def index():

# to do !! figure out what the homepage is

    reviews = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id ORDER BY time DESC")

    for review in reviews:
        review["image"] = b64encode(review["picture"]).decode("utf-8")

    return render_template("index.html", reviews=reviews)


@app.route("/newreview", methods=['GET', 'POST'])
@login_required
def review():

    if request.method == 'POST':

        if not request.form.get("album"):
            flash("missing album")
            return render_template("postreview.html")
        elif not request.form.get("artist"):
            flash("missing artist")
            return render_template("postreview.html")
        elif not request.form.get("rating"):
            flash("missing rating")
            return render_template("postreview.html")
        elif not request.form.get("rating").isdigit():
            flash("invalid rating, please enter a number out of 10")
            return render_template("postreview.html")
        elif float(request.form.get("rating")) > 10.0:
            flash("invalid rating, please enter a number less than or equal 10")
            return render_template("postreview.html")
        elif not request.form.get("review"):
            flash("missing review")
            return render_template("postreview.html")
        elif not request.files["image"]:
             flash("missing album cover")
             return render_template("postreview.html")

        album = request.form.get("album")
        artist = request.form.get("artist")
        rating = request.form.get("rating")
        review = request.form.get("review")
        image = request.files["image"].read()

        id = session["user_id"]

        db.execute("INSERT INTO reviews (user_id, picture, album_title, artist_name, rating, review) VALUES(?,?,?,?,?,?)", id, image, album, artist, rating, review)

        flash("posted!")
        return render_template("postreview.html")

    else:
        print("get")
        return render_template("postreview.html")


@app.route("/run", methods=["GET", "POST"])
@login_required
def run():

    users = db.execute("SELECT * FROM users")

    if request.method == "POST":

        requested_user = (request.form.get("hey"))
        print(requested_user)

        user_id = (db.execute("SELECT id FROM users WHERE username = ?", requested_user))[0]["id"]

        profile = (db.execute("SELECT * FROM users WHERE id = ?", user_id))[0]
        reviews = db.execute("SELECT * FROM reviews WHERE user_id = ?", user_id)

        # got a little help from stackoverflow - https://stackoverflow.com/questions/31358578/display-image-stored-as-binary-blob-in-template
        for review in reviews:
            review["image"] = b64encode(review["picture"]).decode("utf-8")

        return render_template("profile.html", profile=profile, reviews=reviews)


    else:

        return render_template("search.html", users=users)



@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    users = db.execute("SELECT * FROM users")

    return render_template("search.html", users=users)



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Display user's history of history."""

    profile = (db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"]))[0]
    reviews = db.execute("SELECT * FROM reviews WHERE user_id = :id", id=session["user_id"])

    # got a little help from stackoverflow - https://stackoverflow.com/questions/31358578/display-image-stored-as-binary-blob-in-template
    for review in reviews:
        review["image"] = b64encode(review["picture"]).decode("utf-8")

    return render_template("profile.html", profile=profile, reviews=reviews)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # submit input via post to /register
    if request.method == "POST":

        # ask for user to input username --> text field whos name == username.
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # if it's valid, require a password, --> text field where name == password
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # then require it again --> text field where name == confirmation
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)
        # if password doesn't == confirmation, apologize
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 403)
        else:
            username = request.form.get("username")
            password = request.form.get("password")

            # check to see if the username is taken
            if db.execute("SELECT username FROM users WHERE username = ?", username) != []:
                return apology("Username already exists")

            # insert new user into users -- store hash of user's password using generate_password_hash
            new_id = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, generate_password_hash(password))

            # log the user in
            session["user_id"] = new_id

            return redirect("/")
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)