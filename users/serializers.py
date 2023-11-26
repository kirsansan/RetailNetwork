from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'last_name')
        # exclude = ('password', 'last_name')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'phone', 'country', 'avatar', 'last_name', 'telegram_username')


class FullDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """ there I try to save password in encrypted-mode"""
        print("Creating")
        print(validated_data)
        user = User.objects.create_user(**validated_data)  # we rewrote this method in CustomUserManager
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adding user-fields in token
        # token['username'] = user.username
        token['email'] = user.email
        return token
