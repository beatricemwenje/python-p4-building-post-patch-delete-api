#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Game, Review, User

# Genre and platform options
genres = [
    "Platformer", "Shooter", "Fighting", "Stealth", "Survival", "Rhythm",
    "Survival Horror", "Metroidvania", "Text-Based", "Visual Novel",
    "Tile-Matching", "Puzzle", "Action RPG", "MMORPG", "Tactical RPG", "JRPG",
    "Life Simulator", "Vehicle Simulator", "Tower Defense", "Turn-Based Strategy",
    "Racing", "Sports", "Party", "Trivia", "Sandbox"
]

platforms = [
    "NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Nintendo Switch",
    "GameBoy", "GameBoy Advance", "Nintendo DS", "Nintendo 3DS",
    "XBox", "XBox 360", "XBox One", "XBox Series X/S",
    "PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation 5",
    "PSP", "PS Vita", "Genesis", "DreamCast", "PC"
]

fake = Faker()

with app.app_context():
    print("Clearing existing data...")
    Review.query.delete()
    Game.query.delete()
    User.query.delete()

    print("Seeding users...")
    users = []
    for _ in range(50):
        user = User(username=fake.user_name())
        users.append(user)
    db.session.add_all(users)

    print("Seeding games...")
    games = []
    for _ in range(50):
        game = Game(
            title=fake.sentence(nb_words=3),
            genre=rc(genres),
            platform=rc(platforms),
            price=randint(10, 60)
        )
        games.append(game)
    db.session.add_all(games)

    print("Seeding reviews...")
    reviews = []
    for user in users:
        for _ in range(randint(1, 5)):  # Each user writes 1 to 5 reviews
            review = Review(
                score=randint(1, 10),
                comment=fake.sentence(),
                user=user,
                game=rc(games)
            )
            reviews.append(review)
    db.session.add_all(reviews)

    db.session.commit()
    print("Database seeded successfully.")
