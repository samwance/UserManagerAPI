from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "full_name"]
        extra_kwargs = {"full_name": {"write_only": True}}
