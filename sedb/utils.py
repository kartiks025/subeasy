import tarfile, smtplib, re, json
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
import datetime
import pytz

from io import BytesIO


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
                    if not assign.visibility or assign.publish_time>datetime.datetime.now():
                        print("cannot access this assignment")
                        return doredirect(request, 'sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request, sec_user_id, assign_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap

def user3_required(fun):
    def wrap(request, sec_user_id, assign_id,prob_id):
        print("user3_required")
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
                    if not assign.visibility or assign.publish_time>datetime.datetime.now():
                        print("cannot access this assignment")
                        return doredirect(request, 'sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request, sec_user_id, assign_id,prob_id)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap

def user4_required(fun):
    def wrap(request, sec_user_id, assign_id,prob_id,testcase_no):
        print("user4_required")
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
                    if not assign.visibility or assign.publish_time>datetime.datetime.now():
                        print("cannot access this assignment")
                        return doredirect(request, 'sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request, sec_user_id, assign_id,prob_id,testcase_no)

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
                if not assign.visibility or assign.publish_time>datetime.datetime.now():
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


def student2_required(fun):
    def wrap(request, sec_user_id, assign_id,prob_id):
        print("student2")
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
                if not assign.visibility or assign.publish_time>datetime.datetime.now():
                    print("cannot access this assignment")
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in student_required")
            return doredirect(request, 'sedb:user_login')
        print(sec_user.role)
        return fun(request, sec_user_id, assign_id,prob_id)

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

def diff_time(t1,t2):
    diff = t1 - t2

    days, seconds = diff.days, diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return days,hours,minutes,seconds