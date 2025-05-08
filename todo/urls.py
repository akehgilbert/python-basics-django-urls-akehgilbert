# todo/urls.py

from django.urls import path
from . import views
app_name = 'todo'
urlpatterns = [
    path('<int:todo_id>/', views.todo_detail, name='todo_detail'),
]
