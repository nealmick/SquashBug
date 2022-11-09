from __future__ import absolute_import, division, print_function, unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from .models import Bug, File,Comment
from users.models import User
from users.models import Profile
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic import CreateView
from datetime import datetime
from django.template import loader
import requests, json, time, operator, pickle, random
import functools, random
from django.contrib import messages
from .forms import BugUpdateForm,addFileForm
from django import forms
from django.db.models import Q
from django.utils import timezone
import jsonpickle
import datetime


#hello

def profileView(request,username):
    try:
        u = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({'asdf': False})
    ui = User.objects.filter(username=username)

    uid = ui.values('pk')[0]['pk']
    context = {'user':u}
    context['ub'] =  len(Bug.objects.filter(Users=uid).all())
    context['ob'] =  len(Bug.objects.filter(Users=uid).exclude(open=False).all())
    context['cb'] =  len(Bug.objects.filter(Users=uid).exclude(open=True).all())
    context['rb'] =  len(Bug.objects.filter(Users=uid).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='Medium'))
    context['yb'] =  len(Bug.objects.filter(Users=uid).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='High'))
    context['gb'] =  len(Bug.objects.filter(Users=uid).order_by('-date').exclude(open=False).exclude(severity='Medium').exclude(severity='High'))


    return render(request, 'bugs/profile.html',context)
def index(request):
    context = {}
    return render(request, 'bugs/index.html',context)
def addComment(request):
    bpk = request.GET['pk']
    if bpk[-1] == '?':
        bpk = bpk.rstrip(bpk[-1])
    comment_text = request.GET['comment']
    bi = Bug.objects.get(pk=bpk)


    u = User.objects.filter(username=request.user)   
    #User.values('profile')[0]['profile']
    p = Profile.objects.filter(pk=u.values('profile')[0]['profile'])
    print(p.values('image')[0]['image'])

    #print(p.values('image')[0]['image'])
    c = Comment(bug=bi,text=comment_text,author=request.user,pic=p.values('image')[0]['image'])

    c.save()

    return JsonResponse({'asdf': 'asdf'})

def loginR(request):
    return redirect('home-bugs','v')
def addUser(request):
    bpk = request.GET['pk']
    if request.GET['pk'][-1]=='?':
        bpk = bpk.rstrip(bpk[-1])

    bI =Bug.objects.get(pk=int(bpk))
    try:
        bI.Users.add(User.objects.get(username=request.GET['userInput']))
    except ObjectDoesNotExist:
        return JsonResponse({'asdf': False})

    return JsonResponse({'asdf': True})

def completeBug(request, pk):
    b = Bug.objects.filter(pk=pk)
    if b.values('open')[0]['open']:
        b.update(open=False)
        p = Profile.objects.filter(user=request.user)
        p.update(userCompletedBugs=p.values('userCompletedBugs')[0]['userCompletedBugs']+1)
    else:
        b.update(open=True)
        p = Profile.objects.filter(user=request.user)
        p.update(userCompletedBugs=p.values('userCompletedBugs')[0]['userCompletedBugs']-1)
        return redirect('home-bugs','closed')

    return redirect('home-bugs','v')


def uncompleteBug(request, pk):
    b = Bug.objects.filter(pk=pk)
    b.update(open=True)
    #testeddate = '4/25/2015'
    #dt_str = datetime.datetime.strftime(timezone.now,'%Y-%m-%d %H:%M:%S')
    #b.update(date=dt_str)
    p = Profile.objects.filter(user=request.user)
    if p.values('userCompletedBugs')[0]['userCompletedBugs']>0:
        p.update(userCompletedBugs=p.values('userCompletedBugs')[0]['userCompletedBugs']-1)
    return redirect('home-bugs','v')
def delFile(request,pk):
    f = File.objects.filter(pk=pk)
    print()
    bid = f.values('bug')[0]['bug']
    print(bid)
    f.delete()
    return redirect('edit-bug',bid)
def delCom(request, pk):
    c = Comment.objects.filter(pk=pk)
    bid = c.values('bug')[0]['bug']
    c.delete()
    return redirect('edit-bug',bid)


def delBug(request, pk):
    b = Bug.objects.filter(pk=pk)
    s = b.values('severity')[0]['severity']

    p = Profile.objects.filter(user=request.user)

    if b.values('open')[0]['open']:
        b.delete()
        return redirect('home-bugs','v')
    else:
        b.delete()
        return redirect('home-bugs','closed')
def saveBug(request):
    context = {}

    p = Profile.objects.filter(user=request.user)
    id_title = request.GET['id_title']
    id_severity = request.GET['id_severity']
    id_description = request.GET['id_description']
    bugUsers = request.GET['bugUsers']
    bugUsers = bugUsers.split(',')
    bugUsersTemp = []

    for bugUser in range(0,len(bugUsers),2):
        bugUsersTemp.append([bugUsers[bugUser],bugUsers[bugUser+1]])
    bugUsers=bugUsersTemp

    trueBU = []
    falseBU = []
    for bugUser in bugUsers:
        if bugUser[1] == "true":
            trueBU.append(bugUser[0])
        else:
            falseBU.append(bugUser[0])

    print(trueBU)
    print(falseBU)
    bpk = request.GET['pk']
    if request.GET['pk'][-1]=='?':
        bpk = bpk.rstrip(bpk[-1])

    b = Bug.objects.filter(pk=int(bpk))
    bI =Bug.objects.get(pk=int(bpk))

    oofL = bI.Users.all()
    fdsa = []
    for test in oofL:
        fdsa.append(str(test))
    oofL = fdsa

    for foo in b.values('Users'):
        print(foo['Users'])
        currentUser = (User.objects.filter(pk=foo['Users']).values('username')[0]['username'])
        print(currentUser)
        if currentUser in trueBU:
            print('checked good '+currentUser)
            
        else:
            print('needs remove '+currentUser)
            bI.Users.remove(User.objects.get(username=currentUser))

    for fooBU in trueBU:
        if fooBU in oofL:
            #print('already added : ', fooBU)
            pass

        else:
            print('adding ',fooBU)
            bI.Users.add(User.objects.get(username=fooBU))
            bI.save()
        #print(User.objects.filter(username=fooBU).values('Bugs'))
            







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


    return redirect('home-bugs','v')



