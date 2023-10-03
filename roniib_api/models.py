from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone


class APICategories(models.Model):
    category = models.TextField(default='i')
    category_short = models.TextField(default='i')

    class Meta:
        db_table = 'APICategories'

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

    class Meta:
        db_table = 'ApiDocumentation'

    def __str__(self):
        return str(self.api_name)


class ApiEndpoints(models.Model):
    api_name = models.ForeignKey(ApiDocumentation, on_delete=models.CASCADE)
    endpoint_name = models.TextField(default='fgfgf')
    endpoint_url = models.TextField(default='ghfghghgh')
    endpoint_desc = models.TextField(default='api description')

    class Meta:
        db_table = 'ApiEndpoints'

    def __str__(self):
        return str(self.api_name)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.TextField(default='verfx')
    is_verified = models.BooleanField(default=False)
    verf_code = models.TextField(default='verfx')
    date_created = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'UserDetails'

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

    class Meta:
        db_table = 'UserTransactions'

    def __str__(self):
        return str(self.user.username)


class UserNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default='title')
    message = models.TextField(default='message')
    dateSent = models.TextField(default='datesent')

    class Meta:
        db_table = 'UserNotifications'

    def __str__(self):
        return str(self.user.username)


class CustomerQueries(models.Model):
    email = models.TextField(default='title')
    message = models.TextField(default='message')
    is_member = models.BooleanField(default=False)

    class Meta:
        db_table = 'CustomerQueries'

    def __str__(self):
        return str(self.email)


class DailyCounter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    latency = models.IntegerField(null=True)
    errors = models.FloatField(null=True, default=0.0)
    dateSub = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'DailyCounter'

    def __str__(self):
        return str(self.user.username)


class HourData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    formatted_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'HourData'

    def __str__(self):
        return str(self.user.username)


class DayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    formatted_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'DayData'

    def __str__(self):
        return str(self.user.username)


class CallErrors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    class Meta:
        db_table = 'CallErrors'

    def __str__(self):
        return str(self.user.username)


class CallLatency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    class Meta:
        db_table = 'CallLatency'

    def __str__(self):
        return str(self.user.username)


class UserTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    subscription_level = models.TextField(default='Basic')
    requests_count = models.IntegerField(default=100)
    token_expiry = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'UserTokens'

    def __str__(self):
        return str(self.user.username)
