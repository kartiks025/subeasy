from django.conf.urls import url, include

from . import views, helpers, utils, restricted_helpers

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
    url(r'^download_submission/(?P<sub_id>[0-9]+)/$', helpers.download_submission, name='download_submission'),
    

    url(r'^section/(?P<sec_user_id>[0-9]+)/', include([
        url(r'^$', views.display_section, name='display_section'),
        url(r'^save_new_assign/$', restricted_helpers.save_new_assign, name='save_new_assign'),
        url(r'^post_comment/(?P<crib_id>[0-9]+)/$', helpers.post_comment, name='post_comment'),

        #instructor
        url(r'^assignment/(?P<assign_id>[0-9]+)/', include([
            url(r'^get_assign_cribs/$', helpers.get_assign_cribs, name='get_assign_cribs'),
            url(r'^delete_prob/(?P<prob_id>[0-9]+)/$', helpers.delete_prob, name='delete_prob'),
            url(r'^post_crib/(?P<prob_id>[0-9]+)/$', helpers.post_crib, name='post_crib'),
            url(r'^evaluate_all/$', helpers.evaluate_all, name='evaluate_all'),
            url(r'^download_auto_csv/$', helpers.download_auto_csv, name='download_auto_csv'),
            url(r'^upload_inst_csv/$', helpers.upload_inst_csv, name='upload_inst_csv'),
            url(r'^edit_assign_home/$', restricted_helpers.edit_assign_home, name='edit_assign_home'),
            url(r'^$', views.show_assignment, name='show_assignment'),
            url(r'^get_assign_home/$', helpers.get_assign_home, name='get_assign_home'),
            url(r'^get_assign_all_prob/$', helpers.get_assign_all_prob, name='get_assign_all_prob'),
            url(r'^get_new_prob_no/$', restricted_helpers.get_new_prob_no, name='get_new_prob_no'),
            url(r'^get_assign_prob/(?P<prob_id>[0-9]+)/$', helpers.get_assign_prob, name='get_assign_prob'),
            url(r'^edit_assign_prob/(?P<prob_id>[0-9]+)/$', restricted_helpers.edit_assign_prob, name='edit_assign_prob'),
            url(r'^download/$', helpers.download_helper_file, name='download_helper_file'),
            url(r'^download_problem_helper_file/(?P<prob_id>[0-9]+)/$', helpers.download_problem_helper_file, name='download_problem_helper_file'),
            url(r'^download_problem_solution_file/(?P<prob_id>[0-9]+)/$', helpers.download_problem_solution_file, name='download_problem_solution_file'),
            url(r'^download_testcase_file/(?P<prob_id>[0-9]+)/$', helpers.download_testcase_file, name='download_testcase_file'),
            url(r'^problem/(?P<prob_id>[0-9]+)/', include([
                url(r'^download_testcase_input_file/(?P<testcase_no>[0-9]+)/$', helpers.download_testcase_input_file, name='download_testcase_input_file'),
                url(r'^download_testcase_output_file/(?P<testcase_no>[0-9]+)/$', helpers.download_testcase_output_file, name='download_testcase_output_file'),
            ])),
            url(r'^get_all_submissions/$',helpers.get_all_submissions, name='get_all_submissions'),
        ])),

        #student
        url(r'^assignments/(?P<assign_id>[0-9]+)/', include([
            url(r'^submission/$', views.submission, name='submission'),
            url(r'^$', views.stu_assignment, name='stu_assignment'),
            url(r'^download/$', helpers.download_helper_file, name='download_helper_file'),
            url(r'^submit_problem/(?P<prob_id>[0-9]+)/$', helpers.submit_problem, name='submit_problem'),
            url(r'^evaluate_problem/(?P<prob_id>[0-9]+)/$', helpers.evaluate_problem, name='evaluate_problem'),
            url(r'^download_your_submission/(?P<prob_id>[0-9]+)/$', helpers.download_your_submission, name='download_your_submission'),
            url(r'^get_user_assign_prob/(?P<prob_id>[0-9]+)/$', helpers.get_user_assign_prob, name='get_user_assign_prob'),
            url(r'^get_user_marks/$', helpers.get_user_marks, name='get_user_marks'),

        ])),
    ])),

    url(r'^output_compare/(?P<sub_test_id>[0-9]+)/$', views.output_compare, name='output_compare'),


    url(r'^get_assignments/(?P<sec_user_id>[0-9]+)/$', helpers.get_assignments, name='get_assignments'),
    url(r'^get_instructors/(?P<sec_user_id>[0-9]+)/$', helpers.get_instructors, name='get_instructors'),
    url(r'^get_students/(?P<sec_user_id>[0-9]+)/$', restricted_helpers.get_students, name='get_students'),
    url(r'^get_tas/(?P<sec_user_id>[0-9]+)/$', restricted_helpers.get_tas, name='get_tas'),

    url(r'^add_csv_student/(?P<sec_user_id>[0-9]+)/$', views.add_csv_student, name='add_csv_student'),
    url(r'^add_ta/(?P<sec_user_id>[0-9]+)/$', views.add_ta, name='add_ta'),
    url(r'^add_ex_student/(?P<sec_user_id>[0-9]+)/$', views.add_ex_student, name='add_ex_student'),
    url(r'^add_new_student/(?P<sec_user_id>[0-9]+)/$', views.add_new_student, name='add_new_student'),

]
