from django.conf.urls import url, include

from . import views, helpers

app_name = 'sedb'

urlpatterns = [
    url(r'^admin_login/$', views.admin_login, name='admin_login'),
    url(r'^admin_home/$', views.admin_home, name='admin_home'),
    url(r'^add_course$', views.add_course, name='add_course'),
    url(r'^delete_course$', views.delete_course, name='delete_course'),
    url(r'^add_section$', views.add_section, name='add_section'),
    url(r'^delete_section$', views.delete_section, name='delete_section'),
<<<<<<< HEAD
    url(r'^user_login$', views.user_login, name='user_login'),
    url(r'^user_home$', views.user_home, name='user_home'),
    url(r'^user_signup$', views.user_signup, name='user_signup'),
=======
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_home/$', views.user_home, name='user_home'),
    url(r'^display_section/(?P<sec_user_id>[0-9]+)/$', views.display_section, name='display_section'),
    url(r'^user_signup/$', views.user_signup, name='user_signup'),
>>>>>>> 89cce39804d6522968abad413bee05b1bc9f9943
    url(r'^display_instructor$', views.display_instructor, name='display_instructor'),
    url(r'^display_ta$', views.display_ta, name='display_ta'),
    url(r'^display_student$', views.display_student, name='display_student'),
    url(r'^forgot_password$', views.forgot_password, name='forgot_password'),
    url(r'^r_password$', views.r_password, name='r_password'),
    url(r'^verify_account/(?P<uid>[a-z^0-9]+)/$', views.verify_account, name='verify_account'),
    url(r'^reset_password/(?P<uid>[a-z^0-9]+)/$', views.reset_password, name='reset_password'),
    url(r'^forgot_password.html$', views.forgot_password, name='forgot_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^add_assignment/(?P<sec_user_id>[0-9]+)/$', views.add_assignment, name='add_assignment'),
    url(r'^admin_logout/$', views.admin_logout, name='admin_logout'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^add_ta/(?P<sec_user_id>[0-9]+)/$', views.add_ta, name='add_ta'),
    url(r'^add_ex_student/(?P<sec_user_id>[0-9]+)/$', views.add_ex_student, name='add_ex_student'),
    url(r'^add_new_student/(?P<sec_user_id>[0-9]+)/$', views.add_new_student, name='add_new_student'),

    url(r'^section/(?P<sec_user_id>[0-9]+)/', include([
        url(r'^$', views.display_section, name='display_section'),
        url(r'^assignment/(?P<assign_id>[0-9]+)/edit_assign_home/$', helpers.edit_assign_home, name='edit_assign_home'),
        url(r'^assignment/(?P<assign_id>[0-9]+)/$', views.show_assignment, name='show_assignment'),
        url(r'^assignment/(?P<assign_id>[0-9]+)/get_assign_home/$', helpers.get_assign_home, name='get_assign_home'),
    ])),


    url(r'^assignment_tab/(?P<sec_user_id>[0-9]+)/$', views.assignment_tab, name='assignment_tab'),
    url(r'^instructor_tab/(?P<sec_user_id>[0-9]+)/$', views.instructor_tab, name='instructor_tab'),
    url(r'^student_tab/(?P<sec_user_id>[0-9]+)/$', views.student_tab, name='student_tab'),
    url(r'^ta_tab/(?P<sec_user_id>[0-9]+)/$', views.ta_tab, name='ta_tab'),
    url(r'^add_csv_student/(?P<sec_user_id>[0-9]+)/$', views.add_csv_student, name='add_csv_student'),
]
