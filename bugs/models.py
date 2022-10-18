import datetime
from django import forms
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

CHOICES = (
    ('green',	'green'),
    ('yellow',	'yellow'),
    ('red',	'red'),
)

class Bug(models.Model):

    severity = models.CharField(max_length=10, choices=CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True, max_length=1500)
    open = models.BooleanField(default=True)
    def __str__(self):
        return str(self.author)

    def get_absolute_url(self):
        
        return reverse('home-bugs')
        
        #return reverse('home-bugs')
