from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template("main/error.html", title="Error", head="File Not Found",
                           body="This is not the droid you're looking for."), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("main/error.html", title="Error", head="An Error Has Occurred",
                           body="Where is that monkey..."), 500
