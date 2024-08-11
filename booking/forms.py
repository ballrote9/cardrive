from django import forms
from cars.models import BusyCars
from cars.models import CarInstances

class BookingForm(forms.ModelForm):
    class Meta:
        model = BusyCars
        fields = [
            'renting_person', 
            'car', 
            'busy_start', 
            'busy_end'
        ]
        widgets = {
            'renting_person': forms.HiddenInput(),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'busy_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_busy_start'}),
            'busy_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_busy_end'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['renting_person'].initial = self.user.id

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        busy_start = cleaned_data.get('busy_start')
        busy_end = cleaned_data.get('busy_end')

        if car and busy_start and busy_end:
            overlapping_bookings = BusyCars.objects.filter(
                car=car,
                busy_end__gte=busy_start,
                busy_start__lte=busy_end
            ).exclude(id=self.instance.id)

            if overlapping_bookings.exists():
                raise forms.ValidationError("Этот автомобиль уже занят в выбранные даты.")
        
        return cleaned_data
