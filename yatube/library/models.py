from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100)
    pages = models.IntegerField(min_value=1)
