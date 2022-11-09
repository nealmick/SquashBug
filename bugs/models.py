import datetime
from django import forms
from django.db import models
from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from users.models import Profile
from PIL import Image

CHOICES = (
    ('Low',	'Low'),
    ('Medium',	'Medium'),
    ('High',	'High'),
)

class Bug(models.Model):
    Users = models.ManyToManyField(User,default=User)

    severity = models.CharField(max_length=10, choices=CHOICES)
    author = models.ForeignKey(User,related_name ='auth', on_delete=models.CASCADE)

    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True, max_length=1500)
    pic = models.ImageField(upload_to='files')
    open = models.BooleanField(default=True)




    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        
        return reverse('edit-bug',kwargs={'pk': self.pk})
        
        #return reverse('home-bugs')

class File(models.Model):

    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='files')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file.path)


    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs)
        img = Image.open(self.file.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.file.path)






class Comment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(null=True, blank=True, max_length=200)
    author = models.CharField(null=True, blank=True, max_length=50)
    pic = models.ImageField(upload_to='files')
    def __str__(self):
       return str(self.text)




class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }