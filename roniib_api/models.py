from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone


class APICategories(models.Model):
    category = models.TextField(default='i')
    category_short = models.TextField(default='i')

    def __str__(self):
        return str(self.category)


class ApiDocumentation(models.Model):
    api_category = models.ForeignKey(APICategories, on_delete=models.CASCADE, default='')
    api_name = models.TextField(default='i')
    short_name = models.TextField(default='i')
    api_intro = models.TextField(default='intro')
    api_brief_description = models.TextField(default='intro')
    api_image = models.TextField(default='url_img')
    api_subscribers = models.IntegerField(default=0)
    api_total_requests = models.IntegerField(default=0)

    def __str__(self):
        return str(self.api_name)


class ApiEndpoints(models.Model):
    api_name = models.ForeignKey(ApiDocumentation, on_delete=models.CASCADE)
    endpoint_name = models.TextField(default='fgfgf')
    endpoint_url = models.TextField(default='ghfghghgh')
    endpoint_desc = models.TextField(default='api description')

    def __str__(self):
        return str(self.api_name)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.TextField(default='verfx')
    is_verified = models.BooleanField(default=False)
    verf_code = models.TextField(default='verfx')
    date_created = models.DateTimeField(default=datetime.now(timezone.utc))

    def __str__(self):
        return str(self.user.username)


class UserTransactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriber_id = models.TextField(default='WRDfdFF')
    receiver_email = models.TextField(default='WRDfdFF')
    payment_date = models.TextField(default='WRDfdFF')
    transactionId = models.TextField(default='WRDfdFF')
    subscription_type = models.TextField(default='Basic')
    amount = models.FloatField(default=0)
    dateSub = models.DateTimeField(default=datetime.now(timezone.utc))
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)



