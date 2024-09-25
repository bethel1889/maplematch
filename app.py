import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, region_check, program_stream_check, check, REGIONS, PROGRAM_STREAMS, region_numbers, program_stream_numbers

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///jobs.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# HOMEPAGE
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        id = session["user_id"]
        username = db.execute("SELECT * FROM users WHERE id=?;", id)[0]["username"]
    except:
        username = ""
    return render_template("index.html", username=username)



# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    else:
        # Check if the username and password is valid
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if check(username, password) == False:
            return apology("Enter username and password to login")

        # Check if the password and confirmation are both correct
        elif password != confirmation:
            return apology("Password and confirmation password do not match")

        # Check if the username exists in the database
        details = db.execute("SELECT * FROM users WHERE username=?;", username)
        if not details:
            # Enter the user's details into the database if the username doesn't exist
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);",
                       username, generate_password_hash(password))
            rows = db.execute("SELECT * FROM users WHERE username=?;", username)

            # Log the user in
            session["user_id"] = rows[0]["id"]
            flash("You have been registered")
            return redirect("/")

        # if the username and password exist
        elif check_password_hash(details[0]["hash"], password) == True:
            return apology("You already have an account with MapleMatch")

        # If only the username exists
        else:
            return apology("Please choose a different username, this username has been taken")



# LOG IN
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
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
        flash("You have been logged in")
        return redirect("/")



# LOG OUT
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    flash("You have logged out")
    return redirect("/")



