from django.shortcuts import render
import requests

# Create your views here.

def home(request):
    # Health care districts are given an index number
    healthcaredistricts = {'null': 0, 'HUS': 1, 'Pirkanmaa':2, 'Lappi': 3,
                            'Kanta-Häme' : 4, 'Etelä-Karjala' : 5, 'Pohjois-Pohjanmaa': 6,
                            'Pohjois-Savo':7, 'Varsinais-Suomi':8, 'Keski-Suomi':9,
                            'Pohjois-Karjala':10, 'Etelä-Pohjanmaa': 11, 'Satakunta':12,
                            'Vaasa':13, 'Keski-Pohjanmaa':14, 'Päijät-Häme':15, 'Etelä-Savo':16,
                            'Kymenlaakso':17, 'Länsi-Pohja':18, 'Ahvenanmaa':19, 'Itä-Savo':20, 'Kainuu':21}

    # Creates a list for confirmed cases which is as big 
    confirmed_cases = len(healthcaredistricts)*[0]

    # Gets data 
    response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/')
    coronadata = response.json()
    list_of_confirmed = coronadata['confirmed']

    for case in list_of_confirmed:

        if case['healthCareDistrict'] in healthcaredistricts.keys():
            index = healthcaredistricts[case['healthCareDistrict']]
            confirmed_cases[index] = confirmed_cases[index] + 1

        else:
            confirmed_cases[0] = confirmed_cases[0] + 1

    # Counts all the cases together
    all_cases = 0
    for number in confirmed_cases:
        all_cases += number

    confirmed_dct = {}

    for i in range(0, 22):
        districts = list(healthcaredistricts.keys())
        district = districts[i]
        confirmed = confirmed_cases[i]
        confirmed_dct[district] = confirmed

    return render(request, 'home.html',
    {
        'confirmed' : confirmed_dct,
        'all_confirmed' : all_cases
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