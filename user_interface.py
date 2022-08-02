from flask import Flask
import logging
import sched, time
from covid_data_handler import parse_covid_data, process_covid_api_data
from covid_news_handling import news_API_request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,filename="logs.log", encoding='utf-8',format="%(asctime)s: %(message)s,")

def update_news():
    try:
        news_request = news_API_request()
        logging.debug("updated news")
    except:
        logging.critical("Failed to update news")
    return news_request
        

def update_data():
    try:
        exeter_data, national_data = parse_covid_data()
        exeter_name,exeter_7_day_cases, exeter_deaths,nation_name,national_7_day_cases,national_deaths,hospital_cases = process_covid_api_data(exeter_data,national_data)
        logging.debug("Updated covid data")
    except:
        logging.critical("failed to extract data from covid api")
    return exeter_name,exeter_7_day_cases, exeter_deaths,nation_name,national_7_day_cases,national_deaths,hospital_cases

def update_data_news():
    update_news()
    update_data()
    


