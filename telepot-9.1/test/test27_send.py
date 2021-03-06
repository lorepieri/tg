# coding=utf8

import time
import threading
import pprint
import sys
import traceback
import urllib2
import telepot
import telepot.namedtuple

"""
This script tests:
- setWebhook() and getUpdates(), and make sure they are exclusive
- sendZZZ() and sendChatAction() methods
- getUserProfilePhotos()

Run it by:
$ python2.7 test.py <token> <user_id>

It will assume the bot identified by <token>, and only communicate with the user identified by <user_id>.

If you don't know your user id, run:
$ python test.py <token> 0

And send it a message anyway. It will print out your user id as an unauthorized user.
Ctrl-C to kill it, then run the proper command again.
"""

def equivalent(data, nt):
    if type(data) is dict:
        keys = data.keys()

        # number of dictionary keys == number of non-None values in namedtuple?
        if len(keys) != len([f for f in nt._fields if getattr(nt, f) is not None]):
            return False

        # map `from` to `from_`
        fields = list(map(lambda k: k+'_' if k in ['from'] else k, keys))

        return all(map(equivalent, [data[k] for k in keys], [getattr(nt, f) for f in fields]))
    elif type(data) is list:
        return all(map(equivalent, data, nt))
    else:
        return data==nt

def examine(result, type):
    try:
        print 'Examining %s ......' % type

        nt = type(**result)
        assert equivalent(result, nt), 'Not equivalent:::::::::::::::\n%s\n::::::::::::::::\n%s' % (result, nt)

        if type == telepot.namedtuple.Message:
            print 'Message glance: %s' % str(telepot.glance(result, long=True))

        pprint.pprint(result)
        pprint.pprint(nt)
        print
    except AssertionError:
        traceback.print_exc()
        answer = raw_input('Do you want to continue? [y] ')
        if answer != 'y':
            exit(1)

