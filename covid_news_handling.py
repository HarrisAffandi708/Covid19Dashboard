import json
import datetime
import requests
import sched, time

#open config file to read the necessary data
with open("config/config.json", "r") as config_file:
    news_config = json.load(config_file)
    API_key = news_config["News API Configuration"]["APIKey"]

def news_API_request(covid_terms:str="Covid COVID-19 coronavirus"):
    covid_terms = "Covid OR COVID-19 OR coronavirus"
    current_date = datetime.date.today()
    url = ('https://newsapi.org/v2/everything?q='f'{covid_terms}&from={current_date}&language=en&sortBy=popularity&apiKey={API_key}')
    news_api_request = requests.get(url).json()
    news_articles = open("data/articles.json", "w")
    news_articles.write(json.dumps(news_api_request, sort_keys=False, indent=2))
    return news_API_request
    
    

def update_news():
    news_API_request()
    return news_API_request

def schedule_news_updates(update_interval:int):
    updates = sched.scheduler(time.time, time.sleep)
    updates.enter(float(update_interval),1,update_news())
    updates.run()
    return update_interval
