from flask import Flask, render_template
import logging
import sched, time
from covid_data_handler import parse_covid_data, process_covid_api_data
from covid_news_handling import articles, news_API_request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,filename="logs.log", encoding='utf-8',format="%(asctime)s: %(message)s,")

def update_news():
    try:
        news_request = news_API_request()
        news = articles(news_request)
        logging.debug("updated news")
    except:
        logging.critical("Failed to update news")
    return news
        

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

@app.route('/', methods=['GET','post'])
def index():
    return render_template("index.html", title= "Covid Data",location=exeter_name, local_7day_infections= exeter_7_day_cases, nation_location=nation_name,
    national_7day_infections=national_7_day_cases,hospital_cases= hospital_cases, news_articles=news, image= "Coronavirus_3D_illustration_by_CDC_1600x900.jpg",
    deaths_total= national_deaths)

if __name__ == '__main__':
    try:
        exeter_data, national_data= parse_covid_data()
        exeter_name,exeter_7_day_cases, exeter_deaths,nation_name,national_7_day_cases,national_deaths,hospital_cases = process_covid_api_data(exeter_data, national_data)
    except:
        logging.critical("Unable to extract data from covid api")
    try:
        news_request= news_API_request()
        news = articles(news_request)
    except:
        logging.critical("Unable to retrive news from news api")
    app.run(debug=True)

