from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from qishi.forms_forum import NewPostForm


@login_required
def new_post(request):
    if request.method == "POST":
        # Article has been submitted
        print(request.POST["edit_area"])
        pass

    return render(request, "qishi/forum/new_post.html", {
        'form' : NewPostForm
    })
    
