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


#Globals
state = 0
#state 0 -> /start
#state 1..10 -> S1..S10 Selected
sensor_choice = "Standard"


#Bot handle
def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	command = msg['text']
	start_message = "Scegli un'opzione:\n<b>S1</b> sta per Sensore 1\n<b>Mappa</b> spiega posizioni"
	global state
	global sensor_choice

	if content_type == 'text':
		if command == '/start':
			markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Mappa')], [KeyboardButton(text='S1'), KeyboardButton(text='S2'), KeyboardButton(text='S3'), KeyboardButton(text='S4'), KeyboardButton(text='S5')], [KeyboardButton(text='S6'), KeyboardButton(text='S7'), KeyboardButton(text='S8'), KeyboardButton(text='S9'), KeyboardButton(text='S10')] ])
			bot.sendMessage(chat_id, "Ciao <b>{0}</b>\n\n".format(msg["from"]["first_name"]) + start_message, parse_mode = "HTML", reply_markup = markup)

		if command == 'Indietro':
			markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Mappa')], [KeyboardButton(text='S1'), KeyboardButton(text='S2'), KeyboardButton(text='S3'), KeyboardButton(text='S4'), KeyboardButton(text='S5')], [KeyboardButton(text='S6'), KeyboardButton(text='S7'), KeyboardButton(text='S8'), KeyboardButton(text='S9'), KeyboardButton(text='S10')]])
			bot.sendMessage(chat_id, start_message, parse_mode = "HTML", reply_markup = markup) 		
                

                if command == 'Mappa':
			bot.sendMessage(chat_id, "Quando i sensori saranno posizionati qui verra' spiegato dove si trovano (kilometrica e altre informazioni)")
		if command == 'S1' or command == 'S2' or command == 'S3' or command == 'S4' or command == 'S5' or command == 'S6' or command == 'S7' or command == 'S8' or command == 'S9' or command == 'S10':
			markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ultimi 15 minuti'), KeyboardButton(text='Ultime 2 ore')], [KeyboardButton(text='Ultime 24 ore')], [KeyboardButton(text='Indietro')]])
			bot.sendMessage(chat_id, "Scegli un'opzione",  reply_markup = markup)
			if command == 'S1':
				state = 1
				sensor_choice = "'Sensore 1'"
			if command == 'S2':
				state = 2
				sensor_choice = "'Sensore 2'"
			if command == 'S3':
				state = 3
				sensor_choice = "'Sensore 3'"
			if command == 'S4':
				state = 4
				sensor_choice = "'Sensore 4'"
			if command == 'S5': 
				state = 5
				sensor_choice = "'Sensore 5'"
			if command == 'S6':
				state = 6
				sensor_choice = "'Sensore 6'"
			if command == 'S7':
				state = 7
				sensor_choice = "'Sensore 7'"
			if command == 'S8':
				state = 8
				sensor_choice = "'Sensore 8'"
			if command == 'S9':
				state = 9
				sensor_choice = "'Sensore 9'"
			if command == 'S10':
				state = 10
				sensor_choice = "'Sensore 10'"

		if command == 'Ultime 2 ore':
			try:
				sql_query = "SELECT * FROM temperaturedata WHERE dateandtime >= DATE_SUB(NOW(), INTERVAL 2 HOUR) AND sensor LIKE {0}".format(sensor_choice)
				cursor.execute(sql_query)
				results = cursor.fetchall()
				if len(results) == 0:
					bot.sendMessage(chat_id, "Errore 10: Empty list\n\nCheck sensors")
				for row in results:
					dateandtime = row[0]
					sensor = row[1]
					temperature = row[2]
					humidity = row[3]
					formatted_string = "Data e ora: \n{0} \nSensore: {1} \nTemperatura: {2} \nUmidita': {3} \n----------------\nState: {4},\nSensor: {5}".format(dateandtime, sensor, temperature, humidity, state, sensor_choice)
					bot.sendMessage(chat_id, formatted_string)
			except Exception, e:
				bot.sendMessage(chat_id, "Errore 101: DB execute error\n\n" + str(e))
	
		if command == 'Ultimi 15 minuti':
			try:
				sql_query = "SELECT * FROM temperaturedata WHERE dateandtime >= DATE_SUB(NOW(),INTERVAL 15 MINUTE) AND sensor LIKE {0};".format(sensor_choice)
				cursor.execute(sql_query)
				results = cursor.fetchall()
				if len(results) == 0:
					bot.sendMessage(chat_id, "Errore 10: Empty list\n\nCheck sensors")
				for row in results:
					dateandtime = row[0]
					sensor = row[1]
					temperature = row[2]
					humidity = row[3]
					formatted_string = "Data e ora: \n{0} \nSensore: {1} \nTemperatura: {2} \nUmidita': {3} \n---------------\nState: {4},\nSensor: {5}".format(dateandtime, sensor, temperature, humidity, state, sensor_choice)
					bot.sendMessage(chat_id, formatted_string)
			except Exception, e:
				bot.sendMessage(chat_id, "Errore 101: DB execute error\n\n" + str(e))

		if command == 'Ultime 24 ore':
			try:
				sql_query = "SELECT * FROM temperaturedata WHERE dateandtime > DATE_SUB(NOW(), INTERVAL 24 HOUR) AND sensor LIKE {0};".format(sensor_choice)
				cursor.execute(sql_query)
				results = cursor.fetchall()
				if len(results) == 0:
					bot.sendMessage(chat_id, "Errore 10: Empty list\n\nCheck sensors")
				for row in results:
					dateandtime = row[0]
					sensor = row[1]
					temperature = row[2]
					humidity = row[3]
					formatted_string = "{0} Sens: {1} T: {2} H: {3}".format(dateandtime, sensor, temperature, humidity)
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
