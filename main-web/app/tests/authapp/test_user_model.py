from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class TestUserModel(TestCase):
    def setUp(self):
        # Create a user with a plain-text password
        self.email = 'testuser@n.com'
        self.plain_password = 'testpassword'
        self.user = User.objects.create_user(email=self.email, password=self.plain_password)

    def test_password_hashed(self):
        # Check that the password is hashed
        self.assertNotEqual(self.user.password, self.plain_password)

    def test_check_password(self):
        # Verify that the user can log in with the correct password
        self.assertTrue(self.user.check_password(self.plain_password))
        self.assertFalse(self.user.check_password('wrongpassword'))
