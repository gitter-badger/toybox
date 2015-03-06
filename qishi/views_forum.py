from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from markdown import markdown

from qishi.forms_forum import NewPostForm


@login_required
def new_post(request):

    if request.method == "POST":
        # Article has been submitted
        post_info = { 'text' : request.POST['edit_area'] }
        url = reverse( 'qishi.views_forum.display_post', args=(request, ) )
        return HttpResponseRedirect(url)
    
    return render(request, "qishi/forum/new_post.html", {
        'form' : NewPostForm
    })
    


def display_post(request):
    post_info = { 'text' : 'hello world' }
    text = markdown(post_info['text'], safe_mode="escape")

    return render(request, "qishi/forum/display_post.html", {
        'text' : text
    })
    
