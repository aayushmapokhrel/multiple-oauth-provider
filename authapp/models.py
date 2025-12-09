from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_location = models.CharField(max_length=200, blank=True, null=True)


class OAuthAccount(models.Model):
    PROVIDERS = (
        ("google", "google"),
        ("facebook", "facebook"),
        ("github", "github"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="oauth")
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    uid = models.CharField(max_length=200)

    class Meta:
        unique_together = ("provider", "uid")


class BackupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)


class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=200)
    ip = models.GenericIPAddressField()
    location = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
