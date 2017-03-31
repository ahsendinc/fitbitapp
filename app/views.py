from django.shortcuts import render
from django.http import HttpResponse
import fitbit
import requests
from django.contrib.auth.decorators import login_required
from fitapp.decorators import fitbit_integration_warning
from app.models import GenericData, AccessTokenInfo, Data
import json
import configparser
from django.conf import settings
from django.db import transaction
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect    
from django.contrib import auth                 
from app.forms import MyRegistrationForm

from requests_oauthlib import OAuth2Session
import base64

from django.utils import timezone
from datetime import datetime, timedelta

#@fitbit_integration_warning(msg="Integrate your account with Fitbit!")
@login_required
def my_view(request):
    return HttpResponse('You are successfully logged in, '+request.user.username+' .Visible to authenticated users regardless of Fitbit integration status')

def index(request):
   #Load Settings
    consumer_key = settings.FITAPP_CONSUMER_KEY
    consumer_secret = settings.FITAPP_CONSUMER_SECRET

    if request.user.is_authenticated():        
        oauth = OAuth2Session(
                consumer_key,
                redirect_uri    = "http://127.0.0.1:8000/app/accesstoken",
                scope           = "activity heartrate location nutrition profile settings sleep social weight")
        fitbit_url_authorise_2 = "https://www.fitbit.com/oauth2/authorize"
        authorization_url, state = oauth.authorization_url(fitbit_url_authorise_2)

    #if (request.method == "POST"):
        #code = request.POST['token']
        #return HttpResponse("code")
        return HttpResponseRedirect(authorization_url)

    return HttpResponseRedirect("/")
    # unauth_client = fitbit.Fitbit(consumer_key,consumer_secret)
    # user_params = unauth_client.user_profile_get(user_id='5G5L9G')

    #return HttpResponse(request.user.username)

