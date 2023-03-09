from . import db
from werkzeug.security import generate_password_hash

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
        
    def __repr__(self):
        return '<User %r>' % (self.username)

class PropertyProfile(db.Model):
    __tablename__ = 'property_profiles'
    property_id = db.Column(db.Integer, primary_key=True)
    property_title = db.Column(db.String(255), unique=True)
    property_description = db.Column(db.Text())
    number_room = db.Column(db.Integer)
    number_bathroom = db.Column(db.Integer)
    property_price = db.Column(db.Integer)
    property_type = db.Column(db.String(80))
    property_location = db.Column(db.String(255))
    property_photo = db.Column(db.String(255)) #To be completed

    def __init__(self, property_title, property_description, number_room, number_bathroom, property_price, property_type, property_location, property_photo):
        self.property_title = property_title
        self.property_description = property_description
        self.number_room = number_room
        self.number_bathroom = number_bathroom
        self.property_price = property_price
        self.property_type = property_type
        self.property_location = property_location
        self.property_photo = property_photo

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
        
    def __repr__(self):
        return '<User %r>' % (self.username)