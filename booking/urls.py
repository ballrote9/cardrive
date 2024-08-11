from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking, name = 'index'),
    path('<slug:car_slug>/', views.go_booking, name = 'booking_pg')
]