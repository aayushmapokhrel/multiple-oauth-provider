from rest_framework import serializers
from authapp.models import User, OAuthAccount, LoginActivity


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "email_verified", "two_factor_enabled"]

    def validate_email(self, value):
        # If user is updating their own email, allow same value
        request = self.context.get("request")

        if request and request.method in ("PUT", "PATCH"):
            current_user = request.user
            if current_user and current_user.email == value:
                return value

        # Unique email check
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")

        return value


class OAuthAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthAccount
        fields = "__all__"


class LoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = "__all__"
