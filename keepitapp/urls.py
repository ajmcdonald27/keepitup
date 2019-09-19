from django.urls import path

from . import views

app_name = 'keepitapp'
urlpatterns = [
    path('tasks/home/', views.home),
    path('tasks/add/', views.AddTask),
    path('tasks/<name>/', views.TaskView, name='tasklist'),
    path('tasks/remove/<int:task_id>/' , views.DeleteTask),
    path("tasks/check/<int:task_id>/", views.CheckOffTask)

]
