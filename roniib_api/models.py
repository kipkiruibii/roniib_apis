from django.db import models
from django.contrib.auth.models import User


class APICategories(models.Model):
    category = models.CharField(max_length=255)
    category_short = models.CharField(max_length=255)

    def __str__(self):
        return str(self.category)


class ApiDocumentation(models.Model):
    api_category = models.ForeignKey(APICategories, on_delete=models.CASCADE, default='')
    api_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, default='s_name')
    api_intro = models.TextField(default='intro')
    api_brief_description = models.TextField(default='intro')
    api_image = models.CharField(max_length=255, default='url_img')
    api_subscribers = models.IntegerField(default=0)
    api_total_requests = models.IntegerField(default=0)

    def __str__(self):
        return str(self.api_name)


class ApiEndpoints(models.Model):
    api_name = models.ForeignKey(ApiDocumentation, on_delete=models.CASCADE)
    endpoint_name = models.CharField(max_length=255)
    endpoint_url = models.CharField(max_length=255)
    endpoint_desc = models.TextField(default='api description')

    def __str__(self):
        return str(self.api_name)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

