import requests
import json
from datetime import date
import time
import smtplib, ssl


""" To get District IDs

#Retrieve State ID
url = 'http://cdn-api.co-vin.in/api/v2/admin/location/states'
headers = {'accept': 'application/json','Accept-Language' : 'hi_IN','User-Agent': 'Mozilla/4.0'}
result = requests.get(url, headers=headers)
#Print state ID
print(result.content.decode())

#Retrieve districts IDs in the state
url_district = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/141'
headers = {'accept': 'application/json','Accept-Language' : 'hi_IN','User-Agent': 'Mozilla/4.0'}
result = requests.get(url_district, headers=headers)
#print districts Ids
print(result.content.decode())

"""

#url_appointment = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=141&date=09-05-2021'

s = 0
#Specify start date for search
today = date.today()
d1 = today.strftime("%d-%m-%Y")
#Specify list of district for vaccination centers
district = [149,144,150]
port = 465  # For SSL
#provide sender gmail account password
password = "####"

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False

#sender email address
sender_email = "####@gmail.com"
#receiver email address
receiver_email = "####@gmail.com"
message = "Vaccine slot is available in itarsi, Please book it"

try:
    while (s < 5):
        print("Trying Again")
        for d in district:
            print("Checking for district: ", d)
            url_appointment = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(d)+'&date='+str(d1)
            print (url_appointment)
            headers = {'accept': 'application/json','Accept-Language' : 'hi_IN','User-Agent': 'Mozilla/4.0'}
            result = requests.get(url_appointment, headers=headers, verify=False)
            if (result.status_code == 200) :
                print(result)
                js = json.loads(result.content.decode())
                for i in js['centers']:
                    for j in i['sessions']:
                        if int(j['min_age_limit']) == 18 and int(j['available_capacity']) > 10 and j['vaccine'] == 'COVAXIN':
                            print ('min+age = ',j['min_age_limit'] , 'capacity',j['available_capacity'])
                            print (i['district_name'], i['name'])
                            print(j['slots'])
                            print(j['date'])
                            message = str(d)+' '+ i['district_name'] + ' Centre name - '+ i['name']
                            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                                server.login(sender_email, password)
                                server.sendmail(sender_email, receiver_email, message)
                                server.quit()
                                s =1
            else :
                s =10
                print (result.content.decode())
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                    server.quit()
        if(s == 1):
            print("sleep 10")
            s = 0
            time.sleep(10)
        else:
            print ("s",s)
            print("sleep 60")
            time.sleep(60)
except Exception as e:
    message = str(e)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()