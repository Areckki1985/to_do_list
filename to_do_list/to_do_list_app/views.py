from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from to_do_list_app.forms import TaskForm
from to_do_list_app.models import Task, FINISHED_TASK, NEW_TASK
from to_do_list_app.service import ToDoService


class CreateTaskView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        form = TaskForm

        return render(request, 'add_task.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        to_do_service = ToDoService(request.user)

        if form.is_valid() and request.user.is_authenticated:
            to_do_service.add_new_task(form)

            return HttpResponseRedirect('/index/')
        else:
            message = to_do_service.FAILED_CREATION_MESSAGE
            return render(request, 'add_task.html', {'form': form, 'message': message})


class IndexListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        order = self.request.GET.get('order')
        if order:
            queryset = Task.objects.all().order_by(order)
        else:
            queryset = Task.objects.all()
        return queryset


class MyTaskView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        user = request.user
        order = request.GET.get('order', None)
        page = request.GET.get('page', 1)

        if order:
            task_list = Task.objects.filter(user=user).order_by(order)
        else:
            task_list = Task.objects.filter(user=user)

        paginator = Paginator(task_list, 10)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        return render(request, 'my_tasks.html', {'tasks': tasks, 'today': date.today()})

    def post(self, request):
        delete = request.POST.get('Delete')
        status_done = request.POST.get('Status_done')
        status_new = request.POST.get('Status_new')
        user = request.user
        to_do_service = ToDoService(user)

        if delete:
            to_do_service.delete_task(delete)
        elif status_done:
            to_do_service.set_status_done(status_done)
        elif status_new:
            to_do_service.set_status_new(status_new)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TaskDetailView(View):
    def get(self, request, id):
        task = Task.objects.get(id=id)

        return render(request, 'task_detail.html', {'task': task})


class SearchTaskView(View):
    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        search = request.POST.get('search')
        tasks = Task.objects.filter(Q(name__contains=search) | Q(description__contains=search))

        return render(request, 'search.html', {'tasks': tasks, 'today': date.today()})