def accesstoken(request):

    # if(request.method == "POST"):
    #     code = request.POST['code']
    #     HttpResponse(code)
    if request.user.is_authenticated():
        code = request.GET.get('code')
        state = request.GET.get('state')

        consumer_key = settings.FITAPP_CONSUMER_KEY
        consumer_secret = settings.FITAPP_CONSUMER_SECRET
        encodedkeysecret = 'MjI4NUhYOjQzOTQ2ZjIyMWE3ODcxOTI4NzlkNzI0MmVhMjRhZGZh'

        fitbit_url_access_2 = "https://api.fitbit.com/oauth2/token"
        url     = fitbit_url_access_2
        data    = "client_id="      + consumer_key     + "&" +\
                  "grant_type="     + "authorization_code"  + "&" +\
                  "redirect_uri="   + "http://127.0.0.1:8000/app/accesstoken"  + "&" +\
                  "code="           + code 

        headers     = {
            'Authorization': 'Basic ' + encodedkeysecret,
            'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, data=data, headers=headers).json()
        access_token = r['access_token']
        refresh_token = r['refresh_token']
        scope = r['scope']
        expires_in = r['expires_in']
        user_id = r['user_id']
        token_type = r['token_type']

        #storing access token
        filteredModel = AccessTokenInfo.objects.get(user_id = user_id)
        if not filteredModel:
            accessmodel = AccessTokenInfo(
                access_token = access_token, 
                refresh_token = refresh_token, 
                scope = scope, 
                expires_in = expires_in, 
                user_id = user_id, 
                token_type = token_type, 
                username = request.user.username)

            accessmodel.save()

        else:
            filteredModel.access_token = access_token 
            filteredModel.refresh_token = refresh_token
            filteredModel.scope = scope
            filteredModel.expires_in = expires_in
            filteredModel.token_type = token_type

            filteredModel.save()
            
        return HttpResponse("Thanks! You just connected our app to Fitbit!")

    return HttpResponse("You are not logged in!")
   
#get all user data with user_id
def getAllData(user_id):

    filteredToken = AccessTokenInfo.objects.get(user_id=user_id)

    if filteredToken:
        access_token = refreshtoken(filteredToken.refresh_token)
        yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        #---------getting user data-------------
        header = {'Authorization':'Bearer ' + access_token}

        #get profile
        url_profile = "https://api.fitbit.com/1/user/-/profile.json"
        response = requests.get(url_profile,headers=header)

        #get heart rate
        url_heartrate = "https://api.fitbit.com/1/user/" + user_id + "/activities/heart/date/"+ yesterday +"/1d/1min.json"
        response = requests.get(url_heartrate,headers=header)
        parseJsonData(response,'activities-heart', user_id)

        #get calories
        url_calories = "https://api.fitbit.com/1/user/" + user_id + "/activities/calories/date/" + yesterday + "/1d/1min.json"
        response = requests.get(url_calories,headers=header)
        parseJsonData(response,'activities-calories', user_id)

        #get steps
        url_steps = "https://api.fitbit.com/1/user/" + user_id + "/activities/steps/date/" + yesterday + "/1d/1min.json"
        response = requests.get(url_steps,headers=header)
        parseJsonData(response,'activities-steps', user_id)

        #get distance
        url_distance = "https://api.fitbit.com/1/user/" + user_id + "/activities/distance/date/" + yesterday + "/1d/1min.json"
        response = requests.get(url_distance,headers=header)
        parseJsonData(response,'activities-distance', user_id)

        #get floors
        url_floors = "https://api.fitbit.com/1/user/" + user_id + "/activities/floors/date/" + yesterday + "/1d/1min.json"
        response = requests.get(url_floors,headers=header)
        parseJsonData(response,'activities-floors', user_id)

        #get elevation
        url_elevation = "https://api.fitbit.com/1/user/" + user_id + "/activities/elevation/date/" + yesterday + "/1d/1min.json"
        response = requests.get(url_elevation,headers=header)
        parseJsonData(response,'activities-elevation', user_id)

def parseJsonData(response, datatype, user_id):

    objs = response.json()
        #objs = json.loads(response.text)
    for index in range(len(objs[datatype + '-intraday']['dataset'])):
        newdata = Data(
            user_id = user_id,
            date = objs[datatype][0]['dateTime'],
            time= objs[datatype + '-intraday']['dataset'][index]['time'],
            data_type = datatype,
            value = objs[datatype + '-intraday']['dataset'][index]['value']
            )
        newdata.save()

def refreshtoken(refresh_token):
    consumer_key = settings.FITAPP_CONSUMER_KEY
    consumer_secret = settings.FITAPP_CONSUMER_SECRET
    encodedkeysecret = 'MjI4NUhYOjQzOTQ2ZjIyMWE3ODcxOTI4NzlkNzI0MmVhMjRhZGZh'

    fitbit_url_refresh= "https://api.fitbit.com/oauth2/token"
    url     = fitbit_url_refresh
    data    = "client_id="      + consumer_key     + "&" +\
              "grant_type="     + "refresh_token"  + "&" +\
              "refresh_token="           + refresh_token 

    headers     = {
        'Authorization': 'Basic ' + encodedkeysecret,
        'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(url, data=data, headers=headers).json()
    access_token = r['access_token']
    refresh_token = r['refresh_token']
    scope = r['scope']
    expires_in = r['expires_in']
    user_id = r['user_id']
    token_type = r['token_type']

    filteredModel = AccessTokenInfo.objects.get(user_id = user_id)
    if not filteredModel:
        accessmodel = AccessTokenInfo(
            access_token = access_token, 
            refresh_token = refresh_token, 
            scope = scope, 
            expires_in = expires_in, 
            user_id = user_id, 
            token_type = token_type, 
            username = request.user.username)

        accessmodel.save()

    else:
        filteredModel.access_token = access_token 
        filteredModel.refresh_token = refresh_token
        filteredModel.scope = scope
        filteredModel.expires_in = expires_in
        filteredModel.token_type = token_type

        filteredModel.save()
    return access_token

#getting all the data for each user
def data(request):
    for userTokenInfo in AccessTokenInfo.objects.all():
        getAllData(userTokenInfo.user_id)
    return HttpResponse("Fitbit!")

def profile2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/app/registration')
    return render(request, 'profile2.html')

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        #return HttpResponse(user.username + ",You are successfully logged in!" )
        return HttpResponseRedirect('/app/profile2')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("invalid!")


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/app/registration')
    logout(request)
    return HttpResponse("You logged out successfully.")
    # Redirect to a success page.

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect('/accounts/register_success')
            return HttpResponse("Thank you, you are registered!")
    # args = {}
    # args.update(csrf(request))
    # args['form'] = MyRegistrationForm()
    #print args
    return render(request, 'index.html', {
        'form': MyRegistrationForm(),
    })


