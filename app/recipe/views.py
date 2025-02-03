"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View por manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    # queryset represents the objects that are available for this ViewSet,
    # since a ViewSet is expected to work with a model.
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]  # Tells Django to use TokenAuthentication for this view.
    permission_classes = [IsAuthenticated]  # Tells Django to use IsAuthenticated for this view.

    # We override the get_queryset method to return only the recipes that belong to the authenticated user.
    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        auth_user = self.request.user  # Retrieve the authenticated user.
        return self.queryset.filter(user=auth_user).order_by('-id')
