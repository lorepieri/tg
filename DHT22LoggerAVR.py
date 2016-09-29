#For the interface with the DHT22 Sensor
#Copyright (c) 2014 Adafruit Industries
#Author: Tony DiCola

#For the rest of the program
#AVR Group
#Author: Lorenzo Pieri


import sys

import Adafruit_DHT


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
adahumidity, adatemperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if adahumidity is not None and adatemperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(adatemperature, adahumidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
    
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
	
	intTemp = float(adatemperature)
	intHumidity = float(adahumidity)

	return intTemp, intHumidity

# function for getting weekly average temperatures.
def getWeeklyAverageTemp(sensor):
	
	return

# function that sends emails, either warning or weekly averages in order to see that pi is alive
def emailWarning(msg, msgType):
	
	return
	
# helper function for database actions. Handles select, insert and sqldumpings. Update te be added later
def databaseHelper(sqlCommand,sqloperation):

	host = "172.16.12.14"
	user = "logger"
	password = "loggerpassword"
	database = "temperatures"
	
	data = ""
	
	db = MySQLdb.connect(host,user,password,database)
        cursor=db.cursor()

	if sqloperation == "Select":
		try:
			cursor.execute(sqlCommand)
			data = cursor.fetchone()
  		except:
			db.rollback()
	elif sqloperation == "Insert":
        	try:
			cursor.execute(sqlCommand)
                	db.commit()
        	except:
                	db.rollback()
                	emailWarning("Database insert failed", "")
			sys.exit(0)
    
	elif sqloperation == "Backup":	
		# Getting current datetime to create seprate backup folder like "12012013-071334".
		date = datetime.date.today().strftime("%Y-%m-%d")
		backupbathoftheday = backuppath + date

		# Checking if backup folder already exists or not. If not exists will create it.
		if not os.path.exists(backupbathoftheday):
			os.makedirs(backupbathoftheday)

		# Dump database
		db = database
		dumpcmd = "mysqldump -u " + user + " -p" + password + " " + db + " > " + backupbathoftheday + "/" + db + ".sql"
		os.system(dumpcmd)

	return data
	
# function for checking log that when last warning was sended, also inserts new entry to log if warning is sent
def checkWarningLog(sensor, sensortemp):
	
	return

	# Function for checking limits. If temperature is lower or greater than limit -> do something
def checkLimits(sensor,sensorTemperature,sensorHumidity,sensorhighlimit,sensorlowlimit,humidityHighLimit,humidityLowLimit):

	return
	
	# helper function for getting configurations from config json file

def main():

	currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


	# how many sensors there is 1 or 2
	sensorsToRead = 1
		
	# Sensor names to add to database, e.g. carage, outside
	sensor1 = "Sensore 2"


	# type of the sensor used, e.g. DHT22 = 22
	sensorType = "22"

	# Default value for message type, not configurable
	msgType = "Warning"

	d = datetime.date.weekday(datetime.datetime.now())
	h = datetime.datetime.now()

	# check if it is 5 o clock. If yes, take sql dump as backup
	if backupEnabled == "Y" or backupEnabled == "y":
		if h.hour == int(backupHour):
			databaseHelper("","Backup")

	# check if it is sunday, if yes send connection check on 23.00
	if connectionCheckEnabled == "Y" or connectionCheckEnabled == "y":
		okToUpdate = False
		if str(d) == str(connectionCheckDay) and str(h.hour) == str(connectionCheckHour):
			try:
				sensor1weeklyAverage = getWeeklyAverageTemp(sensor1)
				if sensor1weeklyAverage != None and sensor1weeklyAverage != '':
					checkSensor = sensor1+" conchck"
					okToUpdate, tempWarning = checkWarningLog(checkSensor,sensor1weeklyAverage)
					if okToUpdate == True:
						msgType = "Info"
						Message = "Connection check. Weekly average from {0} is {1}".format(sensor1,sensor1weeklyAverage)
						emailWarning(Message, msgType)
						sqlCommand = "INSERT INTO mailsendlog SET mailsendtime='%s', triggedsensor='%s', triggedlimit='%s' ,lasttemperature='%s'" % (currentTime,checkSensor,sensor1lowlimit,sensor1weeklyAverage)
						databaseHelper(sqlCommand,"Insert")
			except:
				emailWarning("Couldn't get average temperature to sensor: {0} from current week".format(sensor1),msgType)
				pass				

			if sensorsToRead != "1":
				okToUpdate = False
				try:
					sensor2weeklyAverage = getWeeklyAverageTemp(sensor2)
					if sensor2weeklyAverage != None and sensor2weeklyAverage != '':
						checkSensor = sensor2+" conchck"
						okToUpdate, tempWarning = checkWarningLog(checkSensor,sensor2weeklyAverage)
						if okToUpdate == True:
							msgType = "Info"	
							Message = "Connection check. Weekly average from {0} is {1}".format(sensor2,sensor2weeklyAverage)
							emailWarning(Message, msgType)
							sqlCommand = "INSERT INTO mailsendlog SET mailsendtime='%s', triggedsensor='%s', triggedlimit='%s' ,lasttemperature='%s'" % (currentTime,checkSensor,sensor2lowlimit,sensor2weeklyAverage)
							databaseHelper(sqlCommand,"Insert")
				except:
					emailWarning( "Couldn't get average temperature to sensor: {0} from current week".format(sensor2),msgType)
					pass			

	# default message type to send as email. DO NOT CHANGE
	msgType = "Warning"	

	sensor1error = 0
	okToUpdate = False
	# Sensor 1 readings and limit check
	try:
		sensor1temperature, sensor1humidity = sensorReadings(gpioForSensor1, sensorType)
		limitsOk,warningMessage = checkLimits(sensor1,sensor1temperature,sensor1humidity,sensor1highlimit,sensor1lowlimit,sensor1_humidity_high_limit,sensor1_humidity_low_limit)
	except:
		emailWarning("Failed to read {0} sensor".format(sensor1),msgType)
		sensor1error = 1
		pass

	if sensor1error == 0:
		try:
			# if limits were trigged
			if limitsOk == False:
				# check log when was last warning sended
				okToUpdate, tempWarning = checkWarningLog(sensor1,sensor1temperature)
		except: 
			# if limits were triggered but something caused error, send warning mail to indicate this
			emailWarning("Failed to check/insert log entry from mailsendlog. Sensor: {0}".format(sensor1),msgType)	
			sys.exit(0)

		if okToUpdate == True:
			# enough time has passed since last warning or temperature has increased/decreased by 5 degrees since last measurement
			warningMessage = warningMessage + "\n" + tempWarning
			# send warning
			emailWarning(warningMessage, msgType)
			try:
			# Insert line to database to indicate when warning was sent
				currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				sqlCommand = "INSERT INTO mailsendlog SET mailsendtime='%s', triggedsensor='%s', triggedlimit='%s' ,lasttemperature='%s'" % (currentTime,sensor1,sensor1lowlimit,sensor1temperature)
				databaseHelper(sqlCommand,"Insert")
			except:
				# if database insert failed, send warning to indicate that there is some issues with database
				emailWarning("Failed to insert from {0} to mailsendlog".format(sensor1),msgType)	
	
	# sensor 2 readings and limit check
	sensor2error = 0
	okToUpdate = False
	
	if sensorsToRead != "1":
		try:
			sensor2temperature, sensor2humidity = sensorReadings(gpioForSensor2, sensorType)
			limitsOk,warningMessage = checkLimits(sensor2,sensor2temperature,sensor2humidity,sensor2highlimit,sensor2lowlimit,sensor2_humidity_high_limit,sensor2_humidity_low_limit)
		except:
			emailWarning("Failed to read {0} sensor".format(sensor2),msgType)
			sensor2error = 1
			pass

		if sensor2error == 0:
			try:		
				if limitsOk == False:
					okToUpdate, tempWarning = checkWarningLog(sensor2,sensor2temperature)	

			except:
				emailWarning("Failed to check/insert log entry from mailsendlog. Sensor: {0}".format(sensor2),msgType)	
				sys.exit(0)

			if okToUpdate == True:
				warningMessage = warningMessage + "\n" + tempWarning
				emailWarning(warningMessage, msgType)
				try:
					# Insert line to database to indicate when warning was sent
			       		sqlCommand = "INSERT INTO mailsendlog SET mailsendtime='%s', triggedsensor='%s', triggedlimit='%s' ,lasttemperature='%s'" % (currentTime,sensor2,sensor2lowlimit,sensor2temperature)
					databaseHelper(sqlCommand,"Insert")
				except:
					emailWarning("Failed to insert entry from {0} to mailsendlog".format(sensor1),msgType)	

	# insert values to db
	try:
		if sensor1error == 0:
			sqlCommand = "INSERT INTO temperaturedata SET dateandtime='%s', sensor='%s', temperature='%s', humidity='%s'" % (currentTime,sensor1,sensor1temperature,sensor1humidity)
			# This row below sets temperature as fahrenheit instead of celsius. Comment above line and uncomment one below to take changes into use
			#sqlCommand = "INSERT INTO temperaturedata SET dateandtime='%s', sensor='%s', temperature='%s', humidity='%s'" % (currentTime,sensor1,(sensor1temperature*(9.0/5.0)+32),sensor1humidity)
			databaseHelper(sqlCommand,"Insert")
		if sensorsToRead != "1" and sensor2error == 0:
			sqlCommand = "INSERT INTO temperaturedata SET dateandtime='%s', sensor='%s', temperature='%s', humidity='%s'" % (currentTime,sensor2,sensor2temperature,sensor2humidity)		
			# This row below sets temperature as fahrenheit instead of celsius. Comment above line and uncomment one below to take changes into use
			#sqlCommand = "INSERT INTO temperaturedata SET dateandtime='%s', sensor='%s', temperature='%s', humidity='%s'" % (currentTime,sensor2,(sensor2temperature*(9.0/5.0)+32),sensor2humidity)
			databaseHelper(sqlCommand,"Insert")
   	except:
		sys.exit(0)

if __name__ == "__main__":
	main()
