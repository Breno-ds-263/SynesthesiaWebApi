from rest_framework import serializers
from .models import Admin

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ('username', 'email', 'name', 'password')

    def create(self, validated_data):
        user = Admin.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return Admin
