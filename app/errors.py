from flask import render_template , flash
from app import app,db


@app.errorhandler(404)
def not_found_error(error):
    flash("Sorry ,, Page not Found")
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    flash("Sorry ,, Internal Error Happend")
    return render_template('index.html')
