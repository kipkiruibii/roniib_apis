from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone


class APICategories(models.Model):
    category = models.TextField(null=True)
    category_short = models.TextField(null=True)

    class Meta:
        db_table = 'APICategories'

    def __str__(self):
        return str(self.category)


class ApiDocumentation(models.Model):
    api_category = models.ForeignKey(APICategories, on_delete=models.CASCADE, default='')
    api_name = models.TextField(null=True)
    short_name = models.TextField(null=True)
    api_intro = models.TextField(null=True)
    api_brief_description = models.TextField(null=True)
    api_image = models.TextField(null=True)
    api_subscribers = models.IntegerField(null=True)
    api_total_requests = models.IntegerField(null=True)

    class Meta:
        db_table = 'ApiDocumentation'

    def __str__(self):
        return str(self.api_name)


class ApiEndpoints(models.Model):
    api_name = models.ForeignKey(ApiDocumentation, on_delete=models.CASCADE)
    endpoint_name = models.TextField(null=True)
    endpoint_url = models.TextField(null=True)
    endpoint_desc = models.TextField(null=True)

    class Meta:
        db_table = 'ApiEndpoints'

    def __str__(self):
        return str(self.api_name)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.TextField(null=True)
    is_verified = models.BooleanField(default=False)
    verf_code = models.TextField(null=True)
    date_created = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'UserDetails'

    def __str__(self):
        return str(self.user.username)


class UserTransactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriber_id = models.TextField(null=True)
    receiver_email = models.TextField(null=True)
    payment_date = models.TextField(null=True)
    transactionId = models.TextField(null=True)
    subscription_type = models.TextField(null=True)
    amount = models.FloatField(null=True)
    dateSub = models.DateTimeField(default=datetime.now(timezone.utc))
    is_successful = models.BooleanField(default=False)

    class Meta:
        db_table = 'UserTransactions'

    def __str__(self):
        return str(self.user.username)


class UserNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True)
    message = models.TextField(null=True)
    dateSent = models.TextField(null=True)

    class Meta:
        db_table = 'UserNotifications'

    def __str__(self):
        return str(self.user.username)


class CustomerQueries(models.Model):
    email = models.TextField(null=True)
    message = models.TextField(null=True)
    is_member = models.BooleanField(default=False)

    class Meta:
        db_table = 'CustomerQueries'

    def __str__(self):
        return str(self.email)


class DailyCounter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    latency = models.IntegerField(null=True)
    errors = models.FloatField(null=True)
    dateSub = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'DailyCounter'

    def __str__(self):
        return str(self.user.username)


class HourData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    error_count = models.IntegerField(null=True)
    formatted_time = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'HourData'

    def __str__(self):
        return f'{self.user.username} || {self.formatted_time.strftime("%d/%m/%Y %H:%M")} || C= {self.count} E= {self.error_count}'


class DayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    error_count = models.IntegerField(null=True)
    formatted_time = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'DayData'

    def __str__(self):
        return f'{self.user.username} || {self.formatted_time.strftime("%d/%m/%Y ")} || C= {self.count} E= {self.error_count}'


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
    token = models.TextField(null=True)
    subscription_level = models.TextField(null=True)
    requests_count = models.IntegerField(null=True)
    token_expiry = models.DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        db_table = 'UserTokens'

    def __str__(self):
        return str(self.user.username)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_code = models.TextField(null=True)
    code_expiry = models.DateTimeField(default=datetime.now(timezone.utc))
    def __str__(self):
        return str(self.user.username)


