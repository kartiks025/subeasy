import smtplib
import pytz
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import *
from django.forms.models import model_to_dict

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bcrypt import hashpw, gensalt
from django.shortcuts import redirect, reverse

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
    def wrap(request):
        try:
            if not request.session['is_user']:
                return redirect('sedb:user_login')
        except KeyError:
            return redirect('sedb:user_login')
        return fun(request)

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
    def wrap(request):
        try:
            if not request.session['is_user']:
                return doredirect(request, 'sedb:user_login')
            else:
                sec_user = SecUser.objects.get(id=request.POST['sec_user_id'])
                if not sec_user.user.user_id == request.session['user_id']:
                    print(sec_user.user.user_id + "," + request.session['user_id'])
                    return doredirect(request, 'sedb:user_login')
        except KeyError:
            print("error in instructor_required")
            return doredirect(request, 'sedb:user_login')
        return fun(request)

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


@instructor_required
def edit_assign_home(request):
    print("edit_assign_home called")

    if request.method == 'POST':
        sec_user_id = request.POST['sec_user_id']
        assign_id = request.POST['assign_id']
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
            deadline = Deadline(soft_deadline=soft_deadline, hard_deadline=hard_deadline,
                                freezing_deadline=freeze_deadline)
            deadline.save()
            assignment = Assignment(assignment_no=assign_num, title=title, description=description,
                                    publish_time=pub_time, visibility=(visibility == '1'), crib_deadline=crib_deadline,
                                    sec=section, num_problems=0, deadline=deadline)

            assignment.save()
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
                assignment.deadline.save()
                assignment.save()
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

    return HttpResponse()


@instructor_required
def get_assign_home(request):
    assignment = Assignment.objects.get(assignment_id=request.POST['assign_id'])
    deadline = assignment.deadline
    context = {'assign': model_to_dict(assignment), 'deadline': model_to_dict(deadline)}
    return JsonResponse(context)
