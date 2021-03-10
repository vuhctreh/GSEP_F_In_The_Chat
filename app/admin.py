""" Enables functionality for interaction with models in admin view. """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.forms import AdminSignUpForm, AdminCUserEditForm
from app.models import CafeTable, CoffeeUser, Task, Message, Report


class CoffeeUserAdmin(UserAdmin):
    """ Allows custom user model (CoffeeUser) to be used with Django admin."""
    add_form = AdminSignUpForm
    form = AdminCUserEditForm
    list_display = ('email', 'first_name', 'last_name', 'university',
                    'is_staff', 'year', 'course')
    list_filter = ('email', 'first_name', 'last_name', 'university',
                   'is_staff', 'year', 'course', 'cafe_table_ids')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name',
                'year', 'course', 'cafe_table_ids')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'is_staff',
                       'university', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('cafe_table_ids',)


admin.site.register(CafeTable)
admin.site.register(CoffeeUser, CoffeeUserAdmin)
admin.site.register(Task)
admin.site.register(Message)
admin.site.register(Report)
