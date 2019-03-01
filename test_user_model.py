"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, FollowersFollowee

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
HASHED_PASSWORD = "$2b$12$sPCpn3/c7WAd623GKiGNWesVRaZCdTsQlBGBILA9QYsJHbpCFA5lW"
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

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.u1 = User(
            id=1000,
            email="test@test.com",
            username="testuser",
            password=HASHED_PASSWORD
        )

        db.session.add(self.u1)
        db.session.commit()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)


    def test_repr(self):
        """ Does the repr work as intended? """

        self.assertEqual(str(self.u1), "<User #1000: testuser, test@test.com>")


    def test_is_following(self):
        """ Does is_following successfully detect when user1 is following user2 and when user2 is not following user1? """

        u2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        f = FollowersFollowee(followee_id=1000, follower_id=2000)
        
        db.session.add(f)
        db.session.commit()

        self.assertTrue(self.u1.is_following(u2))
        self.assertFalse(u2.is_following(self.u1))


    def test_is_followed_by(self):
        """ Does is_followed_by successfully detect when user1 is followed by user2 and when user2 is not followed by user1? """

        u2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        f = FollowersFollowee(followee_id=2000, follower_id=1000)
        
        db.session.add(f)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(self.u1))


    def test_user_create(self):
        """ Does User.create successfully create a new user given valid credentials and fail if validations fail? """
        self.assertIs(User.query.get(1000), self.u1)

        # same email
        u2 = User(
            id=2000,
            email="test@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        # same username
        u3 = User(
            id=3000,
            email="test2@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        # no password
        u4 = User(
            id=4000,
            email="test2@test.com",
            username="testuser"
        )

        db.session.add(u2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        db.session.add(u3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        db.session.add(u4)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()


    def test_user_auth(self):
        """ Does User.authenticate successfully return a user when given a valid username and password and fail if username/password are invalid? """


        self.assertIs(User.authenticate(username="testuser", password="123456"), self.u1)
        self.assertFalse(User.authenticate(username="testuser2", password="123456"))
        self.assertFalse(User.authenticate(username="testuser", password="12345"))        