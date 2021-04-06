from django.urls import path, re_path

from . import views

_USER_ACTIVATE_PATTERN = r'^activate/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z-]{39})/'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    re_path(_USER_ACTIVATE_PATTERN, views.activate, name='activate')
]
