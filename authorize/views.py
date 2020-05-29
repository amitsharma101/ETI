from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
import requests
import json
from .models import extendeduser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


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

    url = "https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~digitalmediaAsset:playableStreams))"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    image_data = r.json()
    
    try:
        image_url = image_data['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier']
    except:
        pass
    fname = data['firstName']['localized']['en_US']
    lname = data['lastName']['localized']['en_US']
    id = data['id']
    email = dat['elements'][0]['handle~']['emailAddress']

    curr_user = extendeduser.objects.filter(lid=id)
    if curr_user:
        user = authenticate(username=email, password=id)
        login(request, user)
        return render(request,'auth.html',{'user':user})
    else:
        user = User.objects.create_user(username=email, email=email, password=id,first_name=fname,last_name=lname)
        extd_user = extendeduser(user=user,lid=id)
        extd_user.save()
        login(request, user)
    
    return redirect('/')
    
@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def edit_profile(request,lid):
    user = extendeduser.objects.get(lid=lid)
    form = ProfileForm(request.POST or None,instance=user)
    
    if form.is_valid():
        form.save()
        return redirect('/profile')
    return render(request,'edit_profile.html',context={'form':form,'user':user})