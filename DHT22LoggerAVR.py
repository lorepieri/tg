# Copyright (c) 2015
# Author: Janne Posio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

# This script is intended to use with Adafruit DHT22 temperature and humidity sensors
# and with sensor libraries that Adafruit provides for them. This script alone, without
# sensor/s to provide data for it doesn't really do anyting useful.
# For guidance how to create your own temperature logger that makes use of this script,
# Adafruit DHT22 sensors and raspberry pi, visit : 
# http://www.instructables.com/id/Raspberry-PI-and-DHT22-temperature-and-humidity-lo/

#!/usr/bin/python2
#coding=utf-8

import os
import re
import sys
import datetime
from datetime import timedelta
import json
import subprocess
import MySQLdb
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# function for reading DHT22 sensors
def sensorReadings(gpio, sensor):
	
	configurations = getConfigurations()	
	adafruit = configurations["adafruitpath"]

	sensorReadings = subprocess.check_output(['sudo',adafruit,sensor,gpio])

	try:
		# try to read neagtive numbers
		temperature = re.findall(r"Temp=(-\d+.\d+)", sensorReadings)[0]
	except: 
		# if negative numbers caused exception, they are supposed to be positive
		try:
			temperature = re.findall(r"Temp=(\d+.\d+)", sensorReadings)[0]
		except:
			pass
	humidity = re.findall(r"Humidity=(\d+.\d+)", sensorReadings)[0]
	intTemp = float(temperature)
	intHumidity = float(humidity)
   	print("WORKING... Temp {0} and Humidity {1}".format(intTemp, intHumidity))

	return intTemp, intHumidity

# function for getting weekly average temperatures
# function that sends emails, either warning or weekly averages in order to see that pi is alive
	
# helper function for database actions. Handles select, insert and sqldumpings. Update te be added later
def databaseHelper():

	configurations = getConfigurations()

	host = "172.16.12.14"
	user = "logger"
	password = "loggerpassword"
	database = "temperatures"
	
	sensor1temp, sensor1humidity = sensorReadings("2", "22")
	sensor1 = "Sensore 2"
	currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	data = ""
	
	db = MySQLdb.connect(host,user,password,database)
        cursor=db.cursor()

	cursor.execute("INSERT INTO temperaturedata SET dateandtime='{0}', sensor='{1}', temperature='{2}', humidity='{3}'".format(currentTime, sensor1, sensor1temp, sensor1humidity))
        db.commit()
	print("Committed..")
	db.close()
	
# function for checking log that when last warning was sended, also inserts new entry to log if warning is sent
def getConfigurations():

	path = os.path.dirname(os.path.realpath(sys.argv[0]))

	#get configs
	configurationFile = path + '/config.json'
	configurations = json.loads(open(configurationFile).read())

	return configurations

def main():
	databaseHelper(
)
if __name__ == "__main__":
	main()
