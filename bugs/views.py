from __future__ import absolute_import, division, print_function, unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Bug
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic import CreateView
from datetime import datetime
from django.template import loader
import requests, json, time, operator, pickle, random
import functools, random
from django.contrib import messages
from .forms import BugUpdateForm
from django.db.models import Q
# Create your views here.




def index(request):
    context = {}
    return render(request, 'bugs/index.html',context)

def completeBug(request, pk):
    b = Bug.objects.filter(pk=pk)
    b.update(open=False)
    p = Profile.objects.filter(user=request.user)
    p.update(userCompletedBugs=p.values('userCompletedBugs')[0]['userCompletedBugs']+1)
    return redirect('home-bugs')



def delBug(request, pk):
    b = Bug.objects.filter(pk=pk)
    s = b.values('severity')[0]['severity']

    p = Profile.objects.filter(user=request.user)
    p.update(userBugs=p.values('userBugs')[0]['userBugs']-1)
    if s =="green":
        p.update(greenBugs=p.values('greenBugs')[0]['greenBugs']-1)
    if s =="yellow":
        p.update(yellowBugs=p.values('yellowBugs')[0]['yellowBugs']-1)

    if s =="red":
        p.update(redBugs=p.values('redBugs')[0]['redBugs']-1)
        
    b.delete()

    return redirect('home-bugs')
def saveBug(request):
    context = {}

    p = Profile.objects.filter(user=request.user)
    id_title = request.GET['id_title']
    id_severity = request.GET['id_severity']
    id_description = request.GET['id_description']
    b = Bug.objects.filter(pk=request.GET['pk'])
    b.update(title=id_title)
    b.update(description=id_description)

    s = b.values('severity')[0]['severity']
    print(id_severity)
    if s != id_severity:
        if s =="green":
            p.update(greenBugs=p.values('greenBugs')[0]['greenBugs']-1)
        if s =="yellow":
            p.update(yellowBugs=p.values('yellowBugs')[0]['yellowBugs']-1)

        if s =="red":
            p.update(redBugs=p.values('redBugs')[0]['redBugs']-1)
        if id_severity == 'green':
            p.update(greenBugs=p.values(id_severity+'Bugs')[0][id_severity+'Bugs']+1)
        if id_severity == 'yellow':
            p.update(yellowBugs=p.values(id_severity+'Bugs')[0][id_severity+'Bugs']+1)
        if id_severity == 'red':
            p.update(redBugs=p.values(id_severity+'Bugs')[0][id_severity+'Bugs']+1)
    
    b.update(severity=id_severity)

    #d = b.values('description')[0]['description']
    #s = b.values('severity')[0]['severity']


    return redirect('home-bugs')


class BugListView(ListView, LoginRequiredMixin):
    model = Bug
    template_name = 'bugs/bugs.html'
    ordering = ['-date']
    paginate_by = 6
    context_object_name = 'bugs'
    context = 'bugs'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BugListView, self).get_context_data(**kwargs)
        p = Profile.objects.filter(user=self.request.user)
        
        context['ub'] =  p.values('userBugs')[0]['userBugs']
        context['ob'] =  p.values('userBugs')[0]['userBugs']-p.values('userCompletedBugs')[0]['userCompletedBugs']
        context['cb'] =  p.values('userCompletedBugs')[0]['userCompletedBugs']
        context['rb'] =  p.values('redBugs')[0]['redBugs']
        context['yb'] =  p.values('yellowBugs')[0]['yellowBugs']
        context['gb'] =  p.values('greenBugs')[0]['greenBugs']


        return context
    def get_queryset(self, **kwargs):
        user = self.request.user

        return Bug.objects.filter(author=user).order_by('-date').exclude(open=False)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
       
        return super().form_valid(form)

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    template_name = 'bugs/new.html'
    fields = ['severity', 'title','description']
    

    def form_valid(self, form, **kwargs):
        s = form.instance.severity
        form.instance.author = self.request.user
        p = Profile.objects.filter(user=self.request.user)

        ub = p.values('userBugs')[0]['userBugs']
        p.update(userBugs=ub+1)

        if s == "red":
            rb = p.values('redBugs')[0]['redBugs']
            p.update(redBugs=rb+1)
        if s == "yellow":
            yb = p.values('yellowBugs')[0]['yellowBugs']
            p.update(yellowBugs=yb+1)
        if s == "green":
            yb = p.values('greenBugs')[0]['greenBugs']
            p.update(greenBugs=yb+1)
            
    

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BugCreateView, self).get_context_data(**kwargs)
        return context
    
@login_required
def editBug(request,pk):
    context = {
        'test': 'test',}


    b = Bug.objects.filter(pk=pk)
    t = b.values('title')[0]['title']
    d = b.values('description')[0]['description']
    s = b.values('severity')[0]['severity']
    context['t'] = t
    context['d'] = d
    context['s'] = s
    context['pk'] = pk

    return render(request, 'bugs/edit.html', context)

@login_required
def FeditBug(request):
    if request.method == 'POST':
        bug_form = BugUpdateForm(request.POST, instance=request.user)
        if bug_form.is_valid():
            bug_form.save()
            messages.success(request, f'Bug Updated!')
            return redirect('home-bugs')
    else:
        bug_form = BugUpdateForm(instance=request.user)
    context = {
        'bug_form': bug_form,
    }
    return render(request, 'bugs/edit.html', context)




    