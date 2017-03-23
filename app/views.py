from django.shortcuts import render
from django.http import HttpResponse
import fitbit
import requests
from django.contrib.auth.decorators import login_required
from fitapp.decorators import fitbit_integration_warning
from app.models import GenericData
import json
import configparser
from django.conf import settings
from django.db import transaction
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect    
from django.contrib import auth                 
from app.forms import MyRegistrationForm

@fitbit_integration_warning(msg="Integrate your account with Fitbit!")
@login_required
def my_view(request):
    return HttpResponse('Visible to authenticated users regardless' + 'of Fitbit integration status')

def index(request):
   #Load Settings
    consumer_key = settings.FITAPP_CONSUMER_KEY
    consumer_secret = settings.FITAPP_CONSUMER_SECRET

    unauth_client = fitbit.Fitbit(consumer_key,consumer_secret)
    user_params = unauth_client.user_profile_get(user_id='5G5L9G')

    return HttpResponse(user_params)

def refreshtoken(refresh_token):
    url = 'https://api.fitbit.com/oauth2/token'
    header= {'content-type':'application/x-www-form-urlencoded', 'Authorization':'Basic MjI4NUhYOjQzOTQ2ZjIyMWE3ODcxOTI4NzlkNzI0MmVhMjRhZGZh'}
    query= {"grant_type":"refresh_token","refresh_token":refresh_token}
    response = requests.post(url,headers=header)
    return response.text

def data(request):
    unauth_client = fitbit.Fitbit('2285HX','43946f221a787192879d7242ea24adfa')
    user_params = unauth_client.user_profile_get(user_id='5G5L9G')
    unauth_client.food_units()
    return HttpResponse("Fitbit!")


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return HttpResponse("logged in!")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("invalid!")

def logout_view(request):
    logout(request)
    # Redirect to a success page.

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/accounts/register_success')
            return HttpResponse("registered")
    # args = {}
    # args.update(csrf(request))
    # args['form'] = MyRegistrationForm()
    #print args
    return render(request, 'index.html', {
        'form': MyRegistrationForm(),
    })

# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
#http://127.0.0.1:8000/app/?code=5080a09ec06919e9fa4562f97b9382b60504a207
#code=5adf26feacf45d63bfc645e95e5f1b5e3cea7ba1 =>for sleep

#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2285HX&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapp%2F&scope=sleep%20heartrate%20activity%20location%20nutrition%20profile%20settings%20social%20weight
#resulting code=0233c47ff3a573107e0c7c091e7cd7e1da38c6d6

#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2285HX&redirect_uri=http://127.0.0.1:8000/app&code=004c0d2c81b6c2c2f658303712a5e99d3f3a4fe3#_=_

#client_id=22942C&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fexample.com%2Ffitbit_auth&code=1234567890


#https://api.fitbit.com/oauth2/token?client_id=2285HX&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/app&code=004c0d2c81b6c2c2f658303712a5e99d3f3a4fe3

#"access_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1RzVMOUciLCJhdWQiOiIyMjg1SFgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNDg4NTM0MzYzLCJpYXQiOjE0ODg1MDU1NjN9.V3OTxYTYkJgB7G4uml8GkPC4ftX6Y50wLC4SL4G4l3M","expires_in": 28800,"refresh_token": "4dd124e3b93ca2d550d4e9e357c36b1aff2a7ad5c6bf2be8232fef82cbc17693","scope": "location heartrate nutrition social sleep activity settings weight profile","token_type": "Bearer","user_id": "5G5L9G"



#----past code---
#  client_id = '2285HX'
#     client_secret = '43946f221a787192879d7242ea24adfa'
#     access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1RzVMOUciLCJhdWQiOiIyMjg1SFgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNDg5MTI5OTg5LCJpYXQiOjE0ODkxMDExODl9.xQRbh6Yt0f9Oipdy2ovEzEJ_0FLPuiPNwwZMgt4rrS8'
#     refresh_token = '73e37ee10e0e9dc40ce8fde453bbaceb3d216fbf25f3994b3bcd9bef0d159b22'
#     expires_at = 28800
    
#     tokentxt = refreshtoken(refresh_token)
#     tokenobj = json.loads(tokentxt)
#     GenericData.objects.create(Jsondata=tokentxt)
    
# #return requests.get("https://api.fitbit.com/1/user/5G5L9G/profile.json").json()

# #unauth_client = fitbit.Fitbit('2285HX','43946f221a787192879d7242ea24adfa')
#     #user_params = unauth_client.user_profile_get(user_id='5G5L9G')
#     #unauth_client.food_units()
#     #url = 'https://api.fitbit.com/oauth2/token'
#     headers= {'content-type':'application/x-www-form-urlencoded', 'Authorization':'Basic MjI4NUhYOjQzOTQ2ZjIyMWE3ODcxOTI4NzlkNzI0MmVhMjRhZGZh'}
#     query= {"client_id":"2285HX","grant_type":"authorization_code","redirect_uri":"http://127.0.0.1:8000/app","code":"32691e4342408da7d94d7e345ff1c3075c44faeb"}
#     #res = requests.post(url,headers=headers,data=query)
#     header = {'Authorization':'Bearer ' + access_token}
#     response = requests.get("https://api.fitbit.com/1/user/5G5L9G/activities/heart/date/2017-03-08/1d/1min.json",headers=header)

#     auth_client = fitbit.Fitbit(client_id, client_secret, access_token=access_token, refresh_token=refresh_token)
#     res = auth_client.heart(date= '2017-03-02', user_id='5G5L9G')
#     objs = json.loads(response.text)
    

#     #user_params = unauth_client.user_profile_get(user_id='5G5L9G')
#     response1 = GenericData.objects.create(Jsondata=response.text)
#     return HttpResponse(response.text)
# # return HttpResponse("Fitbit!")
#return HttpResponse(objs['activities-heart'][0]['value']['heartRateZones'][0]['min'])
#return HttpResponse(requests.get("https://api.fitbit.com/1/user/5G5L9G/profile.json"))
#return HttpResponse(res)

