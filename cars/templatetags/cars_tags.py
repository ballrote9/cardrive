from django import template
from django.db.models import Min, Max
from cars.models import CarInstances, Designers, Carcases


register = template.Library()

@register.simple_tag() 
def tag_designer():
    return Designers.objects.all().order_by('designer_name')

@register.simple_tag() 
def tag_carcase():
    return Carcases.objects.all()
    return Designers.objects.all().order_by('designer_name')

@register.simple_tag() 
def tag_min_price():
    min_price =  CarInstances.objects.aggregate(Min('price'))['price__min']
    if min_price:
        min_price =  int(min_price)
    return min_price

@register.simple_tag() 
def tag_max_price():
    max_price = CarInstances.objects.aggregate(Max('price'))['price__max']
    if max_price:
        max_price = int(max_price)
    return max_price

@register.simple_tag() 
def tag_cars():
    return CarInstances.objects.all()