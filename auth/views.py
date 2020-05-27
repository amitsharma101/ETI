from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

# Create your views here.
def auth(request):
    return render(request,'auth.html')

def auth_response(request):
    code = request.GET['code']
    state = request.GET['state']

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {'grant_type':'authorization_code','code':code,
            'redirect_uri':'http://127.0.0.1:8000/auth',
            'client_id':'86sbo0a0h4tamv',
            'client_secret':'iAuWMiYLGHG5vi9H'
            }
    r = requests.post(url, data=data)
    access_token = r.json()['access_token']

    url = "https://api.linkedin.com/v2/me"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    data = r.json()

    url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    dat = r.json()

    print(dat)
    fname = data['firstName']['localized']['en_US']
    lname = data['lastName']['localized']['en_US']
    id = data['id']
    email = dat['elements'][0]['handle~']['emailAddress']
    

    return HttpResponse('Welcome, '+fname+ ' '+lname+' email : '+email+' ; id : '+id)

