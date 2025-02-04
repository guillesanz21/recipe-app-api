"""
Serializers for recipe APIs.
"""
from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


# * TAG SERIALIZERS
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


# * INGREDIENT SERIALIZERS
class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


# * RECIPE SERIALIZERS
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as neeeded."""
        auth_user = self.context['request'].user  # We get the authenticated user to create the tags.
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)  # Create the tag object.
            recipe.tags.add(tag_obj)  # Add the tag to the recipe object.

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(user=auth_user, **ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a new recipe."""
        tags = validated_data.pop('tags', [])  # Remove tags from validated data.
        ingredients = validated_data.pop('ingredients', [])  # Remove ingredients from validated data.
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)   # Create the tags, and add them to the instance.
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    # instance: the model instance that is being updated. validated_data: the data that is being updated.
    def update(self, instance, validated_data):
        """Update a recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        # An empty list is not None.
        if tags is not None:
            # Clear all tags from the instance. This will be useful when an empty list is provided.
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)  # Create the tags, and add them to the instance.

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        # Everything outside of the tags is assigned to the instance.
        for attr, value in validated_data.items():
            # setattr is a python built-in function that sets the value of an attribute of an object.
            setattr(instance, attr, value)

        # Save the instance, so that the changes are reflected in the database.
        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detaail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Recipe  # The model that we are going to use.
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
