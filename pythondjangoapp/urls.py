from django.urls import path
from django.conf.urls import include
from django.contrib import admin


urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),  # ffffff
]
