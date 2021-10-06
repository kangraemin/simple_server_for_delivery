from rest_framework import serializers
from .models import UserSearchLog


class UserSearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchLog
        fields = "__all__"
