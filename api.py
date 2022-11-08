from rest_framework import viewsets, permissions, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from . import serializers
from . import models
from organization.models import Restaurant


class FoodViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """ViewSet for the Food class"""

    queryset = models.Food.objects.filter(status=True)
    serializer_class = serializers.FoodSerializer
    permission_classes = []  # [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if not self.action == 'list':
            return self.queryset
        location_id = self.request.query_params.get('location_id')
        restaurant_id = self.request.query_params.get('restaurant_id')
        category_id = self.request.query_params.get('category_id')
        if restaurant_id:
            qs = self.queryset.filter(restaurant_id=restaurant_id)
        else:
            restaurant_ids = Restaurant.objects.filter(location_id=location_id).values_list('id', flat=True)
            qs = self.queryset.filter(restaurant_id__in=restaurant_ids)
        if category_id:
            qs = qs.filter(category_id=category_id)
        return self.paginate_queryset(qs)


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """ViewSet for the Category class"""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = []  # [permissions.IsAuthenticated]
