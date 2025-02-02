"""
Test cases for the models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
  """Test models."""

  def test_create_user_with_email_successful(self):
    """Test creating a new user with an email is successful."""
    email = 'test@example.com'
    password = 'testpass123'
    # get_user_model() is a helper function that retrieves the user model that is active in the project
    # It is recommended to use this helper function instead of importing the user model directly
    # object.create_user() is a helper function that comes with the user model that we are creating
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))