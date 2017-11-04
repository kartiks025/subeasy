from django.shortcuts import redirect


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
