from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_login$', views.admin_login, name='admin_login'),
    url(r'^admin_home$', views.admin_home, name='admin_home'),
    url(r'^add_course$', views.add_course, name='add_course'),
    url(r'^delete_course$', views.delete_course, name='delete_course'),
]