# SEARCH
@app.route("/search", methods=["GET","POST"])
def search():
    OCCUPATIONS = db.execute("SELECT * FROM occupations")
    new_occupation = []
    for row in OCCUPATIONS:
        job = row["name"]
        new_occupation.append(job)
    OCCUPATIONS = sorted(new_occupation)

    ids = []
    try:
        id = session["user_id"]
        username = db.execute("SELECT * FROM users WHERE id=?", id)[0]["username"]
        job_ids = db.execute("SELECT * FROM user_jobs WHERE user_id=?", id)
        for row in job_ids:
            ids.append(row["job_id"])
    except:
        ids = False
        username = ""

    '''
        A get request returns a search form to search for jobs and a post request returns
        a list of jobs meeting the search criteria with search and star buttons
    '''

    if request.method == "GET":
        return render_template("search.html", occupations=OCCUPATIONS, REGIONS=REGIONS,
            PROGRAM_STREAMS=PROGRAM_STREAMS, username=username)

    else:
        r = 1
        o = 1
        p = 1
        all = "All"

        # Region
        region = request.form.get("region")
        if region == all:
            r = 0
        if region not in REGIONS and region != all:
            return apology("Invalid Input 1")
        region = region_check(region)

        # Occupation
        occupation = request.form.get("occupation")
        if occupation == all:
            o = 0
        occupations = db.execute("SELECT * FROM occupations WHERE name=?", occupation)
        if not occupations and occupation != all:
            return apology("Invalid Input 2")
        occupation_id = occupations[0]["id"]

        # Program_stream
        program_stream = request.form.get("program_stream")
        if program_stream == all:
            p = 0
        if program_stream not in PROGRAM_STREAMS and program_stream != all:
            return apology("Invalid Input 3")
        program_stream = program_stream_check(program_stream)

        # Selection
        if r == 0 and o == 0 and p == 0:
            raw_results = db.execute("SELECT * FROM jobs ORDER BY approved_lmia DESC, approved_position DESC;")

        elif r == 0 and o == 0 and p == 1:
            raw_results = db.execute("SELECT * FROM jobs WHERE program_stream=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     program_stream)

        elif r == 0 and o == 1 and p == 0:
            raw_results = db.execute("SELECT * FROM jobs WHERE occupation_id=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     occupation_id)

        elif r == 0 and o == 1 and p == 1:
            raw_results = db.execute("SELECT * FROM jobs WHERE program_stream=? AND occupation_id=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     program_stream, occupation_id)

        elif r == 1 and o == 0 and p == 0:
            raw_results = db.execute("SELECT * FROM jobs WHERE region=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                    region)

        elif r == 1 and o == 0 and p == 1:
            raw_results = db.execute("SELECT * FROM jobs WHERE program_stream=? AND region=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     program_stream, region)

        elif r == 1 and o == 1 and p == 0:
            raw_results = db.execute("SELECT * FROM jobs WHERE region=? AND occupation_id=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     region, occupation_id)

        else:
            raw_results = db.execute("SELECT * FROM jobs WHERE program_stream=? AND region=? AND occupation_id=? ORDER BY approved_lmia DESC, approved_position DESC;",
                                     program_stream, region, occupation_id)

        results = []
        sn = 0
        for row in raw_results:
            new_row = {}
            sn += 1

            if ids != False:
                if row["id"] in ids:
                    new_row["star_button"] = "Starred"
                else:
                    new_row["star_button"] = "Star"
            new_row["sn"] = sn
            new_row["id"] = row["id"]
            new_row["region"] = region_check(row["region"])
            new_row["program_stream"] = program_stream_check(row["program_stream"])
            new_row["occupation"] = db.execute("SELECT * FROM occupations WHERE id=?;", row["occupation_id"])[0]["name"]
            new_row["employer"] = db.execute("SELECT * FROM employers WHERE id=?;", row["employer_id"])[0]["company"]
            new_row["address"] = db.execute("SELECT * FROM locations WHERE id=?;", row["location_id"])[0]["address"]
            new_row["approved_lmia"] = row["approved_lmia"]
            new_row["approved_position"] = row["approved_position"]
            results.append(new_row)
        jobs = results
        return render_template("search.html", jobs=jobs, occupations=OCCUPATIONS, REGIONS=REGIONS,
            PROGRAM_STREAMS=PROGRAM_STREAMS, username=username)



# STAR
@app.route("/star", methods=["GET","POST"])
def star():
    id = session["user_id"]
    username = db.execute("SELECT * FROM users WHERE id=?;", id)[0]["username"]
    '''
        A get request returns a list of starred jobs
    '''
    if request.method == "GET":
        raw_results = db.execute('''SELECT * FROM jobs WHERE id IN (SELECT job_id FROM user_jobs WHERE user_id=?);
                                 ''', id)
        results = []
        sn = 0
        for row in raw_results:
            new_row = {}
            sn += 1
            new_row["sn"] = sn
            new_row["id"] = row["id"]
            new_row["region"] = region_check(row["region"])
            new_row["program_stream"] = program_stream_check(row["program_stream"])
            new_row["occupation"] = db.execute("SELECT * FROM occupations WHERE id=?;", row["occupation_id"])[0]["name"]
            new_row["employer"] = db.execute("SELECT * FROM employers WHERE id=?;", row["employer_id"])[0]["company"]
            new_row["address"] = db.execute("SELECT * FROM locations WHERE id=?;", row["location_id"])[0]["address"]
            new_row["approved_lmia"] = row["approved_lmia"]
            new_row["approved_position"] = row["approved_position"]
            results.append(new_row)
        jobs = results
        return render_template("starred.html", jobs=jobs, username=username)

    else:
        job_id = request.form.get("job_id")
        user_job = db.execute("SELECT * FROM user_jobs WHERE user_id=? AND job_id=?;", id, job_id)
        if not user_job:
            db.execute("INSERT INTO user_jobs(user_id, job_id) VALUES(?, ?);", id, job_id)
        flash("Saved")
        return redirect("/star")



# UNSTAR
@app.route("/unstar", methods=["GET","POST"])
@login_required
def unstar():
    id = session["user_id"]
    '''
        A post request removes a job_id from the user_jobs table
    '''
    if request.method == "POST":
        job_id = request.form.get("job_id")
        user_jobs = db.execute("SELECT * FROM user_jobs WHERE user_id=? AND job_id=?;", id, job_id)
        if len(user_jobs) > 0:
            db.execute("DELETE FROM user_jobs WHERE user_id=? AND job_id=?;", id, job_id)
    flash("Removed")
    return redirect("/star")



# ABOUT
@app.route("/about", methods=["GET","POST"])
def about():
    try:
        id = session["user_id"]
        username = db.execute("SELECT * FROM users WHERE id=?", id)[0]["username"]
    except:
        username = ""

    if request.method == "GET":
        return render_template("about.html", username=username)
