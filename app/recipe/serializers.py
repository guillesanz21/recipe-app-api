"""
Serializers for recipe APIs.
"""
from rest_framework import serializers

from core.models import Recipe, Tag


# * TAG SERIALIZERS
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


# * RECIPE SERIALIZERS
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new recipe."""
        tags = validated_data.pop('tags', [])  # Remove tags from validated data.
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user  # We get the authenticated user to create the tags.
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)  # Create the tag object.
            recipe.tags.add(tag_obj)  # Add the tag to the recipe object.
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detaail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
