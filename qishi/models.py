from django.db import models

from django.contrib.auth.models import User

class Post(models.Model):
    posted_by = models.ForeignKey(User)
    message = models.TextField()

