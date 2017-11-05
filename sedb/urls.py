from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_login$', views.admin_login, name='admin_login'),
    url(r'^admin_home$', views.admin_home, name='admin_home'),
    url(r'^add_course$', views.add_course, name='add_course'),
    url(r'^delete_course$', views.delete_course, name='delete_course'),
    url(r'^add_section$', views.add_section, name='add_section'),
    url(r'^delete_section$', views.delete_section, name='delete_section'),
    url(r'^user_login$', views.user_login, name='user_login'),
    url(r'^user_home$', views.user_home, name='user_home'),
    url(r'^display_section$', views.display_section, name='display_section'),
    url(r'^user_signup$', views.user_signup, name='user_signup'),
    url(r'^display_instructor$', views.display_instructor, name='display_instructor'),
    url(r'^display_ta$', views.display_ta, name='display_ta'),
    url(r'^display_student$', views.display_student, name='display_student'),
    url(r'^forgot_password$', views.forgot_password, name='forgot_password'),
    url(r'^verify_account/(?P<uid>[a-z^0-9]+)/$', views.verify_account, name='verify_account'),
    url(r'^reset_password/(?P<uid>[a-z^0-9]+)/$', views.reset_password, name='reset_password'),
    url(r'^forgot_password.html$', views.forgot_password, name='forgot_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
]