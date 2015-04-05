from django.db import models
#Group Permission to be added later
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _
from accounts.models import UserProfile



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    ordering = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('-ordering', 'created_on')

    def __unicode__(self):
        return self.name
        
## ===== Forum =====
class Forum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    ordering = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    #@TODO Group and Permission
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name=_('Groups'),
             help_text=_('Only users from these groups can see this category'))

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
        ordering = ('-ordering', '-created_on')


    @models.permalink
    def get_absolute_url(self):
        pass #@TODO reverse()

    def __unicode__(self):
        return self.name

    
    def has_access(self, user):
        if user.is_superuser:
            return True
        if self.groups.exists():
            if user.is_authenticated():
                if not self.groups.filter(user__pk=user.id).exists():
                    return False
            else:
                return False
        return True
    
    def _count_nums_topic(self):
        return self.topic_set.all().count()


class Topic(models.Model):
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    posted_by = models.ForeignKey(User)
    subject = models.CharField(max_length=999)
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)  
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    mainpost = models.ForeignKey('Post', verbose_name='Mainpost',
                related_name='topics', blank=True, null=True)

    #Moderation features
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    is_blog = models.BooleanField(default=False)
    num_likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User,blank=True, null=True,
                        related_name='topics_liked')

    class Meta:
        ordering = ('created_on',) #TODO 
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        pass #@TODO

    def update_state_info(self, commit=True):
        pass #@TODO



class Post(models.Model):
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    posted_by = models.ForeignKey(User)
    message = models.TextField()
    topic_post = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_on',)
        get_latest_by = ('created_on', )

    def __unicode__(self):
        return self.message[:80]

    def subject(self):
        if self.topic_post:
            return _('Topic: %s') % self.topic.subject
        return _('Re: %s') % self.topic.subject
        
    @models.permalink
    def get_absolute_url(self):
        pass #@TODO

