from flask import redirect, render_template, session
from functools import wraps


REGIONS = ["Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia",
    "New Brunswick", "Quebec", "Ontario", "Manitoba", "Saskatchewan", "Alberta",
    "British Columbia", "Yukon", "Northwest Territories",
    "Employers carrying on business in Canada with Head Office outside of Canada"
]
region_numbers = range(len(REGIONS))

PROGRAM_STREAMS = ["High Wage", "Low Wage", "Primary Agriculture", "Global Talent Stream"]

program_stream_numbers = range(len(PROGRAM_STREAMS))


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def region_check(region):
    if region in REGIONS:
        return REGIONS.index(region)

    elif region in region_numbers:
        return REGIONS[region]

    return False


def program_stream_check(program_stream):
    if program_stream in PROGRAM_STREAMS:
        return PROGRAM_STREAMS.index(program_stream)

    elif program_stream in program_stream_numbers:
        return PROGRAM_STREAMS[program_stream]

    return False

def validate(data):
    for key in data:
        if "blank" in data[key]:
            return False
    return True

def check(username, password):
    if not username:
        return False
    elif not password:
        return False
    return True
