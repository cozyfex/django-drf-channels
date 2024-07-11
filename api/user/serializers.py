from rest_framework import serializers

from core.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'name',
            'is_active',
            'is_staff',
            'date_joined',
        )
