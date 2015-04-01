from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from markdown import markdown

from qishi.models import Category, Forum, Topic, Post
from qishi.forms_forum import NewPostForm, ReplyPostForm, QuickReplyPostForm


@login_required
def new_post(request,forum_id):
    '''New post in the forum with "forum_id".
    '''
    forum = get_object_or_404(Forum, pk=forum_id)
    topic_post = True

    if request.method == "POST":
        p = NewPostForm( data = request.POST)
        if p.is_valid():
            topic = Topic(forum = forum, 
                          posted_by = request.user,
                          subject = p.cleaned_data['subject'],
                          )
            topic.save()
            post = Post(topic=topic, posted_by=request.user,
                        message=p.cleaned_data['message'], 
                        topic_post=topic_post)
            post.save()
                

        return HttpResponseRedirect(reverse("qishi.views_forum.display_forum", args=[forum.id]))
    
    return render(request, "qishi/forum/new_post.html", {
        'form' : NewPostForm,
        'forum_id' : forum_id,
        'topic_post' : topic_post,
    })
@login_required
def new_reply(request, topic_id):  
    '''New reply in the topic with "topic_id".
    '''
    topic = get_object_or_404(Topic, pk=topic_id)
    forum = topic.forum 
    topic_post = False
    if request.method == "POST":
        p = ReplyPostForm( data = request.POST)
        if p.is_valid():
            
            post = Post(topic=topic, posted_by=request.user,
                        message=p.cleaned_data['message'], 
                        topic_post=topic_post)
            post.save()
                

        return HttpResponseRedirect(reverse("qishi.views_forum.topic", args=[topic.id]))
    
    return render(request, "qishi/forum/new_post.html", {
        'form' : ReplyPostForm,
        'topic_id' : topic.id,
        'topic_post' : topic_post,
    })

@login_required
def display_forum(request, forum_id):
    """ view function for display a forum with 'forum_id'
    """
    forum      = get_object_or_404(Forum, pk=forum_id)

    ctx = {}
    ctx['forum_id']   = forum_id
    ctx['topics']     = forum.topic_set.all()
    ctx['categories'] = Category.objects.all()

    return render(request, "qishi/forum/display_forum.html", ctx)
    
@login_required
def delete_topic(request, topic_id):
    """Delete a topic with 'topic_id'. 
    
    The related posts will be deleted as well.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    forum = topic.forum
    #only a staff or the poster can delete the post
    if not (request.user.is_staff or request.user.id == topic.posted_by.id):
        return HttpResponse('no right to delete this post') #@TODO @message framework
    topic.delete()
    #TODO: update related topic and forum
    return HttpResponseRedirect(reverse("qishi.views_forum.display_forum", args=[forum.id]))
    
def category(request):
    """ View function to show all forums grouped by categories.
    """
    ctx = {}
    ctx['categories'] = Category.objects.all()
    return render(request, "qishi/forum/categories.html", ctx)

@login_required
def topic(request, topic_id, template_name="qishi/forum/topic.html"):
    """Display a topic with 'topic_id'.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    topic.num_views += 1
    topic.save()
    posts = topic.posts
    posts = posts.order_by('created_on').select_related()
    ext_ctx = {'topic': topic, 'posts': posts,'form' : QuickReplyPostForm,}
    return render(request, template_name, ext_ctx)
    
@login_required
def update_topic_attr_switch(request, topic_id, attr):
    """Update topic attribute 'attr' for a topic with 'topic_id'.
    
    This function works as a switch. The attribute switches between True and False.
    """
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
    """Display all blog articles.
    
    Blog articles are topics with 'is_blog'=True.
    """
    blogs = Topic.objects.filter(is_blog = True)
    ctx = {'blogs': blogs}
    return render(request,"qishi/forum/blog.html", ctx)   