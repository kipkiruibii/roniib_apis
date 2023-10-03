from django.contrib import admin
from .models import *


admin.site.register(ApiDocumentation)
admin.site.register(ApiEndpoints)
admin.site.register(APICategories)
admin.site.register(UserDetails)
admin.site.register(UserTransactions)
admin.site.register(CustomerQueries)
admin.site.register(DailyCounter)
admin.site.register(CallErrors)
admin.site.register(CallLatency)
admin.site.register(DayData)
admin.site.register(HourData)
admin.site.register(UserTokens)



