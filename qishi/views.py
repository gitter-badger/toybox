from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated():
        pass

    return render( request, "qishi/homepage.html", {} )


            

