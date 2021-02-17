from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CoffeeUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(choices=CoffeeUser.AVAILABLE_UNIS))

    class Meta:
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')
