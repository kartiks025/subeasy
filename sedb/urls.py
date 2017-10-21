from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_login$', views.admin_login, name='admin_login'),
]