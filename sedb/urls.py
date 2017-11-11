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
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_home/$', views.user_home, name='user_home'),
    url(r'^display_section/(?P<sec_user_id>[0-9]+)/$', views.display_section, name='display_section'),
    url(r'^user_signup/$', views.user_signup, name='user_signup'),

    url(r'^display_ta$', views.display_ta, name='display_ta'),
    url(r'^forgot_password$', views.forgot_password, name='forgot_password'),
    url(r'^r_password$', views.r_password, name='r_password'),
    url(r'^verify_account/(?P<uid>[a-z^0-9]+)/$', views.verify_account, name='verify_account'),
    url(r'^reset_password/(?P<uid>[a-z^0-9]+)/$', views.reset_password, name='reset_password'),
    url(r'^forgot_password.html$', views.forgot_password, name='forgot_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^add_assignment/(?P<sec_user_id>[0-9]+)/$', views.add_assignment, name='add_assignment'),
    url(r'^admin_logout/$', views.admin_logout, name='admin_logout'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    

    url(r'^section/(?P<sec_user_id>[0-9]+)/', include([
        url(r'^$', views.display_section, name='display_section'),

        url(r'^assignment/(?P<assign_id>[0-9]+)/', include([
            url(r'edit_assign_home/$', helpers.edit_assign_home, name='edit_assign_home'),
            url(r'^$', views.show_assignment, name='show_assignment'),
            url(r'^get_assign_home/$', helpers.get_assign_home, name='get_assign_home'),
            url(r'^get_new_prob_no/$', helpers.get_new_prob_no, name='get_new_prob_no'),
            url(r'^get_assign_prob/(?P<prob_id>[0-9]+)/$', helpers.get_assign_prob, name='get_assign_prob'),
            url(r'^edit_assign_prob/(?P<prob_id>[0-9]+)/$', helpers.edit_assign_prob, name='edit_assign_prob'),
            url(r'^download/$', helpers.download_helper_file, name='download_helper_file'),
        ])),

        url(r'^assignments/(?P<assign_id>[0-9]+)/$', views.stu_assignment, name='stu_assignment'),
    ])),


    url(r'^get_assignments/(?P<sec_user_id>[0-9]+)/$', helpers.get_assignments, name='get_assignments'),
    url(r'^get_instructors/(?P<sec_user_id>[0-9]+)/$', helpers.get_instructors, name='get_instructors'),
    url(r'^get_students/(?P<sec_user_id>[0-9]+)/$', helpers.get_students, name='get_students'),
    url(r'^get_tas/(?P<sec_user_id>[0-9]+)/$', helpers.get_tas, name='get_tas'),

    url(r'^add_csv_student/(?P<sec_user_id>[0-9]+)/$', views.add_csv_student, name='add_csv_student'),
    url(r'^add_ta/(?P<sec_user_id>[0-9]+)/$', views.add_ta, name='add_ta'),
    url(r'^add_ex_student/(?P<sec_user_id>[0-9]+)/$', views.add_ex_student, name='add_ex_student'),
    url(r'^add_new_student/(?P<sec_user_id>[0-9]+)/$', views.add_new_student, name='add_new_student'),

]
