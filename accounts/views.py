from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm

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
    return render(request, "accounts/login.html", { 
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
            return HttpResponseRedirect('/home/')

        else:
            print( user_form.errors )

    return render(request, "accounts/register.html", { 
        'form' : UserRegisterForm
    })
    
@login_required
def profile(request, user_id=None, template_name="accounts/profile.html"):
    ''' "request.user" try to view his own profile if user_id=None,
    or "view_user"'s profile with a user_id. '''
    
    view_user = request.user
    if user_id:
        view_user = get_object_or_404(User, pk=user_id)
    view_only = view_user != request.user
    ext_ctx = {'view_user'      : view_user, 
               'view_only'      : view_only}
    return render(request, template_name, ext_ctx)