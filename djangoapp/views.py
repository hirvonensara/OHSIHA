from django.shortcuts import render
import requests
import random

# Create your views here.

def home(request):
    # Health care districts are given an index number
    healthcaredistricts = {'null': 0, 'HUS': 1, 'Pirkanmaa':2, 'Lappi': 3,
                            'Kanta-Häme' : 4, 'Etelä-Karjala' : 5, 'Pohjois-Pohjanmaa': 6,
                            'Pohjois-Savo':7, 'Varsinais-Suomi':8, 'Keski-Suomi':9,
                            'Pohjois-Karjala':10, 'Etelä-Pohjanmaa': 11, 'Satakunta':12,
                            'Vaasa':13, 'Keski-Pohjanmaa':14, 'Päijät-Häme':15, 'Etelä-Savo':16,
                            'Kymenlaakso':17, 'Länsi-Pohja':18, 'Ahvenanmaa':19, 'Itä-Savo':20, 'Kainuu':21}

    # Creates lists for confirmed, deaths and recovered 
    confirmed_cases = len(healthcaredistricts)*[0]
    deaths = len(healthcaredistricts)*[0]
    recovered = len(healthcaredistricts)*[0]

    # Gets data 
    response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/')
    coronadata = response.json()
    list_of_confirmed = coronadata['confirmed']
    list_of_deaths = coronadata['deaths']
    list_of_recovered = coronadata['recovered']

    # Goes through confirmed cases and sorts them by health care district
    # and counts them all together
    all_cases = 0
    for case in list_of_confirmed:

        if case['healthCareDistrict'] in healthcaredistricts.keys():
            index = healthcaredistricts[case['healthCareDistrict']]
            confirmed_cases[index] = confirmed_cases[index] + 1
            all_cases += 1

        else:
            confirmed_cases[0] = confirmed_cases[0] + 1
            all_cases += 1

    # Goes through deaths and sorts them by health care district
    # and counts them all together
    all_deaths = 0
    for d in list_of_deaths:

        if d['healthCareDistrict'] in healthcaredistricts.keys():
            index = healthcaredistricts[d['healthCareDistrict']]
            deaths[index] = deaths[index] + 1
            all_deaths += 1

        # if health care district is unknown (null)
        else:
            deaths[0] = deaths[0] + 1
            all_deaths += 1

    # Goes through recovered and sorts them by health care district
    # and counts them all together
    all_recovered = 0
    for r in list_of_recovered:

        if r['healthCareDistrict'] in healthcaredistricts.keys():
            index = healthcaredistricts[r['healthCareDistrict']]
            recovered[index] = recovered[index] + 1
            all_recovered += 1

        # if health care district is unknown (null)
        else:
            recovered[0] = recovered[0] + 1
            all_recovered += 1
    

    corona_dct = {}
    data_lst = []

    # So that it is easy to print the data in html, let's put it in dictionary
    # where district is key and list of confirmed, deaths and recovered value
    for i in range(0, len(healthcaredistricts)):
        districts = list(healthcaredistricts.keys())
        district = districts[i]
        data_lst = [ confirmed_cases[i], deaths[i], recovered[i] ]
        corona_dct[district] = data_lst

    # For charts, creating 22 random colors
    colors = []
    for i in range(len(healthcaredistricts)):
        color = ""
        r1 = random.randint(0, 255)
        r2 = random.randint(0, 255)
        r3 = random.randint(0, 255)

        color = "rgba(" + str(r1) + "," + str(r2)+ "," + str(r3)+ ", 1)"
        colors.append(color)


    return render(request, 'home.html',
    {
        'coronadata' : corona_dct,
        'confirmed' : confirmed_cases,
        'deaths' : deaths,
        'recovered' : recovered,
        'all_confirmed' : all_cases,
        'all_deaths' : all_deaths,
        'all_recovered' : all_recovered,
        'colorlist' : colors
    } )

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