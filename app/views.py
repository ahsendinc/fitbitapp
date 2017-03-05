from django.shortcuts import render
from django.http import HttpResponse
import fitbit
import requests
from django.contrib.auth.decorators import login_required
from fitapp.decorators import fitbit_integration_warning
from app.models import GenericData
import json

@fitbit_integration_warning(msg="Integrate your account with Fitbit!")
@login_required
def my_view(request):
    return HttpResponse('Visible to authenticated users regardless' + 'of Fitbit integration status')

def index(request):
    client_id = '2285HX'
    client_secret = '43946f221a787192879d7242ea24adfa'
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1RzVMOUciLCJhdWQiOiIyMjg1SFgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNDg4NzI5MjYxLCJpYXQiOjE0ODg3MDA0NjF9.cNhdCHqPxTxRE-2qls4qLgxWkEHQKsfqLMipPKzMRb8'
    refresh_token = 'dbd188d9d0de868117888e198d57034ca0f3c179871c4b3399ddb72e1f270b43'
    expires_at = 28800

#return requests.get("https://api.fitbit.com/1/user/5G5L9G/profile.json").json()

#unauth_client = fitbit.Fitbit('2285HX','43946f221a787192879d7242ea24adfa')
    #user_params = unauth_client.user_profile_get(user_id='5G5L9G')
    #unauth_client.food_units()
    #url = 'https://api.fitbit.com/oauth2/token'
    headers= {'content-type':'application/x-www-form-urlencoded', 'Authorization':'Basic MjI4NUhYOjQzOTQ2ZjIyMWE3ODcxOTI4NzlkNzI0MmVhMjRhZGZh'}
    query= {"client_id":"2285HX","grant_type":"authorization_code","redirect_uri":"http://127.0.0.1:8000/app","code":"32691e4342408da7d94d7e345ff1c3075c44faeb"}
    #res = requests.post(url,headers=headers,data=query)
    header = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1RzVMOUciLCJhdWQiOiIyMjg1SFgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNDg4NzI5MjYxLCJpYXQiOjE0ODg3MDA0NjF9.cNhdCHqPxTxRE-2qls4qLgxWkEHQKsfqLMipPKzMRb8'}
    response = requests.get("https://api.fitbit.com/1/user/5G5L9G/activities/heart/date/2017-03-01/1d.json",headers=header)

    auth_client = fitbit.Fitbit(client_id, client_secret, access_token=access_token, refresh_token=refresh_token)
    res = auth_client.heart(date= '2017-03-02', user_id='5G5L9G')
    objs = json.loads(response.text)
    

    #user_params = unauth_client.user_profile_get(user_id='5G5L9G')
    response1 = GenericData.objects.create(Jsondata=response.text)
    
# return HttpResponse("Fitbit!")
    return HttpResponse(objs['activities-heart'][0]['value']['heartRateZones'][0]['min'])
#return HttpResponse(requests.get("https://api.fitbit.com/1/user/5G5L9G/profile.json"))
#return HttpResponse(res)


def data(request):
    unauth_client = fitbit.Fitbit('2285HX','43946f221a787192879d7242ea24adfa')
    user_params = unauth_client.user_profile_get(user_id='5G5L9G')
    unauth_client.food_units()
    return HttpResponse("Fitbit!")
#http://127.0.0.1:8000/app/?code=5080a09ec06919e9fa4562f97b9382b60504a207
#code=5adf26feacf45d63bfc645e95e5f1b5e3cea7ba1 =>for sleep

#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2285HX&redirect_uri=http://127.0.0.1:8000/app&scope=sleep%20heartrate%20activity%20location%20nutrition%20profile%20settings%20social%20weight
#resulting code=0233c47ff3a573107e0c7c091e7cd7e1da38c6d6

#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2285HX&redirect_uri=http://127.0.0.1:8000/app&code=0233c47ff3a573107e0c7c091e7cd7e1da38c6d6

#client_id=22942C&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fexample.com%2Ffitbit_auth&code=1234567890


#https://api.fitbit.com/oauth2/token?client_id=2285HX&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/app&code=32691e4342408da7d94d7e345ff1c3075c44faeb

#"access_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1RzVMOUciLCJhdWQiOiIyMjg1SFgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNDg4NTM0MzYzLCJpYXQiOjE0ODg1MDU1NjN9.V3OTxYTYkJgB7G4uml8GkPC4ftX6Y50wLC4SL4G4l3M","expires_in": 28800,"refresh_token": "4dd124e3b93ca2d550d4e9e357c36b1aff2a7ad5c6bf2be8232fef82cbc17693","scope": "location heartrate nutrition social sleep activity settings weight profile","token_type": "Bearer","user_id": "5G5L9G"
