from django.contrib import admin
from . models import Fund, PaymentHistory
# Register your models here.

admin.site.register( Fund )
admin.site.register( PaymentHistory )