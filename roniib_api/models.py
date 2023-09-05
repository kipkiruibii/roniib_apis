from django.db import models

# Create your models here.

class ApiDocumentation(models.Model):
    api_name=models.CharField(max_length=255)
    introduction=models.TextField(default='intro')
    getting_started=models.TextField(default='getting started')
    authentication=models.TextField(default='authentication')


class ApiEndpoints(models.Model):
    api_name=models.ForeignKey(ApiDocumentation,on_delete=models.CASCADE)