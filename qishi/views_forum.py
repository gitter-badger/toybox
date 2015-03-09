from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
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

    posts = Post.objects.all()
    return render(request, "qishi/forum/display_posts.html", {
        'posts' : posts
    })
    
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #only a staff or the poster can delete the post
    if not (request.user.is_staff or request.user.id == post.posted_by.id):
        return HttpResponse('no right to delete this post') #@TODU @message framework
    post.delete()
    #TODO: update related topic and forum
    return HttpResponseRedirect('/qishi/display_posts/' )

    
