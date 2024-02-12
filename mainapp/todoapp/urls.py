from django.urls import path
from .views import TodoView, TodoDetailView, home

urlpatterns = [
    path('todos/', TodoView.as_view(), name='todos'),
    path('todos/<int:id>/', TodoDetailView.as_view(), name='todo_detail'),
    path('', home, name='home'),
]
