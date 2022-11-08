from django import forms
from . import models


class FoodForm(forms.ModelForm):
    class Meta:
        model = models.Food
        fields = [
            "name",
            "image",
            "price",
            "description",
            "status",
            "priority",
            "category",
            "restaurant",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = [
            "image",
            "priority",
            "status",
            "name",
        ]
