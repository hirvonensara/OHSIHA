from django.shortcuts import render
import requests

# Create your views here.

def home(request):

    return render(request, 'home.html' )

def example(request):
    count_in_pirkanmaa = 0
    count_in_hus = 0
    count_in_other = 0
    all_cases = 0

    response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/')
    coronadata = response.json()
    list_of_confirmed = coronadata['confirmed']

    for case in list_of_confirmed:
        
        if case['healthCareDistrict'] == 'Pirkanmaa':
            count_in_pirkanmaa += 1
        
        elif case['healthCareDistrict'] == 'HUS' :
            count_in_hus += 1
        
        else:
            count_in_other += 1

    all_cases = count_in_hus + count_in_pirkanmaa + count_in_other        

    return render(request, 'index.html', {
      'count_pirkanmaa' : count_in_pirkanmaa,
      'count_hus' : count_in_hus,
      'count_other' : count_in_other,
      'all' : all_cases

      
    })