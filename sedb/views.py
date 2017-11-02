from django.shortcuts import render
from .models import Admin
from django.contrib.auth import login


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']
        print("called with id = " + id_or_email + " pwd = " + pwd)

        if Admin.objects.filter(id=id_or_email, password=pwd).exists():
            print("exists")
            login(request, id_or_email)
            return render(request, "sedb/admin_home.html")
        else:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')
