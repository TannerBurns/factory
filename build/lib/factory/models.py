import zlib

from uuid import uuid4
from django.db import models

# Create your models here.

class CompressedTextField(models.TextField):
    def __init__(self, compress_level=8, *args, **kwargs):
        self.compress_level = compress_level
        super(CompressedTextField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        value = super(CompressedTextField, self).to_python(value)
        return zlib.compress(value.encode(), self.compress_level)
    
    def get_prep_value(self, value):
        value = super(CompressedTextField, self).get_prep_value(value)
        return zlib.decompress(value).decode()

class Session(models.Model):
    class Meta:
        db_table = "factory.session"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(unique=True, default=str(uuid4()), max_length=128)

class Task(models.Model):
    class Meta:
        db_table = "factory.task"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(default=str(uuid4()), max_length=128)
    status = models.CharField(default="CREATED", max_length=256)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session")

class Operation(models.Model):
    class Meta:
        db_table = "factory.operation"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, related_name='operation')
    name = models.CharField(default="", max_length=256)
    docstring = models.TextField(default="")


class Runtime(models.Model):
    class Meta:
        db_table = "factory.runtime"
        app_label = "factory"
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, related_name="runtime")
    start = models.FloatField(default=0)
    stop = models.FloatField(default=0)
    runtime = models.FloatField(default=0)
    

class Content(models.Model):
    class Meta:
        db_table = "factory.content"
        app_label = "factory"
    
    created = models.DateTimeField(auto_now_add=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, related_name='content')
    errors = CompressedTextField(default="[]")
    results = CompressedTextField(default="[]")



