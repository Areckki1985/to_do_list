from django.shortcuts import render
from django.views import View

from to_do_list_app.forms import AddTaskForm

from to_do_list_app.models import Task

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

        return render(request, 'index.html', {'tasks':tasks})

