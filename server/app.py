#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Game, User, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Game/Review/User API"

@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()]
    return make_response(games, 200)

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.get(id)
    if game:
        return make_response(game.to_dict(), 200)
    return make_response({"error": "Game not found"}, 404)

@app.route('/users')
def users():
    users = [user.to_dict() for user in User.query.all()]
    return make_response(users, 200)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews, 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_review = Review(
            score=data.get("score"),
            comment=data.get("comment"),
            user_id=data.get("user_id"),
            game_id=data.get("game_id")
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.get(id)
    if not review:
        return make_response({"error": "Review not found"}, 404)

    if request.method == 'GET':
        return make_response(review.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for attr, value in data.items():
            setattr(review, attr, value)
        db.session.commit()
        return make_response(review.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        return make_response({"delete_successful": True, "message": "Review deleted."}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
