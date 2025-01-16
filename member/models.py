from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
  ph_num = models.CharField(max_length=15, null=False )
  birth = models.DateField(null=False)
  MBTI = models.CharField(max_length=10, null = False)
  addr1 = models.CharField(max_length=10 , default='',blank = True)
  addr2 = models.CharField(max_length=100, default='',blank = True)
  addr3 = models.CharField(max_length=100 , default='',blank = True)
  REQUIRED_FIELDS = ['ph_num','birth','MBTI']
  file_name = models.CharField(max_length=100, blank = True)
  profile = models.CharField(max_length=100, blank = True)

