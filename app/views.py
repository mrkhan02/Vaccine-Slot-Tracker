from django.http import response
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.messages import constants as messages
from django.contrib import messages
import requests
import json
from datetime import date
import time
import smtplib, ssl
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    return render(request,'app/index.html')
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username = request.POST.get('username')
        print(username)
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        print(username)
        # check for errorneous input
        if pass1!=pass2:
            messages.error(request, "Password didnt match")
            return redirect('home')

        
        # Create the user
        try:
            user= User.objects.get(username=username)

            messages.error(request, "Username already exists")
            return redirect('home')
        except User.DoesNotExist:
            try:
                user= User.objects.get(email=email)

                messages.error(request, "email already exists")
                return redirect('home')
            except User.DoesNotExist:
                myuser = User.objects.create_user(username, email, pass1)
                
        myuser.save()
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['username']
        loginpassword=request.POST['pass']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out") 
    return redirect("home")       
def query(request):
    if request.method=="POST":
        email=request.POST['email']
        dis=request.POST['dis']
        vac=request.POST['vac']
        age=request.POST['age']
        da=request.POST['date']
        
        dat = 20
        month='05'
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        
        headers = {'accept': 'application/json','Accept-Language' : 'hi_IN','User-Agent': 'Mozilla/4.0'}
        url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(dis)+'&date='+str(d1)
        response=requests.get(url, headers=headers, verify=False)
        data=response.json()
        c=0
        arr=[]
        if (response.status_code == 200) :
            print(response)
            js = json.loads(response.content.decode())
            for i in js['centers']:
                for j in i['sessions']:
                    if int(j['min_age_limit']) == int(age) and int(j['available_capacity']) > 0 and j['vaccine'] == vac:
                        message = 'Date -'+j['date'] + ' Centre name - '+ i['name'] +"  Available_capacity "+str(j['available_capacity'])
                        arr.append(message)
                        c+=1
                        

                        arr+=['\n']
    s=''
    s=s.join(arr)
    if c>0:
        send_mail(
                        'Avilable vaccine',
                        str(c)+' results found in your district \n'+s,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                        )                       
        
    return redirect("home")    