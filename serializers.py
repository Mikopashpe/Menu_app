from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from utils.images import get_thumb
from . import models


class FoodSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        cache_image_url = get_thumb(obj.image, '50x50', crop='center')
        return request.build_absolute_uri(cache_image_url)

    class Meta:
        model = models.Food
        fields = [
            "name",
            "image",
            "price",
            "status",
            "priority",
            "description",
            "created",
            "last_updated",

        ]


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        cache_image_url = get_thumb(obj.image, '50x50', crop='center')
        return request.build_absolute_uri(cache_image_url)

    class Meta:
        model = models.Category
        fields = [
            'id',
            "name",
            "image",
            "priority",
            "status",
        ]
