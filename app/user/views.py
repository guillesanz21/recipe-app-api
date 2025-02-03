"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (UserSerializer, AuthTokenSerializer)


# generics.CreateAPIView is a generic view that provides the following features:
# - Create a model instance (POST).
# - Provide a serializer_class attribute, an authentication_classes attribute, and a permission_classes attribute.
class CreateUserView(generics.CreateAPIView):
  """Create a new user in the system."""
  serializer_class = UserSerializer


# generics.RetrieveUpdateAPIView is a generic view that provides the following features:
# - Retrieve a model instance (GET).
# - Update a model instance (PUT and PATCH).
# - Provide a serializer_class attribute, an authentication_classes attribute, a permission_classes attribute, etc.
class ManagerUserView(generics.RetrieveUpdateAPIView):
  """Manage the authenticated user."""
  serializer_class = UserSerializer
  authentication_classes = [authentication.TokenAuthentication]  # Authentication (token based).
  permission_classes = [permissions.IsAuthenticated]  # Authorization (authenticated users only).

  def get_object(self):
    """Retrieve and return authenticated user."""
    return self.request.user  # The user is authenticated, so we can return the user object.


# ObtainAuthToken is a view provided by Django REST framework that allows users to authenticate and receive a token.
class CreateTokenView(ObtainAuthToken):
  """Create a new auth token for user."""
  serializer_class = AuthTokenSerializer  # This is the custom serializer used to validate the user input.
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # Optional: Enables the view in the Django admin site.
