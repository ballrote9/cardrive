from django import forms
from cars.models import BusyCars

class BookingForm(forms.ModelForm):
    class Meta:
        model = BusyCars
        fields = ['renting_person', 'car', 'busy_start', 'busy_end']
        widgets = {
            'renting_person': forms.HiddenInput(),
            'car': forms.HiddenInput(),
            'busy_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_busy_start'}),
            'busy_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_busy_end'}),
        }
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['car'].required = False
        self.fields['renting_person'].required = False