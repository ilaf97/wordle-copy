import os
import unittest
from unittest.mock import patch
from flask import Flask
from app import create_test_app
import src
from src.model.userModel import User
from src.service.userService import UserService
from src import db
from tests.fixtures.load_fixture_data import get_fixtures, load_user_fixture_data
from src.utils.exceptions import DatabaseError

class TestUserService(unittest.TestCase):

    user_service = UserService()

    def setUp(self) -> None:
        app = create_test_app()
        self.fixture_data = get_fixtures('users')
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        User.query.delete()
        # load_user_fixture_data(db)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch.object(src, 'db', db)
    def test_add_user_succeeds(self) -> None:
        user_to_add = self.fixture_data[0]['records'][0]
        result = self.user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
        )
        user_obj = db.session.query(User).order_by(User.id.asc()).first()
        self.assertIsNotNone(user_obj)
        if user_obj is not None:
            self.assertEqual(user_to_add['email'], user_obj.email)
            self.assertEqual(user_to_add['username'], user_obj.username)
            # Ensures password has been hashed
            self.assertNotEqual(user_to_add['password'], user_obj.password)

    @patch.object(src, 'db', db)
    @patch('src.service.userService.db.session.add')
    def test_add_user_fails(self, mock_db_add) -> None:
        user_to_add = self.fixture_data[0]['records'][1]
        mock_db_add.side_effect = Exception('Bad operation')
        with self.assertRaises(DatabaseError):
            self.user_service.add_user(
                email=user_to_add['email'],
                username=user_to_add['username'],
                password=user_to_add['password']
            )
        mock_db_add.assert_called_once()
        user_obj = db.session.query(User).order_by(User.id.asc()).first()
        self.assertIsNone(user_obj)



    def test_check_credentials_correct(self) -> None:
        user_to_add = self.fixture_data[0]['records'][1]
        self.user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
        )
        result = self.user_service.check_credentials(
            email=user_to_add['email'],
            password=user_to_add['password']
        )
        self.assertTrue(result)
        User.query.delete()


    def test_check_credentials_email_incorrect(self) -> None:
        user_to_add = self.fixture_data[0]['records'][1]
        self.user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
        )
        result = self.user_service.check_credentials(
            email="this_is_not_a_real_email",
            password=user_to_add['password']
        )
        self.assertFalse(result)
        User.query.delete()
    
    def test_check_credentials_password_incorrect(self) -> None:
        user_to_add = self.fixture_data[0]['records'][1]
        self.user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
        )
        result = self.user_service.check_credentials(
            email=user_to_add['email'],
            password="_________"
        )
        self.assertFalse(result)
        User.query.delete()

    def test_get_user_by_email(self) -> None:
        user_to_add = self.fixture_data[0]['records'][1]
        self.user_service.add_user(
            email=user_to_add['email'],
            username=user_to_add['username'],
            password=user_to_add['password']
        )
        user_obj = self.user_service.get_user_by_email(
            email=user_to_add['email'],
        )
        self.assertIsNotNone(user_obj)
        if user_obj is not None:
            self.assertEqual(user_to_add['email'], user_obj.email)
            self.assertEqual(user_to_add['username'], user_obj.username)
            # Ensures password has been hashed
            self.assertNotEqual(user_to_add['password'], user_obj.password)
        User.query.delete()

    

        