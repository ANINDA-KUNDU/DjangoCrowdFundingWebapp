from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class PasswordReset( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    reset_id = models.UUIDField( editable = False, unique = True, default = uuid.uuid4 )
    created_at = models.DateTimeField( auto_now_add = True )
    
    def __str__(self):
        return f"The Password Reset is generated for {self.user.username} at {self.created_at}"
    
    class Meta:
        verbose_name_plural = "Password Reset"