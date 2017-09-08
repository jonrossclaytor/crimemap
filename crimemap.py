from flask import Flask
from flask import render_template
from flask import request
import json
import dbconfig
import sys

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

f = open('log.txt','w')


@app.route("/")
def home():
    f.write('made it to home')
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    print('this is home')
    return render_template("home.html", crimes=crimes)


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    f.write('made it to submitcrime')
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()


f.close()

if __name__ == '__main__':
    app.run(debug=True)
