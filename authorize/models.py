from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class extendeduser(models.Model):
    def __str__(self):
        try:
            return self.user.email + ' : ' + self.user.first_name+' '+self.user.last_name
        except:
            return self.user.first_name+' '+self.user.last_name
    lid = models.CharField(max_length= 100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class ProfileFields(models.Model):
    def __str__(self):
        return self.field
    field = models.CharField(max_length=100)

class FieldValues(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    field = models.ForeignKey(ProfileFields,on_delete=models.CASCADE)
    value = models.TextField()
