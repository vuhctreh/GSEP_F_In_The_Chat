from django.contrib import admin
from django.contrib.auth.models import User

from .models import CafeTable, CoffeeUser, Task, Message

admin.site.register(CafeTable)
admin.site.register(CoffeeUser)
#admin.site.register(User)
admin.site.register(Task)
admin.site.register(Message)
