from django.db import models

# Create your models here.

class Details(models.Model):
    username=models.CharField(max_length=50,unique=True,null=False,blank=False,verbose_name="username")
    name=models.CharField(max_length=50,null=False,blank=False,verbose_name="name")
    email=models.EmailField(verbose_name="email",unique=True)
    # employee=models.BooleanField(verbose_name="employee")
    # customer=models.BooleanField(verbose_name="customer")
    # is_status=models.BooleanField(verbose_name="is_status")
    option=(
        ('employee','employee'),
        ('customer','customer'),
    )
    status=models.CharField(max_length=100, choices=option, verbose_name="status")
    password=models.CharField(verbose_name="password",max_length=50)
    repassword=models.CharField(verbose_name="repassword",max_length=50)



class Leave(models.Model):
    username=models.CharField(max_length=50,verbose_name="username")
    email=models.EmailField(verbose_name="email")
    option=(
        ('casual leave','casual leave'),
        ('sick leave','sick leave'),
        ('medical leave','medical leave'),
        ('vacation leave','vacation leave'),
    )
    leavetype=models.CharField(max_length=100, choices=option, verbose_name="leavetype")
    startdate=models.DateField(verbose_name="startdate")
    enddate=models.DateField(verbose_name="enddate")
    totaldays=models.IntegerField(verbose_name="totaldays",null=False,blank=False)
    reason=models.CharField(verbose_name="reason",max_length=500,null=False,blank=False)
    reqstatus=models.CharField(max_length=100,verbose_name="reqstatus")
    # allowed=models.IntegerField(verbose_name="allowed",default=0)
    # taken=models.IntegerField(verbose_name="taken",default=0)
    # balanace=models.IntegerField(verbose_name="balance",default=0)


