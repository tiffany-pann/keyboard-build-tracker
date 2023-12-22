from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Implement database model classes
class User(db.Model):
    """
    Holds information about a user. Has a one to many relationship with Keyboards.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    keyboards = db.relationship("Keyboard", cascade="delete")

    def __init__(self, **kwargs):
        # Key Word Arguments : Is essentially a dictionary
        self.username = kwargs.get("username", "example username")
        self.password = kwargs.get("password", "example password")
        self.email = kwargs.get("email", "example@example.com")

    def serialize(self):
        """
        Converts User object into a more readable dictionary.
        Serializes a User object.
        """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "keyboards": [keyboard.serialize() for keyboard in self.keyboards],
        }


class Keyboard(db.Model):
    __tablename__ = "keyboards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    switches = db.Column(db.String, nullable=False)
    keycaps = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    # To link to the user, we need to add a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Creates a keyboard object.
        """
        self.name = kwargs.get("name", "Unnamed Keyboard")
        self.switches = kwargs.get("switches", "No switches given")
        self.keycaps = kwargs.get("keycaps", "No keycaps given")
        self.image = kwargs.get("image", "No image given")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serializes a keyboard object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "switches": self.switches,
            "keycaps": self.keycaps,
            "image": self.image,
        }
