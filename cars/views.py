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

    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)

    if designer_filter:
        cars = cars.filter(designer=designer_filter)

    if power_filter:
        if (power_filter == '250'):
            cars = cars.filter(power__gte=power_filter)
        else:
            cars = cars.filter(power__lte=power_filter)

    if carcase_filter:
        cars = cars.filter(carcase=carcase_filter)
    '''
    today = date.today()
    cars = cars.annotate(
        is_available=Case(
            When(
                Q(busycars_set__busy_start__lte=today, busycars_set__busy_end__gte=today),
                then=Value(False)
            ),
            default=Value(True),
            output_field=BooleanField()
        )
    ).distinct()'''

    if availability_filter == 'available':
        cars = cars.filter(is_available=True)
    elif availability_filter == 'unavailable':
        cars = cars.filter(is_available=False)
    
    context = {'cars': cars}
    return render(request, 'cars/catalog.html', context=context)

def carModels(request, car_slug):
    car = CarInstances.objects.get(slug = car_slug)
    context = {'car':car,}
    return render(request, 'cars/cars.html', context=context) 


