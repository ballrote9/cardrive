import json
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import CarInstances
from booking.forms import BookingForm
from django.contrib import messages
from django.db.models import Q
from cars.models import BusyCars
from django.utils import timezone
from django.utils.dateformat import DateFormat

def go_booking(request, car_slug):
    car = get_object_or_404(CarInstances, slug=car_slug)

    if request.method == 'POST':
        # Проверка наличия данных
        if not request.user.is_authenticated:
            messages.error(request, 'Для бронирования необходимо авторизоваться.')
            return redirect('booking:booking_pg', car_slug)
        if not request.user.passport_num:
            messages.error(request, 'Для бронирования необходимо ввести данные паспорта.')
            return redirect('booking:booking_pg', car_slug)  # Перенаправляем обратно на страницу бронирования
        if not request.user.drive_license_num:
            messages.error(request, 'Для бронирования необходимо ввести номер водительского удостоверения.')
            return redirect('booking:booking_pg', car_slug)
        # Обработка формы бронирования
        booking_form = BookingForm(data=request.POST)

        if booking_form.is_valid():
            busy_start = booking_form.cleaned_data['busy_start']
            busy_end = booking_form.cleaned_data['busy_end']
            today = timezone.now().date()
            # Проверка: дата начала не может быть в прошлом
            if busy_start < today:
                messages.error(request, 'Нельзя бронировать автомобиль на прошедшую дату.')
                return redirect('booking:booking_pg', car_slug)

            # Проверка, занят ли автомобиль на выбранные даты
            conflicting_bookings = BusyCars.objects.filter(
                # Проверяем пересечение диапазонов дат
                Q(busy_start__lte=busy_end, busy_end__gte=busy_start),
                car=car

            )
            if conflicting_bookings.exists():
                messages.error(request, 'Автомобиль уже занят на выбранные даты.')
                return redirect('booking:booking_pg', car_slug)

            booking = booking_form.save(commit=False)
            booking.renting_person = request.user
            booking.car = car
            booking.save()
            return redirect('user:profile')  # Перенаправление на профиль пользователя
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print("Ошибки в форме:", booking_form.errors)
    
    else:
        booking_form = BookingForm()

    bookings = BusyCars.objects.filter(car=car)
    busy_intervals = [
        {
            'start': DateFormat(booking.busy_start).format('d-m-Y'),  # Форматируем даты как 'день-месяц-год'
            'end': DateFormat(booking.busy_end).format('d-m-Y')
        }
        for booking in bookings
        ]

    context = {
        'car': car,
        'booking_form': booking_form,
        'busy_intervals': busy_intervals,
    }
    return render(request, 'booking/booking.html', context=context)

