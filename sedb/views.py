from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']
        print("called with id = " + id_or_email + " pwd = " + pwd)

        if Admin.objects.filter(id=id_or_email, password=pwd).exists():
            print("exists")
            # login(request, id_or_email)
            return redirect('admin_home');
        else:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')

def admin_home(request):
	courses = Course.objects.all();
	return render(request, 'sedb/admin_home.html', {'courses': courses})

def add_course(request):
	if request.method == 'POST':
		course_id = request.POST['course_id']
		name = request.POST['name']
		if Course.objects.filter(course_id=course_id).exists():
			print("course already exists")
		else:
			c = Course(course_id=course_id, name = name)
			c.save()
	return redirect('admin_home');

def delete_course(request):
	return
