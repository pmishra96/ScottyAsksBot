# coding: utf-8

import warnings
import os
import json
import requests
from flask import Flask, request

from chatbot import *
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
bot = dict() # bot as key and fbid as value
#know_id_flag = False

URL = "http://ac958344.ngrok.io"

@app.route('/verify', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == 'scotty_asks_project_2016':
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token ejfherkuf'

def bot_exists(sender_id):
    # checks if the bot exists in the database
    if (sender_id in bot):
        return True
    return False

@app.route('/verify', methods=['POST'])
def webhook():
    print "DEBUG: WEBHOOK STARTS"
    #global know_id_flag
    #global Bot
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print ("Incoming from %s: %s") % (sender, message)
        sender = str(sender)

        # if bot exists
        if sender not in bot:
            bot[sender] = Bot()


        bot[sender].fbid = sender


        data = check_andrew_ID(bot[sender].fbid)
        if bot[sender].andrewID != None and data["andrewID"] != "":
            bot[sender].andrewID = data["andrewID"]
        elif bot[sender].andrewID == None and data["andrewID"] != "":
            bot[sender].andrewID = data["andrewID"]
            response = "Welcome to ScottyAsks" + data["andrewID"]
            bot[sender].user.first_name = data["first_name"]
            bot[sender].user.last_name = data["last_name"]
            bot[sender].user.btc_address = data["btc_address"]
            bot[sender].user.btc_value = data["btc_value"]

        response = "welcome!"
        if bot[sender].andrewID == None:
            response = "Welcome to ScottyAsks. What is your Andrew ID?"
            bot[sender].andrewID = ''
        elif bot[sender].andrewID == '':
            data = send_unknown_id(bot[sender].fbid, str(message))
            if data == "":
                response = "What is your Andrew ID?"
            else:
                print "hitting this"
                bot[sender].user.andrewID = data["andrewID"]
                bot[sender].user.first_name = data["first_name"]
                bot[sender].user.last_name = data["last_name"]
                bot[sender].user.btc_address = data["btc_address"]
                bot[sender].user.btc_value = data["btc_value"]

        else:
            response = bot[sender].respond_to(message)






        # user_info_dict = check_andrew_ID(sender)
        # curr_user_andrew_ID = user_info_dict["andrewID"]
        #
        #
        #
        # if (bot_exists(sender)):
        #     print "DEBUG: BOT EXISTS"
        #     # find existing bot set bot to it
        #     curr_bot = bot[sender]
        #     curr_bot.text = message
        #     response = curr_bot.respond_to(message)
        # else: # no existing bot
        #     bot[sender] = Bot()
        #     if user_info_dict["andrewID"] != '':
        #         print "DEBUG: BOT DOESNT EXIST, RECORD EXISTS"
        #         # create new bot with info received from get
        #         # only if record already exists in the db
        #         curr_bot = bot[sender]
        #         curr_bot.user.first_name = user_info_dict["first_name"]
        #         curr_bot.user.last_name = user_info_dict["last_name"]
                # curr_bot.user.btc_address = user_info_dict["btc_address"]
                # curr_bot.user.btc_value = user_info_dict["btc_value"]
        #         curr_bot.andrewID = curr_user_andrew_ID
        #         response = curr_bot.respond_to(message)
        #     else:
        #         # no record exists, ask the user for AndrewID
        #         if bot[sender].andrewID == None:
        #             print "DEBUG: BOT DOESNT EXIST, RECORD DOESNT EXIST, ASK USER FOR ANDREWID"
        #             # entering this the first time before the user gave us the andrewID
                    # response = "We don't know you. What is your Andrew ID?"
                    # bot[sender].andrewID = ''
        #         else:
        #             print "DEBUG: BOT DOESNT EXIST, RECORD DOESNT EXIST, GOT ANDREW ID, ASK DB FOR INFO"
        #             # user entered andrewID
        #             curr_user_andrew_ID = str(message)
        #
        #             if (send_unknown_id(sender,curr_user_andrew_ID) == ""):
        #                 # andrewID is wrong
        #                 bot[sender].andrewID = None
        #                 #know_id_flag = True
        #             else:
        #                 #curr_bot = Bot()
        #                 bot[sender].andrewID = curr_user_andrew_ID
        #                 user_info_dict["andrewID"] = curr_user_andrew_ID
        #                 #know_id_flag = False
        #         # else:
        #         #     response = curr_bot.respond_to(message)

        print ("Outgoing to %s: %s") % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"



if __name__ == '__main__':
    print "sadasd"
    app.run(port=5000, debug=True)

def check_andrew_ID(fbid):
    r = requests.get(URL + "/users/fb/" + fbid)
    user_info_dict = {};
    if r.text == "":
        return {"andrewID":""}
    else:
        user_info_dict = json.loads(str(r.text))
    if r.status_code != requests.codes.ok:
        print (r.text)
    return user_info_dict

def send_unknown_id(fbid,andrewID):
    r = requests.post(URL + "/users/new",params = {"andrewID":andrewID, "fbid":fbid})
    return json.loads(str(r.text))
