from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# @cross_origin(supports_credentials=True)

class User(db.Model):
    __tablename__ = 'user'


    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phoneNo = db.Column(db.Integer, nullable=False)
    # password_hash = db.Column(db.String(128))

    def __init__(self, name, email, password, phoneNo):
        self.name = name
        self.email = email
        self.password = password
        self.phoneNo = phoneNo

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

    def json(self):
        return {"userID": self.userID, "name": self.name, "email": self.email, "password": self.password, "phoneNo": self.phoneNo}


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


@app.route("/user/<int:userID>")
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


@app.route("/user", methods=['POST'])
def create_user():

    data = request.get_json()
    print(data)

    # Check if email already exists
    if db.session.query(User).filter_by(email=data.get('email')).first():
        return jsonify({"code": 400, "message": "User with this email already exists."}), 400

    # Create user object
    if data:
            user = User(email=data['email'],phoneNo=data['phoneNo'],password=data['password'],name=data['name'])
 

    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the user."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201


@app.route("/user/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Retrieve the user from the database
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"code": 404,
                        "message": "User not found."}
                    ), 404

    # Update user attributes
    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the user."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

# check user info on login
@app.route('/checkuser', methods=['POST'])
def check_user():
    print(request.json)
    data = request.json  # Assuming you're sending JSON
    email = data['email']
    password = data['password']
    user = db.session.scalars(
    	db.select(User).filter_by(email=email).
    	limit(1)
        ).first()
    print(user.password)
    if user:
        if password == user.password:
            print(user.userID)
            # session["userID"] = user.userID 
            # session["authenticated"] = True
            return jsonify({
            "code": 201,
            "data": user.json()
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401
    # Perform your check or operation here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)