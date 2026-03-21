from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Fund( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    first_name = models.CharField( max_length = 255 )
    last_name = models.CharField( max_length = 255 )
    address = models.CharField( max_length = 255 )
    city = models.CharField( max_length = 255 )
    pin = models.IntegerField()
    amount = models.IntegerField()
    
    def __str__(self):
        return f"The fund is given by {self.user.username} with the amount ${self.amount}"
    
    class Meta:
        verbose_name_plural = "Fund"


class PaymentHistory( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    fund_amount = models.IntegerField()
    created_at = models.DateTimeField( auto_now_add = True )
    status = models.BooleanField( default = False )
    
    def __str__(self):
        return self.user.username 
    
    class Meta:
        verbose_name_plural = 'Payment History'