from django.db import models

from django.utils.timezone import now
# Create your models here.
class Query(models.Model):
    sno=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone=models.CharField(max_length=15)
    email=models.CharField(max_length=100)
    dis=models.CharField(max_length=100)
    age=models.CharField(max_length=10)
    vac=models.CharField(max_length=100)
    date= models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return "Query from "+ self.name