#!/usr/bin/python

import os
import sys
import time
import requests
import json
from flask import Flask
from lxml import html
import re

from flask import jsonify
app = Flask(__name__)

#weather report, set cords variable for your area
@app.route('/weather')
def getweather():
 #Set the for weather.gov and the coords of home in our case
 weather_url = "https://api.weather.gov/points/"
 cords = "40.825,-74.209"
 
 #requst the weather from NOAA, it gets returned as JSON
 weather_raw = requests.get( weather_url + cords + "/forecast/" )
 
 #parse the JSON into a dict called forecast
 forecast = json.loads(weather_raw.text)
 #Get the data out of the Main response, we only Need period under properties
 forecast_table = forecast['properties']
 forecast_periods = forecast_table['periods']
 count = 0
 #for the first 3 entries (0-3) pull out the data under periods, then get the information we need)
 #Create 3 dict items, Now, Later and Tomorrow referring to those 3 items
 while count <= 3:
  forecast_data_main = forecast_periods[count]
  if count == 0:
      now = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'][:12], 'wind_info': forecast_data_main['windSpeed'] + " " + forecast_data_main['windDirection']}
  if count == 1:
      later = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'][:12], 'wind_info' :  forecast_data_main['windSpeed'] + " " + forecast_data_main['windDirection']}
  if count == 2:
      tomorrow = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'], 'wind_info' :  forecast_data_main['windSpeed']+ " " + forecast_data_main['windDirection']}
  count += 1
 return jsonify(now,later,tomorrow)

#Returns the next 5 NY Penn bound trains
#set station to your DepartureVision 
@app.route('/get_inbound_trains')
def get_inbound_trains():
 baseurl = 'http://dv.njtransit.com/mobile/tid-mobile.aspx?sid='
 station = 'MC'
 page = requests.get(baseurl + station)
 tree = html.fromstring(page.content)
 first_train = 2
 ny_train_count = 0
 attempt_count = 0
 ny_counter = first_train # Start out with 0 known NYC trains
 ny_train_list = [] #initalize empty list for NY trains
 while ny_train_count <= 5 and attempt_count <= 20: #while we know than less than 5 trains and go through the data 10x
  regex = re.compile(r'NY.Penn(....)*') #compile the regex for NYP
  train_dest = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[2])'.format(ny_counter)) #Look at the Destinations
  if re.match(regex, train_dest) is not None: #if the Train Destination is NYP:
   ny_train_list.append(ny_counter) #add the value of the tr[x] to the list
   ny_counter += 1  #set up for the next train
   ny_train_count += 1 #Add one train to the number of NYP bound trains we'vefound so far
  else: #if the train isn't headed for NY:
   ny_counter += 1 #set up for the next train
   attempt_count += 1 #log the attempt and move on

  train_info_list=[] #generate an empty list to return on
  #Return the Train Information
 for ny_trains in ny_train_list: #for each of the tr[x] in the list we created above
  train_data = {} #initalize an empty dict object
  train_data["status"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[6])' .format(ny_trains))
  train_data["time"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[1])' .format(ny_trains)).split(' ', 1)[0]
  train_data["number"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[5])' .format(ny_trains))
  train_info_list.append(train_data)
 return jsonify(train_info_list)

@app.route('/get_nyp_issues')
def get_nyp_cancellations():
 baseurl = 'http://dv.njtransit.com/mobile/tid-mobile.aspx?sid='
 station = 'NY'
 page = requests.get(baseurl + station)
 tree = html.fromstring(page.content)
 train_issue_list = [] # Create an empty list of outbound trains
 train_count = 0
 train_delay_count = 0
 train_cancel_count= 0
 while train_count <= 15:
    train_status = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[6])' .format(train_count + 2)) #gets the status of each train
    if train_status == "DELAYED" or train_status == "STAND BY":
        train_delay_count += 1
    if train_status == "CANCELLED":
        train_cancel_count += 1
    train_count += 1
 train_issues = { 'checked': str(train_count), 'delay': str(train_delay_count), 'cancel': str(train_cancel_count) }
 train_issue_list.append(train_issues)
 return jsonify(train_issue_list)

@app.after_request
def after_request(response):
    #add some headers to allow cross site scripting
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
  return response

