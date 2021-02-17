from django.contrib import admin

from .models import CafeTable, CoffeeUser, Task, Message

admin.site.register(CafeTable)
admin.site.register(CoffeeUser)
admin.site.register(Task)
admin.site.register(Message)

# u can't add or change the users in admin portal yet bc stuff needs to be
# added bc of the custom user model used
# https://stackoverflow.com/questions/28981057/cant-get-django-custom-user-model-to-work-with-admin
