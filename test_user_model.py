"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

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

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

# Does the repr method work as expected?

    def test_repr(self):
        """ Does the repr work as intended? """

        u = User(
            id=1000,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        self.assertEqual(str(u), "<User #1000: testuser, test@test.com>")
        
# Does is_following successfully detect when user1 is following user2?
# Does is_following successfully detect when user1 is not following user2?

    def test_is_following(self):
        """ Does is_following successfully detect when user1 is following user2 and when user2 is not following user1 """

        u1 = User(
            id=1000,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        f = FollowersFollowee(followee_id=1000, follower_id=2000)
        
        db.session.add(f)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

# Does is_followed_by successfully detect when user1 is followed by user2?
# Does is_followed_by successfully detect when user1 is not followed by user2?

    def test_is_followed_by(self):
        """ Does is_followed_by successfully detect when user1 is followed by user2 and when user2 is not followed by user1 """

        u1 = User(
            id=1000,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            id=2000,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        f = FollowersFollowee(followee_id=2000, follower_id=1000)
        
        db.session.add(f)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(u1))
        
# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?
