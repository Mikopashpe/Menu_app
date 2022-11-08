from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import urllib.parse
from django.db.models import Model
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from image_cropping import ImageRatioField, ImageCropField
from image_cropping.templatetags.cropping import cropped_thumbnail
from smart_selects.db_fields import ChainedForeignKey

MODIFIERS_CHOICE = (
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large')
)


class Food(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=250, blank=False, null=False)

    # Relationships
    restaurant = models.ForeignKey("organization.Restaurant", verbose_name='Ресторан', on_delete=models.CASCADE,
                                   related_query_name='foods')
    category = models.ForeignKey("menu.Category", verbose_name='Категория', on_delete=models.DO_NOTHING, null=True,
                                 blank=True)
    additives = models.ManyToManyField('menu.Additive', verbose_name="Добавки", blank=True)
    discounts = models.ManyToManyField('stock.Discount', verbose_name='Блюдо со скидкой', blank=True)
    base_dish_as_a_gift = models.ManyToManyField('stock.DishAsAGift', verbose_name='Основное блюдо', blank=True,
                                                 related_name='food_base_dish_as_a_gift')
    dish_as_a_gifts = models.ManyToManyField('stock.DishAsAGift', verbose_name='Блюдо в подарок', blank=True)
    food_birthday_gifts = models.ManyToManyField('stock.BirthdayGift', verbose_name='Блюдо в подарок', blank=True)
    birthday_foods = models.ManyToManyField('stock.BirthdayGift', verbose_name='Основное блюдо', blank=True,
                                            related_name='food_for_birthday_gift')
    combos = models.ManyToManyField('stock.Combo', verbose_name='Блюдо дя комбо', blank=True)
    pay_term = ChainedForeignKey('paygate.PayTerm', verbose_name='Правил оплаты', null=True, blank=True,
                                 chained_field="restaurant",
                                 chained_model_field="restaurant",
                                 show_all=False,
                                 auto_choose=False,
                                 sort=True, on_delete=models.DO_NOTHING)
    # Fields
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    status = models.BooleanField(verbose_name="Статус (активный)", default=True)
    image = ImageCropField(verbose_name="Изображение", upload_to="upload/images/food/", blank=True, null=True,
                           max_length=250)
    final_image = models.ImageField(verbose_name="Изображение (после обработки)", upload_to="upload/images/food/",
                                    blank=True, null=True, max_length=250)
    cropping = ImageRatioField('image', '200x200', verbose_name="Редактирование")
    priority = models.PositiveIntegerField(verbose_name='Приоритет', default=1, null=False, blank=False,
                                           validators=[MaxValueValidator(20), MinValueValidator(1)])
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    weight = models.PositiveIntegerField(verbose_name="Вес", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("menu_Food_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("menu_Food_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Food.objects.filter(pk=self.pk).first()
            if self.cropping != original.cropping:
                cropped_image_url = cropped_thumbnail({}, self, 'cropping')
                self.final_image = urllib.parse.unquote(cropped_image_url.lstrip('/').lstrip(settings.MEDIA_URL))
        super().save(*args, **kwargs)


class Category(models.Model):
    discounts = models.ManyToManyField('stock.Discount', verbose_name='Категории со скидкой', blank=True)
    # Fields
    name = models.CharField(verbose_name="Наименование", max_length=200, null=False, blank=False)
    image = ImageCropField(verbose_name="Изображение", upload_to="upload/images/category/", blank=True, null=True,
                           max_length=250)
    final_image = models.ImageField(verbose_name="Изображение (после обработки)", upload_to="upload/images/category/",
                                    blank=True, null=True, max_length=250)
    cropping = ImageRatioField('image', '200x200', verbose_name="Редактирование")
    priority = models.PositiveIntegerField(verbose_name='Приоритет', default=1, null=False, blank=False,
                                           validators=[MaxValueValidator(20), MinValueValidator(1)])
    status = models.BooleanField(verbose_name="Статус (активный)", default=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("menu_Category_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("menu_Category_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if self.pk is not None:
            original = Category.objects.filter(pk=self.pk).first()
            if self.cropping != original.cropping:
                cropped_image_url = cropped_thumbnail({}, self, 'cropping')
                self.final_image = urllib.parse.unquote(cropped_image_url.lstrip('/').lstrip(settings.MEDIA_URL))
        super().save(*args, **kwargs)


class Additive(models.Model):
    foods = models.ManyToManyField('menu.Food', verbose_name="Блюда", blank=True, through=Food.additives.through)

    name = models.CharField(max_length=50, verbose_name='Наименование добавки')
    image = ImageCropField(verbose_name="Изображение", upload_to="upload/images/additive/", blank=True, null=True,
                           max_length=250)
    final_image = models.ImageField(verbose_name="Изображение (после обработки)", upload_to="upload/images/additive/",
                                    blank=True, null=True, max_length=250)
    cropping = ImageRatioField('image', '200x200', verbose_name="Редактирование")
    description = models.TextField(verbose_name="Описание добавки", blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    weight = models.PositiveIntegerField(verbose_name="Вес", blank=True, null=True)

    class Meta:
        verbose_name = 'Добавка'
        verbose_name_plural = 'Добавки'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("menu_Additive_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("menu_Additive_update", args=(self.pk,))

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Additive.objects.filter(pk=self.pk).first()
            if self.cropping != original.cropping:
                cropped_image_url = cropped_thumbnail({}, self, 'cropping')
                self.final_image = urllib.parse.unquote(cropped_image_url.lstrip('/').lstrip(settings.MEDIA_URL))
        super().save(*args, **kwargs)


class Modification(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование модификации')
    type = models.CharField(verbose_name="Тип модификатора", max_length=30, blank=True, choices=MODIFIERS_CHOICE)

    class Meta:
        verbose_name = 'Модификатор'
        verbose_name_plural = 'Модификаторы'

    def __str__(self):
        return str(self.name)


class FoodModifierSet(models.Model):
    food = models.ForeignKey('menu.Food', verbose_name="Блюдо", blank=True,
                             on_delete=models.DO_NOTHING)
    modification = models.ForeignKey('menu.Modification', verbose_name='Модификатор', null=True, blank=True,
                                     on_delete=models.DO_NOTHING)

    weight = models.PositiveIntegerField(verbose_name="Вес (гр)", blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Модификатор блюда'
        verbose_name_plural = 'Модификаторы блюд'

    def __str__(self):
        return str(self.modification)
