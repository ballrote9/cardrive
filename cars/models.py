from django.db import models
from django.utils.text import slugify
from datetime import date
from users.models import Users

class Designers(models.Model):
    designer_name = models.CharField(max_length=15, unique=True, null=False, verbose_name="Название производителя")

    def __str__(self) -> str:
        return self.designer_name

class Carcases(models.Model):
    carcase_name = models.CharField(max_length=15, unique=True, verbose_name="Название кузова")

    def __str__(self) -> str:
        return self.carcase_name

class CarModels(models.Model):
    designer = models.ForeignKey(Designers, on_delete=models.PROTECT, verbose_name="Производитель")
    model_name = models.CharField(max_length=15, unique=True, verbose_name="Модель")

    def __str__(self) -> str:
        return self.model_name

class CarInstances(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='cars_images', blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name="Цена")
    designer = models.ForeignKey(Designers, on_delete=models.PROTECT, verbose_name="Производитель")
    model = models.ForeignKey(CarModels, on_delete=models.PROTECT, related_name='models', verbose_name="Название модели")
    carcase = models.ForeignKey(Carcases, on_delete=models.PROTECT, verbose_name="Кузов")
    power = models.IntegerField(verbose_name="Лошадиные силы")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.designer.designer_name}-{self.model.model_name}')
        super().save(*args, **kwargs)

    def is_available(self, check_date: date = date.today()):
        busy_periods = self.busycars_set.filter(busy_start__lte=check_date, busy_end__gte=check_date)
        return not busy_periods.exists()

    def __str__(self) -> str:
        return self.slug if self.slug else 'Car Instance'

class BusyCars(models.Model):
    car = models.ForeignKey(CarInstances, on_delete=models.PROTECT, verbose_name="ID машины", related_name='busycars_set')
    renting_person = models.ForeignKey(Users, on_delete = models.PROTECT, verbose_name="Арендующий", default= 0)
    busy_start = models.DateField(verbose_name="Начало аренды")
    busy_end = models.DateField(verbose_name="Конец аренды")

    class Meta:
        verbose_name_plural = "Занятые машины"
        verbose_name = "Занятая машина"
        constraints = [
            models.CheckConstraint(
                check=models.Q(busy_start__lte=models.F('busy_end')),
                name='check_busy_dates'
            )
        ]

    def save(self, *args, **kwargs):
        if self.busy_start > self.busy_end:
            raise ValueError("Дата начала аренды не может быть позже даты окончания аренды")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.car} занята с {self.busy_start} по {self.busy_end}'

