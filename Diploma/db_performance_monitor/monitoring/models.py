from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Database(models.Model):
    PostgreSQL = None
    DB_TYPE_CHOICES = (
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('mongodb', 'MongoDB'),
        # Добавьте другие типы баз данных по мере необходимости
    )

    name = models.CharField(max_length=255, unique=True)
    db_type = models.CharField(max_length=32, choices=DB_TYPE_CHOICES)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class DatabaseMetric(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.database.name} - {self.metric.name} - {self.timestamp}"