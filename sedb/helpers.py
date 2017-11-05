from django.shortcuts import redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bcrypt import hashpw, gensalt

def admin_required(fun):
    def wrap(request):
        try:
            if not request.session['is_admin']:
                return redirect('admin_login')
        except KeyError:
            return redirect('admin_login')
        return fun(request)
    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap

def user_required(fun):
    def wrap(request):
        try:
            if not request.session['is_user']:
                return redirect('user_login')
        except KeyError:
            return redirect('user_login')
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

print(gethashedpwd("kartik"))
print(gethashedpwd("pranay"))