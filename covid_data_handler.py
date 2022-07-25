import csv
import json
#from uk_covid19 import Cov19API
import sched
import time
from uk_covid19 import Cov19API


def parse_csv_data(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        csvReader1 =csv.reader(csvfile)
        rows = []
        for row in csvReader1:
            rows.append(row)
    return rows

def process_covid_csv_data(covid_csv_data):
    with open(covid_csv_data, 'r') as csvfile:
        count = 0 
        sum7daysCases = 0
        deathCases = 0
        NullValue = True
        csvReader1 = csv.DictReader(csvfile)
        #current hospital cases
        #gets the first row from the csv file and reads the dictionary key "hospitalCases" and returns the value
        row1= next(csvReader1)
        hospitalCases = row1.get("hospitalCases")
        count += 1
            
        #last 7 days covid cases
        #takes the last 7 days excluding the current day and adds them together returning the summed value
        if count ==1:
            row1= next(csvReader1)
            count += 1
        for x in range(count,9):
            row7= next(csvReader1)
            totalCases = row7.get("newCasesBySpecimenDate")
            str(totalCases)
            number = int(totalCases)
            sum7daysCases += number
            
        
        #total deaths
        #reads through the cumDailyNsoDeathsByDeathDate column and continues if the value is null then
        #returns the the number when it reaches a value that isnt null
        #create a new csv reader to reset the csv next counter as new data may enter the csv file when it
        #refresed and the counter may skip the data if its not reset
        csvfile.seek(0)
        while NullValue == True:
            row5 = next(csvReader1)
            #twice to remove the header
            row5=next(csvReader1)
            deathsTotal = row5.get("cumDailyNsoDeathsByDeathDate")
            if deathsTotal != "":
                NullValue = False
        return sum7daysCases, hospitalCases, deathsTotal


def covid_API_request(location, location_type):
    #filters
    #uses the parameter and adds it into the filter with the default value being Exeter and ltla for location and location type respectively
    location = "Exeter"
    location_type = "ltla"
    filter = [
        'areaType='+location_type,
        'areaName='+location,
    ]
    #structure
    cases_and_deaths = {
        "date" : "date",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "cumCasesBySpecimenDate": "cumCasesBySpecimenDate",
        "cumDeathsByPublishDate": "cumDeathsByPublishDate",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
    }
    #Instantiation
    api = Cov19API(filters=filter, structure=cases_and_deaths)

    api_data = api.get_csv()
    print(api_data)

def schedule_covid_updates(update_interval, update_name):
    pass

covid_API_request("Exeter","ltla")