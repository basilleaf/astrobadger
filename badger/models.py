from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    login_name = models.CharField(max_length=500)
    full_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)

# blog post metadata
class Post(models.Model):
    user = models.ForeignKey('User')
    timestamp = models.DateTimeField(auto_now=True)
    word_count = models.IntegerField(null=True, blank=True)
