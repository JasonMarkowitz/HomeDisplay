#!/usr/bin/python

#this script scrapes NJT's Departurevision to pull the next 5 62xx trains eastbound

from lxml import html
import requests
import re
import json

#base URL of NJ transit's Departurevision and their station code. Want to put these in a config file
baseurl = 'http://dv.njtransit.com/mobile/tid-mobile.aspx?sid='
station = 'MC'

page = requests.get(baseurl + station)
tree = html.fromstring(page.content)

# First train is tr[tr2] first element is column names
# these are element list items under td[1]
# 1 = Scheduled Time  -- note this grabs everything and requires some special handling, grab the first word
# 2 = Destination
# 3 = Arrival Time
# 4 = Line
# 5 = Train Number
# 6 = Status
#print "Response: " +  str(page)
#status2 = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[2]//td[1])')
#status = tree.xpath('normalize-space(//*[@id="GridView1"]/tr[2])')
#print status2

# Get the next 5 Trains:
def get_inbound_trains(tree):
    first_train = 2
    ny_train_count = 0
    attempt_count = 0
    ny_counter = first_train # Start out with 0 known NYC trains
    ny_train_list = [] #initalize empty list for NY trains
    while ny_train_count <= 5 and attempt_count <= 10: #while we know than less than 5 trains and go through the data 10x
       regex = re.compile(r'NY.Penn(....)*') #compile the regex for NYP
       train_dest = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[2])'.format(ny_counter)) #Look at the Destinations
       if re.match(regex, train_dest) is not None: #if the Train Destination is NYP:
         ny_train_list.append(ny_counter) #add the value of the tr[x] to the list
         ny_counter += 1  #set up for the next train
         ny_train_count += 1 #Add one train to the number of NYP bound trains we'vefound so far
       else: #if the train isn't headed for NY:
        ny_counter += 1 #set up for the next train
        attempt_count += 1 #log the attempt and move on

    #Return the Train Information
    for ny_trains in ny_train_list: #for each of the tr[x] in the list we created above
     train_data = {} #initalize an empty dict object
     train_data["status"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[6])' .format(ny_trains))
     train_data["time"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[1])' .format(ny_trains)).split(' ', 1)[0] 
     train_data["number"] = tree.xpath('normalize-space(//*[@id="GridView1"]//tr[{0}]//td[5])' .format(ny_trains)) 
     print train_data #print the dict object with the information about our train


get_inbound_trains(tree)
