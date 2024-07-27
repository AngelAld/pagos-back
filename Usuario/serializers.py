from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "is_active": {"read_only": True},
        }

    @atomic
    def create(self, validated_data):
        email = validated_data.get("username")
        password = validated_data.get("password", None)

        if not password:
            raise serializers.ValidationError({"password": "This field is required."})
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        user = User.objects.create_user(**validated_data, email=email, is_active=False)
        return user

    @atomic
    def update(self, instance, validated_data):
        _ = validated_data.pop("password", None)
        return super().update(instance, validated_data)


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = self.context["request"].user
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Incorrect password"})

        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return data
