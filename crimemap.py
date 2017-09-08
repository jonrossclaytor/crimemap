import datetime
#import dateparser
import dbconfig
from flask import Flask
from flask import render_template
from flask import request
import json
import string


if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging','break-in']

@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    
    date = request.form.get("date")
    #date = format_date(date)
    if not date:
        return home("Invalid date.  Please use yyyy-mm-dd format.")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except:
        return home()
    description = sanitize_string(request.form.get("description"))
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

"""
def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None
"""

def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + "!@#$%^&*()?'"
    return filter(lambda x: x in whitelist, userinput)
    
if __name__ == '__main__':
    app.run(debug=True)
