from django.contrib import admin

# Register your models here.

from .models import GenericData

class GenericDataAdmin (admin.ModelAdmin):

    list_display = ('Jsondata', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['pub_date']

admin.site.register(GenericData,GenericDataAdmin)
