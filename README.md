# Python Covid Exam (covid dashboard)
## Introduction
This is a covid data and news dashboard. I developed this for my programming module in University. The program uses python and flask to run on a local server.
The data that is displayed on the website is collected from the uk-covid19 API and NewsAPI for news articles.

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

