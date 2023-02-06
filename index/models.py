from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from unittest.util import _MAX_LENGTH

class Course(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    __str__ = lambda self: self.name

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # grabs data from user
    #add info here for classes through SIS API
    class_subject = models.CharField(max_length=5)
    class_number = models.CharField(max_length=5)
    class_section = models.CharField(max_length=5)
    #course = models.ForeignKey(Course, on_delete = models.CASCADE)
class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default="This is the default bio")
    degree = models.CharField(max_length=200, default="Unknown")
    year = models.CharField(max_length=50, default="Unknown")
    __str__ = lambda self: self.bio

class Friend(models.Model):
    # # User who made friend request
    adder = models.ForeignKey(User, on_delete=models.CASCADE)
    # # User who was looked up
    # user name
    addee_uid = models.CharField(max_length=150)
    # birth name 
    addee_nom = models.CharField(max_length=150)

class Meeting(models.Model):
    creation_date = models.DateTimeField('Date Created')
    title_text = models.CharField(max_length=40)
    owner_text = models.CharField(max_length=40)
    description_text = models.CharField(max_length=200)
    date = models.DateField('Date')
    start_date = models.TimeField('Start')
    end_date = models.TimeField('End')
class userMeeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
class Member(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    member_text = models.CharField(max_length=200)
    context_username = models.CharField(max_length=200, default="error")

