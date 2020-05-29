from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extendeduser(models.Model):
    phone_num = models.CharField(max_length= 15)
    semester = models.IntegerField()
    lid = models.CharField(max_length= 100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)