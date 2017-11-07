from django.shortcuts import render, redirect
from .models import *
from .helpers import *
from django.http import JsonResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from bcrypt import hashpw, checkpw
import uuid
import hashlib
from datetime import datetime
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    print("login called")
    if request.session.get('is_admin') is not None:
        if request.session['is_admin'] == True:
            return redirect('admin_home')
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']
        try:
            user = Admin.objects.get(id=id_or_email)
            if checkpw(pwd.encode('utf-8'), user.password.encode('utf-8')):
                print("It matches")
                request.session['admin_id'] = user.id
                request.session['is_admin'] = True
                request.session['is_user'] = False
                request.session.set_expiry(5 * 60)
                return redirect('admin_home')
            else:
                print("It does not match")
        except ObjectDoesNotExist:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')


@admin_required
def admin_home(request):
    courses = Course.objects.all().order_by('course_id')
    for c in courses:
        section = Section.objects.filter(course_id=c.course_id).order_by('-year')
        setattr(c, 'section', section)
        for s in section:
            cursor = connection.cursor()
            cursor.execute(
                '''select name from "user" where user_id in (select user_id from sec_user where sec_id =%s);''',
                [s.sec_id])
            row = [item[0] for item in cursor.fetchall()]
            print(row)
            setattr(s, 'instructor', row);
    users = User.objects.all()
    return render(request, 'sedb/admin_home.html', {'courses': courses, 'user': users})


