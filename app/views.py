from django.shortcuts import render
from django.http import HttpResponse
import fitbit
import requests


def index(request):
#return HttpResponse("Index Page")
    return requests.get("https://api.fitbit.com/1/user/5G5L9G/profile.json").json()

def data(request):
    if(request.method == GET):
        unauth_client = fitbit.Fitbit('2285HX','43946f221a787192879d7242ea24adfa')
        user_params = unauth_client.user_profile_get(user_id='5G5L9G')
        return HttpResponse("Fitbit!")
