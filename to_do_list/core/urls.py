"""to_do_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from to_do_list_app.views import IndexListView, CreateTaskView, MyTaskView, TaskDetailView, SearchTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('add_task/', CreateTaskView.as_view(), name='add_task'),
    path('index/', IndexListView.as_view(), name='index'),
    path('my_tasks/', MyTaskView.as_view(), name='my_tasks'),
    path('task_detail/<int:id>/', TaskDetailView.as_view(), name='task_detail'),
    path('search_task/', SearchTaskView.as_view(), name='search_task'),


]
