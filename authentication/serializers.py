from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import AuthenticationFailed



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['full_name'] = self.user.full_name
            data['role'] = self.user.role
            return data
        except AuthenticationFailed as e:
            raise AuthenticationFailed("Invalid credentials")
        except Exception as e:
            raise AuthenticationFailed(e)

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            return data
        except AuthenticationFailed as e:
            raise AuthenticationFailed("Invalid refresh token")
        except Exception as e:
            raise AuthenticationFailed(e)