from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from markdown import markdown

from qishi.models import Post
from qishi.forms_forum import NewPostForm


@login_required
def new_post(request):

    if request.method == "POST":
        p = NewPostForm( data=request.POST )
        if p.is_valid():
            # create new form, but don't save the new instance
            new_post = p.save( commit=False )

            # add user info
            new_post.posted_by = request.user
            new_post.save()

            return HttpResponseRedirect( '/qishi/display_posts/' )
    
    return render(request, "qishi/forum/new_post.html", {
        'form' : NewPostForm
    })
    

@login_required
def display_posts(request):

    posts = [ { 
        'user'    : p.posted_by,
        'message' : markdown( p.message, safe_mode="escape" ),
    } for p in Post.objects.all() ]
    
    return render(request, "qishi/forum/display_posts.html", {
        'posts' : posts
    })
    
