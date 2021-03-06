from django.shortcuts import render
import requests
import json 
import datetime
from django.contrib.gis.geoip2 import GeoIP2

# Create your views here.
def main(request):
    if request.method=="POST":
       name=request.POST.get('location')
    
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        g = GeoIP2()
        data = g.city(ip)
        name=data['city']
     
        
        
    url=f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid=997ab8def5358d01472eccc64093dc44"
    raw=requests.get(url).json()
    if raw['cod'] !='400' and raw['cod'] !='404':
        data={
            'city':raw['name'],
            'temperature':int(raw['main']['temp']-273),
            'type':raw['weather'][0]['main'],
            'time':datetime.datetime.now(),
            'clouds':raw['clouds']['all'],
            'humidity':raw['main']['humidity'],
            'wind':raw['wind']['speed'],
            'visibility':raw['visibility']
        }
        return render(request,'home/index.html',{'data':data})
    else:
        name='hisar'
        url=f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid=997ab8def5358d01472eccc64093dc44"
        raw=requests.get(url).json()
        data={
            'city':raw['name'],
            'temperature':int(raw['main']['temp']-273),
            'type':raw['weather'][0]['main'],
            'time':datetime.datetime.now(),
            'clouds':raw['clouds']['all'],
            'humidity':raw['main']['humidity'],
            'wind':raw['wind']['speed'],
            'visibility':raw['visibility']
        }
        return render(request,'home/index.html',{'data':data})