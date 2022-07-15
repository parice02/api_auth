from rest_framework import serializers

from .models import CustomUser


class ExtendedUserSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = CustomUser
        fields = "__all__"


class SecureUserSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "phone"]


class RestrictedUserSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone"]
