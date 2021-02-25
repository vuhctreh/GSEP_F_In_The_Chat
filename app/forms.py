from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from app.models import CoffeeUser, Message, Task
from django.utils.translation import ugettext_lazy


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


class AdminSignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(choices=CoffeeUser.AVAILABLE_UNIS))

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
class AdminCUserEditForm(UserChangeForm):

    class Meta:
        model = CoffeeUser
        fields = ('first_name', 'last_name', 'year', 'course',
                  'cafe_table_ids')


class CUserEditForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(required=False)
    year = forms.IntegerField(required=False)
    course = forms.CharField(max_length=50, required=False)
    add_table_id = forms.CharField(max_length=50, required=False)
    remove_table_id = forms.CharField(max_length=50, required=False)


class createTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('task_name', 'task_content', 'points', 'table_id')


# Isabel 22/2/21
class PostMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('message_content',)
        labels = {
            'message_content': ugettext_lazy('Enter message:'),
        }
