from django.db import models

# Create your models here.
class Data(models.Model):
    text = models.CharField(max_length=100)
    cre_date = models.DateTimeField()