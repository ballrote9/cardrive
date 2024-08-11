from django import forms

class NumericCharField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        if value:
            if not value.isdigit():
                raise forms.ValidationError("В номере документа могут присутствовать только цифры.")
            if len(value) < 10 and len(value) != 0:
                raise forms.ValidationError("В номере документа должно быть 10 символов.")