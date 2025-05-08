from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import todos

# Create your views here.
# todo/views.py


def home(request):
    first_todo_url = reverse('todo:todo_detail', args=[1])
    html = f"""
        <h1>Welcome to my To-Do list!</h1>
        <p><a href="{first_todo_url}">Read my first todo</a></p>
    """
    return HttpResponse(html)


def todo_detail(request, todo_id):
    if todo_id < 1 or todo_id > len(todos):
        raise Http404("To-Do not found")

    todo = todos[todo_id - 1]
    text = todo['text']
    topic = todo['topic']
    status = todo['status']

    prev_link = ""
    next_link = ""

    if todo_id > 1:
        prev_url = reverse('todo:todo_detail', args=[todo_id - 1])
        prev_link = f'<a href="{prev_url}">previous todo</a>'
    else:
        prev_link = "previous todo"

    if todo_id < len(todos):
        next_url = reverse('todo:todo_detail', args=[todo_id + 1])
        next_link = f'<a href="{next_url}">next todo</a>'
    else:
        next_link = "next todo"

    home_url = reverse('home')
    home_link = f'<a href="{home_url}">Back to home</a>'

    html = f"""
        <h1>To Do number {todo_id}</h1>
        <h2>{topic}</h2>
        <p>{text}</p>
        <p>Status: {status}</p>
        <p>{prev_link} | {home_link} | {next_link}</p>
    """
    return HttpResponse(html)
