from django.shortcuts import render


# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        id_or_email = request.POST['id_email']
        pwd = request.POST['pwd']
        print("called with id = " + id_or_email + " pwd = " + pwd)

        
    return render(request, 'sedb/admin_login.html')
