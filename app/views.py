from django.http import response
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.messages import constants as messages
from django.contrib import messages
from .models import Query
import requests
import json
from datetime import date
import time
import smtplib, ssl
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    availableTags = ['Lepa Rada', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 'Tirap', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang', 'Ahmedabad', 'Ahmedabad Corporation', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Bhavnagar Corporation', 'Botad', 'Chhotaudepur', 'Dahod', 'Dang', 'Devbhumi Dwaraka', 'Gandhinagar', 'Gandhinagar Corporation', 'Gir Somnath', 'Jamnagar', 'Jamnagar Corporation', 'Junagadh', 'Junagadh Corporation', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Rajkot Corporation', 'Sabarkantha', 'Surat', 'Surat Corporation', 'Surendranagar', 'Tapi', 'Vadodara', 'Vadodara Corporation', 'Valsad', 'East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim', 'Aizawl East', 'Aizawl West', 'Champhai', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Serchhip', 'Siaha', 'Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul', 'Chandigarh', 'Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi', 'Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahebganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum', 'Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran', 'Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Badaun', 'Baghpat', 'Bahraich', 'Balarampur', 'Ballia', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnour', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kushinagar', 'Lakhimpur Kheri', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Raebareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi', 'Agatti Island', 'Lakshadweep', 'Kargil', 'Leh', 'Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Prakasam', 'Sri Potti Sriramulu Nellore', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari', 'YSR District, Kadapa (Cuddapah)', 'Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurgaon', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar', 'Ahmednagar', 'Akola', 'Amravati', 'Aurangabad ', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal', 'Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozpur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Pathankot', 'Patiala', 'Rup Nagar', 'Sangrur', 'SAS Nagar', 'SBS Nagar', 'Sri Muktsar Sahib', 'Tarn Taran', 'Aranthangi', 'Ariyalur', 'Attur', 'Chengalpet', 'Chennai', 'Cheyyar', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Kovilpatti', 'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Palani', 'Paramakudi', 'Perambalur', 'Poonamallee', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Sivakasi', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi (Tuticorin)', 'Tiruchirappalli', 'Tirunelveli', 'Tirupattur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore', 'Viluppuram', 'Virudhunagar', 'North Goa', 'South Goa', 'Karaikal', 'Mahe', 'Puducherry', 'Yanam', 'Anantnag', 'Bandipore', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Poonch', 'Pulwama', 'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur', 'Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khurda', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh', 'Bagalkot', 'Bangalore Rural', 'Bangalore Urban', 'BBMP', 'Belgaum', 'Bellary', 'Bidar', 'Chamarajanagar', 'Chikamagalur', 'Chikkaballapur', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Gulbarga', 'Hassan', 'Haveri', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysore', 'Raichur', 'Ramanagara', 'Shimoga', 'Tumkur', 'Udupi', 'Uttar Kannada', 'Vijayapura', 'Yadgir', 'Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Kumuram Bheem', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak', 'Medchal', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Rangareddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal(Rural)', 'Warangal(Urban)', 'Yadadri Bhuvanagiri', 'Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti', 'West Tripura', 'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Peren', 'Phek', 'Tuensang', 'Wokha', 'Zunheboto'];
    dic={'Districts':availableTags}
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
        username = request.user.username
        email=request.POST['email']
        dis=request.POST['dis']
        vac=request.POST['vac']
        age=request.POST['age']
        phone=request.POST['phone']
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        query= Query(name=username,email=email,phone=phone,dis=dis,age=age,vac=vac)
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
                    if int(j['min_age_limit']) == int(age) and int(j['available_capacity']) > 0 and j['vaccine'] == vac:
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
  
  

