from django.contrib import admin
from cars.models import CarInstances, Designers, CarModels, Carcases, BusyCars

@admin.register(CarInstances)
class CarInstancesAdmin(admin.ModelAdmin):
    pass

admin.site.register(BusyCars)
admin.site.register(Designers)
admin.site.register(CarModels)
admin.site.register(Carcases)
