from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length = 20)
    upasswd = models.CharField(max_length = 40)
    uemail = models.CharField(max_length = 30)
    ushou = models.CharField(max_length = 20, default = '')
    uaddress = models.CharField(max_length = 100, default = '')
    uZipcode = models.CharField(max_length = 6, null = True ,default = '')
    uphone = models.CharField(max_length = 11, default = '')
