from django.shortcuts import render
from .models import Admin


def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']
        print("called with id = " + id_or_email + " pwd = " + pwd)

        if Admin.objects.filter(id=id, password=pwd).exists():
            print("exists")
        else:
            print("doesn't exist")
    return render(request, 'sedb/admin_login.html')
