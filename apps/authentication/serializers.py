from rest_framework import serializers
# serializers = DRF's tool to validate and convert data

from django.contrib.auth.password_validation import validate_password
# validate_password = Django's built-in password strength checker
# Rejects passwords like "123" or "abc" — too weak
# In real company we always validate password strength

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    # ModelSerializer = automatically creates fields from our User model
    # We don't need to rewrite email, full_name fields — it reads from model

    password = serializers.CharField(
        write_only=True,        # password goes IN but never comes OUT in response
        required=True,
        validators=[validate_password]  # checks password strength automatically
    )
    confirm_password = serializers.CharField(
        write_only=True,        # only for input, never returned in response
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'confirm_password']
        # Only these fields are accepted in the request body
        # id, created_at etc are NOT accepted — they're auto-generated

    def validate(self, data):
        # validate() runs after individual field validation
        # Used to check things that involve MULTIPLE fields together
        # Here we check: do both passwords match?

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
            # This returns a 400 error with the message to the client
        return data

    def create(self, validated_data):
        # create() runs when serializer.save() is called in the view
        # validated_data = clean, validated dictionary of user input

        validated_data.pop('confirm_password')
        # Remove confirm_password — we don't save it to the database
        # pop() removes a key from dictionary and returns its value

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
            # create_user() automatically hashes the password
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    # This serializer is used to SHOW user profile data
    # Only READ — no creating or updating here

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'created_at']
        # We return these fields in the profile response
        # We never return password — even hashed version stays hidden