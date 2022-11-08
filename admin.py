from django.contrib import admin
from django.utils.safestring import mark_safe
from image_cropping.templatetags.cropping import cropped_thumbnail
from sorl.thumbnail import get_thumbnail
from image_cropping import ImageCroppingMixin
from utils.images import get_thumb
from . import models
from .models import Category, Food, Additive, Modification, FoodModifierSet


@admin.action(description='Сделать категорию неактивной')
def make_category_status_inactive(model_admin, request, queryset):
    queryset.update(status=False)


@admin.action(description='Сделать категорию активной')
def make_category_status_active(model_admin, request, queryset):
    queryset.update(status=True)


class FoodModifierSetInline(admin.TabularInline):
    model = FoodModifierSet


class ModificationInline(admin.TabularInline):
    model = Modification


class AdditiveInline(admin.TabularInline):
    model = Additive.foods.through


@admin.register(models.Additive)
class AdditiveAdmin(ImageCroppingMixin, admin.ModelAdmin):
    def image_logo(self, obj):
        cache_image_url = get_thumb(obj.final_image, '100x100', crop='center')
        return mark_safe(f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="100"/></a>')

    image_logo.short_description = "Фото"
    image_logo.allow_tags = True

    def image_card(self, obj):
        cache_image_url = get_thumb(obj.final_image, '250x250', crop='center')
        return mark_safe(
            f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="250"/></a>')

    image_card.short_description = "Фото"
    image_card.allow_tags = True

    readonly_fields = ['image_logo', 'image_card', ]
    list_display = [
        "name",
        'image_logo',
        'price',
        'weight'
    ]
    fieldsets = (
        (None, {'fields': (
            "name",
            'image',
            'cropping',
            'image_card',
            'description',
            'price',
            'weight',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'image', 'cropping', 'image_card', 'description', 'price', 'weight'),
        }),
    )


@admin.register(models.Food)
class FoodAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "restaurant",
        "category",
        "image_logo",
        "price",
        "status",
        "priority",
        'pay_term'
    ]

    def image_logo(self, obj):
        cache_image_url = get_thumb(obj.final_image, '100x100', crop='center')
        return mark_safe(f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="100"/></a>')

    image_logo.short_description = "Фото"
    image_logo.allow_tags = True

    def image_card(self, obj):
        cache_image_url = get_thumb(obj.final_image, '250x250', crop='center')
        return mark_safe(
            f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="250"/></a>')

    image_card.short_description = "Фото"
    image_card.allow_tags = True

    readonly_fields = ['image_logo', 'image_card', ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',
                       'restaurant',
                       'category',
                       'image',
                       'cropping',
                       'image_card',
                       'price',
                       'status',
                       'priority',
                       'pay_terms'),
        }),
    )

    fieldsets = (
        (None, {'fields': (
            'name', 'restaurant', 'category', 'image', 'cropping', 'image_card', 'price', 'status', 'priority',
            'pay_term')}),
    )
    list_filter = ('name', 'restaurant', 'category', 'status',)
    inlines = [AdditiveInline, FoodModifierSetInline]


@admin.register(Category)
class AdminCategory(ImageCroppingMixin, admin.ModelAdmin):

    def image_logo(self, obj):
        cache_image_url = get_thumb(obj.final_image, '100x100', crop='center')
        return mark_safe(f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="100"/></a>')

    image_logo.short_description = "Фото"
    image_logo.allow_tags = True

    def image_card(self, obj):
        cache_image_url = get_thumb(obj.final_image, '250x250', crop='center')
        return mark_safe(
            f'<a href="{cache_image_url}" target="_blank"><img src="{cache_image_url}" width="250"/></a>')

    image_card.short_description = "Фото"
    image_card.allow_tags = True

    readonly_fields = ['image_card']

    fieldsets = (
        (None, {'fields': ('name', 'priority', 'image', 'cropping', 'image_card', 'status',)}),  # 'image_card',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'status', 'image', 'cropping', 'image_card', 'priority',),  # 'image_card',
        }),
    )
    list_filter = ('name', 'status',)
    #
    list_editable = (
        'priority',
    )
    list_display = ('name', 'image_logo', 'priority', 'status',)  # 'image_logo'


admin.site.register(models.Modification)
