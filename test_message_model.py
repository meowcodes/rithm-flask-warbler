# Test likes relaSHAWNSHAIP

"""Message model tests."""

# run these tests like:
#
# python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError, DataError
from datetime import datetime
from models import db, User, Message, FollowersFollowee, Like


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
HASHED_PASSWORD = "$2b$12$sPCpn3/c7WAd623GKiGNWesVRaZCdTsQlBGBILA9QYsJHbpCFA5lW"
LOREM_IPSUM_REG = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
LOREM_IPSUM_LONG = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."
# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        Like.query.delete()
        Message.query.delete()
        User.query.delete()

        self.u1 = User(
            id=1000,
            email="test@test.com",
            username="testuser",
            password=HASHED_PASSWORD
        )

        self.m1 = Message(
           id=1000001,
           text=LOREM_IPSUM_REG,
           user_id=1000
        )

        db.session.add(self.u1)
        db.session.add(self.m1)

        db.session.commit()

        # self.client = app.test_client()

    def test_message_model(self):
        """Does basic message model work?"""

        m20 = Message(
           id=1000020,
           text=LOREM_IPSUM_REG,
           user_id=1000
        )

        db.session.add(m20)
        db.session.commit()
        m10 = Message.query.get(1000020)

        self.assertEqual(self.m1.user_id, 1000)
        self.assertIsInstance(self.m1.timestamp, datetime)
        self.assertIs(m20, m10)


    def test_repr(self):
        """ Does the repr work as intended? """

        self.assertEqual(str(self.m1), "<Message #1000001: authored by 1000>")


    def test_is_liked(self):
        """ Does is_liked successfully detect when a user has liked a message? """


        l1 = Like(user_id=1000,
                  msg_id=1000001)

        db.session.add(l1)
        db.session.commit()

        u2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        self.assertTrue(self.m1.is_liked(self.u1))
        self.assertFalse(self.m1.is_liked(u2))

    def test_likes_relationship(self):
        """ tests if the likes relationship is functional """

        l1 = Like(user_id=1000,
                  msg_id=1000001)

        db.session.add(l1)
        db.session.commit()


        self.assertEqual(self.m1.likes, [l1])


    def test_author_relationship(self):
        """ Does message.author find the correct instance of user? """

        self.assertIs(self.m1.author, self.u1)

    def test_message_create(self):
        """ Does the model successfully create new messages that follow the constraints? """

        # txt too long
        m2 = Message(
           id=1000002,
           text=LOREM_IPSUM_LONG,
           user_id=1000
        )

        # no text
        m3 = Message(
           id=1000003,
           user_id=1000
        )

        db.session.add(m2)
        self.assertRaises(DataError, db.session.commit)
        db.session.rollback()

        db.session.add(m3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
