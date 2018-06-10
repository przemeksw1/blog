from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nickname


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamps = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.id})


class Comment(models.Model):
    comment_text = models.CharField(max_length=300)
    comment_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.comment_text
