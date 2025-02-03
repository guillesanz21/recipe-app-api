"""
Views for the recipe APIs.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


# * RECIPE VIEWSET
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    # queryset represents the objects that are available for this ViewSet,
    # since a ViewSet is expected to work with a model.
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]  # Tells Django to use TokenAuthentication for this view.
    permission_classes = [IsAuthenticated]  # Tells Django to use IsAuthenticated for this view.

    # We override the get_queryset method to return only the recipes that belong to the authenticated user.
    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        auth_user = self.request.user  # Retrieve the authenticated user.
        return self.queryset.filter(user=auth_user).order_by("-id")

    # We override the get_serializer_class method to return the appropriate serializer class for the request.
    # We need different serializers for list and detail views, for example.
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


# * TAG VIEWSET
class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
