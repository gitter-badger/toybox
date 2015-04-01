from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from markdown import markdown

from qishi.models import Category, Forum, Topic, Post
from qishi.forms_forum import NewPostForm


@login_required
def new_post(request,forum_id, topic_id=None):
    '''
        New post in forum "forum_id".
        If topic_id = None, a new topic is constructed along with a new post.
        Otherwise, a new post (reply) is attached to a topic.
    '''
    forum = get_object_or_404(Forum, pk=forum_id)
    topic = None
    #@TODO if this is a reply, then find the topic with topic_id
    
    if request.method == "POST":
        p = NewPostForm( data = request.POST)
        if p.is_valid():
            # create new form, but don't save the new instance
            #new_post = p.save(commit=False)
            topic_post = False
            if not topic:
                topic = Topic(forum = forum, 
                              posted_by = request.user,
                              subject = p.cleaned_data['subject'],
                              )
                topic_post = True
                topic.save()
            else:
                topic = topic
            post = Post(topic=topic, posted_by=request.user,
                        message=p.cleaned_data['message'], 
                        topic_post=topic_post)
            post.save()
                

        return HttpResponseRedirect(reverse("qishi.views_forum.display_forum", args=[forum.id]))
    
    return render(request, "qishi/forum/new_post.html", {
        'form' : NewPostForm,
        'forum_id' : forum_id
    })
    

@login_required
def display_forum(request, forum_id):
    forum      = get_object_or_404(Forum, pk=forum_id)

    ctx = {}
    ctx['forum_id']   = forum_id
    ctx['topics']     = forum.topic_set.all()
    ctx['categories'] = Category.objects.all()

    return render(request, "qishi/forum/display_forum.html", ctx)
    
@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    forum = topic.forum
    #only a staff or the poster can delete the post
    if not (request.user.is_staff or request.user.id == topic.posted_by.id):
        return HttpResponse('no right to delete this post') #@TODU @message framework
    topic.delete()
    #TODO: update related topic and forum
    return HttpResponseRedirect(reverse("qishi.views_forum.display_forum", args=[forum.id]))

def category(request):
    ctx = {}
    ctx['categories'] = Category.objects.all()
    return render(request, "qishi/forum/categories.html", ctx)

@login_required
def topic(request, topic_id, template_name="qishi/forum/topic.html"):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.num_views += 1
    topic.save()
    posts = topic.posts
    posts = posts.order_by('created_on').select_related()
    ext_ctx = {'topic': topic, 'posts': posts}
    return render(request, template_name, ext_ctx)
    
@login_required
def update_topic_attr_switch(request, topic_id, attr):
    if not request.user.is_staff:
        pass #@TODO
    topic = get_object_or_404(Topic, id=topic_id)
    if attr == 'sticky':
        topic.sticky = not topic.sticky
    elif attr == 'close':
        topic.closed = not topic.closed
    elif attr == 'is_blog':
        topic.is_blog = not topic.is_blog
    topic.save()
    
    return HttpResponseRedirect(reverse("qishi.views_forum.topic", args=[topic.id]))

def blog(request):
    blogs = Topic.objects.filter(is_blog = True)
    ctx = {'blogs': blogs}
    return render(request,"qishi/forum/blog.html", ctx)   
