from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Producer(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    title = models.CharField(max_length=100)


class Films(models.Model):
    title = models.CharField(max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_films = models.ManyToManyField(Films, related_name='favorited_by_users')
