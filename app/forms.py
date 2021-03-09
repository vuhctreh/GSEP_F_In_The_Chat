""" All the required forms that users can complete and submit are located here """

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy
from app.models import CoffeeUser, Message, Task, Report


# Isabel: 18/2/21
class SignUpForm(UserCreationForm):
    """ Contains all information for signing up """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(
                    choices=CoffeeUser.AVAILABLE_UNIS))
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        """ Sign up data """
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')


class AdminSignUpForm(UserCreationForm):
    """ Contains all information for signing up as an admin user """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)
    university = forms.CharField(widget=forms.Select(
                    choices=CoffeeUser.AVAILABLE_UNIS))

    class Meta:
        """ Sign up data """
        model = CoffeeUser
        fields = ('email', 'first_name', 'last_name', 'is_staff', 'university',
                  'password1', 'password2')


# Victoria: 18/2/21
class LoginForm(forms.ModelForm):
    """ Contains the information for logging in """
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        """ Login data """
        model = CoffeeUser
        fields = ('email', 'password')

    def clean(self):
        """ Contains login data that have passed the validation tests """
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


# Isabel 19/2/21
class AdminCUserEditForm(UserChangeForm):
    """ The edit profile form from the admin page """

    class Meta:
        """ Edit info metadata """
        model = CoffeeUser
        fields = ('first_name', 'last_name', 'year', 'course',
                  'cafe_table_ids')


class CUserEditForm(forms.Form):
    """ Contains the information present in the edit info form """
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
    """ Contains the edit info form information for staff users """
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(required=False)
    course = forms.CharField(max_length=50, required=False)


class CreateTaskForm(forms.ModelForm):
    """ Contains the information from the create task form """

    def __init__(self, *args, **kwargs):
        """ Checking how many points the specific user can put for a task
            depending on if he/she is a staff user or not
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['points'].choices = ((1, '1'), (2, '2'), (3, '3'),
                                             (4, '4'), (5, '5'))

    class Meta:
        """ Task metadata """
        model = Task
        fields = ('task_name', 'task_content', 'points', 'table_id',
                  'recurrence_interval', 'max_repeats')


# Isabel 22/2/21
class PostMessageForm(forms.ModelForm):
    """ Contains the information for a message """

    class Meta:
        """ message metadata """
        model = Message
        fields = ('message_content',)
        labels = {
            'message_content': ugettext_lazy('Enter message:'),
        }


# Isabel 3/3/21
class StudyBreaksForm(forms.Form):
    """ Contains the minutes that a user is studying for """
    minutes_studying_for = forms.IntegerField(min_value=5, max_value=300)


class ReportForm(forms.ModelForm):
    """ Contains the fields that a user needs to input before submitting 
        a report
    """

    class Meta:
        """ Data regarding report """
        model = Report
        fields = ('title', 'category', 'detail', 'table_id')
