from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=100)
