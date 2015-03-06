from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    username = "Please login"
    if request.user.is_authenticated():
        username = request.user.get_full_name()

    return render(request, "qishi/homepage.html", {
        "username" : username,
    })

            

