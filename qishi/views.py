from django.shortcuts import render
from django.http import HttpResponse

from qishi.forms_user import UserLoginForm, UserRegisterForm

def home(request):
    if request.user.is_authenticated():
        pass

    return render( request, "qishi/homepage.html", {
        'login_form' : UserLoginForm,
        'register_form' : UserRegisterForm
    })


            

