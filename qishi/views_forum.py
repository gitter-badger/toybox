from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime

from markdown import markdown

from qishi.models import Category, Forum, Topic, Post
from qishi.forms_forum import NewPostForm, ReplyPostForm,\
     QuickReplyPostForm, EditPostForm


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
            topic.mainpost = post
            topic.save()
                

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
    ctx['forum']      = forum
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

@login_required
def delete_post(request, post_id):
    """Delete a post with 'post_id'. 
    
    If the post is the mainpost of a topic, replace the post message by a "delete" message.
    """
    post = get_object_or_404(Post, id=post_id)
    topic = post.topic
    #only a staff or the poster can delete the post
    if not (request.user.is_staff or request.user.id == post.posted_by.id):
        return HttpResponse('no right to delete this post') #@TODO @message framework
    if post.topic_post:
        post.message = "Deleted by %s. Originally posted by %s"\
                         % (request.user.username,post.posted_by.username)
        #change the posted_by to a superuser so that the original user cannot 
        #edit the post anymore.
        post.posted_by = User.objects.filter(is_superuser=True)[0]
        post.save()
    else:
        post.delete()
    #TODO: update related topic and forum: num_posts
    return HttpResponseRedirect(reverse("qishi.views_forum.topic", args=[topic.id]))

@login_required
def edit_post(request, post_id):
    """edit a post.
    """
    edit_post = get_object_or_404(Post, id=post_id)
    topic = edit_post.topic
    if not (request.user.is_staff or request.user == edit_post.posted_by):
        return HttpResponse( 'no right')    #@TODO @message framework
        
    if request.method == "POST":
        p = EditPostForm( data = request.POST,instance=edit_post)
        if p.is_valid():
            if edit_post.topic_post:
                topic.subject = p.cleaned_data['subject']
            topic.save()
            edit_post.message = p.cleaned_data['message']
            edit_post.updated_on = datetime.now()
            edit_post.save()
                
        return HttpResponseRedirect(reverse("qishi.views_forum.topic", args=[topic.id]))
    
    form = EditPostForm(instance=edit_post)
    return render(request, "qishi/forum/new_post.html", {
        'form' : form,
        'post_id' : edit_post.id,
        'topic_post' : edit_post.topic_post,
        'edit' : True,
    })
    
@login_required
def like_topic(request, topic_id):
    """like a topic.
    """
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.liked_by.add(request.user)
    topic.num_likes += 1
    topic.save()
    
    return HttpResponseRedirect(reverse("qishi.views_forum.topic", args=[topic.id]))
    
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
        return HttpResponse( 'no right')    #@TODO @message framework
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