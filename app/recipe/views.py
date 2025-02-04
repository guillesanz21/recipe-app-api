"""
Views for the recipe APIs.
"""

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    # @action allows us to create custom actions on the view.
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()  # Get the recipe object.
        # We get the serializer, which it will indirectly run through the get_serializer_class class and
        # return the RecipeImageSerializer class.
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# * TAG AND INGREDIENT VIEWSETS
# ! The mixins provide the actions that can be performed on the view.
# The order of the mixins is important.
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()  # What models we want to be managable by this view set.


# Without refactor
# class TagViewSet(mixins.DestroyModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.ListModelMixin,
#                  viewsets.GenericViewSet):
#     """Manage tags in the database."""

#     serializer_class = serializers.TagSerializer
#     queryset = Tag.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Filter queryset to authenticated user."""
#         return self.queryset.filter(user=self.request.user).order_by("-name")

# * IMAGE UPLOAD VIEWSET
