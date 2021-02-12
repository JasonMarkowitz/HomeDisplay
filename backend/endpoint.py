#!/usr/bin/python2.7

import os
import sys
import time
import requests
import json
from flask import Flask
from lxml import html
from lxml import etree
import re
import datetime

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
      now = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'][:18], 'wind_info': forecast_data_main['windSpeed'] + " " + forecast_data_main['windDirection']}
  if count == 1:
      later = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'][:18], 'wind_info' :  forecast_data_main['windSpeed'] + " " + forecast_data_main['windDirection']}
  if count == 2:
      tomorrow = { 'temp' : str(forecast_data_main['temperature']) + " F", 'period' : forecast_data_main['name'] + ":" , 'conditions': forecast_data_main['shortForecast'], 'wind_info' :  forecast_data_main['windSpeed']+ " " + forecast_data_main['windDirection']}
  count += 1
 return jsonify(now,later,tomorrow)

#Returns the next 5 HOB bound trains
#set station to your DepartureVision 
@app.route('/get_inbound_trains_HOB')
def get_inbound_trains_HOB():
 # URL Handling Section
 baseurl = 'https://traindata.njtransit.com/NJTSignData.asmx/getTrainScheduleJSON19Rec?username=DV4&password=ekd0J4MsYgmN56&station=MC&status=n'
 #station = 'MC'
 page = requests.get(baseurl)
 tree = html.fromstring(page.content)
 cleaned = etree.tostring(tree, encoding='utf8', method='text')
 cleaned = cleaned.decode("utf8")
 cleanedj1 = json.loads(cleaned)
 stationdata = cleanedj1['STATION']['ITEMS']['ITEM']
 #End of URL handling
 first_train = 0
 ny_train_count = 0
 attempt_count = 0
 ny_counter = first_train # initalize empty list for ny trains as we don't know any yet
 train_list = [] #initalize empty list for NY trains
 stationdata_object_count = len(stationdata)
 train_info_list = [] 
 #Iterate over the list, stationdata_object_count is the number of the indexes we have
 while attempt_count < stationdata_object_count and ny_counter <= 5:
  train = stationdata[attempt_count]
  attempt_count += 1
  #now lets look for if it's HOB bound
  if train['DESTINATION'] == "Hoboken": #if it's HOBOKEN bound
   ny_counter += 1
   train_data = {}
   train_data["status"] = train['STATUS']
   # Time is a pain in the butt, convert it before we do things with it:
   time_of_train = datetime.datetime.strptime(train['SCHED_DEP_DATE'], '%d-%b-%Y %I:%M:%S %p')
   time_of_train = str(time_of_train.hour) + ":" + str(time_of_train.minute)
   train_data["time"] = time_of_train
   train_data["number"] = train['TRAIN_ID']
   train_info_list.append(train_data)
 return jsonify(train_info_list)

#Returns the next 5 NY Penn bound trains
#set station to your DepartureVision 
@app.route('/get_inbound_trains')
def get_inbound_trains():
 # URL Handling Section
 baseurl = 'https://traindata.njtransit.com/NJTSignData.asmx/getTrainScheduleJSON19Rec?username=DV4&password=ekd0J4MsYgmN56&station=MC&status=n'
 #station = 'MC'
 page = requests.get(baseurl)
 tree = html.fromstring(page.content)
 cleaned = etree.tostring(tree, encoding='utf8', method='text')
 cleaned = cleaned.decode("utf8")
 cleanedj1 = json.loads(cleaned)
 stationdata = cleanedj1['STATION']['ITEMS']['ITEM']
 #End of URL handling
 first_train = 0
 ny_train_count = 0
 attempt_count = 0
 train_data = {}
 ny_counter = first_train # initalize empty list for ny trains as we don't know any yet
 train_list = [] #initalize empty list for NY trains
 stationdata_object_count = len(stationdata)
 train_info_list = [] 
#Iterate over the list, stationdata_object_count is the number of the indexes we have
 while attempt_count < stationdata_object_count and ny_counter <= 10:
  train = stationdata[attempt_count]
  attempt_count += 1
 #now lets look for if it's HOB bound
  #print (re.search("New.York.*", train['DESTINATION']))
  if re.search("New.York.*", train['DESTINATION']) is not None : #if it's New York bound
#   print ("Found a NY Train", train['TRAIN_ID'])
   ny_counter += 1
   train_data = {}
   train_data["status"] = train['STATUS']
  # Time is a pain in the butt, convert it before we do things with it:
   time_of_train = datetime.datetime.strptime(train['SCHED_DEP_DATE'], '%d-%b-%Y %I:%M:%S %p')
   time_of_train = str(time_of_train.hour) + ":" + str(time_of_train.minute)
   train_data["time"] = time_of_train
   train_data["number"] = train['TRAIN_ID']
   train_info_list.append(train_data)
 return jsonify(train_info_list)

@app.route('/get_nyp_issues')
def get_nyp_cancellations():
 baseurl = 'https://traindata.njtransit.com/NJTSignData.asmx/getTrainScheduleJSON19Rec?username=DV4&password=ekd0J4MsYgmN56&station=NY&status=n'
 station = 'NY'
 page = requests.get(baseurl)
 tree = html.fromstring(page.content)
 cleaned = etree.tostring(tree, encoding='utf8', method='text')
 cleaned = cleaned.decode("utf8")
 cleanedj1 = json.loads(cleaned)
 stationdata = cleanedj1['STATION']['ITEMS']['ITEM']
 #End of URL handling
 train_issue_list = [] # Create an empty list of outbound trains
 train_count = 0
 train_delay_count = 0
 train_cancel_count= 0
 attempt_count = 0
 stationdata_object_count = len(stationdata)
 train = stationdata[attempt_count]
 while attempt_count < stationdata_object_count and train_count <= 15:
  train = stationdata[attempt_count]
  attempt_count += 1
  train_status = train['STATUS']  #gets the status of each train

  if train_status == "DELAYED" or train_status == "STAND BY":
   train_delay_count += 1
  if train_status == "CANCELLED":
   train_cancel_count += 1

  train_count += 1
 train_issues = { 'checked': str(train_count), 'delay': str(train_delay_count), 'cancel': str(train_cancel_count) }
  #print (train_issues)
 train_issue_list.append(train_issues)
 return jsonify(train_issue_list)

@app.route('/time_to_work')
def time_to_work():
#set Base URL, Home and Work ADDRS, and Compile the request string to google
 baseurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
 apikey = ''
 homeaddr = ''
 workaddr = ''
 work_driving_time_raw = requests.get(baseurl + "units=imperial&origins=" + homeaddr + "&destinations=" + workaddr + "&departure_time=now" + "&key=" + apikey)
 work_driving_time = json.loads(work_driving_time_raw.text)
 #Get the Miles out of the "Rows" Returned
 work_driving_time_rows = work_driving_time['rows']
 work_driving_time_elements = work_driving_time_rows[0]
 work_driving_time_element_list = work_driving_time_elements.get('elements')
 work_driving_time_duration = work_driving_time_element_list[0]
 work_driving_time_actual = work_driving_time_duration.get('duration_in_traffic')
 work_driving_time_mins = work_driving_time_actual.get('text')
 work_driving_distance = work_driving_time_duration.get('distance')
 work_driving_distance_miles = work_driving_distance.get('text')
 time_work = { 'time' : str(work_driving_time_mins) , 'distance' : str(work_driving_distance_miles) }
 return jsonify(time_work)


@app.after_request
def after_request(response):
    #add some headers to allow cross site scripting
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
  return response

