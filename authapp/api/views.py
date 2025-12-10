from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from authapp.models import User, OAuthAccount
from authapp.api.serializers import (
    UserSerializer,
    OAuthAccountSerializer,
    LoginActivitySerializer,
    SignupSerializer,
    LoginSerializer,
)
from authapp.utils import send_verification_email, send_otp


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email(user)
        return Response({"status": "verification_sent"})

    @action(detail=False, methods=["post"])
    def verify(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()  # safer than get()
        if not user:
            return Response({"status": "user not found"}, status=404)

        user.email_verified = True
        user.save()
        return Response({"status": "verified"})

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "invalid credentials"}, status=400)

        if not user.email_verified:
            return Response({"error": "email not verified"}, status=400)

        if user.two_factor_enabled:
            otp = send_otp(user)
            return Response({"2fa": "otp_sent"})

        return Response({"login": "success", "user": UserSerializer(user).data})

    @action(detail=True, methods=["post"])
    def enable_2fa(self, request, pk=None):
        user = self.get_object()
        user.two_factor_enabled = True
        user.save()
        return Response({"2fa": "enabled"})

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        user = self.get_object()
        data = {
            "user": UserSerializer(user).data,
            "linked": OAuthAccountSerializer(user.oauth.all(), many=True).data,
            "logins": LoginActivitySerializer(
                user.loginactivity_set.all(), many=True
            ).data,
        }
        return Response(data)


class OAuthViewSet(ModelViewSet):
    queryset = OAuthAccount.objects.all()
    serializer_class = OAuthAccountSerializer

    @action(detail=False, methods=["post"])
    def link(self, request):
        obj = OAuthAccount.objects.create(
            user_id=request.data["user"],
            provider=request.data["provider"],
        )
        return Response(OAuthAccountSerializer(obj).data)
