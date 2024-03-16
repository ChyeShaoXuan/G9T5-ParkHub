from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/user"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'


    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phoneNo = db.Column(db.Integer, nullable=False)
    notifAllowed = db.Column(db.Boolean, default=False)


    def __init__(self, userID, name, email, password, phoneNo, notifAllowed):
        self.userID = userID
        self.name = name
        self.email = email
        self.password = password
        self.phoneNo = phoneNo
        self.notifAllowed = notifAllowed


    def json(self):
        return {"userID": self.userID, "name": self.name, "email": self.email, "password": self.password, "phoneNo": self.phoneNo, "notifAllowed": self.notifAllowed}


@app.route("/user")
def get_all():
    userlist = db.session.scalars(db.select(User)).all()


    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

@app.route("/user/<integer:userID>")
def find_by_userID(userID):
    user = db.session.scalars(
    	db.select(User).filter_by(userID=userID).
    	limit(1)
).first()


    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404

@app.route("/user/<integer:userID>", methods=['POST'])
def create_user(userID):
    if (db.session.scalars(
    	db.select(User).filter_by(userID=userID).
    	limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userID": userID
                },
                "message": "User already exists."
            }
        ), 400


    data = request.get_json()
    user = User(userID, **data)


    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID
                },
                "message": "An error occurred creating the user."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201


@app.route("/user/<integer:userID>", methods=['POST'])
def create_user(userID):
    if (db.session.scalars(
    	db.select(User).filter_by(userID=userID).
    	limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userID": userID
                },
                "message": "User already exists."
            }
        ), 400


    data = request.get_json()
    user = User(userID, **data)


    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID
                },
                "message": "An error occurred creating the user."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)