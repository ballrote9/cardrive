from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import Users
from users.fields import NumericCharField
class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    class Meta:
        model = Users
        fields = ['username', 'password']
class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    middle_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = Users
        fields = ["first_name",
                  "last_name",
                  "middle_name",
                  "username",
                  "email",
                  "password1",
                  "password2",
        ]


class ProfileForm(forms.ModelForm):
    passport_num = NumericCharField(max_length=10, label='Серия и номер паспорта', required=False)
    drive_license_num = NumericCharField(max_length=10, label='Серия и номер водительского удостоверения', required= False)
    class Meta:
        model = Users
        fields = [  
            'first_name', 
            'last_name', 
            'middle_name',
            'passport_num',
            'drive_license_num',
            'username', 
            'email', 
            'image']
