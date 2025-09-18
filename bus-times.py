import requests # for http requests
import json # for formatting json object
from rich import print_json # for colourising json output
from tabulate import tabulate # for formatting tables
from datetime import datetime # for handling date and time

    # loop through all the services
    # for each service, loop through all the next buses
    # for each bus, get the eta and calculate the difference between now and eta
    # use tabulate to put the data in a table

def main():
    bus_stop = input("Enter bus stop code: ")
    buses = get_json()

def get_json():
    API_KEY = "qfJiF6MVSTilUYq/UBiPxQ=="
    api_url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival?BusStopCode="
    headers = {
        "AccountKey": API_KEY,
        "accept": "application/json"
    }

    response = requests.get(api_url + bus_stop, headers=headers)
    obj = response.json()
    return obj["Services"] # this is an array of dicts of buses
    # print(json.dumps(obj, indent=4))



main()