from django.shortcuts import render, redirect
from .models import *
from .helpers import *
from django.http import JsonResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']

        try:
            user = Admin.objects.get(id=id_or_email, password=pwd)
            request.session['admin_id'] = user.id
            request.session['is_admin'] = True
            request.session['is_user'] = False
            request.session.set_expiry(5 * 60)
            return redirect('admin_home')
        except ObjectDoesNotExist:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')


@admin_required
def admin_home(request):
    courses = Course.objects.all()
    for c in courses:
        section = Section.objects.filter(course_id=c.course_id)
        setattr(c, 'section', section)
        for s in section:
            cursor = connection.cursor()
            cursor.execute(
                '''select name from "user" where user_id in (select user_id from sec_user where sec_id =%s);''',
                [s.sec_id])
            setattr(s, 'instructor', cursor.fetchall());
    users = User.objects.all()
    return render(request, 'sedb/admin_home.html', {'courses': courses, 'user': users})


@admin_required
def add_course(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        name = request.POST['name']
        if Course.objects.filter(course_id=course_id).exists():
            print("course already exists")
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
            user = User.objects.get(user_id=id_or_email, password=pwd)
            print("exists")
            request.session['user_id'] = user.user_id
            request.session['is_admin'] = False
            request.session['is_user'] = True
            request.session.set_expiry(5 * 60)
            return redirect('user_home')
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

        if User.objects.filter(user_id = userID).exists():
            messages.add_message(request,messages.ERROR,'User ID already taken')
            return render(request, 'sedb/user_signup.html')

        if User.objects.filter(email = email_id).exists():
            messages.add_message(request,messages.ERROR,'Email ID already taken')
            return render(request, 'sedb/user_signup.html')

        if pwd != cnfrpwd:
            messages.add_message(request,messages.ERROR,'Password do not match')
            return render(request, 'sedb/user_signup.html')

        newuser=User(user_id=userID,name=user_name,email=email_id,password=pwd)
        newuser.save()
        messages.add_message(request,messages.ERROR,'Succesfully Registered')
        return render(request, 'sedb/user_signup.html')
    return render(request, 'sedb/user_signup.html')



def display_section(request):
	if request.method == 'POST':
		secuser = SecUser.objects.get(id=request.POST['sec_id']);
		request.session['sec_id'] = request.POST['sec_id']
		if(secuser.role=="Instructor"):
			return redirect('display_instructor')
		elif(secuser.role=="TA"):
			return redirect('display_ta')
		elif(secuser.role=="Student"):
			return redirect('display_student')


	return render(request, 'sedb/display_section.html')

def display_instructor(request):
	return render(request, 'sedb/display_instructor.html')

def display_ta(request):
	return render(request, 'sedb/display_ta.html')

def display_student(request):
	return render(request, 'sedb/display_student.html')