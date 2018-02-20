from django.db import models
from register.models import Studentinfo, Hostels
# Create your models here.

class HostelBranchYear(models.Model):

    year = (
        (1),(2),(3),(4),(5),
    )
    #branches = (())##import from choices of user profile
    branch = models.CharField(max_length=10,blank=False,null=False)
    year = models.IntegerField(choices=year,blank=False,null=False)
    hostel = models.ForeignKey(Hostels, blank=False, null=False)##better keep it as key to hostel model
    start_room = models.PositiveIntegerField(blank=True,null=True)
    end_room = models.PositiveIntegerField(blank=True,null=True)








class Roominfo(models.Model):
    room_no = models.IntegerField(blank=False,null=False)
    hostel = models.ForeignKey(Hostels,blank=False,null=False)
    member1 = models.ForeignKey(Studentinfo,blank=True,null=True)
    member2 = models.ForeignKey(Studentinfo,blank=True,null=True)
    member3 = models.ForeignKey(Studentinfo,blank=True,null=True)
    is_filled = models.BooleanField(default=False)
    in_queue = models.BooleanField(default=False)
    timestamp = models.DateTimeField(blank=True,null=True)
