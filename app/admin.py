from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminSignUpForm, CUserEditForm
from .models import CafeTable, CoffeeUser, Task, Message


class CoffeeUserAdmin(UserAdmin):
    add_form = AdminSignUpForm
    form = CUserEditForm
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
