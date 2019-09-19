from django.shortcuts import render, reverse, redirect
from keepitapp.models import Task
from keepitapp.models import User
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
# Create your views here.

def TaskView(request, name):
    current_user = User.objects.get(username=name)
    task_list = Task.objects.filter(user_id=current_user)
    task_completed = {}
    for task in task_list:
        task_completed[task] = task.checked_today()
        if not task_completed[task]:
            # Reset the user's streak if they didn't check off the task yesterday.
            if not task.checked_yesterday():
                task.current_streak = 0
                task.save()

    return render(request, 'tasks.html', {'task_list': task_completed, 'name' : name})

def home(request):
    return HttpResponseRedirect(reverse('keepitapp:tasklist', kwargs={'name': request.user.username}))

def AddTask(request):
    data = request.POST.dict()
    description = data.get('description')
    frequency = data.get('frequency')
    user = request.user
    user.task_set.create(description=description, daily_or_weekly=frequency)
    return HttpResponseRedirect(reverse('keepitapp:tasklist', kwargs={'name': request.user.username}))

def DeleteTask(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return HttpResponseRedirect(reverse('keepitapp:tasklist', kwargs={'name': request.user.username}))

def CheckOffTask(request, task_id):
    task = Task.objects.get(id=task_id)

    task.current_streak = task.current_streak + 1
    task.total_count = task.total_count + 1
    task.last_checked_off = datetime.utcnow()

    if task.best_streak < task.current_streak:
        task.best_streak = task.current_streak

    task.save()
    return HttpResponseRedirect(reverse('keepitapp:tasklist', kwargs={'name': request.user.username}))
