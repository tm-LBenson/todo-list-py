from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    pass

class Todo(models.Model):
    description = models.charField(max_length=200)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
