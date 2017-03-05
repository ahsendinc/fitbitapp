from django.db import models
import datetime
from django.utils import timezone


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
