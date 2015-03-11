from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User,related_name='user_profile')

    # Other fields here
    #@TODO last_activity = models.DateTimeField(auto_now_add=True)
    #@TODO last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=1000, blank=True)
    #@TODO: delete later
    favorite_animal = models.CharField(max_length=20, default="Dragons.")
    
    def __unicode__(self):
        return self.user.username

    #@TODO def get_total_posts(self):
       
    def get_absolute_url(self):
        return self.user.get_absolute_url()


""" signals """

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)