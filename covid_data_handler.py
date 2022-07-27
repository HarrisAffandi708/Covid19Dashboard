import csv
import json
import sched
import time
from uk_covid19 import Cov19API
import sched, time

#config file code
with open("config/config.json", "r") as configFile:
    loadConfigFile = json.load(configFile)
    APIFilters = [f'areaType={loadConfigFile["Covid Data Configuration"]["Location_type"]}',
    f'areaName={loadConfigFile["Covid Data Configuration"]["Location"]}']
    APIFormat = loadConfigFile["Covid Data Configuration"]["API Output Structure"]



#code asked in criteria, wont be used in actual application

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
            
        
        """total deaths
        reads through the cumDailyNsoDeathsByDeathDate column and continues if the value is null then
        returns the the number when it reaches a value that isnt null
        create a new csv reader to reset the csv next counter as new data may enter the csv file when it
        refresed and the counter may skip the data if its not reset
        """
        csvfile.seek(0)
        while NullValue == True:
            row5 = next(csvReader1)
            #twice to remove the header
            row5=next(csvReader1)
            deathsTotal = row5.get("cumDailyNsoDeathsByDeathDate")
            if deathsTotal != "":
                NullValue = False
        return sum7daysCases, hospitalCases, deathsTotal


def covid_API_request(location:str="Exeter", location_type:str="ltla"):
    #Instantiation
    api = Cov19API(filters=[f'areaType={location_type}', f'areaName={location}'], structure=APIFormat)

    api_data = api.get_json()
    return api_data


def api_update():
    data = covid_API_request()
    return data

def schedule_covid_updates(update_interval, update_name):
    #create a sched object named updates
    #enter delay, priority and action into sched(updates)
    updates = sched.scheduler(time.time, time.sleep)
    updates.enter(float(update_interval),1, api_update())
    updates.run()
    return update_interval, update_name

#used in actual application

def parse_covid_data():
    exeter_api = Cov19API(filters=APIFilters, structure=APIFormat)
    national_api= Cov19API(filters=['areaType=nation',f'areaName={loadConfigFile["Covid Data Configuration"]["Nation"]}'], structure=APIFormat)
    exeter_data= exeter_api.get_json()
    national_data = national_api.get_json()
    exeter_file = open("data/Exeter_data.json", "w")
    exeter_file.write(json.dumps(exeter_data,indent=2, sort_keys=False))
    national_file = open("data/national_data.json", "w")
    national_file.write(json.dumps(national_data, indent=2,sort_keys=False))
    


parse_covid_data()
    
