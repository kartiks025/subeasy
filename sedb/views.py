from django.shortcuts import render, redirect
from .models import *
from .helpers import *
from django.http import JsonResponse


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
    courses = Course.objects.all()
    for c in courses:
    	section = Section.objects.filter(course_id=c.course_id)
    	setattr(c,'section',section);
    users = User.objects.all()
    return render(request, 'sedb/admin_home.html', {'courses': courses, 'user':users})


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
    	s = Section(sec_name=request.POST['sec_name'],semester=request.POST['semester'],year=request.POST['year'],course_id=request.POST['course_id'],num_assignments=0)
    	s.save()
    	instructor = request.POST.getlist('instructor')
    	for i in instructor:
    		u = User.objects.filter(user_id=i)
    		secuser = SecUser(role="Instructor",user=u[0],sec=s)
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
