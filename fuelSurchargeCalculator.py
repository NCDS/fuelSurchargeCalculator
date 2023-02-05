#!/usr/bin/env python
import sys
import time
import requests
import json
import datetime
import timedelta

#Custom functions
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def switch_case(value):
    switch = {
        "Millseat": 16 * 2, #millseat
        "High Acres": 15 * 2, #high acres
        "Ontario": 39 * 2, #ontaio
        "Hyland": 67 * 2, #hyland
    }
    return switch.get(value, 0)

def roundDate(dt, formatStr):                      
    dateToRound = datetime.datetime.strptime(dt, formatStr).date()
    tmpDate = (dateToRound.weekday()) % 7 # if we are adding days, make .weekday() + 1
    modifier = timedelta.Timedelta(days=-tmpDate)# figure how many days from most recent monday
    return dateToRound + modifier# set date to monday of respective week, per eia.gov standards

def getFuelPrice(roundedDate):
    key = "mI4uF6ycU5xUjQa15MC9c2IZ0kbx28U6yp4Y4zHo"
    response = requests.get("https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key="+key+"&frequency=weekly&data[0]=value&facets[series][]=EMD_EPD2D_PTE_R10_DPG&start="+str(roundedDate)+"&end="+str(roundedDate)+"&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1")
    data = response.json()
    #jprint(data)
    price = data["response"]["data"][0]["value"]
    return price

def calculateSurcharge(loc, dateToRound, formatStr):
    surcharge = 0
    miles = switch_case(loc)
    if miles > 0:
        mpg = 4.8
        gals = miles/mpg
        price = getFuelPrice(roundDate(dateToRound, "%Y-%m-%d"))
        surcharge = (price - 5.00)*gals # only apply surcharge when diesel cost is over $5.00/gal
    return surcharge # if cost is less than 5, surcharge will return < 0, returning 0 means the funciton failed



        

    
