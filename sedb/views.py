from django.shortcuts import render, redirect
from .models import *


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']

        user = Admin.objects.get(id=id_or_email)
        if user.password == pwd:
            print("exists")
            request.session['admin_id'] = user.id
            return redirect('admin_home')
        else:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')


def admin_home(request):
    courses = Course.objects.all()
    return render(request, 'sedb/admin_home.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        name = request.POST['course_id']
        return redirect('admin_home');
