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

  def test_new_user_email_normalized(self):
    """Test the email for a new user is normalized."""

    sample_emails = [
      ['test1@EXAMPLE.com', 'test1@example.com'],
      ['Test2@Example.com', 'Test2@example.com'],
      ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
      ['test4@example.COM', 'test4@example.com'],
    ]

    for email, expected in sample_emails:
      user = get_user_model().objects.create_user(email, 'sample123')
      self.assertEqual(user.email, expected)
