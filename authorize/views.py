from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
import requests
import json
from .models import extendeduser,ProfileFields,FieldValues,VerificationRequests
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
#from .forms import ProfileForm


# Create your views here.
def auth(request):
    user = request.user
    if str(user) == 'AnonymousUser':
        return redirect('login_user')
    print('Here')
    return render(request,'auth.html')

def login_user(request):
    user = request.user
    if str(user) == 'AnonymousUser':
        return render(request,'login.html')
    return redirect('/')

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
    print(image_data)
    
    try:
        image_url = image_data['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier']
        print(image_url)
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
        return redirect('/')
    else:
        user = User.objects.create_user(username=email, email=email, password=id,first_name=fname,last_name=lname)
        extd_user = extendeduser(user=user,lid=id)
        extd_user.save()
        login(request, user)
    
    return redirect('/')
    
@login_required
def profile(request):
    current_user = request.user
    all_fields = ProfileFields.objects.all()
    
    fields = {}
    for field in all_fields:
        fields[field.field]=field.id

    values = {}
    for field_name,field_id in fields.items():
        res = FieldValues.objects.filter(user_id=current_user.id,field_id=field_id)
        if res:
            values[field_name] = res[0].value
        else:
            values[field_name] = ''
    print(values)
    return render(request,'profile.html',{'values':values})

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def edit_profile(request):    
    if request.method=='GET':
        current_user = request.user
        all_fields = ProfileFields.objects.all()
    
        fields = {}
        for field in all_fields:
            fields[field.field]=field.id

        values = {}
        for field_name,field_id in fields.items():
            res = FieldValues.objects.filter(user_id=current_user.id,field_id=field_id)
            if res:
                values[field_name] = res[0].value
            else:
                values[field_name] = ''
        print(values)
        return render(request,'edit_profile.html',{'values':values})
    else:
        all_fields = ProfileFields.objects.all()
    
        fields = {}
        for field in all_fields:
            fields[field.field]=field.id

        response = {}
        for field_name in fields.keys():
            response[field_name] = request.POST[field_name]
        print(fields)
        print(response)

        changes = []
        for field in fields.keys():
            obj = FieldValues.objects.filter(user_id=request.user.id,field_id=fields[field])
            if obj:
                obj = obj[0]
                if obj.value != response[field]:
                    changes.append(field)
            else:
                if response[field]:
                    changes.append(field)

        print(changes)

        for field in changes:
            if ProfileFields.objects.get(id=fields[field]).verifiable == False:
                print('Hello')
                obj = FieldValues.objects.filter(user_id=request.user.id,field_id=fields[field])
                if not obj:
                    obj = FieldValues(user_id=request.user.id,field_id=fields[field],value=response[field])
                    obj.save()
                else:
                    obj = obj[0]
                    obj.value = response[field]
                    obj.save()
            else:
                check_obj = VerificationRequests.objects.filter(user_id=request.user.id,field_id=fields[field])
                if check_obj:
                    obj = check_obj[0]
                    if obj.value != response[field]:
                        obj.delete()
                        obj = VerificationRequests(user_id=request.user.id,field_id=fields[field],value=response[field])
                        obj.save()
                else:
                    obj = VerificationRequests(user_id=request.user.id,field_id=fields[field],value=response[field])
                    obj.save()

        return redirect('/profile')

@user_passes_test(lambda u: u.is_superuser)
def verify_requests(request):
    if request.method=='GET':
        objs = VerificationRequests.objects.all()
        values = []
        for obj in objs:
            id = obj.id
            user_id = obj.user_id
            user = User.objects.get(id=user_id)
            name = user.first_name+' '+user.last_name
            field_id = obj.field_id
            field = ProfileFields.objects.get(id=field_id)
            field_name = field.field
            value = obj.value
            values.append((id,name,field_name,value))
        return render(request,'verify_requests.html',{'values':values})
    else:
        vid = request.POST['vid']
        operation = request.POST['operation']
        obj = VerificationRequests.objects.get(id=int(vid))
        user_id = obj.user_id
        print(vid)
        print(obj)
        if operation=='delete':
            obj.delete()
        else:
            print(obj.field_id)
            field_obj = FieldValues.objects.filter(user_id=user_id,field_id=obj.field_id)
            print(field_obj)
            if field_obj:
                field_obj = field_obj[0]
                print(field_obj.value)
                print(obj.value)
                field_obj.value = obj.value
                field_obj.save()
            else:
                field_obj = FieldValues(user_id=user_id,field_id=obj.field_id,value=obj.value)
                field_obj.save()
            obj.delete()
        return redirect('verify_requests')



        