def send_everything_on_contact(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)

    if chat_id != USER_ID:
        print 'Unauthorized user:', msg['from']['id']
        exit(1)

    print 'Received message from ID: %d' % chat_id
    print 'Start sending various messages ...'

    ##### forwardMessage

    r = bot.forwardMessage(chat_id, chat_id, msg_id)
    examine(r, telepot.namedtuple.Message)

    ##### sendMessage

    r = bot.sendMessage(chat_id, 'Hello, I am going to send you a lot of things.', reply_to_message_id=msg_id)
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)  # slow it down for inspecting messages

    r = bot.sendMessage(chat_id, u'中文')
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    r = bot.sendMessage(chat_id, '*bold text*\n_italic text_\n[link](http://www.google.com)', parse_mode='Markdown')
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    bot.sendMessage(chat_id, 'http://www.yahoo.com\nwith web page preview')
    time.sleep(0.5)

    bot.sendMessage(chat_id, 'http://www.yahoo.com\nno web page preview', disable_web_page_preview=True)
    time.sleep(0.5)

    show_keyboard = {'keyboard': [['Yes', 'No'], ['Maybe', 'Maybe not']]}
    hide_keyboard = {'hide_keyboard': True}
    force_reply = {'force_reply': True}

    nt_show_keyboard = telepot.namedtuple.ReplyKeyboardMarkup(**show_keyboard)
    nt_hide_keyboard = telepot.namedtuple.ReplyKeyboardHide(**hide_keyboard)
    nt_force_reply = telepot.namedtuple.ForceReply(**force_reply)

    bot.sendMessage(chat_id, 'Here is a custom keyboard', reply_markup=show_keyboard)
    time.sleep(0.5)

    bot.sendMessage(chat_id, 'Hiding it now.', reply_markup=nt_hide_keyboard)
    time.sleep(0.5)

    bot.sendMessage(chat_id, 'Force reply', reply_markup=nt_force_reply)
    time.sleep(0.5)

    ##### sendPhoto

    bot.sendChatAction(chat_id, 'upload_photo')
    r = bot.sendPhoto(chat_id, open('lighthouse.jpg', 'rb'))
    examine(r, telepot.namedtuple.Message)

    file_id = r['photo'][0]['file_id']

    bot.sendPhoto(chat_id, file_id, caption='Show original message and keyboard', reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
    time.sleep(0.5)

    bot.sendPhoto(chat_id, file_id, caption='Hide keyboard', reply_markup=hide_keyboard)
    time.sleep(0.5)

    furl = urllib2.urlopen('http://i.imgur.com/35HSRQ6.png')
    bot.sendPhoto(chat_id, ('abc.jpg', furl))
    time.sleep(0.5)

    bot.sendPhoto(chat_id, (u'中文照片.jpg', open('lighthouse.jpg', 'rb')), caption=u'中文照片')
    time.sleep(0.5)

    ##### getFile

    f = bot.getFile(file_id)
    examine(f, telepot.namedtuple.File)

    ##### download_file, smaller than one chunk (65K)

    try:
        print 'Downloading file to non-existent directory ...'
        bot.download_file(file_id, 'non-existent-dir/file')
    except:
        print 'Error: as expected'

    print 'Downloading file to down.1 ...'
    bot.download_file(file_id, 'down.1')

    print 'Open down.2 and download to it ...'
    with open('down.2', 'wb') as down:
        bot.download_file(file_id, down)

    ##### sendAudio
    # Need one of `performer` or `title' for server to regard it as audio. Otherwise, server treats it as voice.

    bot.sendChatAction(chat_id, 'upload_audio')
    r = bot.sendAudio(chat_id, open('dgdg.mp3', 'rb'), title='Ringtone')
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    file_id = r['audio']['file_id']

    bot.sendAudio(chat_id, file_id, duration=6, performer='Ding Dong', title='Ringtone', reply_to_message_id=msg_id, reply_markup=show_keyboard)
    time.sleep(0.5)

    bot.sendAudio(chat_id, file_id, performer='Ding Dong', reply_markup=nt_hide_keyboard)
    time.sleep(0.5)

    bot.sendAudio(chat_id, (u'中文歌.mp3', open('dgdg.mp3', 'rb')), title=u'中文歌')
    time.sleep(0.5)

    ##### sendDocument

    bot.sendChatAction(chat_id, 'upload_document')
    r = bot.sendDocument(chat_id, open('document.txt', 'rb'))
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    file_id = r['document']['file_id']

    bot.sendDocument(chat_id, file_id, reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
    time.sleep(0.5)

    bot.sendDocument(chat_id, file_id, reply_markup=hide_keyboard)
    time.sleep(0.5)

    bot.sendDocument(chat_id, (u'中文文件.txt', open('document.txt', 'rb')))
    time.sleep(0.5)

    ##### sendSticker

    r = bot.sendSticker(chat_id, open('gandhi.png', 'rb'))
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    file_id = r['sticker']['file_id']

    bot.sendSticker(chat_id, file_id, reply_to_message_id=msg_id, reply_markup=show_keyboard)
    time.sleep(0.5)

    bot.sendSticker(chat_id, file_id, reply_markup=nt_hide_keyboard)
    time.sleep(0.5)

    ##### sendVideo

    bot.sendChatAction(chat_id, 'upload_video')
    r = bot.sendVideo(chat_id, open('hktraffic.mp4', 'rb'))
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    try:
        file_id = r['video']['file_id']

        bot.sendVideo(chat_id, file_id, duration=5, caption='Hong Kong traffic', reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
        time.sleep(0.5)
        bot.sendVideo(chat_id, file_id, reply_markup=hide_keyboard)
        time.sleep(0.5)

    except KeyError:
        # For some reason, Telegram servers may return a document.
        print '****** sendVideo returns a DOCUMENT !!!!!'

        file_id = r['document']['file_id']

        bot.sendDocument(chat_id, file_id, reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
        time.sleep(0.5)
        bot.sendDocument(chat_id, file_id, reply_markup=hide_keyboard)
        time.sleep(0.5)

    ##### download_file, multiple chunks

    print 'Downloading file to down.3 ...'
    bot.download_file(file_id, 'down.3')

    ##### sendVoice

    r = bot.sendVoice(chat_id, open('example.ogg', 'rb'))
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    file_id = r['voice']['file_id']

    bot.sendVoice(chat_id, file_id, duration=6, reply_to_message_id=msg_id, reply_markup=show_keyboard)
    time.sleep(0.5)

    bot.sendVoice(chat_id, file_id, reply_markup=nt_hide_keyboard)
    time.sleep(0.5)

    ##### sendLocation

    bot.sendChatAction(chat_id, 'find_location')
    r = bot.sendLocation(chat_id, 22.33, 114.18)  # Hong Kong
    examine(r, telepot.namedtuple.Message)
    time.sleep(0.5)

    bot.sendLocation(chat_id, 49.25, -123.1, reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)  # Vancouver
    time.sleep(0.5)

    bot.sendLocation(chat_id, -37.82, 144.97, reply_markup=hide_keyboard)  # Melbourne
    time.sleep(0.5)

    ##### Done sending messages

    bot.sendMessage(chat_id, 'I am done.')

def get_user_profile_photos():
    print 'Getting user profile photos ...'

    r = bot.getUserProfilePhotos(USER_ID)
    examine(r, telepot.namedtuple.UserProfilePhotos)

def test_webhook_getupdates_exclusive():
    bot.setWebhook('https://www.fake.com/fake', open('old.cert', 'rb'))
    print 'Fake webhook set.'

    try:
        bot.getUpdates()
    except telepot.exception.TelegramError as e:
        print "%d: %s" % (e.error_code, e.description)
        print 'As expected, getUpdates() produces an error.'

    bot.setWebhook()
    print 'Fake webhook cancelled.'


TOKEN = sys.argv[1]
USER_ID = long(sys.argv[2])

bot = telepot.Bot(TOKEN)

test_webhook_getupdates_exclusive()
get_user_profile_photos()

print 'Text me to start.'
bot.message_loop(send_everything_on_contact, run_forever=True)
