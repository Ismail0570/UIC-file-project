from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField()
    shared_with = models.ManyToManyField(User, related_name='shared_files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    files = models.ManyToManyField(File)
    created_at = models.DateTimeField(auto_now_add=True)