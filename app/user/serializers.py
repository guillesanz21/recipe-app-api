"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Extra keyword arguments to control how the serializer is used.
        # write_only=True means that the password is only used for creating objects and not for retrieving objects.
        # (we don't want to retrieve the password in the response).
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)

    # instance is the model instance that is being updated.
    # validated_data is the data that is being used to update the instance.
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it."""
        # pop() removes the password from the validated_data dictionary.
        # We don't force the client to update the password every time they update the user.
        password = validated_data.pop('password', None)
        # Call the parent class update() method to update the user.
        user = super().update(instance, validated_data)

        # If the client is updating the password, then set the password and save the user.
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        # Optional, but it makes the input field a password field in the browsable API.
        style={'input_type': 'password'},
        # This is to allow for leading and trailing whitespace in the password.
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
