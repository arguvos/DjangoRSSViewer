from django.db import models
from django.contrib.auth.models import User

class RSS_url(models.Model):
	url = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
	user = models.ForeignKey(User)
	url = models.ForeignKey(RSS_url);
	date = models.DateTimeField(auto_now_add=True)
        show = models.BooleanField(default=True)

class Images(models.Model):
	rss_url = models.ForeignKey(RSS_url)
	image_url = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
