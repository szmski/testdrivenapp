import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justatest', 'test@gmail.com', 'greaterthaneight')

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.active)

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'greaterthaneight')
        user_two = add_user('justatest2', 'test@test2.com', 'greaterthaneight')

        self.assertNotEqual(user_one.password, user_two.password)

    def test_add_user_duplicate_username(self):
        user = add_user('justatest', 'test@gmail.com', 'greaterthaneight')

        db.session.add(user)
        db.session.commit()

        duplicate_user = User({
            username='justatest',
            email='test@gmail2.com',
            password= 'greaterthaneight'            
        })

        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('justatest', 'test@gmail.com', 'greaterthaneight')

        db.session.add(user)
        db.session.commit()

        duplicate_user = User({
            username='justatest2',
            email='test@gmail.com',
            password= 'greaterthaneight'
        })

        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('justatest', 'test@gmail.com', 'greaterthaneight')

        self.assertTrue(isinstance(user.to_json(), dict))

    if __name__ == "__main__":
        unittest.main()
