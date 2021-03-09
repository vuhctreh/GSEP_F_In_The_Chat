""" Placeholder """

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy
from app.models import CoffeeUser, Message, Task, Report


# Isabel: 18/2/21
class SignUpForm(UserCreationForm):
    """ Placeholder """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(
                    choices=CoffeeUser.AVAILABLE_UNIS))
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        """ Placeholder """
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')


class AdminSignUpForm(UserCreationForm):
    """ Placeholder """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(
                    choices=CoffeeUser.AVAILABLE_UNIS))

    class Meta:
        """ Placeholder """
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')


# Victoria: 18/2/21
class LoginForm(forms.ModelForm):
    """ Placeholder """
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        """ Placeholder """
        model = CoffeeUser
        fields = ('email', 'password')

    def clean(self):
        """ Placeholder """
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


# Isabel 19/2/21
class AdminCUserEditForm(UserChangeForm):
    """ Placeholder """

    class Meta:
        """ Placeholder """
        model = CoffeeUser
        fields = ('first_name', 'last_name', 'year', 'course',
                  'cafe_table_ids')


class CUserEditForm(forms.Form):
    """ Placeholder """
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(required=False)
    year = forms.IntegerField(required=False)
    course = forms.CharField(max_length=50, required=False)
    add_table_id = forms.CharField(max_length=50, required=False)
    remove_table_id = forms.CharField(max_length=50, required=False)
    share_tables = forms.CharField(required=False,
                                   widget=forms.Select(
                                       choices=(('', ''), ('Yes', 'Yes'),
                                                ('No', 'No'))))
    facebook_link = forms.CharField(max_length=255, required=False)
    instagram_username = forms.CharField(max_length=200, required=False)
    twitter_handle = forms.CharField(max_length=200, required=False)


class CUserEditFormStaff(forms.Form):
    """ Placeholder """
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(required=False)
    course = forms.CharField(max_length=50, required=False)


class CreateTaskForm(forms.ModelForm):
    """ Placeholder """

    def __init__(self, *args, **kwargs):
        """ Placeholder """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['points'].choices = ((1, '1'), (2, '2'), (3, '3'),
                                             (4, '4'), (5, '5'))

    class Meta:
        """ Placeholder """
        model = Task
        fields = ('task_name', 'task_content', 'points', 'table_id',
                  'recurrence_interval', 'max_repeats')


# Isabel 22/2/21
class PostMessageForm(forms.ModelForm):
    """ Placeholder """

    class Meta:
        """ Placeholder """
        model = Message
        fields = ('message_content',)
        labels = {
            'message_content': ugettext_lazy('Enter message:'),
        }


# Isabel 3/3/21
class StudyBreaksForm(forms.Form):
    """ Placeholder """
    minutes_studying_for = forms.IntegerField(min_value=5, max_value=300)


class ReportForm(forms.ModelForm):
    """ Placeholder """

    class Meta:
        """ Placeholder """
        model = Report
        fields = ('title', 'category', 'detail', 'table_id')
