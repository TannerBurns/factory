import zlib

from uuid import uuid4
from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Operation(models.Model):
    class Meta:
        db_table = "factory_operation"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default="Unknown", max_length=256)
    docstring = models.TextField(default="")
    hash = models.BigIntegerField(default=0)
    sha256 = models.CharField(unique=True, max_length=256, default="")


class Task(models.Model):
    class Meta:
        db_table = "factory_task"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    task = models.CharField(default=str(uuid4()), max_length=128)
    status = models.CharField(default="CREATED", max_length=256)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="operation")


class Session(models.Model):
    class Meta:
        db_table = "factory_session"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(unique=True, default="None", max_length=256)
    session_id = models.CharField(default=str(uuid4()), max_length=128)
    tasks = models.ManyToManyField(Task, related_name="sessions")


class Runtime(models.Model):
    class Meta:
        db_table = "factory_runtime"
        app_label = "factory"
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, related_name="runtime")
    created = models.DateTimeField(auto_now_add=True)
    start = models.FloatField(default=0)
    stop = models.FloatField(default=0)
    total = models.FloatField(default=0)
    

class Content(models.Model):
    class Meta:
        db_table = "factory_content"
        app_label = "factory"
    
    created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='content', blank=True)
    input_type = models.CharField(max_length=64, default="None")
    input_count = models.IntegerField(default=0)
    input_sha256 = models.CharField(max_length=256, default="")
    output_count = models.IntegerField(default=0)
    output_sha256 = models.CharField(unique=True, max_length=256, default="")
    errors = JSONField(default=list)
    results = JSONField(default=list)



