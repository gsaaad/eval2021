from django.shortcuts import render
from django.urls import path
from .login import loginForm
from pymongo import MongoClient

import requests
# Create your views here.

def index(request):
    return render(request, 'index2.htm')

def home(request):
   # get the list of todos
#    response = requests.get('https://jsonplaceholder.typicode.com/todos/')
   # transfor the response to json objects
    url = "https://investing-cryptocurrency-markets.p.rapidapi.com/coins/list"

    querystring = {"edition_currency_id":"12","time_utc_offset":"28800","lang_ID":"1","sort":"MARKETCAP_DN","page":"1"}

    headers = {
        "X-RapidAPI-Key": "204482477cmshdd6f520fedecd46p1ea1fbjsne7e8a3e634f6",
        "X-RapidAPI-Host": "investing-cryptocurrency-markets.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
#    todos = response.json()
    total_data = response.json()['data']
    # print(total_data)
    # print("RESPONSE:", response)
    # print("TOTAL DATA:                   ",total_data)
    # print(type(total_data))
    
    # print("----------------------")
    data_dict = total_data[0]
    # print(type(data_dict))
    ("---------------")
    screen_data = data_dict['screen_data']
    crypto_data = screen_data['crypto_data']
    # get top
    crypto_data = crypto_data[:15]
    # print(type(crypto_data))
    # print(len(crypto_data))
    # print(crypto_data)
    
    # print()
    

    return render(request, "home.html", {"data": crypto_data})

def login(request):
    client = MongoClient('mongodb+srv://gsaaad:mongodjango@cluster0.4yjqtsv.mongodb.net/?retryWrites=true&w=majority', 27017)

    print("LOGIN",login)
    print("----------")
    form = loginForm()
    
    if request.method == 'POST':
        form = loginForm(request.POST)
        
        if form.is_valid():
            print("VALIDATED!")
            print("Email: "+form.cleaned_data['email'])
            print("Password: "+form.cleaned_data['password'])
            db = client['miWallets']
            Users = db['Users']
            print(form.cleaned_data['email'])
            
            result = Users.find_one({"email":form.cleaned_data['email']})
            print(result)
            
            if result:
                print("we found your email in your mongo database! login! auth!]")

     
    return render(request, 'login.html', {'form':form})

def register(request):
    return render(request, 'register.html')