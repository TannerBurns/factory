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

class Operation(models.Model):
    class Meta:
        db_table = "factory.operation"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default="Unknown", max_length=256)
    docstring = models.TextField(default="")
    hash = models.IntegerField(default=0)
    sha256 = models.CharField(unique=True, max_length=256, default="")

class Task(models.Model):
    class Meta:
        db_table = "factory.task"
        app_label = "factory"

    created = models.DateTimeField(auto_now_add=True)
    task = models.CharField(default=str(uuid4()), max_length=128)
    session = models.CharField(default=str(uuid4()), max_length=128)
    status = models.CharField(default="CREATED", max_length=256)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="operation")


class Runtime(models.Model):
    class Meta:
        db_table = "factory.runtime"
        app_label = "factory"
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, related_name="runtime")
    created = models.DateTimeField(auto_now_add=True)
    start = models.FloatField(default=0)
    stop = models.FloatField(default=0)
    total = models.FloatField(default=0)
    

class Content(models.Model):
    class Meta:
        db_table = "factory.content"
        app_label = "factory"
    
    created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='content', blank=True)
    input_type = models.CharField(max_length=64, default="None")
    input_count = models.IntegerField(default=0)
    input_sha256 = models.CharField(max_length=256, default="")
    output_count = models.IntegerField(default=0)
    output_sha256 = models.CharField(unique=True, max_length=256, default="")
    errors = CompressedTextField(default="[]")
    results = CompressedTextField(default="[]")



