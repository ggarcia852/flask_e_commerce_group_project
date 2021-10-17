from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    items = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username=username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    skill= db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image= db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    order =db.relationship('Cart', backref='item', lazy=True)
    

    def __init__(self, color, skill, description, image, price):
        self.color = color
        self.skill = skill
        self.description = description
        self.image = image
        self.price = price


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    hours = db.Column(db.Integer)
    