from django.urls import path
from .views import list_todos, create_todo, home, edit_todo_form, update_todo, todo_detail, delete_todo

urlpatterns = [
    path('todos/', list_todos, name='list_todos'),
    path('todos/create', create_todo, name='create_todo'),
    path('todos/<int:id>/update', update_todo, name='update_todo'), 
    path('todos/<int:id>/', todo_detail, name='todo_detail'),
    path('todos/<int:id>/delete', delete_todo, name='delete_todo'),
    path('todos/<int:id>/edit', edit_todo_form, name='edit_todo_form'),
    path('', home, name='home'),
]
