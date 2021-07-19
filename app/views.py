from django.http import response
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.messages import constants as messages
from django.contrib import messages
from .models import Query_set
 
import requests
import json
from datetime import date
import time
import smtplib, ssl
from django.core.mail import send_mail
from django.conf import settings
import random
import string
# Create your views here.
def home(request):
    if(request.user.is_authenticated):
        return render(request,'app/index.html')
    return render(request,'register.html')
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username = request.POST.get('username')
        
        pass1=''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
        pass1=str(pass1)
        email=request.POST['email'] 
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
                send_mail(
                        'Co-Bo password',
                        'Hi '+username +'\n your password is : '+ pass1,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                        )
                
        myuser.save()
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['username']
        loginpassword=request.POST['password']
        user=authenticate(username=loginusername, password= loginpassword)
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
        username = request.user.username
        email=request.POST['email']
        dis=request.POST['dis']
        vac=request.POST['vac']
        age=request.POST['age']
        dis=str(dis)
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        query= Query_set(user=request.user,name=username,email=email,dis=dis,age=age,vac=vac)
        query.save()
        
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
                    if int(j['min_age_limit']) == int(age) and int(j['available_capacity']) > 0 and j['vaccine'] == str(vac):
                        message = 'Date -'+j['date'] + ' Centre name - '+ i['name'] +"  Available_capacity "+str(j['available_capacity'])
                        arr.append(message)
                        c+=1

                        arr+=['\n']
    s=''
    s=s.join(arr)
    if c>0:
        send_mail(
                        'Available vaccine',
                        str(c)+' results found in your district for '+str(age) +'+ \n'+s,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                        )                       
      
           
    return redirect("home")    
def query_set(request):
    s=Query_set.objects.all().filter(user=request.user)
    context={'query':s}
    return render (request,'app/query.html',context)
def delete_(request,slug):
    p=Query_set.objects.filter(sno=slug)
    p.delete()
    return redirect("query_set") 
# c=1
# import threading

# def fun1():
#     global c
    
#     if c==0:
#         return redirect("home") 
        
# def fun2(d1,age,vac,dis,email):
#     global c
#     threading.Timer(5.0,fun2).start()
#     c+=1
#     headers = {'accept': 'application/json','Accept-Language' : 'hi_IN','User-Agent': 'Mozilla/4.0'}
#     url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(dis)+'&date='+str(d1)
#     response=requests.get(url, headers=headers, verify=False)
#     data=response.json()
#     c=0
#     arr=[]
#     if (response.status_code == 200) :
#         print(response)
#         js = json.loads(response.content.decode())
#         for i in js['centers']:
#             for j in i['sessions']:
#                     if int(j['min_age_limit']) == int(age) and int(j['available_capacity']) > 0 and j['vaccine'] == vac:
#                         message = 'Date -'+j['date'] + ' Centre name - '+ i['name'] +"  Available_capacity "+str(j['available_capacity'])
#                         arr.append(message)
#                         c+=1
                        

#                         arr+=['\n']
#     s=''
#     s=s.join(arr)
#     if c>0:
#         send_mail(
#                         'Avilable vaccine',
#                         str(c)+' results found in your district \n'+s,
#                         settings.EMAIL_HOST_USER,
#                         [email],
#                         fail_silently=False,
#                         ) 



# def query(request):
#     global c
#     if request.method=="POST":
#         email=request.POST['email']
#         dis=request.POST['dis']
#         vac=request.POST['vac']
#         age=request.POST['age']
#         today = date.today()
#         d1 = today.strftime("%d-%m-%Y")
#     threading.Timer(7.0,fun1).start()
#     threading.Timer(5.0,fun2(d1,age,vac,dis,email)).start()
  
  

