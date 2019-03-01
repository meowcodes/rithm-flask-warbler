"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from flask import session
from unittest import TestCase

from models import db, connect_db, User, Message

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None)

        db.session.add(self.testuser)
        db.session.commit()

    def test_signup_route(self):
        """Can you add a user?"""

        # can you see the sign in page?
        get_resp = self.client.get("/signup")

        self.assertEqual(get_resp.status_code, 200)
        # find form action and id for signup form
        self.assertIn(b'form method="POST" id="user_form"', get_resp.data)

        # can you make a user?
        post_resp = self.client.post(
            "/signup",
            data={
                "username": "testuser2",
                "email": "test2@test.com",
                "password": "123456",
                "image_url": ""},
            follow_redirects=True)

        # redirects to 200 resp
        self.assertEqual(post_resp.status_code, 200)
        # user info is shown
        self.assertIn(b'alt="Image for testuser2"', post_resp.data)
    
    def test_login_route(self):
        """ Can you log in? """

        # can you see the login page?
        get_resp = self.client.get("/login")

        self.assertEqual(get_resp.status_code, 200)
        # find form action and id for signup form
        self.assertIn(b'form method="POST" id="user_form"', get_resp.data)

        # can you login?
        post_resp = self.client.post(
            "/login",
            data={"username": "testuser",
                  "password": "testuser"},
            follow_redirects=True)

        # redirects to 200 resp
        self.assertEqual(post_resp.status_code, 200)
        # user info is shown
        self.assertIn(b'alt="Image for testuser"', post_resp.data)
        
    def test_log_out(self):
        """ Can you logout? """

        # can you log out?
        resp = self.client.get("/logout", follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        # gets correct flash msg
        self.assertIn(b'Log out successful!', resp.data)