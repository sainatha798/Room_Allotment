from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Hostels(models.Model):
    hostels = (
        ('SNBOSE'),
        ('Ramanujan'),
        ('Aryabhatt-A'),
        ('Aryabhatt-B'),
        ('Aryabhatt-C'),
        ('DG'),
        ('Morvi'),
        ('C.V.Raman'),
        ('RJ'),
        ('Limbdi'),
        ('S.C.Dey'),
        ('vivekananda'),
        ('vK'),
        ('gsmc old'),
        ('gsmc new'),
    )
    hostel = models.CharField(max_length=15,choices=hostels)
    Room_Count = models.PositiveIntegerField(blank=False,null=False)
    per_room = models.PositiveIntegerField(blank=False,null=True)


class Studentinfo(models.Model):

    mobile_no = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=False,related_name='personal')
    profile_picture = models.FileField(default=None, null=True,blank=True)
    dob = models.DateField(null=True)
    roll_no = models.PositiveIntegerField(max_length=10,null=False,blank=False)
    dept = models.CharField(max_length=50,blank=True,null=True)
    year = models.PositiveIntegerField(blank=True,null=True)
    hostel = models.ForeignKey(Hostels, blank=True,null=True)


    def __str__(self):
        return self.user.username

    ##def get_absolute_url(self):
        ##return reverse('index')


