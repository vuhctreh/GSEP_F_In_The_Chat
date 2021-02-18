from django.urls import path

from . import views

urlpatterns = [
               path('', views.index, name='index'),
               path('signup', views.signup, name="signup"),
               path('health', views.health, name='health'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               path('privacy', views.privacy, name='privacy'),
               path('terms', views.terms, name='terms'),
               ]