class CompletedListView(ListView, LoginRequiredMixin):
    model = Bug
    template_name = 'bugs/completed.html'
    ordering = ['-date']
    paginate_by = 6
    context_object_name = 'bugs'
    context = 'bugs'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CompletedListView, self).get_context_data(**kwargs)
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

        return Bug.objects.filter(Users=user).order_by('-date').exclude(open=True)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
       
        return super().form_valid(form)

class BugListView(ListView, LoginRequiredMixin):
    model = Bug
    template_name = 'bugs/bugs.html'
    ordering = ['-date']
    paginate_by = 10
    context_object_name = 'bugs'
    context = 'bugs'
    def get_context_data(self, **kwargs):

        user = self.request.user
        context = super(BugListView, self).get_context_data(**kwargs)
        p = Profile.objects.filter(user=self.request.user)
        context['filter'] = self.kwargs['v']
        print()
        context['ub'] =  len(Bug.objects.filter(Users=user).all())
        context['ob'] =  len(Bug.objects.filter(Users=user).exclude(open=False).all())
        context['cb'] =  len(Bug.objects.filter(Users=user).exclude(open=True).all())
        context['rb'] =  len(Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='Medium'))
        context['yb'] =  len(Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='High'))
        context['gb'] =  len(Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Medium').exclude(severity='High'))


        return context
    def get_queryset(self, **kwargs):
        user = self.request.user

        print(self.kwargs['v'])
        if self.kwargs['v'] =='v':
            return Bug.objects.filter(Users=user).order_by('-date').exclude(open=False)
        if self.kwargs['v'] =='high':
            return Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='Medium')
        if self.kwargs['v'] =='medium':
            return Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Low').exclude(severity='High')
        if self.kwargs['v'] =='low':
            return Bug.objects.filter(Users=user).order_by('-date').exclude(open=False).exclude(severity='Medium').exclude(severity='High')
        if self.kwargs['v'] =='total':
            return Bug.objects.filter(Users=user).order_by('-date')
        if self.kwargs['v'] =='closed':
            return Bug.objects.filter(Users=user).order_by('-date').exclude(open=True)
        return Bug.objects.filter(Users=user).order_by('-date').exclude(open=False)

    def form_valid(self, form):
        form.instance.author = self.request.user
       
        return super().form_valid(form)

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    template_name = 'bugs/new.html'
    #form_class = BugUpdateForm
    
    Users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    fields = ['severity', 'title','description']

    def form_valid(self, form, **kwargs):
        s = form.instance.severity
        form.instance.author = self.request.user
        p = Profile.objects.filter(user=self.request.user)

        u = User.objects.filter(username=self.request.user)   
        #User.values('profile')[0]['profile']
        p = Profile.objects.filter(pk=u.values('profile')[0]['profile'])
        print(p.values('image')[0]['image'])
        form.instance.pic = p.values('image')[0]['image']
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
        

        form.instance.save()

        form.instance.Users.set([self.request.user]) 

        form.instance.save()

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        user = self.request.user


        context = super(BugCreateView, self).get_context_data(**kwargs)
        return context
  



@login_required
def editBug(request,pk):
    context = {'test': 'test',}
    b = Bug.objects.filter(pk=pk)
    bi = Bug.objects.get(pk=pk)
    nf = File(bug=bi)

    if request.method == 'POST':

        f_form = addFileForm(request.POST, request.FILES, instance=nf)
        if f_form.is_valid():
            f_form.save()
            return redirect('edit-bug',pk)

    else:
        f_form = addFileForm(instance=nf)



    context['f_form'] = f_form


    files = File.objects.filter(bug=pk).order_by('-date')
    comments = Comment.objects.filter(bug=pk).order_by('-date')
    u = User.objects.filter(pk=b.values('author')[0]['author'])

    t = b.values('title')[0]['title']
    d = b.values('description')[0]['description']
    s = b.values('severity')[0]['severity']
    date = b.values('date')[0]['date']
    context['author'] = u.values('username')[0]['username']



    bUsers = b.values('Users')

    #User.object.filter(pk=pk)


    tempList = []
    for foo in bUsers:
        tempList.append(int(foo['Users']))
    bUsers = tempList

    context['t'] = t
    context['date'] = date
    context['d'] = d
    context['s'] = s
    context['pk'] = pk
    context['files'] = files
    context['comments'] = comments
    idl = User.objects.values_list('pk')

    ful = []
    for id in idl:
        if int(id[0]) in bUsers:
            
            ful.append([User.objects.filter(pk=id[0]).values('username')[0]['username'],True])
            #ful.append([au[0]])
        else:

            ful.append([User.objects.filter(pk=id[0]).values('username')[0]['username'],False])

    context['usersList'] = ful
    allUsersStr = ''
    for foo in User.objects.values_list('username'):
        allUsersStr+=str(foo)+'~'
    context['allUsers'] = allUsersStr

    testdata = ful
    return render(request, 'bugs/edit.html', context)


    