from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', backref='game')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "platform": self.platform,
            "price": self.price,
            "reviews": [review.to_dict_basic() for review in self.reviews]
        }

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    reviews = db.relationship('Review', backref='user')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "reviews": [review.to_dict_basic() for review in self.reviews]
        }

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "comment": self.comment,
            "game": self.game.title if self.game else None,
            "user": self.user.username if self.user else None
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "score": self.score,
            "comment": self.comment,
            "game_id": self.game_id,
            "user_id": self.user_id
        }
