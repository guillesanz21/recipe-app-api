"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# The BaseUserManager class is a helper class that Django provides that we can use to create a user or superuser
# It provides some helper functions that make it easier to work with our custom user model
class UserManager(BaseUserManager):
  """Manager for user."""

  def create_user(self, email, password=None, **extra_fields):
    """Create, save and return a new user."""

    if not email:
      raise ValueError('Users must have an email address')

    # self.model is a reference to the model that the manager is for (User)
    # normalize_email is a helper function that comes with the BaseUserManager
    # that will normalize the email address (i.e. make the domain part all lower case)
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password) # encrypts the password
    user.save(using=self._db) # supports multiple databases

    return user

# The User model is a custom model that we are creating that will inherit from:
#  - The AbstractBaseUser class provides the core implementation of a User model, including hashed passwords and tokenized password resets
#  - The PermissionsMixin class is a helper class that adds the fields and methods necessary to support Django's Group and Permission model
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # objects is a UserManager object that we will use to manage the User model
    objects = UserManager()

    # USERNAME_FIELD is a constant that we can set on the User model to specify the field that we want to use as the unique identifier for the user
    USERNAME_FIELD = 'email'