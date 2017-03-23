from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class GenericData (models.Model):

    pub_date = models.DateTimeField(auto_now_add=True)
    Jsondata = models.CharField(max_length=500)

# def __str__(self):
#       return self.pub_date.strftime('%Y-%m-%d %H:%M:%S')
    
    def recent_published(self):
        now = timezone.now()
        return now - datetime.timedelta(minutes=2) <= self.pub_date <= now
        recent_published.admin_order_field = 'pub_date'
        recent_published.boolean = True
        recent_published.short_description = 'Recent Data'

class Data (models.Model):
    
    clientId = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    data_type = models.CharField(max_length=200)
    value = models.FloatField()

# class Profile(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     firstname = models.CharField(max_length=100, blank=True)
#     lastname = models.CharField(max_length=100, blank=True)
#     fitbitid = models.CharField(max_length=100, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
