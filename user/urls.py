from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView
from app.views import AuthViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path("api/auth/token/revoke/", TokenBlacklistView.as_view(), name="token_revoke"),
]