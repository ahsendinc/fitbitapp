from django.contrib import admin

# Register your models here.

from .models import GenericData, AccessTokenInfo, Data

class GenericDataAdmin (admin.ModelAdmin):

    list_display = ('Jsondata', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['pub_date']

class AccessTokenInfoAdmin (admin.ModelAdmin):

	list_display = ('access_token', 'refresh_token', 'scope', 'expires_in', 'user_id', 'token_type', 'pub_date', 'username')
	list_filter = ['user_id', 'scope', 'username', 'pub_date']
	search_fields = ['user_id', 'username', 'pub_date']

class DataAdmin (admin.ModelAdmin):

	list_display = ('user_id', 'date', 'time', 'data_type', 'value')
	list_filter = ['user_id', 'date', 'data_type']
	search_fields = ['user_id', 'date', 'time', 'data_type', 'value']

admin.site.register(GenericData,GenericDataAdmin)
admin.site.register(AccessTokenInfo, AccessTokenInfoAdmin)
admin.site.register(Data, DataAdmin)
