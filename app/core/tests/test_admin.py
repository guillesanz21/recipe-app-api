"""
Test for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
  """Tests for Django admin."""

  # * This setUp function is a function that is ran before every test that we run
  def setUp(self):
    """Create user and client, and save it in database."""
    self.client = Client()  # Create a test client that we can use to make requests to our app
    self.admin_user = get_user_model().objects.create_superuser(
      email="admij@example.com",
      password="test123"
    )
    self.client.force_login(self.admin_user)  # Log in the admin user
    self.user = get_user_model().objects.create_user(
      email="user@example.com",
      password="test123",
      name="Test user full name"
    )

  def test_users_listed(self):
    """Test that users are listed on user page."""
    url = reverse("admin:core_user_changelist")  # Generate the URL for our list user page
    res = self.client.get(url)  # Perform an HTTP GET request on the URL

    self.assertContains(res, self.user.name)  # Check that the response contains a certain item
    self.assertContains(res, self.user.email)

  def test_edit_user_page(self):
    """Test the edit user page works."""
    url = reverse("admin:core_user_change", args=[self.user.id])  # Generate the URL for the user edit page
    res = self.client.get(url)  # Perform an HTTP GET request on the URL

    self.assertEqual(res.status_code, 200)  # Check that the response status code is 200

  def test_create_user_page(self):
    """Test the create user page works."""
    url = reverse("admin:core_user_add")  # Generate the URL for the user add page
    res = self.client.get(url)  # Perform an HTTP GET request on the URL

    self.assertEqual(res.status_code, 200)  # Check that the response status code is 200
