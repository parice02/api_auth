from rest_framework import serializers

from .models import CustomUser


class ExtendedUserSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        """
        @override: must call create_user for authorization token system to function appropriately
        """
        return CustomUser.objects.create_user(**validated_data)


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
