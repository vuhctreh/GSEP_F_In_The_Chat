from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
               path('', views.index, name='index'),  # login
               path('logout', views.log_out, name='logout'),
               path('report', views.report, name='report'),
               path('signup', views.signup, name='signup'),
               path('table_view', views.table_view, name='table_view'),
               path('tables/<pk>', views.table_chat,
                    name='table_chat'),
               path('get_msgs/<table>', views.get_msgs, name='get_msgs'),
               path('upvote/<pk>', views.upvote, name='upvote_message'),
               path('dashboard/edit_info', views.edit_info, name='edit_info'),
               path('health', views.health, name='health'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               path('privacy', views.privacy, name='privacy'),
               path('terms', views.terms, name='terms'),
               path('set_tasks', views.set_tasks, name='set_tasks'),
               path('view_tasks', views.view_tasks, name='viewtasks'),
               path('complete/<pk>', views.completeTask, name='complete'),
               path('dashboard', views.dashboard, name='dashboard'),
               path('profile_page/<pk>', views.profile_page,
                    name='profile_page'),
               path('favicon.ico',
                    RedirectView.as_view(
                        url=staticfiles_storage.url('static/images/favicon.ico'))
                    ),
               ]