@admin_required
def add_course(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        name = request.POST['name']
        if Course.objects.filter(course_id=course_id).exists():
            print("course already exists")
            messages.add_message(request, messages.ERROR, 'Course ID already exists')
        else:
            c = Course(course_id=course_id, name=name)
            c.save()
    return redirect('admin_home')


@admin_required
def delete_course(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        if Course.objects.filter(course_id=course_id).exists():
            Course.objects.filter(course_id=course_id).delete()
            return JsonResponse({'success': True})
        else:
            print("course doesn't exists")
    return JsonResponse({'success': False})


@admin_required
def add_section(request):
    if request.method == 'POST':
        if Section.objects.filter(sec_name=request.POST['sec_name'], semester=request.POST['semester'],
                                  year=request.POST['year'],
                                  course_id=request.POST['course_id']).exists():
            messages.add_message(request, messages.ERROR, 'Same Section already exists')
        else:
            s = Section(sec_name=request.POST['sec_name'], semester=request.POST['semester'], year=request.POST['year'],
                        course_id=request.POST['course_id'], num_assignments=0)
            s.save()
            instructor = request.POST.getlist('instructor')
            for i in instructor:
                u = User.objects.filter(user_id=i)
                secuser = SecUser(role="Instructor", user=u[0], sec=s)
                secuser.save()
    return redirect('admin_home')


@admin_required
def delete_section(request):
    if request.method == 'POST':
        sec_id = request.POST['sec_id']
        if Section.objects.filter(sec_id=sec_id).exists():
            Section.objects.filter(sec_id=sec_id).delete()
            return JsonResponse({'success': True})
        else:
            print("section doesn't exists")
    return JsonResponse({'success': False})


def user_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']

        try:
            user = User.objects.get(user_id=id_or_email)
            if checkpw(pwd.encode('utf-8'), user.password.encode('utf-8')):
                print("It matches")
                request.session['user_id'] = user.user_id
                request.session['is_admin'] = False
                request.session['is_user'] = True
                request.session.set_expiry(5 * 60)
                return redirect('user_home')
            else:
                print("It does not match")
        except ObjectDoesNotExist:
            print("doesn't exist")
    return render(request, 'sedb/user_login.html')


@user_required
def user_home(request):
    secuser = SecUser.objects.filter(user=request.session['user_id']);
    return render(request, 'sedb/user_home.html', {'section': secuser})


def user_signup(request):
    if request.method == 'POST':
        userID = request.POST['userID']
        user_name = request.POST['user_name']
        email_id = request.POST['email_id']
        pwd = request.POST['pwd']
        cnfrpwd = request.POST['cnfrpwd']

        if User.objects.filter(user_id=userID).exists():
            messages.add_message(request, messages.ERROR, 'User ID already taken')
            return render(request, 'sedb/user_signup.html')

        if User.objects.filter(email=email_id).exists():
            messages.add_message(request, messages.ERROR, 'Email ID already taken')
            return render(request, 'sedb/user_signup.html')

        if VerifyAccount.objects.filter(user_id=userID).exists():
            VerifyAccount.objects.filter(user_id=userID).delete()
        if VerifyAccount.objects.filter(email=email_id).exists():
            VerifyAccount.objects.filter(email=email_id).delete()
        uid = uuid.uuid4().hex
        dt = datetime.now()
        newuser = VerifyAccount(user_id=userID, name=user_name, email=email_id, password=gethashedpwd(pwd),
                                uuid=hashlib.sha256(uid.encode('utf-8')).hexdigest(), timestamp=dt)
        newuser.save()
        send_verify_account_email(uid, email_id)
        messages.add_message(request, messages.ERROR, 'Succesfully Registered')
        return render(request, 'sedb/user_signup.html')
    return render(request, 'sedb/user_signup.html')


@user_required
def display_section(request):
    if request.method == 'POST':
        secuser = SecUser.objects.get(id=request.POST['sec_id']);
        request.session['sec_id'] = request.POST['sec_id']
        if secuser.role == "Instructor":
            return redirect('display_instructor')
        elif secuser.role == "TA":
            return redirect('display_ta')
        elif secuser.role == "Student":
            return redirect('display_student')

    return render(request, 'sedb/display_section.html')


@user_required
def display_instructor(request):
    users = User.objects.all()
    return render(request, 'sedb/display_instructor.html',{'user' :users})


@user_required
def display_ta(request):
    return render(request, 'sedb/display_ta.html')


@user_required
def display_student(request):
    return render(request, 'sedb/display_student.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        ResetPassword.objects.filter(email=email).delete()
        print(email)
        if User.objects.filter(email=email).exists():
            print("yes")
            u = User.objects.get(email=email);
            uid = uuid.uuid4().hex
            dt = datetime.now()
            print(uid)
            print()
            rs = ResetPassword(email_id=email, uuid=hashlib.sha256(uid.encode('utf-8')).hexdigest(), timestamp=dt)
            rs.save()
            send_forgot_password_email(uid, email)
    return render(request, 'sedb/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        print("yes")
    return render(request, 'sedb/forgot_password.html')

@user_required
def add_assignment(request):
    return render(request, 'sedb/add_assignment.html')


def verify_account(request, uid):
    print(uid)
    if VerifyAccount.objects.filter(uuid=hashlib.sha256(uid.encode('utf-8')).hexdigest()).exists():
        va = VerifyAccount.objects.get(uuid=hashlib.sha256(uid.encode('utf-8')).hexdigest())
        u = User(user_id=va.user_id, email=va.email, password=va.password, name=va.name)
        u.save()
        va.delete()
        return render(request, 'sedb/verify_account.html')
    else:
        return redirect('user_login')


def reset_password(request, uid):
    request.session['uid'] = uid
    return render(request, 'sedb/reset_password.html')


def change_password(request):
    if request.method == 'POST':
        uid = request.session['uid']
        print(request.session['uid'])
        print(hashlib.sha256(uid.encode('utf-8')).hexdigest())
        rp = ResetPassword.objects.get(uuid=hashlib.sha256(uid.encode('utf-8')).hexdigest())
        u = User.objects.get(email=rp.email_id)
        u.password = gethashedpwd(request.POST['pwd'])
        u.save()
        print("done-dana-dan")
    return redirect('user_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    if request.session.get('is_admin') is not None:
        if request.session['is_admin']:
            request.session.delete()
    return redirect('admin_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    if request.session.get('is_user') is not None:
        if request.session['is_user']:
            request.session.delete()
    return redirect('user_login')

@user_required
def add_ta(request):
	if request.method == 'POST':
		ta = request.POST.getlist('ta')
		for i in ta:
		    u = User.objects.get(user_id=i)
		    secuser = SecUser(role="TA", user=u, sec_id=request.session['sec_id'])
		    secuser.save()
	return redirect('display_instructor')