from django.contrib import admin
from .models import Bug,MyModelAdmin,File,Comment
# Register your models here.
admin.site.register(Bug,MyModelAdmin)
admin.site.register(File)
admin.site.register(Comment)
