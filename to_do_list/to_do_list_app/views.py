from django.shortcuts import render
from django.views import View

from to_do_list_app.forms import AddTaskForm

from to_do_list_app.models import Task

from django.db.models import Q

from datetime import date

today = date.today()

class CreateTaskView(View):

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
            return render (request, 'add_task.html', {'form':form})
        else:
            message = 'Wypełnij poprawnie wszystkie pola'
            return render(request, 'add_task.html', {'form': form, 'message':message})

class IndexView(View):
    def get(self, request):

        tasks = Task.objects.all()


        return render(request, 'index.html', {'tasks':tasks, 'today': today})

class MyTaskView(View):
    def get(self, request):

        user = request.user

        tasks = Task.objects.filter(user=user)

        return render(request, 'my_tasks.html', {'tasks':tasks, 'today': today})

    def post(self, request):

        task_id = request.POST.get('Delete')
        task_status_done = request.POST.get('Status_done')
        task_status_new = request.POST.get('Status_new')

        if task_id:
            task = Task.objects.get(id=task_id)
            task.delete()
        elif task_status_done:
            done_status_task = Task.objects.get(id=task_status_done)
            done_status_task.status = 2
            done_status_task.save()
        elif task_status_new:
            new_status_task = Task.objects.get(id=task_status_new)
            new_status_task.status = 1
            new_status_task.save()

        user = request.user
        tasks = Task.objects.filter(user=user)

        return render(request, 'my_tasks.html', {'tasks':tasks, 'today': today})

class TaskDetailView(View):
    def get(self, request, id):

        task = Task.objects.get(id=id)

        return render(request, 'task_detail.html', {'task':task})

class SearchTaskView(View):
    def get(self, request):

        return render (request, 'search.html')

    def post(self, request):

        task_description = request.POST.get('search')
        tasks = Task.objects.filter(Q(name__contains=task_description) | Q(description__contains=task_description))

        return render(request, 'search.html', {'tasks':tasks, 'today': today})


