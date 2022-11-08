from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register("Food", api.FoodViewSet)
router.register("Category", api.CategoryViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
)
