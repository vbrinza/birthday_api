from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import os

def get_connection_string():
    db_user = os.environ.get('DB_USER', 'test_user')
    db_password = os.environ.get('DB_PASSWORD', 'test_password')
    db_name = os.environ.get('DB_NAME', 'test_database')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    connection_template = 'mysql+pymysql://%s:%s@%s/%s'
    return connection_template % (db_user, db_password, db_host, db_name)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test_user:test_password@192.168.50.4/test_database'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    date_of_birth = db.Column(db.DateTime)

    def __init__(self, username, date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return '<User %r>' % self.username
db.create_all()
db.session.commit()

@app.route('/hello/<name>', methods=['GET', 'PUT'])
def hello_name(name):
    if request.method == 'GET':
      today = date.today()
      user_by_name = Users.query.filter_by(username=name).first()
      dob_data = user_by_name.date_of_birth.strftime('%Y-%m-%d').split("-")
      dob_year = int(dob_data[0])
      dob_month = int(dob_data[1])
      dob_day = int(dob_data[2])
      dob = date(dob_year,dob_month,dob_day)
      number_of_days = (today - dob).days
      age = number_of_days // 365
      this_year = today.year
      next_birt_day = date(this_year, dob_month, dob_day)
      results = []

      if today < next_birt_day:
        gap = (next_birt_day - today).days
        return jsonify("message: Hello", name, "! Your birthday is in ", gap, " days.")
      elif today == next_birt_day:
        return jsonify("message: Hello", name, "! Today is your birthday!")
      else:
        next_birt_day = date(this_year + 1,dob_month,dob_day)
        gap = (next_birt_day - today).days
        return jsonify("message: Hello", name, "! Your birthday is in ", gap, " days.")
    else:
        input_json = request.get_json()
        user_by_name = Users.query.filter_by(username=name).first()
        if not user_by_name:
            try:
                input_date = input_json['dateOfBirth']
                verify_date = datetime.strptime(input_date, '%Y-%m-%d')
            except ValueError:
                return("Unrecognized date format, please use YYYY-MM-DD")
            user=Users(name, input_date)
            db.session.add(user)
            db.session.commit()
            return Response("No Content", status=204, mimetype='application/json')

        else:
            return ("Username exists. UPDATE method not implemented.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
