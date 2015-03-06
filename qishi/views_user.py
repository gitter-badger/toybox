from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from qishi.forms_user import UserLoginForm


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate( username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/home/")
            else:
                # disabled user
                pass
        else:
            # incorrect username/password
            pass

    return _login_page(request)

    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/')

    
def _login_page(request):
    return render(request, "qishi/user/login.html", { 
        'form' : UserLoginForm
    })
