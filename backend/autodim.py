#!/usr/bin/python


import os
import sys
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Set brightness of display to mode")
args = parser.parse_args()
mode = args.mode

global currentbrightness
#Get the current brightness:
def get_brightness():
 global currentbrightness
 with open('/sys/class/backlight/rpi_backlight/brightness') as inputfile:
  currentbrightness = inputfile.read()
  currentbrightness = int(currentbrightness)
def set_brightness():
 if transition_speed == "fast":
  counter_skip = 5
  sleep_time = 0.02
 if transition_speed == "medium":
  counter_skip = 5
  sleep_time = 0.10
 if transition_speed == "slow":
  counter_skip = 5
  sleep_time = 1.75
 brightdevice = open('/sys/class/backlight/rpi_backlight/brightness', 'w')
 while brightnessnumber != currentbrightness :
  if brightnessnumber < currentbrightness :
   bright = int(currentbrightness) - counter_skip
  if brightnessnumber > currentbrightness :
   bright = int(currentbrightness) + counter_skip
  brightdevice.write(str(bright))
  brightdevice.flush()
  get_brightness()
  time.sleep(sleep_time)

 brightdevice.close()

if mode == "dusk":
 brightnessnumber = 95
 transition_speed = "medium"

if mode == "night":
 brightnessnumber = 15
 transition_speed = "medium"

if mode == "morning":
 brightnessnumber = 255
 transition_speed = "slow"

get_brightness()
set_brightness()
