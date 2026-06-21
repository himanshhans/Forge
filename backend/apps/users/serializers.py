from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_pro = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "plan", "is_public", "is_pro", "created_at")
        read_only_fields = ("id", "email", "plan", "is_pro", "created_at")
