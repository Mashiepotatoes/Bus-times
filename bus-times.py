import requests # for http requests
import json # for formatting json object
from rich import print_json # for colourising json output
from tabulate import tabulate # for formatting tables
from datetime import datetime, timezone # for handling date and time
from sys import argv
import argparse

    # The program from CLI should take two arguments, this file, and a txt file with the API key. 
    # loop through all the services
    # for each service, loop through all the next buses
    # for each bus, get the eta and calculate the difference between now and eta
    # use tabulate to put the data in a table
NOW_UTC = datetime.now(timezone.utc)    

def main():
    # Handle wrong number of arguments
    parser = argparse.ArgumentParser(description="Requires exactly two positional args")
    parser.add_argument(
        "items",
        nargs=1, # require exactly 2 values
        help="One additional argument after script, e.g. <python-script.py> api_key.txt "
    )
    parser.parse_args()
    
    # Handle wrong file type

    bus_stop = input("Enter bus stop code: ")
    buses = get_json(bus_stop)
    print(f"RETRIEVING RESULTS FOR BUS STOP NO.: {bus_stop}")
    print(waiting_time_table(buses))

def get_json(bus_stop):
    try:
        with open("API-KEY.txt") as f:
            API_KEY = f.read()
    except FileNotFoundError:
        print("File not found!")
        
    api_url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival?BusStopCode="
    headers = {
        "AccountKey": API_KEY,
        "accept": "application/json"
    }

    response = requests.get(api_url + bus_stop, headers=headers)
    obj = response.json()
    return obj["Services"] # this is an array of dicts of buses
    # print(json.dumps(obj, indent=4))

def waiting_time_table(buses):
    headers = [f"Bus Number", "First Bus", "Second Bus", "Third Bus"]
    table = []             

    for bus in buses:
        bus_num = bus["ServiceNo"]
        # finding the difference between the ETA provided and the current time                  
        b1 = get_eta(bus["NextBus"]["EstimatedArrival"])
        b2 = get_eta(bus["NextBus2"]["EstimatedArrival"])
        b3  = get_eta(bus["NextBus3"]["EstimatedArrival"])
        table.append([bus_num, b1, b2, b3])
        
    return tabulate(table, headers, tablefmt="heavy_outline")

def get_eta(bus_eta):
    if bus_eta == '':
        return "-"
    target_time = datetime.fromisoformat(bus_eta)
    min_diff = (target_time - NOW_UTC).total_seconds() / 60
    return round(min_diff)

main()