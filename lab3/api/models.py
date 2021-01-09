from django.db import models

class Cat(models.Model):
  name = models.CharField(max_length=200, null=True)
  age = models.IntegerField(null=True)
  sex = models.BooleanField(default=False, null=True)