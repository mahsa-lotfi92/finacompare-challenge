from django.db import models


class Contact(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

