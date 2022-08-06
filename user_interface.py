from flask import Flask, render_template, request
import logging
import sched, time
from datetime import datetime
from covid_data_handler import parse_covid_data, process_covid_api_data
from covid_news_handling import articles, news_API_request

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG,filename="logs/logs.log", encoding='utf-8',format="%(asctime)s: %(message)s,")

data_sched = sched.scheduler(time.time, time.sleep)
news_sched = sched.scheduler(time.time, time.sleep)
data_news_sched = sched.scheduler(time.time, time.sleep)

data_update_info = []
news_update_info = []
overall_updates_dict = {}
double_update_info = []

def time_difference(update):
    hours_mins = update.split(':')
    hours_to_secs = int(hours_mins)[0]*60*60
    mins_to_secs = int(hours_mins)[1]*60
    total_secs = hours_to_secs + mins_to_secs
    now = datetime.now().strftime("%H:%M")
    now_hours_mins = now.split(':')
    now_hours_to_secs = int(now_hours_mins)[0]*60*60
    now_mins_to_secs = int(now_hours_mins)[1]*60
    now_total_secs = now_hours_to_secs + now_mins_to_secs
    seconds_diff = now_total_secs - total_secs
    return seconds_diff



def add_news():
    #checks whether the i (the artice's title) is in the removed article list and in the news list, if not in both, i is appended to news list
    for i in news_request["articles"]:
        if i['title'] not in removed_article and i not in news:
            news.append(i)
            break
    return news


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

def sched_data_update(update_name, update_time, update_repeat):
    data_update_time = time_difference(update_time)
    #with open("config/config.json" 'W'):
        
    if update_time not in data_update_info:
        data_update_info.append({"update_name":update_name,"update_time":update_time,"update_repeat": update_repeat})
        sched_data_update = data_sched.enterabs(data_update_time,1,update_data)
        overall_updates_dict[update_name] = sched_data_update
        logging.info("succefully scheduled an update")
    else:
        logging.error("scheduled update is already existing")
    return data_update_info

def sched_news_update(update_name, update_time,update_repeat):
    news_update_time = time_difference(update_time)
    if update_time not in news_update_info:
        news_update_info.append({"update_time":update_time,"update_repeat":update_repeat})
        sched_news_update = news_sched.enterabs(news_update_time,1,update_news)
        overall_updates_dict[update_name] = sched_news_update
        logging.info("succefully scheduled news update")
    else:
        logging.error("scheduled update is alrready existing")
    return news_update_info

def sched_data_news_update(update_name,update_time,update_repeat):
    data_news_time = time_difference(update_time)
    if update_time in news_update_info or data_update_info or double_update_info:
        double_update_info.append({"update_name":update_name,"update_time":update_time, "update_repeat":update_repeat})
        logging.error("already scheduled an update at this time")
    else:
        double_update_info.append(update_time)
        sched_double_update = data_news_sched.enterabs(data_news_time,1,update_data_news)
        overall_updates_dict[update_name] =sched_double_update
    return double_update_info


@app.route('/index', methods=["POST", "GET"])
def index():
    #retreives the keywords from the url when an action from the user is made, e.g updating name
    update_time = request.args.get('update')
    update_name = request.args.get('two')
    repeat_update = request.args.get('repeat')
    update_data= request.args.get('covid-data')
    update_news = request.args.get('news')
    cancel_news = request.args.get('notif')

    #scheduling section done according to user actions, since update_name is a required field. we will use it as the root if statement
    if update_name:
        #checks whether the user checked the update news and covid data boxes
        if update_data =="covid-data" and update_news=="news":
            sched_data_news_update(update_name,update_time,repeat_update)
            logging.info("news and data update")
        elif update_data =="covid-data":
            sched_data_update(update_name,update_time,repeat_update)
        elif update_news =="news":
            sched_news_update(update_name,update_time,repeat_update)
    
    if cancel_news != None:
        removed_article_title = str(cancel_news).replace("+","")
        if removed_article_title not in removed_article:
            removed_article.append(removed_article_title)
        for i in news:
            if i["title"] ==removed_article_title:
                news.remove(i)
                logging.info("news article removed")
                add_news()
                logging.info("news article added")


    return render_template("index.html", title= "Covid Data",location=exeter_name, local_7day_infections= exeter_7_day_cases, nation_location=nation_name,
    national_7day_infections=national_7_day_cases,hospital_cases= hospital_cases, news_articles=news, image= "Coronavirus_3D_illustration_by_CDC_1600x900.png",
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
    removed_article = []
    app.run(debug=True)

