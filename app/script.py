import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid.settings")

import django
django.setup()

from django.core.management import call_command
from models import Query_set
import requests
import json
from datetime import date
import time
import smtplib, ssl
from django.core.mail import send_mail
from django.conf import settings

def script():
    s=Query_set.objects.all()
    for i in s:
        email=i.email
        dis=i.dis
        vac=i.vac
        age=i.age
        dis=str(dis)
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
      
           

    return

script()