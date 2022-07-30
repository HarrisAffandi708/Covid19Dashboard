import json
import datetime
import requests

with open("config/config.json", "r") as config_file:
    news_config = json.load(config_file)
    API_key = news_config["News API Configuration"]["APIKey"]

articles = []


def news_API_request(covid_terms:str="Covid COVID-19 coronavirus"):
    covid_terms = "Covid OR COVID-19 OR coronavirus"
    current_date = datetime.date.today()
    url = ('https://newsapi.org/v2/everything?q='f'{covid_terms}&from={current_date}&language=en&sortBy=popularity&apiKey={API_key}')
    news_api_request = requests.get(url).json()
    
    print(news_api_request)

def update_news(news_API_request):
    x= 1


news_API_request()