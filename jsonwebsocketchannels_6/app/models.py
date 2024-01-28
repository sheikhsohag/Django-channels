from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class Chat(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now = True)
    content = models.CharField(max_length = 500)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    
