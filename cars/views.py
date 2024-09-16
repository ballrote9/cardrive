from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Q, Value, BooleanField, Case, When, Count
from datetime import date
from cars.models import CarInstances, BusyCars

def catalog(request):
    cars = CarInstances.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    availability_filter = request.GET.get('availability')
    designer_filter = request.GET.get('designer')
    power_filter = request.GET.get('power')
    carcase_filter = request.GET.get('carcase')

    # Фильтрация по цене
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)

    # Фильтрация по производителю, мощности и кузову
    if designer_filter:
        cars = cars.filter(designer=designer_filter)

    if power_filter:
        if power_filter == '250':
            cars = cars.filter(power__gte=power_filter)
        else:
            cars = cars.filter(power__lte=power_filter)

    if carcase_filter:
        cars = cars.filter(carcase=carcase_filter)
    
    # Определяем текущую дату
    today = date.today()

    if availability_filter == 'available':
        # Ищем машины, которые НЕ заняты на текущий момент
        cars = cars.annotate(
            is_occupied=Count(
                'busycars_set',
                filter=Q(busycars_set__busy_start__lte=today, busycars_set__busy_end__gte=today)
            )
        ).filter(is_occupied=0)
    elif availability_filter == 'unavailable':
        # Ищем машины, которые заняты на текущий момент
        cars = cars.annotate(
            is_occupied=Count(
                'busycars_set',
                filter=Q(busycars_set__busy_start__lte=today, busycars_set__busy_end__gte=today)
            )
        ).filter(is_occupied__gt=0)

    context = {'cars': cars}
    return render(request, 'cars/catalog.html', context=context)


def carModels(request, car_slug):
    car = CarInstances.objects.get(slug = car_slug)
    context = {'car':car,}
    return render(request, 'cars/cars.html', context=context) 


