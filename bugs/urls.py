


from . import views

from django.urls import include, path
from .views import BugListView,BugCreateView

urlpatterns = [
    path('', views.index, name='index'),
    path('bugs/', BugListView.as_view() , name='home-bugs'),
    path('new/', BugCreateView.as_view(), name='new-bug'),
    path('edit/<int:pk>', views.editBug, name='edit-bug'),
]
