from django.shortcuts import render, redirect
from .models import *
from .helpers import *


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']

        user = Admin.objects.get(id=id_or_email)
        if user.password == pwd:
            print("exists")
            request.session['admin_id'] = user.id
            request.session['is_admin'] = True
            return redirect('admin_home')
        else:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')


@admin_required
def admin_home(request):
    print("hi")
    courses = Course.objects.all()
    return render(request, 'sedb/admin_home.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        name = request.POST['name']
        if Course.objects.filter(course_id=course_id).exists():
            print("course already exists")
        else:
            c = Course(course_id=course_id, name=name)
            c.save()
    return redirect('admin_home');


def delete_course(request):
    return
