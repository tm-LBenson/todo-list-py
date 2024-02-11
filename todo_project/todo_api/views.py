from rest_framework import viewsets
from .models import TodoItem
from .serializers import TodoItemSerializer
from django.shortcuts import render


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer


def index(request):
    return render(request, 'index.html')
