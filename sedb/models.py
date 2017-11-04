# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class AssignIp(models.Model):
    start_ip = models.CharField(max_length=60)
    end_ip = models.CharField(max_length=60)
    assignment = models.ForeignKey('Assignment', models.DO_NOTHING)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'assign_ip'
        unique_together = (('start_ip', 'end_ip', 'assignment'),)


class Assignment(models.Model):
    assignment_id = models.BigAutoField(primary_key=True)
    assignment_no = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    publish_time = models.DateTimeField()
    visibility = models.BooleanField()
    helper_file_name = models.CharField(max_length=50, blank=True, null=True)
    helper_file = models.BinaryField(blank=True, null=True)
    crib_deadline = models.DateTimeField()
    sec = models.ForeignKey('Section', models.DO_NOTHING)
    deadline = models.ForeignKey('Deadline', models.DO_NOTHING)
    num_problems = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assignment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    crib = models.ForeignKey('Crib', models.DO_NOTHING)
    text = models.TextField()
    timestamp = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'course'


class Crib(models.Model):
    crib_id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    resolved = models.BooleanField()
    timestamp = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    problem = models.ForeignKey('Problem', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'crib'
        unique_together = (('user', 'problem'),)


class Deadline(models.Model):
    deadline_id = models.BigAutoField(primary_key=True)
    soft_deadline = models.DateTimeField()
    hard_deadline = models.DateTimeField()
    freezing_deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'deadline'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Problem(models.Model):
    problem_id = models.BigAutoField(primary_key=True)
    problem_no = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    helper_file_name = models.CharField(max_length=50, blank=True, null=True)
    helper_file = models.BinaryField(blank=True, null=True)
    solution_filename = models.CharField(max_length=50, blank=True, null=True)
    solution_file = models.BinaryField(blank=True, null=True)
    compile_cmd = models.TextField(blank=True, null=True)
    sol_visibility = models.BooleanField()
    assignment = models.ForeignKey(Assignment, models.DO_NOTHING)
    resource_limit = models.ForeignKey('ResourceLimit', models.DO_NOTHING)
    num_testcases = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'problem'


class ResourceLimit(models.Model):
    resource_limit_id = models.BigAutoField(primary_key=True)
    cpu_time = models.IntegerField()
    clock_time = models.IntegerField()
    memory_limit = models.IntegerField()
    stack_limit = models.IntegerField()
    open_files = models.IntegerField()
    max_filesize = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'resource_limit'


class SecUser(models.Model):
    role = models.CharField(max_length=10)
    user = models.ForeignKey('User', models.DO_NOTHING)
    sec = models.ForeignKey('Section', models.DO_NOTHING)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sec_user'
        unique_together = (('user', 'sec'),)


class Section(models.Model):
    sec_id = models.BigAutoField(primary_key=True)
    sec_name = models.CharField(max_length=20)
    semester = models.CharField(max_length=10)
    year = models.IntegerField()
    course = models.ForeignKey(Course, models.DO_NOTHING)
    num_assignments = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'


class Submission(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    sub_no = models.IntegerField()
    marks_auto = models.IntegerField()
    marks_inst = models.IntegerField()
    sub_file_name = models.CharField(max_length=50)
    sub_file = models.BinaryField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'submission'
        unique_together = (('sub_no', 'problem', 'user'),)


class Testcase(models.Model):
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    testcase_no = models.IntegerField()
    infile_name = models.CharField(max_length=50)
    infile = models.BinaryField()
    outfile_name = models.CharField(max_length=50)
    outfile = models.BinaryField()
    marks = models.IntegerField()
    visibility = models.BooleanField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'testcase'
        unique_together = (('testcase_no', 'problem'),)


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'user'


class UserSubmissions(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    problem = models.ForeignKey(Problem, models.DO_NOTHING)
    num_submissions = models.IntegerField()
    final_submission_no = models.IntegerField()
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user_submissions'
        unique_together = (('user', 'problem'),)
