from django.urls import path

from . import views

urlpatterns = [
               path('', views.index, name='index'),  # login
               path('logout', views.log_out, name='logout'),
               path('signup', views.signup, name='signup'),
               path('table_view', views.table_view, name='table_view'),
               path('tables/<pk>', views.table_chat,
                    name='table_chat'),
               path('health', views.health, name='health'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               path('privacy', views.privacy, name='privacy'),
               path('terms', views.terms, name='terms'),
               ]
