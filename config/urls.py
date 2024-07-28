from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
