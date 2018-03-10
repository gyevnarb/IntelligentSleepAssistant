from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from bson import ObjectId
from json import JSONEncoder
import json
import os
import datetime




app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class MBedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    tempData = db.Column(db.String(80))
    lightData = db.Column(db.String(80))
    moistureData = db.Column(db.String(80))
    airData = db.Column(db.String(80))
    def __init__(self,date,time, data):
        self.date = date
        self.time = time
        self.tempData = str(data[0])
        self.lightData = str(data[1])
        self.moistureData = str(data[2])
        self.airData = str(data[3])
    def serialize(self):
        return {
            'time' : self.time,
            'tempData' : self.tempData,
            'lightData' : self.lightData,
            'moistureData' : self.moistureData,
            'airData' : self.airData
        }

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('date', 'time', 'tempData', 'lightData', 'moistureData','airData');


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/data", methods=["POST"])
def add_user():
    now = datetime.datetime.now()
    month = str(now.month)
    if (len(month) == 1):
        month = "0" + month
    date = str(now.year) +'-' + month + '-' + str(now.day)
    time = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    temp = str(request.json['Tempr'])
    light = str(request.json['Light'])
    co2 = str(request.json['eCO2'])
    moisture = str(request.json['Humid'])
    #data = []
    data = [temp,light,moisture,co2]
    new_entry = MBedData(date ,time, data)
    db.session.add(new_entry)
    db.session.commit()
    return user_schema.jsonify(new_entry)

# endpoint to show all users
@app.route("/data", methods=["GET"])
def get_user():
    all_data = MBedData.query.all()
    result = users_schema.dump(all_data)
    return jsonify(result.data)

# endpoint to get user detail by id
@app.route("/data/<date>", methods=["GET"])
def user_detail(date):
    data_points = MBedData.query.filter_by(date=str(date)).all()
    return jsonify(data=[e.serialize() for e in data_points])

@app.route("/data", methods=["DELETE"])
def user_delete():
    info =  MBedData.query.delete()
    db.session.commit()
    return info

if __name__ == '__main__':
    app.run(debug=True)
