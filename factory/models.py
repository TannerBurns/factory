import zlib

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

class Tasks(models.Model):
    class Meta:
        db_table = "factory.tasks"
        app_label = "factory"
    
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="CREATE", max_length=256)
    name = models.CharField(default="UNKNOWN", max_length=256)
    task_id = models.CharField(default="ERROR", max_length=64)
    session = models.CharField(default="NONE", max_length=256)
    start = models.FloatField(default=0)
    runtime = models.FloatField(default=0)
    errors = models.TextField(default="")
    results = CompressedTextField(default="[]")