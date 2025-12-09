from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OAuthViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("oauth", OAuthViewSet, basename="oauth")

urlpatterns = router.urls
