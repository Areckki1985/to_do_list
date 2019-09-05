from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from to_do_list_app.forms import AddTaskForm
from to_do_list_app.models import Task, FINISHED_TASK, NEW_TASK


class CreateTaskView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        form = AddTaskForm

        return render(request, 'add_task.html', {'form': form})

    def post(self, request):
        form = AddTaskForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            user = request.user
            task = form.save(commit=False)
            task.user = user
            task.save()
            return HttpResponseRedirect('/index/')
        else:
            message = 'Wypełnij poprawnie wszystkie pola'
            return render(request, 'add_task.html', {'form': form, 'message': message})


class IndexListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    paginate_by = 10
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class MyTaskView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        user = request.user
        task_list = Task.objects.filter(user=user)
        page = request.GET.get('page', 1)

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

        if delete:
            task = Task.objects.get(id=delete)
            if user.id == task.user_id:
                task.delete()
        elif status_done:
            done_status_task = Task.objects.get(id=status_done)
            if user.id == done_status_task.user_id:
                done_status_task.status = FINISHED_TASK
                done_status_task.save()
        elif status_new:
            new_status_task = Task.objects.get(id=status_new)
            if user.id == new_status_task.user_id:
                new_status_task.status = NEW_TASK
                new_status_task.save()

        user = request.user
        tasks = Task.objects.filter(user=user)

        return render(request, 'my_tasks.html', {'tasks': tasks, 'today': date.today()})


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
