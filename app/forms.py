from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.models import CoffeeUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(choices=CoffeeUser.AVAILABLE_UNIS))
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')


class CUserEditForm(UserChangeForm):

    class Meta:
        model = CoffeeUser
        fields = ('first_name', 'last_name', 'year', 'course',
                  'cafe_table_ids')
