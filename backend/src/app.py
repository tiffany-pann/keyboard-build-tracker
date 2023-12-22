import json, os
from flask import Flask, request
from db import db, User, Keyboard

db_file = "keyboards.db"
app = Flask(__name__)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return f"Hello, {os.environ.get('NAME')}"


def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(error, code=404):
    return json.dumps({"error": error}), code


@app.route("/users/", methods=["GET"])
def get_users():
    """Endpoint for getting all users"""
    # User.query.all() is the equivalent to the SQL vers of select * from users
    users = [user.serialize() for user in User.query.all()]

    return success_response({"users": users})


@app.route("/users/<int:user_id>/", methods=["GET"])
def get_specific_user(user_id):
    """Endpoint for getting a single user"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())


@app.route("/users/", methods=["POST"])
def create_user():
    """Endpoint for creating a user"""
    body = json.loads(request.data)
    user = User(
        username=body.get("username"),
        password=body.get("password"),
        email=body.get("email"),
    )
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)


## For keyboards
@app.route("/users/<int:user_id>/keyboards/", methods=["GET"])
def get_keyboards(user_id):
    """Endpoint for getting all keyboards for a user"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(
        {"keyboards": [keyboard.serialize() for keyboard in user.keyboards]}
    )


@app.route("/users/<int:user_id>/keyboards/", methods=["POST"])
def add_keyboard(user_id):
    """Endpoint for adding a keyboard for a user"""
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found!")
    keyboard = Keyboard(
        name=body.get("name"),
        switches=body.get("switches"),
        keycaps=body.get("keycaps"),
        image=body.get("image"),
        user_id=user_id,
    )

    db.session.add(keyboard)
    db.session.commit()

    return success_response(keyboard.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
