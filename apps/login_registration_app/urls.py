from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login_registration$', views.login_registration, name = 'login_registration'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^clear_user$', views.clear_user, name = 'clear_user')
]
