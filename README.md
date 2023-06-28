# Python Covid Exam (covid dashboard)
## Introduction
This is a covid data and news dashboard. I developed this for my programming module in University. The program uses python and flask to run on a local server.
The data that is displayed on the website is collected from the uk-covid19 API and NewsAPI for news articles.
The code is uploaded onto github [https://github.com/HarrisAffandi708/Covid19Dashboard]

## Prerequisites
the program uses python version 3.10.6 or above
modules are also required to be installed are listed below:
- csv
- json
- sched
- time
- requests
- flask
- logging
- datetime

## Getting started
###### **Configuring the program**
Once you have installed the program, you need to head on towards the `config.json` file in the `congfig` folder. Here you need to put in your API key in quatation marks in `APIKey`
Putting in the API key is crucial as the program cannot run without it. You can also modify the local location named `Location`, it is "Exeter" by default.
You can also change the location type named `Location_type`
###### **Covid data**
The covid data displayed include the following
- Total local cases in the past 7 days
- Total national cases in the past 7 days
- Total hospital cases
- Total deaths

To edit the format and what data you want displayed, edit the `config.json` file in order to retrieve specific data from the uk-covid19 API. However once the
format and data is changed, the source code is required to be changed as well in order to run. The HTML code has to be modified as well if the data is changed. for example
the "Total deaths" part of the website, if the total deaths data is changed to total hospital cases in the past 7 days, the title in the html code has to be changed.

###### **Deleting news articles**
The website displays 10 different news articles about covid19. To delete the news article shown on the website, simply press the button that looks like
an X. This will cause a new article to be added to the list.

###### **Closing the program**
to close the program on windows, simply press the control and c (CTRL + C) in the terminal/command line

# Developer documentation
There are 3 source code modules:
- `covid_data_handler.py`
- `covid_news_handler.py`
- `user_interface.py`

The source code also includes:
- `config.json` (configuration file)
- `data folders` (stores covid data and news articles from API)
- `logs.logs` (stores the logs of the program)
- `index.html` (the template html code used in the program)
- `nation_2021-10-28` (sample csv file)
- `test.py` (used for testing functions of the program)
- `PNG photo` (used to display a photo in the website

## covid_data_handler.py
Purpose:

`Used to handle covid data for the website`

Content:
```
def parse_csv_data(csv_filename):
    returns the csv content in a list

def process_covid_csv_data(covid_csv_data):
    returns data from the parsed csv data, the returned data includes:
    total cases in the past 7 days, total hospital cases and total deaths


def covid_API_request(location:str="Exeter", location_type:str="ltla"):
    Instantiates the covid data API and returns the data in JSON form.


def api_update():
    Updated the api to bring in new data

def schedule_covid_updates(update_interval, update_name):
    Schedule covid data updates
    Uses schedular objects
    returns the update name and the update interval

def parse_covid_data():
    parses live covid data from the API and dumps the data into the Exeter_data.json and National_data.json files.
    returns the local and national data in json format
    
def process_covid_api_data(exeter_data:dict, national_data:dict):
    processes the parsed covid data from the API.
    The function returns local last 7 day cases for local and national, total hospital cases and deaths. it also returns the local location name and national name
            
    return (exeter_name,exeter_7_day_cases, exeter_deaths,nation_name,national_7_day_cases,national_deaths,hospital_cases)
```
## covid_news_handler.py
purpose:

`used to handle the news data for the website`

content:
```
def news_API_request(covid_terms:str="Covid COVID-19 coronavirus"):
    function takes in the covid terms, adds it to the url and uses the new url with the API key to access the news API to retieve news articles.
    Then dumps the articles into a file called articles.json
    returns the news api in json form
    
def articles(news_list:dict) -> list:
    selects 10 latest news articles from articles.json, appends the 10 articles to a local list named article_list
    the 10 articles are also dumped into a file named selected_articles.json
    returns the article_list

def update_news():
    uses the news_API_request function to update the news
    returns the news_API_request output

def schedule_news_updates(update_interval:int):
    schedule news article updates
    uses schedular objects
    returns the update interval

```

## user_interface.py
purpose:

`The module that is for the user interface, uses flask to display website and take in functions`

Content:
```
app = Flask(__name__)
^initiates the flask object

logging.basicConfig(level=logging.DEBUG,filename="logs.log", encoding='utf-8',format="%(asctime)s: %(message)s,")
^initiates the logging object and places logging data to a file named logs.log

data_sched = sched.scheduler(time.time, time.sleep)
news_sched = sched.scheduler(time.time, time.sleep)
data_news_sched = sched.scheduler(time.time, time.sleep)
^schedular objects


data_update_info = []
news_update_info = []
overall_updates_dict = {}
double_update_info = []
^global variable

def time_difference(update):
    calculates the difference between the current time and the time the user inputed for an update
    returns the difference in time in seconds as the schedular takes in seconds



def add_news():
    adds new news to the website when the user deletes a news article
    returns the 10 news article list


def update_news():
    updates the news articles using the news_API_request function and article funtions
    returns the 10 news article list
        

def update_data():
    uses parse_covid_data function
    returns local location name, local last 7 day cases, local deaths, national name, national last 7 days cases, national deaths and hoospital cases

def update_data_news():
    uses the update_data and update_news function

def sched_data_update(update_name, update_time, update_repeat):
    uses the time_difference funtion and uses the data_sched
    returns the data update information

def sched_news_update(update_name, update_time,update_repeat):
    uses the time_difference function and uses the news_sched
    returns the  news update information

def sched_data_news_update(update_name,update_time,update_repeat):
    uses the time_differnce function and uses the data_news_sched
    returns double update information
```
# Details
## Authors
- Harris Ilhan Bin Ahmad Affandi
