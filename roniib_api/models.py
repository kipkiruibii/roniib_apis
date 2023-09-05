from django.db import models

# Create your models here.

class ApiDocumentation(models.Model):
    api_name=models.CharField(max_length=255)
    short_name=models.CharField(max_length=255,default='f')
    api_intro=models.TextField(default='intro')
    def __str__(self):
        return str(self.api_name)


class ApiEndpoints(models.Model):
    api_name=models.ForeignKey(ApiDocumentation,on_delete=models.CASCADE)
    endpoint_name=models.CharField(max_length=255)
    endpoint_url=models.CharField(max_length=255)
    endpoint_desc=models.TextField(default='api desc')

    def __str__(self):
        return str(self.api_name)