import smtplib
import pytz
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import *
from django.forms.models import model_to_dict

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bcrypt import hashpw, gensalt
from django.shortcuts import redirect, reverse
from django.core import serializers
from django.db import connection

from .models import *


def admin_required(fun):
    def wrap(request):
        try:
            if not request.session['is_admin']:
                return redirect('sedb:admin_login')
        except KeyError:
            return redirect('sedb:admin_login')
        return fun(request)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def user_required(fun):
    def wrap(*args):
        print("user_required")
        try:
            if not args[0].session['is_user']:
                return redirect('sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(*args)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def user1_required(fun):
    def wrap(request, sec_user_id):
        print("user1_required")
        try:
            if not request.session['is_user']:
                return redirect('sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                if not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request, sec_user_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def user2_required(fun):
    def wrap(request, sec_user_id, assign_id):
        print("user2_required")
        try:
            if not request.session['is_user']:
                return redirect('sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                print(sec_user.role)
                if not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
                elif sec_user.role != "Instructor" and sec_user.role != "TA":
                    assign = Assignment.objects.get(assignment_id=assign_id)
                    if not assign.visibility:
                        print("cannot access this assignment")
                        return doredirect(request, 'sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request, sec_user_id, assign_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def doredirect(request, url):
    if request.is_ajax():
        print("ajax request")
        return JsonResponse({
            'success': True,
            'to_redirect': True,
            'url': reverse(url)
        })
    else:
        return redirect(url)


def instructor_required(fun):
    def wrap(request, sec_user_id):
        print("instructor")
        try:
            if not request.session['is_user']:
                print(sec_user_id)
                return doredirect(request, 'sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                if not sec_user.role == "Instructor" or not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in instructor_required")
            return doredirect(request, 'sedb:user_login')
        return fun(request, sec_user_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def instructor1_required(fun):
    def wrap(request, sec_user_id, assign_id):
        print("instructor1")
        try:
            if not request.session['is_user']:
                print(sec_user_id)
                return doredirect(request, 'sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                print("yes " + sec_user.role)
                if not sec_user.role == "Instructor" or not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in instructor_required")
            return doredirect(request, 'sedb:user_login')
        print(sec_user.role)
        return fun(request, sec_user_id, assign_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def student_required(fun):
    def wrap(request, sec_user_id):
        print("student")
        try:
            if not request.session['is_user']:
                print(sec_user_id)
                return doredirect(request, 'sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                if not sec_user.role == "Student" or not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in student_required")
            return doredirect(request, 'sedb:user_login')
        return fun(request, sec_user_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def student1_required(fun):
    def wrap(request, sec_user_id, assign_id):
        print("student1")
        try:
            if not request.session['is_user']:
                print(sec_user_id)
                return doredirect(request, 'sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                print("yes " + sec_user.role)
                if not sec_user.role == "Student" or not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
                assign = Assignment.objects.get(assignment_id=assign_id)
                if not assign.visibility:
                    print("cannot access this assignment")
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in student_required")
            return doredirect(request, 'sedb:user_login')
        print(sec_user.role)
        return fun(request, sec_user_id, assign_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def instructor2_required(fun):
    def wrap(request, sec_user_id, assign_id, prob_id):
        try:
            if not request.session['is_user']:
                print(sec_user_id)
                return doredirect(request, 'sedb:user_login')
            else:
                print(sec_user_id)
                sec_user = SecUser.objects.get(id=sec_user_id)
                if not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in instructor_required")
            return doredirect(request, 'sedb:user_login')
        return fun(request, sec_user_id, assign_id, prob_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap


def send_verify_mail():
    fromaddr = "kartik_singhal@iitb.ac.in"
    toaddr = "kartiks025@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Verify Your Account"

    body = "Click here man"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-auth.iitb.ac.in', 25)
    server.starttls()
    server.login("kartik_singhal@iitb.ac.in", "")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def gethashedpwd(pwd):
    return hashpw(pwd.encode('utf-8'), gensalt()).decode('utf-8')


def send_forgot_password_email(uid, email):
    fromaddr = "kartik_singhal@iitb.ac.in"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Reset Password"

    body = "Click on this link http://localhost:8000/sedb/reset_password/" + uid + "/"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-auth.iitb.ac.in', 25)
    server.starttls()
    server.login("kartik_singhal@iitb.ac.in", "yamini@1990")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def send_verify_account_email(uid, email):
    fromaddr = "kartik_singhal@iitb.ac.in"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Verify Account"

    body = "Click on this link http://localhost:8000/sedb/verify_account/" + uid + "/"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-auth.iitb.ac.in', 25)
    server.starttls()
    server.login("kartik_singhal@iitb.ac.in", "yamini@1990")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@instructor1_required
def edit_assign_home(request, sec_user_id, assign_id):
    print("edit_assign_home called")
    assignment_id = 0
    if request.method == 'POST':
        assign_num = request.POST['assign_num']
        title = request.POST['assign_title']
        visibility = request.POST['visibility']
        pub_time = request.POST['pub_time']
        soft_deadline = request.POST['soft_deadline']
        hard_deadline = request.POST['hard_deadline']
        freeze_deadline = request.POST['freeze_deadline']
        crib_deadline = request.POST['crib_deadline']
        description = request.POST['description']


        section = SecUser.objects.get(id=sec_user_id).sec
        if assign_id == '0':
            print("New Assignment")
            try:
                helper_file = request.FILES['helper_file'].file.read()
                helper_file_name = request.FILES['helper_file'].name
            except Exception:
                helper_file = None
                helper_file_name = ""
            deadline = Deadline(soft_deadline=soft_deadline, hard_deadline=hard_deadline,
                                freezing_deadline=freeze_deadline)
            deadline.save()
            assignment = Assignment(assignment_no=assign_num, title=title, description=description,
                                    publish_time=pub_time, visibility=(visibility == '1'), crib_deadline=crib_deadline,
                                    sec=section, num_problems=0, deadline=deadline,helper_file=helper_file,helper_file_name=helper_file_name)

            assignment.save()
            assignment_id = assignment.assignment_id
        else:
            try:
                assignment = Assignment.objects.get(assignment_id=assign_id)
                assignment.assignment_no = assign_num
                assignment.title = title
                assignment.visibility = (visibility == '1')
                assignment.publish_time = pub_time
                assignment.deadline.soft_deadline = soft_deadline
                assignment.deadline.hard_deadline = hard_deadline
                assignment.deadline.freezing_deadline = freeze_deadline
                assignment.description = description
                try:
                    print("try")
                    assignment.helper_file = request.FILES['helper_file'].file.read()
                    assignment.helper_file_name = request.FILES['helper_file'].name
                    print("try1")
                except Exception:
                    print("except")
                assignment.deadline.save()
                assignment.save()
                assignment_id = assignment.assignment_id
            except ObjectDoesNotExist:
                print("assignment doesn't exist")
                # do something

        print(sec_user_id)
        print(assign_num)
        print(title)
        print(visibility)
        print(pub_time)
        print(soft_deadline)
        print(hard_deadline)
        print(freeze_deadline)
        print(crib_deadline)
        print(description)

    return JsonResponse({
        'r_id': assignment_id
    })


@user2_required
def get_assign_home(request, sec_user_id, assign_id):
    if assign_id == '0':
        return JsonResponse(
            {
                'new_assign': True
            }
        )
    assignment = Assignment.objects.get(assignment_id=assign_id)
    deadline = assignment.deadline
    context = {'new_assign': False, 'assign': model_to_dict(assignment), 'deadline': model_to_dict(deadline)}
    return JsonResponse(context)


@user2_required
def download_helper_file(request, sec_user_id, assign_id):
    contents = Assignment.objects.get(assignment_id=assign_id).helper_file
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename='+Assignment.objects.get(assignment_id=assign_id).helper_file_name
    return response


@user1_required
def get_assignments(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    if sec_user.role == "Instructor" or sec_user.role == "TA":
        assign = Assignment.objects.filter(sec=sec_user.sec)
    elif sec_user.role == "Student":
        assign = Assignment.objects.filter(sec=sec_user.sec, visibility=True)
    assignments = [{'id': a.assignment_id, 'title': a.title} for a in assign]
    context = {'assignments': assignments}
    return JsonResponse(context, content_type="application/json")


@instructor_required
def get_instructors(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    ins = SecUser.objects.filter(sec_id=sec_user.sec_id, role="Instructor")
    instructor = [{'id': a.user.user_id, 'name': a.user.name} for a in ins]
    print(instructor)
    context = {'instructor': instructor}
    return JsonResponse(context, content_type="application/json")


@instructor_required
def get_students(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    stu = SecUser.objects.filter(sec_id=sec_user.sec_id, role="Student")
    student = [{'id': a.user.user_id, 'name': a.user.name} for a in stu]

    cursor = connection.cursor()
    cursor.execute(
        '''select user_id,name from "user" where user_id not in (select user_id from sec_user where sec_id=%s);''',
        [sec_user.sec_id])
    users = dictfetchall(cursor)

    context = {'user': users, 'student': student}
    return JsonResponse(context, content_type="application/json")


@instructor_required
def get_tas(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    teach = SecUser.objects.filter(sec_id=sec_user.sec_id, role="TA")
    ta = [{'id': a.user.user_id, 'name': a.user.name} for a in teach]

    cursor = connection.cursor()
    cursor.execute(
        '''select user_id,name from "user" where user_id not in (select user_id from sec_user where sec_id=%s);''',
        [sec_user.sec_id])
    users = dictfetchall(cursor)

    context = {'user': users, 'ta': ta}
    return JsonResponse(context, content_type="application/json")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def send_new_account_email(uid, email):
    fromaddr = "kartik_singhal@iitb.ac.in"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Registered on SubEasy! Reset Password"

    body = "Click on this link http://localhost:8000/sedb/reset_password/" + uid + "/"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp-auth.iitb.ac.in', 25)
    server.starttls()
    server.login("kartik_singhal@iitb.ac.in", "yamini@1990")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@instructor1_required
def get_new_prob_no(request, sec_user_id, assign_id):
    assignment = Assignment.objects.get(assignment_id=assign_id)
    assignment.num_problems += 1
    assignment.save()
    return JsonResponse({
        'problem_no': assignment.num_problems
    })


@instructor2_required
def get_assign_prob(request, sec_user_id, assign_id, prob_id):
    print("get_assign_prob called")
    if prob_id == '0':
        return JsonResponse({
            'new_prob': True
        })
    problem = Problem.objects.get(problem_id=prob_id)
    resource = problem.resource_limit
    return JsonResponse({
        'new_prob': False,
        'problem': model_to_dict(problem),
        'resource': model_to_dict(resource)
    })


@instructor1_required
def get_assign_all_prob(request, sec_user_id, assign_id):
    print("all prob called")
    assignment = Assignment.objects.get(assignment_id=assign_id)
    problems = Problem.objects.filter(assignment=assignment)
    prob_json = [{'problem': model_to_dict(problem),
                  'resource': model_to_dict(problem.resource_limit)} for problem in problems]
    return JsonResponse({
        'problems': prob_json
    })


@instructor2_required
def edit_assign_prob(request, sec_user_id, assign_id, prob_id):
    print("edit_assign_prob called")
    problem_id = 0
    assignment = Assignment.objects.get(assignment_id=assign_id)

    if request.method == "POST":
        prob_num = request.POST['prob_num']
        prob_title = request.POST['prob_title']
        description = request.POST['description']
        sol_visibility = (request.POST['sol_visibility'] == '1')
        files_to_submit = request.POST['files_to_submit']
        compile_cmd = request.POST['compile_cmd']
        resources_spec = False;
        try:
            cpu_time = request.POST['cpu_time']
            clock_time = request.POST['clock_time']
            memory_limit = request.POST['memory_limit']
            stack_limit = request.POST['stack_limit']
            open_files = request.POST['open_files']
            max_filesize = request.POST['max_file_size']

            resources_spec = True
        except KeyError:
            pass

        if prob_id == '0':
            print("New problem")
            if resources_spec:
                resource = ResourceLimit(cpu_time=cpu_time, clock_time=clock_time, memory_limit=memory_limit,
                                         stack_limit=stack_limit, open_files=open_files, max_filesize=max_filesize)
                resource.save()
            else:
                resource = ResourceLimit.objects.get(resource_limit_id=1)
            problem = Problem(problem_no=prob_num, title=prob_title, description=description,
                              compile_cmd=compile_cmd, sol_visibility=sol_visibility, assignment=assignment,
                              resource_limit=resource, num_testcases=0, files_to_submit=files_to_submit)
            problem.save()
            problem_id = problem.problem_id
        else:
            problem = Problem.objects.get(problem_id=prob_id)
            resource = problem.resource_limit
            if resources_spec:
                resource.cpu_time = cpu_time
                resource.clock_time = clock_time
                resource.memory_limit = memory_limit
                resource.stack_limit = stack_limit
                resource.open_files = open_files
                resource.max_filesize = max_filesize
                resource.save()

            problem.problem_no = prob_num
            problem.title = prob_title
            problem.description = description
            problem.compile_cmd = compile_cmd
            problem.sol_visibility = sol_visibility
            problem.assignment = assignment
            problem.resource_limit = resource
            problem.files_to_submit = files_to_submit

            problem.save()
            problem_id = problem.problem_id
    return JsonResponse({
        'r_id': problem_id
    })
