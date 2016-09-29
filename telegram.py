#!/usr/local/lib/python2.7

#Imports
import telepot
import sys
import time
import MySQLdb
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply


#Bot token
bot = telepot.Bot('253194885:AAHESX3CfiOB2Kh9OYSdhvBv2fP098a2mM8')

#Database
host = 'localhost'
user = 'logger'
password = 'loggerpassword'
database = 'temperatures'

#Database connection
dbconn = MySQLdb.connect(host, user, password, database)
cursor = dbconn.cursor()
#Fetch single row -> cursor.fetchone()
#Fetch data -> cursor.execute(sql_query)
#Fetch all the data -> results = cursor.fetchall() after cursor.execute(sql_query)
#for row in results: dateandtime = row[0] sensor = row[1] temperature = row[2] humidity = row[3]
#try: cursor.execute(sql_query) except: print 'error'

#Global variables
sensor_choice = "Standard"


#Bot handle
def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	command = msg['text']
	
	if content_type == 'text':
		if command == '/start':
			markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Mappa')], [KeyboardButton(text='S1'), KeyboardButton(text='S2'), KeyboardButton(text='S3'), KeyboardButton(text='S4'), KeyboardButton(text='S5')], [KeyboardButton(text='S6'), KeyboardButton(text='S7'), KeyboardButton(text='S8'), KeyboardButton(text='S9'), KeyboardButton(text='S10')] ])
			bot.sendMessage(chat_id, "Ciao <b>{0}</b>\nScegli un'opzione:\n<b>S1</b> sta per Sensore 1\n<b>Mappa</b> spiega posizioni".format(msg["from"]["first_name"]), parse_mode = "HTML", reply_markup = markup)		

		if command == 'S1':
			global sensor_choice
			sensor_choice = "Sensore 1"
			markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ultimi 15 minuti'), KeyboardButton(text='Ultime 2 ore')]])
			bot.sendMessage(chat_id, "Scegli un'opzione",  reply_markup = markup)

		if command == 'Ultime 2 ore':
			try:
				cursor.execute('SELECT * FROM temperaturedata WHERE dateandtime >= DATE_SUB(NOW(),INTERVAL 2 HOUR);')
				results = cursor.fetchall()
				for row in results:
					dateandtime = row[0]
					sensor = row[1]
					temperature = row[2]
					humidity = row[3]
					formatted_string = "Data e ora: \n{0} \nSensore: {1} \nTemperatura: {2} \nUmidita': {3} \n---------------- \n {4}".format(dateandtime, sensor, temperature, humidity, sensor_choice)
					bot.sendMessage(chat_id, formatted_string)
			except Exception, e:
				bot.sendMessage(chat_id, "Errore 101: DB execute error\n\n" + str(e))
	
		if command == 'Ultimi 15 minuti':
			try:
				cursor.execute('SELECT * FROM temperaturedata WHERE dateandtime >= DATE_SUB(NOW(),INTERVAL 15 MINUTE);')
				results = cursor.fetchall()
				for row in results:
					dateandtime = row[0]
					sensor = row[1]
					temperature = row[2]
					humidity = row[3]
					formatted_string = "Data e ora: \n{0} \nSensore: {1} \nTemperatura: {2} \nUmidita': {3} \n--------------- \n {4}".format(dateandtime, sensor, temperature, humidity, sensor_choice)
					bot.sendMessage(chat_id, formatted_string)
			except Exception, e:
				bot.sendMessage(chat_id, "Errore 101: DB execute error\n\n" + str(e))
	#Send the answer to the user
	#bot.sendMessage(chat_id, reply)


#Listening
bot.message_loop(handle)
print 'Listening...'



#Keep the program running
while 1:
	time.sleep(10)
