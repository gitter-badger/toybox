from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from qishi.views import home
from qishi.forms_user import UserLoginForm, UserRegisterForm

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

def _login_page(request):
    return render(request, "qishi/user/login.html", { 
        'form' : UserLoginForm
    })

    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/')



def user_register(request):

    if request.method == "POST":
        user_form = UserRegisterForm( data=request.POST )

        if user_form.is_valid():
            #@ToDo: need to check if user already exists

            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method.
            user.set_password(user.password)
            user.save()

            # Login 
            new_user = authenticate( username=request.POST['username'],
                                     password=request.POST['password'] )
            login(request, new_user)
            return HttpResponseRedirect('/qishi/')

        else:
            print( user_form.errors )

    return render(request, "qishi/user/register.html", { 
        'form' : UserRegisterForm
    })
    
