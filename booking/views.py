import json
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import CarInstances
from booking.forms import BookingForm
from cars.models import BusyCars
from users.forms import ProfileForm

def booking(request):
    cars = CarInstances.objects.all()
    booked_dates = list(BusyCars.objects.values_list('busy_start', 'busy_end'))
    booked_dates = [date for sublist in booked_dates for date in sublist]
    booked_dates = [date.isoformat() for date in booked_dates]

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.renting_person = request.user
            booking.save()
            return redirect('user:profile')  # Укажите URL для успешного бронирования
    else:
        form = BookingForm()

    context = {
        'cars': cars,
        'form': form,
        'booked_dates_json': json.dumps(booked_dates)
    }
    return render(request, 'booking/booking.html', context=context)



def go_booking(request, car_slug):
    car = get_object_or_404(CarInstances, slug=car_slug)
    booked_dates = list(car.busycars_set.values_list('busy_start', 'busy_end'))
    booked_dates = [date for sublist in booked_dates for date in sublist]
    booked_dates = [date.isoformat() for date in booked_dates]

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, initial={'car': car}, user=request.user)
        user_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if booking_form.is_valid() and user_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.renting_person = request.user
            booking.save()
            user_form.save()
            return redirect('user:profile')  # Укажите URL для успешного бронирования
    else:
        booking_form = BookingForm(initial={'car': car}, user=request.user)
        user_form = ProfileForm(instance=request.user)

    context = {
        'car': car,
        'booking_form': booking_form,
        'user_form': user_form,
        'booked_dates_json': json.dumps(booked_dates),
    }
    return render(request, 'booking/booking.html', context=context)

