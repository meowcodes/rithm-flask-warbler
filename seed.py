"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import User, Message, FollowersFollowee, Like


db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(FollowersFollowee, DictReader(follows))

like1 = Like(user_id=100, msg_id=97)
like2 = Like(user_id=72, msg_id=17)
like3 = Like(user_id=193, msg_id=97)

db.session.add(like1)
db.session.add(like2)
db.session.add(like3)

db.session.commit()