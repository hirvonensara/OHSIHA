from django.shortcuts import render
import requests

# Create your views here.

def example(request):
   # response = requests.get('http://freegeoip.net/json/')
   # geodata = response.json()
    return render(request, 'index.html', {
      #  'ip': geodata['ip'],
      #  'country': geodata['country_name']
    })