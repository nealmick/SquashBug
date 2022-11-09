


from . import views

from django.urls import include, path

from .views import BugListView,BugCreateView,CompletedListView

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/adduser/', views.addUser, name='add-user'),
    path('dashboard/<str:v>', BugListView.as_view() , name='home-bugs'),
    path('loginr/', views.loginR, name='login_r'),
    path('completed/', CompletedListView.as_view() , name='completed-bugs'),
    path('new/', BugCreateView.as_view(), name='new-bug'),
    path('edit/save/', views.saveBug, name='save-bug'),
    path('edit/<int:pk>', views.editBug, name='edit-bug'),
    path('edit/comment/', views.addComment, name='comment-bug'),
    path('del/<int:pk>', views.delBug, name='del-bug'),
    path('delcom/<int:pk>', views.delCom, name='del-com'),
    path('delfile/<int:pk>', views.delFile, name='del-file'),
    path('complete/<int:pk>', views.completeBug, name='complete-bug'),
    path('uncomplete/<int:pk>', views.uncompleteBug, name='uncomplete-bug'),
    path('profile/<str:username>', views.profileView, name='profile-view'),

]

path('edit/<int:pk>', views.editBug, name='edit-bug'),