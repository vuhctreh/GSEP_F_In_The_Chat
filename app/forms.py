from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from app.models import CoffeeUser


# Isabel: 18/2/21
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


# Victoria: 18/2/21
class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CoffeeUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


# Isabel 19/2/21
class CUserEditForm(UserChangeForm):

    class Meta:
        model = CoffeeUser
        fields = ('first_name', 'last_name', 'year', 'course',
                  'cafe_table_ids')
